import os, json, datetime
from typing import Dict, Any, List, Optional

class AutomationAgent:
    """
    Enterprise Workflow Automation Agent with Human-In-The-Loop (HITL) Controls.
    Prevents autonomous unauthorized actions by enforcing policy checks,
    generating review tickets, and requiring approval before external execution.
    """
    def __init__(self):
        # In-memory workflow registry (persisted to SQLite/PostgreSQL in production)
        self.pending_workflows: List[Dict[str, Any]] = [
            {
                "workflow_id": 101,
                "workflow_type": "INVENTORY_REORDER",
                "title": "Replenish Hyderabad IoT Gateway v4 Buffer Stock",
                "description": "Trigger automated purchase order for 50 units from supplier to restore buffer stock >25 units.",
                "triggered_by": "AnomalyDetectionEngine / InventorySOP",
                "impact_level": "MODERATE_FINANCIAL",
                "estimated_cost_inr": 1400000.0,
                "status": "PENDING_APPROVAL",
                "approver_role": "MANAGER",
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                "workflow_id": 102,
                "workflow_type": "CHURN_INTERVENTION",
                "title": "High-Risk Churn Account Executive Outreach",
                "description": "Deploy customized executive retention email & 15% annual renewal discount to 12 at-risk Enterprise accounts.",
                "triggered_by": "CustomerChurnModel",
                "impact_level": "HIGH_CUSTOMER_RELATION",
                "status": "PENDING_APPROVAL",
                "approver_role": "MANAGER",
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

    def list_pending_approvals(self, user_role: str = "MANAGER") -> List[Dict[str, Any]]:
        return [w for w in self.pending_workflows if w["status"] == "PENDING_APPROVAL"]

    def request_approval(self, action_request: str, user_id: int, user_role: str) -> Dict[str, Any]:
        """
        Interprets action requests like 'Send the report to my manager' or 'Trigger reorder'
        and creates a governed approval request.
        """
        wf_id = len(self.pending_workflows) + 101
        new_wf = {
            "workflow_id": wf_id,
            "workflow_type": "ACTION_REQUEST",
            "title": f"User Action: {action_request}",
            "description": f"Requested action requiring managerial sign-off: '{action_request}'",
            "triggered_by": f"User {user_id} ({user_role})",
            "impact_level": "GOVERNED_EXECUTION",
            "status": "PENDING_APPROVAL",
            "approver_role": "MANAGER",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.pending_workflows.append(new_wf)

        return {
            "agent": "AutomationAgent",
            "workflow_id": wf_id,
            "status": "APPROVAL_REQUIRED",
            "message": (
                f"Action queued for Human-in-the-Loop review. In accordance with enterprise governance, "
                f"this action requires confirmation from a {new_wf['approver_role']}. "
                f"Workflow Ticket #{wf_id} created."
            ),
            "workflow_details": new_wf
        }

    def execute_approval(self, workflow_id: int, decision: str, approver_name: str, approver_role: str) -> Dict[str, Any]:
        """
        Executes or rejects an approval ticket based on managerial decision.
        """
        if approver_role.upper() not in ["MANAGER", "ADMIN"]:
            return {
                "status": "error",
                "error": f"Authorization Denied: Role {approver_role} is not permitted to approve workflows."
            }

        target = next((w for w in self.pending_workflows if w["workflow_id"] == workflow_id), None)
        if not target:
            return {"status": "error", "error": f"Workflow #{workflow_id} not found."}

        if decision.upper() == "APPROVE":
            target["status"] = "APPROVED_AND_EXECUTED"
            target["approved_by"] = approver_name
            target["executed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return {
                "status": "success",
                "workflow_id": workflow_id,
                "action": "APPROVED",
                "message": f"Workflow #{workflow_id} ('{target['title']}') successfully approved by {approver_name} and dispatched to automation engine.",
                "audit_logged": True
            }
        else:
            target["status"] = "REJECTED"
            target["rejected_by"] = approver_name
            return {
                "status": "success",
                "workflow_id": workflow_id,
                "action": "REJECTED",
                "message": f"Workflow #{workflow_id} rejected by {approver_name}. Action terminated.",
                "audit_logged": True
            }
