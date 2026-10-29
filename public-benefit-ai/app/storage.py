"""Opt-in, privacy-minimal SQLite metadata store.

No user question, response, IP address, location, records or message bodies are persisted.
This is local-only demonstration telemetry, not production audit infrastructure.
"""
import sqlite3
from pathlib import Path
from contextlib import closing
import tempfile
from time import time

VALID_SCHEMA = """
CREATE TABLE IF NOT EXISTS demo_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_slug TEXT NOT NULL,
    recorded_at INTEGER NOT NULL,
    elapsed_ms REAL NOT NULL CHECK (elapsed_ms >= 0),
    abstained INTEGER NOT NULL CHECK (abstained IN (0,1))
);
CREATE INDEX IF NOT EXISTS demo_runs_slug_time ON demo_runs(project_slug, recorded_at);
"""

class SQLiteDemoMetrics:
    def __init__(self, path=None):
        self.path = str(path or (Path(tempfile.gettempdir()) / "public-benefit-ai-demo-metrics.sqlite3"))
        with closing(self._db()) as conn:
            conn.executescript(VALID_SCHEMA)
            conn.commit()

    def _db(self):
        conn=sqlite3.connect(self.path,timeout=10)
        conn.row_factory=sqlite3.Row
        return conn

    def record(self, slug:str, elapsed_ms:float, abstained:bool=False):
        if len(slug)>120 or not slug.replace("-","").isalnum():
            raise ValueError("Invalid project slug")
        if elapsed_ms<0 or elapsed_ms>3600000:
            raise ValueError("Invalid elapsed time")
        with closing(self._db()) as db, db:
            db.execute("INSERT INTO demo_runs(project_slug,recorded_at,elapsed_ms,abstained) VALUES(?,?,?,?)",
                       (slug,int(time()),round(elapsed_ms,3),int(bool(abstained))))

    def summary(self):
        with closing(self._db()) as db:
            rows=db.execute(
                "SELECT project_slug, COUNT(*) AS runs, SUM(abstained) AS abstentions,"
                " ROUND(AVG(elapsed_ms),2) AS mean_runtime_ms FROM demo_runs GROUP BY project_slug"
                ).fetchall()
        return [dict(r) for r in rows]

    def purge(self):
        with self._db() as db:
            db.execute("DELETE FROM demo_runs")
