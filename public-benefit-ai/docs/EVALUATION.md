# Measurable evaluation contract

Run `python -m scripts.evaluate`; the script writes `reports/synthetic_evaluation.json` from fixed synthetic smoke cases. It measures complete module execution and simple retrieval recall@2. This narrow smoke set is **not** performance on real incidents.

For controlled offline evaluation of predictive demos, each forecast returns model MAE and naive persistence baseline MAE from the same chronological holdout. It must not be described as a live prediction. Spatial reporting returns **counts**, not exposure-adjusted risk. Classification confidence is labeled uncalibrated.

Before a credible employer claim: add larger non-synthetic labeled data, maintain a frozen time- and geography-separated test set, report classwise precision/recall/PR-AUC, document error cases, evaluate multilingual parity and adversarial attacks, and compare to established baselines. Do not claim lives saved, fraud prevented or government decisions granted.
