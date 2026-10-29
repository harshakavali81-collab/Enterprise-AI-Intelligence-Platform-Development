# AI Accessibility and Civic Issue Reporting Platform — model card

- **Intended use:** Synthetic-data educational demonstration for residents and municipal issue reviewers.
- **Out of scope:** Real operational decisions, verified warnings, clinical decisions, official government rulings or claims of true field predictions.
- **Model / method:** TF-IDF logistic text categorization and similarity-based deduplication; human moderation; images and audio are NOT implemented.
- **Dataset:** Clearly fictional examples or caller-provided numeric/test input. No live authorized feeds.
- **Required evaluation:** Per-class precision/recall, duplicate F1, accessibility audits and reviewed resolution time.
- **Baseline:** Lexical retrieval abstention, persistence for numerical forecasts, or human-review rule as appropriate.
- **Bias and error analysis:** Build an independently labeled holdout, test class and subgroup disparities where lawful, check distribution drift and conflicts, record false-positive and false-negative cases.
- **Known limitations:** Tiny fixtures; no calibrated real-world confidence, comprehensive multilingual evaluation, or incident validation.
- **Release status:** NOT approved for real-world use.
