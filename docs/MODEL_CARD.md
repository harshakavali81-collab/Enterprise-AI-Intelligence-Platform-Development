# AI Road Safety and Accident Hotspot Intelligence — model card

- **Intended use:** Synthetic-data educational demonstration for road safety analysts and city planners.
- **Out of scope:** Real operational decisions, verified warnings, clinical decisions, official government rulings or claims of true field predictions.
- **Model / method:** Validated latitude/longitude and 0.01° grid aggregation over synthetic coordinates; no causal attribution or prediction.
- **Dataset:** Clearly fictional examples or caller-provided numeric/test input. No live authorized feeds.
- **Required evaluation:** Spatial holdout hit rate; exposure-adjusted hotspot precision once real data exists.
- **Baseline:** Lexical retrieval abstention, persistence for numerical forecasts, or human-review rule as appropriate.
- **Bias and error analysis:** Build an independently labeled holdout, test class and subgroup disparities where lawful, check distribution drift and conflicts, record false-positive and false-negative cases.
- **Known limitations:** Tiny fixtures; no calibrated real-world confidence, comprehensive multilingual evaluation, or incident validation.
- **Release status:** NOT approved for real-world use.
