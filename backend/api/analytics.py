from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from backend.database.schemas import SqlExecutionRequest, SqlExecutionResponse
from backend.agents.sql_agent import SqlAgent
from backend.api.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["SQL & Business Analytics"])
sql_agent = SqlAgent()

@router.post("/sql", response_model=SqlExecutionResponse)
def execute_sql_analytics(req: SqlExecutionRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = current_user.get("role", "ANALYST")
    prompt = req.prompt or req.raw_sql or "top products"
    result = sql_agent.execute_query(prompt, user_role=user_role)

    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))

    return SqlExecutionResponse(
        sql=result["sql"],
        columns=result["columns"],
        rows=result["rows"],
        total_rows=result["total_rows"],
        execution_time_ms=result["execution_time_ms"],
        visualization=result.get("visualization"),
        status="success"
    )

@router.get("/kpis")
def get_kpis(current_user: Dict[str, Any] = Depends(get_current_user)):
    # Aggregated executive KPIs
    return {
        "gross_revenue_inr": 485000000.0,
        "active_customers": 182,
        "total_transactions": 1065,
        "average_order_value_inr": 184500.0,
        "hyderabad_recent_mom_growth": -14.8,
        "top_performing_region": "South (Bengaluru + Hyderabad)",
        "churn_risk_flagged_count": 18,
        "critical_inventory_alerts": 1
    }
