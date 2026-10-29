import json
from pathlib import Path
from app.main import PROJECT_SLUG
from app.engine import process
if __name__=="__main__":
    obj=json.loads(Path("sample_request.json").read_text(encoding="utf8"))
    print(json.dumps(process(PROJECT_SLUG,obj),indent=2))
