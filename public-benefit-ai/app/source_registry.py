"""Official portals are navigation hints only, not authenticated live data feeds."""
from .sources import PORTALS, DOCS

def source_manifest(slug):
    items=[]
    for doc in DOCS.get(slug,[]):
        items.append({"id":doc["id"],"title":doc["title"],
                      "origin":"synthetic training material","verified_official":False,
                      "url":doc.get("url"),"is_live":False})
    return {"sources":items,"official_portal_for_independent_check":PORTALS.get(slug),
            "portal_ingested":False,"freshness_verified":False,
            "notice":"No official alert, scheme notice or health advisory feed is connected."}
