"""Simple descriptive geospatial aggregation, never a warning system."""
from collections import Counter
def hotspots(events:list):
    if not isinstance(events,list) or len(events)>2000:
        raise ValueError("events must be an array of at most 2000 coordinates")
    count=Counter()
    for event in events:
        if not isinstance(event,dict) or "latitude" not in event or "longitude" not in event:
            raise ValueError("each event needs latitude and longitude")
        lat,lon=float(event["latitude"]),float(event["longitude"])
        if not (-90<=lat<=90 and -180<=lon<=180):
            raise ValueError("coordinates out of bounds")
        count[(round(lat,2),round(lon,2))]+=1
    return {"cells":[{"latitude":p[0],"longitude":p[1],"historical_count":n} for p,n in count.most_common(20)],
      "method":"Rounded geographic grid (0.01 degree), counts not exposure-adjusted risk",
      "limitations":["Synthetic fixtures or user supplied data, no real crash verification","Not predictive of individual safety or a validated accident probability"]}
