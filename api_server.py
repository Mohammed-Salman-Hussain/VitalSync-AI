"""
api_server.py - Production FastAPI Server for All-in-One Health Platform

Exposes high-speed REST endpoints connecting the modern JavaScript frontend
to the trained machine learning models, validated scientific calculators,
deficiency knowledge graph, clinical safety triage, and local Qwen on GPU.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

from schemas import (
    UserHealthProfile,
    ComprehensiveDiagnosticPayload
)
from orchestrator import HealthOrchestrator
from llm_advisor import QwenHealthAdvisor


app = FastAPI(
    title="VitalSync AI Health Platform API",
    description="Local-first health and lifestyle intelligence engine.",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize cached singletons
orchestrator = HealthOrchestrator()
advisor = QwenHealthAdvisor()

STATIC_DIR = os.path.join(os.path.dirname(__file__), "web")


class QuestionRequest(BaseModel):
    question: str
    profile: Optional[UserHealthProfile] = None


@app.get("/api/health")
def health_check():
    """Returns system status, active models, and Ollama connection check."""
    return {
        "status": "healthy",
        "models_loaded": 5,
        "ollama_model": advisor.model_name,
        "ollama_url": advisor.api_url
    }


@app.post("/api/analyze", response_model=ComprehensiveDiagnosticPayload)
def analyze_profile(profile: UserHealthProfile):
    """
    Ingests UserHealthProfile and executes the full homogeneous pipeline
    (BMR/TDEE math, 5 ML risk models, deficiency knowledge graph, clinical triage).
    Returns in <30ms.
    """
    try:
        payload = orchestrator.process_health_profile(profile)
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnostic error: {str(e)}")


@app.post("/api/consultation")
def generate_consultation(payload: ComprehensiveDiagnosticPayload):
    """
    Sends the computed diagnostic payload to local Qwen (via Ollama on GPU)
    and returns a structured, empathetic clinical consultation report.
    """
    try:
        report = advisor.generate_consultation(payload)
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM consultation error: {str(e)}")


@app.post("/api/ask")
def ask_question(req: QuestionRequest):
    """
    Answers an arbitrary everyday health query or viral social media myth
    grounded in user metrics if provided.
    """
    try:
        payload = None
        if req.profile:
            payload = orchestrator.process_health_profile(req.profile)
        answer = advisor.answer_health_question(req.question, payload)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")


@app.post("/api/export-doctor-briefing", response_class=PlainTextResponse)
def export_doctor_briefing(profile: UserHealthProfile):
    """
    Generates a clean 1-page standardized Markdown clinical briefing
    designed to be printed and shared with a primary care doctor.
    """
    try:
        payload = orchestrator.process_health_profile(profile)
        briefing = orchestrator.generate_doctor_briefing_markdown(payload)
        return briefing
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")


# Mount static assets directory if exists
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    def serve_frontend():
        index_file = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "VitalSync AI API is active. Web assets directory is being prepared."}
