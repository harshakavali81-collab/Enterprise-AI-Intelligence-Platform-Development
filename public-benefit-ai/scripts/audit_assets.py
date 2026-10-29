"""Validate the full 10-project evidence pack independently from runtime smoke tests."""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from app.catalog import PROJECTS

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={"README.md","sample_request.json","cli.py","assets/cover.svg","assets/architecture.svg","assets/synthetic-trend.svg","docs/ARCHITECTURE.md","docs/MODEL_CARD.md","docs/THREAT_MODEL.md","docs/workflow.mmd"}

def audit():
    errors=[]
    for slug in PROJECTS:
        base=ROOT/"projects"/slug
        for f in EXPECTED:
            p=base/f
            if not p.is_file() or p.stat().st_size<5:
                errors.append(str(p)+" missing/empty")
        try:
            json.loads((base/"sample_request.json").read_text())
        except (ValueError,OSError) as exc:
            errors.append(f"{slug} invalid sample JSON: {exc}")
        for f in ("cover.svg","architecture.svg","synthetic-trend.svg"):
            try:
                tree=ET.parse(base/"assets"/f)
                if tree.getroot().tag!="{http://www.w3.org/2000/svg}svg":
                    errors.append(f"{slug}/{f} missing SVG root")
            except (ET.ParseError,OSError) as exc:
                errors.append(f"{slug}/{f}: {exc}")
    return {"projects":len(PROJECTS),"images":len(PROJECTS)*3,"errors":errors}

if __name__=="__main__":
    result=audit()
    print(json.dumps(result,indent=2))
    raise SystemExit(bool(result["errors"]))
