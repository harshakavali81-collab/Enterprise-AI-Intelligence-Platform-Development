# Minimal metadata storage

By default **no input or output is persisted**. Set `DEMO_DB_ENABLED=true` to enable local-only SQLite metadata: project identifier, epoch timestamp, processing duration and abstention boolean. It never stores user questions, incident details, personal identifiers, images or model responses. Use `GET /api/v1/demo-metrics` for aggregate counts.

The opt-in database is in the operating-system temporary folder. The operator can remove it, or use `SQLiteDemoMetrics.purge()` to clear rows. This is not a durable regulatory audit log. Public deployment would require identity/access management, rate limits, encryption at rest, retention rules, security review, and an approved privacy policy.

`GET /api/v1/{slug}/sources` describes **synthetic knowledge and independent-check portal links**; it does not claim real official feeds were ingested or updated. No live source-collection process exists.
