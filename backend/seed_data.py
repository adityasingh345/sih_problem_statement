import json
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path(__file__).parent / "data"
LOCATIONS = [
    ("Shimla", "Himachal Pradesh", 31.1048, 77.1734, "Flood", "High"),
    ("Dehradun", "Uttarakhand", 30.3165, 78.0322, "Heavy Rainfall", "High"),
    ("Delhi", "Delhi", 28.6139, 77.2090, "Heatwave", "High"),
    ("Mumbai", "Maharashtra", 19.0760, 72.8777, "Flood", "High"),
    ("Kolkata", "West Bengal", 22.5726, 88.3639, "Thunderstorm", "Medium"),
    ("Guwahati", "Assam", 26.1445, 91.7362, "Heavy Rainfall", "High"),
    ("Chennai", "Tamil Nadu", 13.0827, 80.2707, "Strong Wind", "Medium"),
    ("Jaipur", "Rajasthan", 26.9124, 75.7873, "Dust Storm", "Medium"),
    ("Srinagar", "Jammu & Kashmir", 34.0837, 74.7973, "Fog", "Low"),
    ("Kochi", "Kerala", 9.9312, 76.2673, "Heavy Rainfall", "High"),
    ("Patna", "Bihar", 25.5941, 85.1376, "Flood", "Medium"),
    ("Bengaluru", "Karnataka", 12.9716, 77.5946, "Thunderstorm", "Medium"),
    ("Shimla", "Himachal Pradesh", 31.1048, 77.1734, "Heavy Rainfall", "Medium"),
    ("Mumbai", "Maharashtra", 19.0760, 72.8777, "Strong Wind", "Medium"),
    ("Delhi", "Delhi", 28.6139, 77.2090, "Dust Storm", "Low"),
]
WEATHER = {
 "Shimla": {"temperature":18,"rainfall":82,"humidity":91,"wind_speed":23}, "Dehradun":{"temperature":20,"rainfall":74,"humidity":89,"wind_speed":19},
 "Delhi":{"temperature":42,"rainfall":4,"humidity":52,"wind_speed":15}, "Mumbai":{"temperature":27,"rainfall":64,"humidity":88,"wind_speed":18},
 "Kolkata":{"temperature":30,"rainfall":24,"humidity":78,"wind_speed":36}, "Guwahati":{"temperature":26,"rainfall":71,"humidity":93,"wind_speed":17},
 "Chennai":{"temperature":32,"rainfall":12,"humidity":74,"wind_speed":43}, "Jaipur":{"temperature":38,"rainfall":0,"humidity":29,"wind_speed":39},
 "Srinagar":{"temperature":12,"rainfall":3,"humidity":84,"wind_speed":8}, "Kochi":{"temperature":28,"rainfall":58,"humidity":91,"wind_speed":21},
 "Patna":{"temperature":31,"rainfall":41,"humidity":86,"wind_speed":14}, "Bengaluru":{"temperature":25,"rainfall":18,"humidity":73,"wind_speed":29}
}

def build():
    reports, incidents = [], []
    base = datetime(2026, 9, 1, 8, 0)
    texts = {"Flood":"Water logging and flooding reported near main road", "Heavy Rainfall":"Very heavy rainfall causing disruption", "Thunderstorm":"Thunderstorm with lightning reported", "Heatwave":"Extreme heat conditions reported", "Fog":"Dense fog reducing visibility", "Dust Storm":"Dust storm affecting roads", "Strong Wind":"Strong gusty winds reported"}
    for ix, (city, state, lat, lng, event, severity) in enumerate(LOCATIONS, 1):
        count = 5 if ix <= 12 else 0
        status = "VERIFIED" if ix % 4 in (1,2) else ("PENDING" if ix % 4 == 3 else "SUSPICIOUS")
        incident = {"id":ix,"event_type":event,"location":city,"state":state,"latitude":lat,"longitude":lng,"severity":severity,"status":status,"confidence":92 if status=="VERIFIED" else (63 if status=="PENDING" else 34),"report_count":count,"first_report":(base+timedelta(days=(ix-1)%12)).isoformat(),"last_updated":(base+timedelta(days=(ix-1)%12,hours=4)).isoformat()}
        incidents.append(incident)
        for j in range(count):
            # Preserve the SIH demo filter: Shimla flood has verified activity on 10–12 Sep.
            day_offset = 9 + (j % 3) if ix == 1 else (ix*3+j) % 12
            t = base + timedelta(days=day_offset, hours=j*2)
            source = ["Official", "Verified source", "Reliable citizen", "Normal citizen", "New/untrusted"][j]
            rstatus = status if j == 0 else ("DUPLICATE" if j >= 2 else status)
            report={"id":len(reports)+1,"text":f"{texts[event]} in {city}; update {j+1}","source":source,"location":city,"state":state,"latitude":lat,"longitude":lng,"event_type":event,"severity":severity,"timestamp":t.isoformat(),"confidence":max(25, incident['confidence']-j*3),"status":rstatus,"incident_id":ix}
            if ix == 1 and j == 1:
                report.update({"language":"HI","original_text":"शिमला में भारी बारिश के कारण सड़क पर पानी भर गया है।","english_text":"Heavy rainfall has caused waterlogging in Shimla."})
            reports.append(report)
    incoming = [
      {"text":"Massive flooding reported near Mall Road in Shimla", "source":"Reliable citizen", "timestamp":"2026-09-12T12:14:00"},
      {"text":"शिमला में भारी बारिश के कारण सड़क पर पानी भर गया है", "source":"Normal citizen", "timestamp":"2026-09-12T12:21:00"},
      {"text":"Extreme heat wave reported across Delhi", "source":"Verified source", "timestamp":"2026-09-12T13:05:00"},
      {"text":"Strong winds disrupting traffic in Chennai", "source":"New/untrusted", "timestamp":"2026-09-12T14:10:00"}
    ]
    ROOT.mkdir(exist_ok=True)
    for name, data in [("reports.json",reports),("incidents.json",incidents),("weather.json",WEATHER),("incoming_reports.json",incoming)]:
        (ROOT/name).write_text(json.dumps(data, indent=2), encoding="utf8")

if __name__ == "__main__": build()
