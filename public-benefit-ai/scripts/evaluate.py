"""Run small, transparent smoke evaluations; never substitute for field validation."""
import json
from pathlib import Path
from app.catalog import PROJECTS
from app.engine import process
from app.retrieval import retrieve
from app.sources import DOCS

def run():
    runs = []
    for slug in PROJECTS:
        request={"text":"flood emergency health scheme streetlight scam"}
        output=process(slug,request)
        runs.append({"slug":slug,"completed":bool(output.get("result")),"synthetic":output["demo_mode"]})
    # Small fixed retrieval test; this is not a production quality metric.
    qa=[("flood preparedness","ai-disaster-response-public-safety-assistant","d-flood"),
        ("resource availability","emergency-services-coordination-copilot","e-resources"),
        ("eligibility","multilingual-civic-services-navigator","c-eligibility")]
    hits=[]
    for q,slug,expected in qa:
        r=retrieve(q,DOCS[slug])
        hits.append(any(x["id"]==expected for x in r["citations"]))
    report={"evaluation_scope":"synthetic smoke set only",
            "project_smoke_passed":sum(x["completed"] for x in runs),"project_smoke_total":len(runs),
            "retrieval_recall_at_2":sum(hits)/len(hits),"retrieval_questions":len(hits),
            "per_project":runs,"limitations":["Very small fictional test set","No real-world performance guarantees","No multilingual or live-data validation"]}
    out=Path("reports");out.mkdir(exist_ok=True)
    (out/"synthetic_evaluation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
    print(json.dumps(report,indent=2))

if __name__=="__main__":run()
