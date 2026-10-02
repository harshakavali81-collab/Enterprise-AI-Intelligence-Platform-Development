from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from backend.database.schemas import WorkflowActionRequest
from backend.agents.automation_agent import AutomationAgent
from backend.api.auth import get_current_user

router = APIRouter(prefix="/workflows", tags=["Workflow Automation & Approvals"])
automation_agent = AutomationAgent()

@router.get("/pending")
def list_pending_workflows(current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = current_user.get("role", "EMPLOYEE")
    return automation_agent.list_pending_approvals(user_role=user_role)

@router.post("/decision")
def submit_workflow_decision(req: WorkflowActionRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = current_user.get("role", "EMPLOYEE")
    user_name = current_user.get("full_name", current_user.get("username", "Approver"))
    res = automation_agent.execute_approval(
        workflow_id=req.workflow_id,
        decision=req.decision,
        approver_name=user_name,
        approver_role=user_role
    )
    if res.get("status") == "error":
        raise HTTPException(status_code=403, detail=res.get("error"))
    return res
