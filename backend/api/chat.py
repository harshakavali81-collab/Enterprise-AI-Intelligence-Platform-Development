from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from backend.database.schemas import ChatQueryRequest, ChatQueryResponse, CitationItem
from backend.agents.orchestrator import AIOrchestrator
from backend.security.guardrails import AIGuardrails
from backend.api.auth import get_current_user
from backend.utils.logger import log_audit_event

router = APIRouter(prefix="/chat", tags=["AI Chat & Orchestration"])
orchestrator = AIOrchestrator()
guardrails = AIGuardrails()

@router.post("", response_model=ChatQueryResponse)
def handle_chat_message(req: ChatQueryRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = current_user.get("role", "EMPLOYEE")
    user_id = current_user.get("user_id", 1)

    # 1. Guardrail validation
    is_safe, guardrail_msg = guardrails.validate_input(req.query)
    if not is_safe:
        log_audit_event(user_id, "PROMPT_INJECTION_BLOCKED", "CHAT", "INPUT", {"query": req.query, "msg": guardrail_msg}, "BLOCKED")
        raise HTTPException(status_code=400, detail=guardrail_msg)

    # 2. Process via AI Orchestrator
    result = orchestrator.process_request(req.query, user_role=user_role, user_id=user_id)

    # 3. Format citations
    citations_list = []
    for c in result.get("rag_citations", []) or result.get("citations", []):
        citations_list.append(CitationItem(
            citation_id=c.get("citation_id", "CIT-1"),
            document_title=c.get("document_title", "Document"),
            document_id=c.get("document_id", "DOC-1"),
            page_number=c.get("page_number", 1),
            section=c.get("section", "General"),
            formatted_source=c.get("formatted_source", "[Source Document]"),
            snippet=c.get("snippet", "")
        ))

    log_audit_event(user_id, "CHAT_QUERY_EXECUTED", "ORCHESTRATOR", result.get("intent", "UNKNOWN"), {"query": req.query, "agent": result.get("agent_selected")})

    return ChatQueryResponse(
        query=req.query,
        intent=result.get("intent", "UNKNOWN"),
        agent_selected=result.get("agent_selected", "Orchestrator"),
        response=result.get("response", ""),
        citations=citations_list if citations_list else None,
        visualization=result.get("visualization"),
        sql_query=result.get("sql_query") or result.get("sql_data", {}).get("sql"),
        execution_time_ms=result.get("execution_time_ms", 100.0),
        language=result.get("language", "en"),
        status=result.get("status", "success")
    )
