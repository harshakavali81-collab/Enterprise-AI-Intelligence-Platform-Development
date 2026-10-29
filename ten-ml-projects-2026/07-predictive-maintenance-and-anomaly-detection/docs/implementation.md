# Engineering and evaluation notes — Predictive Maintenance and Anomaly Detection

## Reproducibility and implementation
- Python 3.11+, NumPy, scikit-learn, joblib, FastAPI, matplotlib.
- `engine.py train` uses random seed 42 and creates artifacts on disk.
- Evaluation: Isolation Forest vs supervised classifier, PR-AUC and F1.
- Data provenance: documented, generated demo data; no license assumed for external datasets.
- Model output is suitable for developer review only. Do not deploy exposed demo endpoints to untrusted traffic.

## Caveats and production acceptance
Synthetic sensors only. Real alarm logic needs units, failure labeling, temporal leakage checks, false-alarm-cost estimates and maintenance review.

1. Replace synthetic data with authorized/licensed real-world data and document its schema, limitations and permissions.
2. Add independent holdout evaluation, model selection discipline, reproducible environment, calibrated thresholds and error analysis appropriate to the use case.
3. Add authentication/authorization, secret management, security review, logging policy, rate limits, retention policy and cloud hosting only after operator approval.
4. Verify CI on GitHub after publishing; local unit tests are not proof of cloud deployment.
5. Reassess fairness, drift, safety and domain-specific validation with qualified reviewers.
