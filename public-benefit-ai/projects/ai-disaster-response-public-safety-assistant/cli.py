"""Run this project's example from public-benefit-ai/ working directory."""
import json
from pathlib import Path
from app.engine import process

if __name__ == "__main__":
    example = json.loads((Path(__file__).parent / "sample_request.json").read_text(encoding="utf-8"))
    print(json.dumps(process("ai-disaster-response-public-safety-assistant",example),indent=2))
