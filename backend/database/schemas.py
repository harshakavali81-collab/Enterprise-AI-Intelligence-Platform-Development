from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# Authentication
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    role: str
    user_id: int
    department: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: str
    department: str
    role_name: str
    is_active: bool

# Chat & Orchestration
class ChatQueryRequest(BaseModel):
    query: str = Field(..., json_schema_extra={"example": "Why did sales decrease last month in Hyderabad?"})
    session_id: Optional[str] = None
    language: Optional[str] = "auto" # auto, en, hi, te

class CitationItem(BaseModel):
    citation_id: str
    document_title: str
    document_id: str
    page_number: int
    section: str
    formatted_source: str
    snippet: str

class ChatQueryResponse(BaseModel):
    query: str
    intent: str
    agent_selected: str
    response: str
    citations: Optional[List[CitationItem]] = None
    visualization: Optional[Dict[str, Any]] = None
    sql_query: Optional[str] = None
    execution_time_ms: float
    language: str
    status: str

# SQL Analytics
class SqlExecutionRequest(BaseModel):
    prompt: Optional[str] = None
    raw_sql: Optional[str] = None

class SqlExecutionResponse(BaseModel):
    sql: str
    columns: List[str]
    rows: List[Dict[str, Any]]
    total_rows: int
    execution_time_ms: float
    visualization: Optional[Dict[str, Any]] = None
    status: str

# ML Prediction
class ChurnPredictionRequest(BaseModel):
    customer_id: Optional[int] = None
    days_since_last_order: Optional[int] = 45
    order_frequency: Optional[int] = 6
    total_spend: Optional[float] = 150000.0
    support_tickets_count: Optional[int] = 1
    segment: Optional[str] = "Enterprise"

class ForecastRequest(BaseModel):
    city: str = "Hyderabad"
    horizon_months: int = 1

# Reports & Workflows
class ReportGenerationRequest(BaseModel):
    title: Optional[str] = "Monthly Business Intelligence & Performance Report"
    format: Optional[str] = "PDF"

class WorkflowActionRequest(BaseModel):
    workflow_id: int
    decision: str = Field(..., json_schema_extra={"example": "APPROVE"}) # APPROVE or REJECT
