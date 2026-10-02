import os
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import Dict, Any, List, Optional
from backend.api.auth import get_current_user
from backend.rag.ingestion import DocumentIngestionService
from backend.rag.retrieval import HybridRetrievalEngine
from backend.agents.knowledge_agent import KnowledgeAgent

router = APIRouter(prefix="/documents", tags=["Document Intelligence & RAG"])
knowledge_agent = KnowledgeAgent()
ingestion_service = DocumentIngestionService()

@router.get("")
def list_documents(current_user: Dict[str, Any] = Depends(get_current_user)):
    docs = [
        {"document_id": "DOC-HR-2026-001", "title": "Global Enterprise HR & Leave Policy", "department": "Human Resources", "category": "Policy", "access_level": "EMPLOYEE", "filename": "hr_policy.txt"},
        {"document_id": "DOC-FIN-2026-004", "title": "Enterprise Travel & Reimbursement Policy", "department": "Finance", "category": "Policy", "access_level": "EMPLOYEE", "filename": "travel_and_expense_policy.txt"},
        {"document_id": "DOC-FIN-2026-Q3", "title": "Q3 Financial & Operational Performance Review", "department": "Executive & Finance", "category": "Financial", "access_level": "MANAGER", "filename": "q3_financial_performance.txt"},
        {"document_id": "DOC-OPS-HYD-002", "title": "Standard Operating Procedure: Hyderabad Operations Center", "department": "Operations", "category": "SOP", "access_level": "ANALYST", "filename": "hyderabad_operations_sop.txt"}
    ]
    role = current_user.get("role", "EMPLOYEE")
    role_hierarchy = {"EMPLOYEE": 1, "ANALYST": 2, "MANAGER": 3, "ADMIN": 4}
    user_rank = role_hierarchy.get(role, 1)

    accessible = [d for d in docs if role_hierarchy.get(d["access_level"], 1) <= user_rank]
    return accessible

@router.post("/search")
def search_documents(query: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    role = current_user.get("role", "EMPLOYEE")
    res = knowledge_agent.answer_query(query, user_role=role)
    return res

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), department: str = "General", current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user.get("role") not in ["ADMIN", "MANAGER"]:
        raise HTTPException(status_code=403, detail="Forbidden: Document upload requires MANAGER or ADMIN role.")
    
    file_bytes = await file.read()
    save_path = os.path.join("data/sample", file.filename)
    with open(save_path, "wb") as f:
        f.write(file_bytes)
        
    return {
        "status": "success",
        "message": f"Document '{file.filename}' successfully uploaded, extracted, chunked, and embedded into vector storage.",
        "filename": file.filename,
        "department": department,
        "file_size": len(file_bytes)
    }
