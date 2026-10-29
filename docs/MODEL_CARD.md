# AI Air Quality and Environmental Health Monitor — model card

- **Intended use:** Synthetic-data educational demonstration for environment analysts studying pollutant time series.
- **Out of scope:** Real operational decisions, verified warnings, clinical decisions, official government rulings or claims of true field predictions.
- **Model / method:** Lagged Ridge forecast for PM2.5 synthetic series; chronological holdout versus persistence, input quality checks.
- **Dataset:** Clearly fictional examples or caller-provided numeric/test input. No live authorized feeds.
- **Required evaluation:** MAE/RMSE per station and horizon, missing-sensor robustness, interval coverage.
- **Baseline:** Lexical retrieval abstention, persistence for numerical forecasts, or human-review rule as appropriate.
- **Bias and error analysis:** Build an independently labeled holdout, test class and subgroup disparities where lawful, check distribution drift and conflicts, record false-positive and false-negative cases.
- **Known limitations:** Tiny fixtures; no calibrated real-world confidence, comprehensive multilingual evaluation, or incident validation.
- **Release status:** NOT approved for real-world use.
