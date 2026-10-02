import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Dict, Any, Optional
from backend.database.schemas import ReportGenerationRequest
from backend.agents.report_agent import ReportAgent
from backend.services.report_service import PDFReportGenerator
from backend.api.auth import get_current_user

router = APIRouter(prefix="/reports", tags=["AI Report Generation"])
report_agent = ReportAgent()
pdf_generator = PDFReportGenerator()

@router.post("/generate")
def generate_report(req: ReportGenerationRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = current_user.get("role", "MANAGER")
    res = report_agent.generate_executive_report(title=req.title or "Monthly Business Intelligence Report", user_role=user_role)
    if res.get("status") == "error":
        raise HTTPException(status_code=403, detail=res.get("error"))

    # Also build PDF artifact
    pdf_path = pdf_generator.generate_pdf(filename="Project_Report.pdf", title=req.title or "Enterprise AI Intelligence Report", report_data=res)
    res["pdf_path"] = pdf_path
    res["download_url"] = "/reports/download/Project_Report.pdf"
    return res

@router.get("/download/{filename}")
def download_pdf_report(filename: str):
    file_path = os.path.join("reports", filename)
    if not os.path.exists(file_path):
        # Generate default if not yet compiled
        file_path = pdf_generator.generate_pdf(filename=filename)
    return FileResponse(file_path, media_type="application/pdf", filename=filename)
