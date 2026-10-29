import json
from pathlib import Path
from app.main import PROJECT_SLUG
from app.engine import process
if __name__=="__main__":print(json.dumps(process(PROJECT_SLUG,json.loads(Path("sample_request.json").read_text())),indent=2))
