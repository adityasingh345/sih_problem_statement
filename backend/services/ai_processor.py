LOCATIONS = {"shimla":("Shimla","Himachal Pradesh",31.1048,77.1734),"शिमला":("Shimla","Himachal Pradesh",31.1048,77.1734),"delhi":("Delhi","Delhi",28.6139,77.2090),"mumbai":("Mumbai","Maharashtra",19.076,72.8777),"chennai":("Chennai","Tamil Nadu",13.0827,80.2707)}
EVENTS = {"Flood":["flood","flooding","पानी भर"],"Heavy Rainfall":["rain","rainfall","बारिश"],"Heatwave":["heat","hot","heat wave"],"Strong Wind":["wind","gust"],"Thunderstorm":["thunder","lightning"],"Fog":["fog"],"Dust Storm":["dust"]}
def classify(text):
    lower=text.lower(); event=next((e for e, words in EVENTS.items() if any(w in lower for w in words)),"Heavy Rainfall")
    city,state,lat,lng=next((v for k,v in LOCATIONS.items() if k in lower),("Delhi","Delhi",28.6139,77.2090))
    severity="High" if event in ("Flood","Heatwave","Heavy Rainfall") else "Medium"
    return {"event_type":event,"location":city,"state":state,"latitude":lat,"longitude":lng,"severity":severity,"confidence":91}
