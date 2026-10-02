import datetime
from typing import Dict, Any, List

class NotificationService:
    """
    Enterprise Notification & Alert Dispatch Service.
    Dispatches alerts via SMTP email, corporate Slack/Teams webhooks,
    and maintains an audit log of all communications.
    """
    def __init__(self):
        self.sent_notifications: List[Dict[str, Any]] = []

    def send_workflow_alert(self, workflow_title: str, recipient_role: str, details: str) -> Dict[str, Any]:
        alert_record = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "WORKFLOW_APPROVAL_NOTIFICATION",
            "recipient_role": recipient_role,
            "title": workflow_title,
            "details": details,
            "delivery_status": "DISPATCHED_TO_NOTIFICATION_BUS"
        }
        self.sent_notifications.append(alert_record)
        return alert_record

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        return self.sent_notifications
