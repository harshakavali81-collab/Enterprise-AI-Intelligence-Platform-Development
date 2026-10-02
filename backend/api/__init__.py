from .auth import router as auth_router
from .chat import router as chat_router
from .documents import router as documents_router
from .analytics import router as analytics_router
from .predictions import router as predictions_router
from .reports import router as reports_router
from .workflows import router as workflows_router

__all__ = [
    "auth_router",
    "chat_router",
    "documents_router",
    "analytics_router",
    "predictions_router",
    "reports_router",
    "workflows_router"
]
