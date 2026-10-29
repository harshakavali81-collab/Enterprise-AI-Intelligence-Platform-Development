# Emergency Services Information and Coordination Copilot — model card

- **Intended use:** Synthetic-data educational demonstration for authorized staff performing training exercises.
- **Out of scope:** Real operational decisions, verified warnings, clinical decisions, official government rulings or claims of true field predictions.
- **Model / method:** Synthetic SOP retrieval, source citation and evidence-preserving draft; no tools execute dispatch or resource allocation.
- **Dataset:** Clearly fictional examples or caller-provided numeric/test input. No live authorized feeds.
- **Required evaluation:** Field extraction F1, groundedness, staleness detection and summary omission.
- **Baseline:** Lexical retrieval abstention, persistence for numerical forecasts, or human-review rule as appropriate.
- **Bias and error analysis:** Build an independently labeled holdout, test class and subgroup disparities where lawful, check distribution drift and conflicts, record false-positive and false-negative cases.
- **Known limitations:** Tiny fixtures; no calibrated real-world confidence, comprehensive multilingual evaluation, or incident validation.
- **Release status:** NOT approved for real-world use.
