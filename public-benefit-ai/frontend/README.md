# Local interactive frontend

Start in `public-benefit-ai/`:

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
# second terminal
python -m http.server 5173 --directory frontend
```

Visit [http://127.0.0.1:5173](http://127.0.0.1:5173). Select one of ten projects, inspect or edit the fictional JSON fixture and run a request.

**This is not a hosted service.** The frontend uses only `http://127.0.0.1:8000`; it requires a local FastAPI server, and displays a connection error if unavailable. No remote LLM or official source integration is implied.

For production: replace demo fixtures with licensed sources; implement authentication, rate limiting, audit history and review workflows, and deploy only after expert validation.
