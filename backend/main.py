import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .seed_data import build
from .services.ai_processor import classify
from .services.duplicate_detector import find_duplicate
from .services.credibility import score
from .services.verification_engine import verify

DATA=Path(__file__).parent/"data"; build()
app=FastAPI(title="SIH 26069 Local MVP")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_methods=["*"],allow_headers=["*"])
def load(name): return json.loads((DATA/name).read_text())
def save(name,value): (DATA/name).write_text(json.dumps(value,indent=2))
def matches(item, q):
    timestamp=item.get("timestamp",item.get("first_report",""))[:10]
    return (not q.get("start") or timestamp>=q["start"]) and (not q.get("end") or timestamp<=q["end"]) and (not q.get("event") or item["event_type"] in q["event"].split(",")) and (not q.get("state") or item["state"]==q["state"]) and (not q.get("city") or item["location"]==q["city"]) and (not q.get("status") or item["status"]==q["status"])
def queried(q):
    reports=[r for r in load("reports.json") if matches(r,q)]
    # Incidents inherit the combined filter from their matching reports; an
    # incident's original first-report date must not hide its current activity.
    incident_ids={r["incident_id"] for r in reports}; incidents=[i for i in load("incidents.json") if i["id"] in incident_ids]
    return reports,incidents
@app.get("/api/dashboard")
def dashboard(start:str="",end:str="",event:str="",state:str="",city:str="",status:str=""):
    q=locals(); reports,incidents=queried(q)
    statuses={s:sum(1 for r in reports if r["status"]==s) for s in ["VERIFIED","PENDING","SUSPICIOUS","DUPLICATE"]}
    by_event={}; by_state={}; timeline={}
    for r in reports:
        by_event[r["event_type"]]=by_event.get(r["event_type"],0)+1; by_state[r["state"]]=by_state.get(r["state"],0)+1; d=r["timestamp"][:10];timeline[d]=timeline.get(d,0)+1
    return {"reports":reports,"incidents":incidents,"stats":{"total_reports":len(reports),"total_incidents":len(incidents),**{k.lower():v for k,v in statuses.items()}},"charts":{"event":[{"name":k,"value":v} for k,v in by_event.items()],"state":[{"name":k,"value":v} for k,v in by_state.items()],"status":[{"name":k.title(),"value":v} for k,v in statuses.items()],"timeline":[{"name":k[5:],"value":v} for k,v in sorted(timeline.items())]},"options":{"states":sorted({r['state'] for r in load('reports.json')}),"cities":sorted({r['location'] for r in load('reports.json')})}}
@app.get("/api/incidents/{incident_id}")
def incident_detail(incident_id:int):
    incident=next((x for x in load("incidents.json") if x["id"]==incident_id),None)
    if not incident: raise HTTPException(404,"Incident not found")
    reports=[r for r in load("reports.json") if r["incident_id"]==incident_id]
    weather=load("weather.json").get(incident["location"],{})
    return {"incident":incident,"reports":reports,"weather":weather,"analysis":{"citizen_evidence":"✓ Matching citizen reports","weather_evidence":"✓ Local mock weather evidence","location_match":"✓ Location match","source_credibility":"✓ Scored locally","duplicate_reports":sum(r["status"]=="DUPLICATE" for r in reports),"confidence":incident["confidence"],"final_status":incident["status"]}}
@app.post("/api/simulate")
def simulate():
    incoming=load("incoming_reports.json")
    if not incoming: return {"message":"All seeded incoming reports have been processed"}
    raw=incoming.pop(0); processed=classify(raw["text"]); reports=load("reports.json"); incidents=load("incidents.json"); weather=load("weather.json")
    candidate={**raw,**processed,"id":max([r["id"] for r in reports],default=0)+1}
    duplicate, similarity=find_duplicate(candidate,reports)
    incident=next((i for i in incidents if i["location"]==candidate["location"] and i["event_type"]==candidate["event_type"]),None)
    confidence,status,analysis=verify(candidate,incident,weather.get(candidate["location"],{}),duplicate,score(raw["source"]))
    candidate.update({"confidence":confidence,"status":"DUPLICATE" if duplicate and similarity>.20 else status,"incident_id":incident["id"] if incident else len(incidents)+1})
    if incident: incident.update({"report_count":incident["report_count"]+1,"last_updated":raw["timestamp"],"confidence":max(incident["confidence"],confidence)})
    else: incidents.append({"id":candidate["incident_id"],**{k:candidate[k] for k in ["event_type","location","state","latitude","longitude","severity","status","confidence"]},"report_count":1,"first_report":raw["timestamp"],"last_updated":raw["timestamp"]})
    reports.append(candidate); save("reports.json",reports);save("incidents.json",incidents);save("incoming_reports.json",incoming)
    return {"report":candidate,"duplicate_similarity":round(similarity,2),"analysis":analysis}
@app.post("/api/reset")
def reset(): build(); return {"ok":True}
