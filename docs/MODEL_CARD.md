# AI Scam, Phishing and Digital Fraud Awareness Assistant — model card

- **Intended use:** Synthetic-data educational demonstration for everyday users reviewing suspicious messages.
- **Out of scope:** Real operational decisions, verified warnings, clinical decisions, official government rulings or claims of true field predictions.
- **Model / method:** TF-IDF logistic regression trained on tiny labeled synthetic texts; URL parsing without visiting the link.
- **Dataset:** Clearly fictional examples or caller-provided numeric/test input. No live authorized feeds.
- **Required evaluation:** Classwise precision, recall, PR-AUC and false-positive rate on future non-synthetic holdouts.
- **Baseline:** Lexical retrieval abstention, persistence for numerical forecasts, or human-review rule as appropriate.
- **Bias and error analysis:** Build an independently labeled holdout, test class and subgroup disparities where lawful, check distribution drift and conflicts, record false-positive and false-negative cases.
- **Known limitations:** Tiny fixtures; no calibrated real-world confidence, comprehensive multilingual evaluation, or incident validation.
- **Release status:** NOT approved for real-world use.
