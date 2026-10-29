"""Privacy-minimal SQLite store is an optional demonstration-only component."""
from app.storage import SQLiteDemoMetrics
import sqlite3
import pytest

def test_aggregated_metrics_contain_no_raw_user_text(tmp_path):
    path=tmp_path/"demo.sqlite3"
    metrics=SQLiteDemoMetrics(path)
    metrics.record("ai-flood-disaster-early-warning",17.5,False)
    metrics.record("ai-flood-disaster-early-warning",22,True)
    rows=metrics.summary()
    assert rows==[{"project_slug":"ai-flood-disaster-early-warning","runs":2,"abstentions":1,"mean_runtime_ms":19.75}]
    db=sqlite3.connect(path)
    schema=[row[1] for row in db.execute("PRAGMA table_info(demo_runs)")]
    assert "question" not in schema and "raw_response" not in schema and "ip_address" not in schema

def test_sql_slug_input_rejected(tmp_path):
    metrics=SQLiteDemoMetrics(tmp_path/"demo.sqlite3")
    with pytest.raises(ValueError):metrics.record("anything;DROP TABLE demo_runs",3,False)

def test_purge_deletes_all_telemetry(tmp_path):
    metrics=SQLiteDemoMetrics(tmp_path/"demo.sqlite3")
    metrics.record("some-project",0.0)
    metrics.purge()
    assert metrics.summary()==[]
