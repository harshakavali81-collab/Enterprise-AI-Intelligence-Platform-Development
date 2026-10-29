"""Pseudonymous review only; no face recognition, PII, automated record merging."""
from difflib import SequenceMatcher
from uuid import uuid4
def duplicate_review(candidate:dict, existing:list):
    if not isinstance(candidate,dict) or "description_tags" not in candidate:
        raise ValueError("candidate requires description_tags")
    if not isinstance(existing,list) or len(existing)>200:
        raise ValueError("existing must be a list <=200")
    tags=str(candidate["description_tags"])[:500].lower()
    suggestions=[]
    for row in existing:
        code=str(row.get("reference_code",""))[:40]
        if not code or not code.replace("-","").isalnum():continue
        sim=SequenceMatcher(None,tags,str(row.get("description_tags",""))[:500].lower()).ratio()
        if sim>=.55:
            suggestions.append({"reference_code":code,"text_similarity":round(sim,3),"requires_human_review":True})
    return {"suggestions":sorted(suggestions,key=lambda v:-v["text_similarity"])[:10],
            "matched_identity":False,"merged":False,
            "limitations":["Not an identity-verification service","Input must be synthetic or authorized and access-controlled outside this demo"]}
def issue_ticket(text:str,history:list):
    for row in history:
        if SequenceMatcher(None,text.lower(),str(row.get("description","")).lower()).ratio()>.82:
            return {"ticket_id":None,"possible_duplicate_of":str(row.get("ticket_id",""))[:40],"status":"human_review"}
    return {"ticket_id":"DEMO-"+uuid4().hex[:8],"possible_duplicate_of":None,"status":"awaiting_human_review"}
