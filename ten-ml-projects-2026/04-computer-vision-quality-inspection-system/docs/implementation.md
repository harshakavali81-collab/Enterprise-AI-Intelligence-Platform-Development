# Engineering and evaluation notes — Computer Vision Quality Inspection System

## Reproducibility and implementation
- Python 3.11+, NumPy, scikit-learn, joblib, FastAPI, matplotlib.
- `engine.py train` uses random seed 42 and creates artifacts on disk.
- Evaluation: Image features, Logistic Regression vs Random Forest, precision and recall.
- Data provenance: documented, generated demo data; no license assumed for external datasets.
- Model output is suitable for developer review only. Do not deploy exposed demo endpoints to untrusted traffic.

## Caveats and production acceptance
Synthetic texture feature classifier only. Upgrade to real licensed MVTec/production images and a CNN with batch-level splits plus defect localization; benchmark after acquiring data.

1. Replace synthetic data with authorized/licensed real-world data and document its schema, limitations and permissions.
2. Add independent holdout evaluation, model selection discipline, reproducible environment, calibrated thresholds and error analysis appropriate to the use case.
3. Add authentication/authorization, secret management, security review, logging policy, rate limits, retention policy and cloud hosting only after operator approval.
4. Verify CI on GitHub after publishing; local unit tests are not proof of cloud deployment.
5. Reassess fairness, drift, safety and domain-specific validation with qualified reviewers.
