def verify(report, incident, weather, duplicate, credibility):
    citizen=min(30, 10 + incident.get("report_count",0)*4) if incident else 10
    weather_score=25 if weather and (weather.get("rainfall",0)>20 or weather.get("temperature",0)>38 or weather.get("wind_speed",0)>30) else 8
    total=min(100, citizen+weather_score+20+round(credibility*.25) - (8 if duplicate else 0))
    status="VERIFIED" if total>=75 else ("PENDING" if total>=45 else "SUSPICIOUS")
    return total,status,{"citizen_evidence":citizen,"weather_evidence":weather_score,"location_match":20,"source_credibility":round(credibility*.25),"duplicate_penalty":8 if duplicate else 0}
