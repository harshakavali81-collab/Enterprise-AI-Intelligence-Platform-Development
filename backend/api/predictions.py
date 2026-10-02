from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from backend.database.schemas import ChurnPredictionRequest, ForecastRequest
from backend.agents.ml_agent import MlAgent
from backend.api.auth import get_current_user

router = APIRouter(prefix="/predict", tags=["Predictive Machine Learning Engine"])
ml_agent = MlAgent()

@router.post("/churn")
def predict_churn(req: ChurnPredictionRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = current_user.get("role", "ANALYST")
    res = ml_agent.handle_prediction_query("Which customers are likely to churn?", user_role=user_role)
    if res.get("status") == "error":
        raise HTTPException(status_code=403, detail=res.get("error"))
    return res

@router.post("/forecast")
def predict_forecast(req: ForecastRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = current_user.get("role", "ANALYST")
    query = f"Predict next month sales in {req.city}"
    res = ml_agent.handle_prediction_query(query, user_role=user_role)
    if res.get("status") == "error":
        raise HTTPException(status_code=403, detail=res.get("error"))
    return res

@router.get("/anomalies")
def get_anomalies(current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = current_user.get("role", "ANALYST")
    res = ml_agent.handle_prediction_query("detect sales anomalies", user_role=user_role)
    if res.get("status") == "error":
        raise HTTPException(status_code=403, detail=res.get("error"))
    return res
