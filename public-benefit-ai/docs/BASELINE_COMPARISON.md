# Reproducible baselines & synthetic evaluation artifacts

From the `public-benefit-ai/` directory:

```bash
python -m scripts.evaluate
python -m scripts.evaluate_models
```

The scripts write `reports/synthetic_evaluation.json`, `reports/model_baseline_comparison.json` and `reports/model_baseline_chart.svg`. The SVG compares computed macro-F1 values for a tiny separately authored set of **fictional** scam messages and civic issue descriptions, measured against a most-frequent-label baseline. The JSON also reports explicit prediction mistakes and numerical Ridge versus persistence MAE on an illustrative sequence.

These metrics **must not** be quoted as real-world model accuracy or proof of public benefit. Some runs may perform poorly on the small test set. This is an engineering exercise in honest measurement, not independent validation.

Before deployment, gather appropriately licensed real labeled data, document consent and data minimization, split by time and geography where relevant, evaluate precision/recall, groundedness, citation quality, multilingual safety, calibration, drift, vulnerability to adversarial inputs, latency and operational incident-review protocols.
