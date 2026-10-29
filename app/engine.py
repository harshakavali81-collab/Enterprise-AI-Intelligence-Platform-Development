"""Domain-specific, testable engines; never impersonate official agencies."""
from .catalog import PROJECTS
from .sources import DOCS, PORTALS
from .retrieval import retrieve
from .forecasting import forecast
from .classification import SCAM_TRAIN,ISSUE_TRAIN,classify,suspicious_link_indicators
from .spatial import hotspots
from .records import duplicate_review,issue_ticket
import re
SYNTH_SERIES={"ai-flood-disaster-early-warning":[9,12,11,14,13,18,17,16,20,19,22,23,21,26,24,27],
              "air-quality-environmental-health-monitor":[38,40,45,42,50,48,51,47,53,52,57,54,55,59,58,60]}
SYNTH_CRASHES=[{"latitude":17.401+i*.001,"longitude":78.481+i*.001} for i in (0,1,2,6,7,8,9)]
SYNTH_CASES=[{"reference_code":"DEMO-101","description_tags":"blue bag bus terminal"},{"reference_code":"DEMO-102","description_tags":"green coat market"}]
URGENT = re.compile(r"\b(chest pain|difficulty breathing|unconscious|suicide|severe bleeding)\b",re.I)

def process(slug:str,payload:dict):
    if slug not in PROJECTS:raise KeyError("Unknown project")
    if not isinstance(payload,dict):raise ValueError("JSON object required")
    title,kind=PROJECTS[slug]
    text=str(payload.get("text",""))[:4000]
    meta={"project":title,"slug":slug,"demo_mode":True,
          "data_provenance":"Synthetic examples or user-provided data, not official live data",
          "safety_notice":"Education/demo only; no official alert, clinical diagnosis or autonomous operational decision."}
    if kind=="rag":
        if slug=="trusted-public-health-information-assistant" and URGENT.search(text):
            return {**meta,"result":{"answer":"Urgent health concern: seek qualified emergency medical assistance. No diagnosis provided.","citations":[],"abstained":True,"escalation":True}}
        output=retrieve(text,DOCS[slug])
        output["official_portal_for_independent_verification"]=PORTALS.get(slug)
        if slug=="emergency-services-coordination-copilot":
            output["incident_report_draft"]={"input_excerpt":text[:240],"review_status":"requires_authorized_human_approval"}
            output["actions_executed"]=[]
        if slug=="multilingual-civic-services-navigator":
            output["eligibility_decision"]=None
        return {**meta,"result":output}
    if kind=="forecast":
        observations=payload.get("observations",SYNTH_SERIES[slug])
        target="pm25" if slug=="air-quality-environmental-health-monitor" else "illustrative_rainfall"
        return {**meta,"result":forecast(observations,target),
                "official_portal_for_independent_verification":PORTALS.get(slug)}
    if kind=="spatial":
        return {**meta,"result":hotspots(payload.get("events",SYNTH_CRASHES))}
    if slug=="scam-phishing-awareness-assistant":
        if not text.strip():raise ValueError("text cannot be empty")
        classification=classify(text,SCAM_TRAIN)
        return {**meta,"result":{"classification":classification,"url_indicators":suspicious_link_indicators(text),
          "advice":"Treat unexpected credential/OTP requests cautiously. Verify separately through trusted official channels. A non-flagged message is not necessarily safe.",
          "urls_visited":False}}
    if slug=="privacy-preserving-missing-person-coordination":
        return {**meta,"result":duplicate_review(payload.get("candidate",{"description_tags":text}),payload.get("existing",SYNTH_CASES))}
    if slug=="accessibility-civic-issue-reporting":
        if not text.strip():raise ValueError("text cannot be empty")
        return {**meta,"result":{"classification":classify(text,ISSUE_TRAIN),
             "ticket":issue_ticket(text,payload.get("history",[])),
             "needs_human_moderation":True,"image_understanding_enabled":False}}
    raise RuntimeError("Unimplemented engine")
