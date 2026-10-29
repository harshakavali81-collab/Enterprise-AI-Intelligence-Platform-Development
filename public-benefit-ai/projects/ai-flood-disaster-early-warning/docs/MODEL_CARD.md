# AI Flood and Natural Disaster Early-Warning Support — model card

- **Intended use:** Synthetic-data educational demonstration for researchers and disaster preparedness teams.
- **Out of scope:** Real operational decisions, verified warnings, clinical decisions, official government rulings or claims of true field predictions.
- **Model / method:** Lagged Ridge model with chronological MAE vs persistence baseline, using only synthetic fixture or uploaded numerical series.
- **Dataset:** Clearly fictional examples or caller-provided numeric/test input. No live authorized feeds.
- **Required evaluation:** MAE, RMSE, event recall, lead time and calibration after real labels.
- **Baseline:** Lexical retrieval abstention, persistence for numerical forecasts, or human-review rule as appropriate.
- **Bias and error analysis:** Build an independently labeled holdout, test class and subgroup disparities where lawful, check distribution drift and conflicts, record false-positive and false-negative cases.
- **Known limitations:** Tiny fixtures; no calibrated real-world confidence, comprehensive multilingual evaluation, or incident validation.
- **Release status:** NOT approved for real-world use.
