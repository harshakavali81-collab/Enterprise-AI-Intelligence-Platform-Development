"""Chronological holdout and a simple autoregressive Ridge baseline."""
from math import isfinite
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

def forecast(values: list, name: str):
    if not isinstance(values,list) or len(values)<8 or len(values)>1000:
        raise ValueError("observations must be an array of 8 to 1000 numbers")
    try:
        arr = np.asarray(values,dtype=float)
    except (TypeError,ValueError) as exc:
        raise ValueError("observations must be numeric") from exc
    if not all(isfinite(float(v)) for v in arr):
        raise ValueError("observations must be finite")
    if name=="pm25" and np.any(arr<0):
        raise ValueError("PM2.5 cannot be negative")
    # Two lag features, chronological 75/25 split, baseline last observation.
    X = np.array([[arr[i-2],arr[i-1]] for i in range(2,len(arr))])
    y = arr[2:]
    cut = max(4,int(len(X)*.75))
    cut = min(cut,len(X)-1)
    model = Ridge(alpha=2.).fit(X[:cut],y[:cut])
    yhat = model.predict(X[cut:])
    baseline = X[cut:,-1]
    next_value = float(model.predict([[arr[-2],arr[-1]]])[0])
    if name=="pm25":
        next_value=max(0.,next_value)
    return {
       "target":name,"next_step_estimate":round(next_value,2),
       "holdout_mae":round(float(mean_absolute_error(y[cut:],yhat)),3),
       "persistence_baseline_mae":round(float(mean_absolute_error(y[cut:],baseline)),3),
       "holdout_n":len(y[cut:]),"training_n":cut,
       "model":"Ridge regression, lag 1 and lag 2","data_origin":"caller-provided or synthetic fixture",
       "limitations":["One-step academic baseline, not validated for operational alerts","No calibrated interval or externally validated hazard threshold"]
    }
