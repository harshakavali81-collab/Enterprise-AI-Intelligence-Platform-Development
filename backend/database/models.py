from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class User:
    user_id: int
    username: str
    email: str
    hashed_password: str
    full_name: str
    department: str
    role_id: int
    is_active: bool = True

@dataclass
class Customer:
    customer_id: int
    customer_name: str
    email: str
    city: str
    state: str
    segment: str
    churn_risk_score: float
    total_spend: float
    order_frequency: int
    days_since_last_order: int
    support_tickets_count: int

@dataclass
class Product:
    product_id: int
    product_name: str
    category: str
    unit_price: float
    cost_price: float
    stock_quantity: int
    is_discontinued: bool = False

@dataclass
class DocumentChunk:
    chunk_id: int
    document_id: int
    chunk_index: int
    content: str
    page_number: int
    metadata_json: Dict[str, Any]
    embedding: Optional[List[float]] = None
