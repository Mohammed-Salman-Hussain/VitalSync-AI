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


class WhatIfRequest(BaseModel):
    profile: UserHealthProfile
    phone_reduction_min: int = 30
    extra_steps: int = 3000
    caffeine_cutoff_earlier_hours: float = 3.0


@app.get("/api/health")
def health_check():
    """Returns system status, active models, and real-time Ollama connection check."""
    ollama_status = advisor.check_connection()
    return {
        "status": "healthy",
        "models_loaded": 5,
        "ollama": ollama_status,
        "ollama_model": advisor.model_name,
        "ollama_url": advisor.api_url,
        "active_engine": "Qwen on GPU" if ollama_status.get("connected") else "Deterministic Clinical Synthesizer (Zero-Crash Fallback Active)"
    }


@app.get("/api/benchmarks")
def get_model_benchmarks():
    """Returns audited scientific validation metrics for the 5 machine learning pipelines."""
    return {
        "models": [
            {
                "id": "cardio",
                "name": "Lifestyle Heart Disease Risk",
                "algorithm": "Balanced Logistic Regression with ColumnTransformer",
                "dataset": "CDC BRFSS 2020 (319,795 adult records)",
                "metric_name": "ROC-AUC",
                "metric_value": "0.8170",
                "accuracy": "76.4%",
                "features": ["BMI", "Smoking", "AlcoholDrinking", "PhysicalActivity", "SleepTime", "DiffWalking", "Sex", "AgeCategory"],
                "clinical_rationale": "Forecasts vascular atherosclerosis likelihood from modifiable daily behaviors."
            },
            {
                "id": "prediabetes",
                "name": "Pre-Diabetes Non-Invasive Screener",
                "algorithm": "HistGradientBoostingClassifier",
                "dataset": "CDC BRFSS 50/50 Balanced Diabetes Indicators (70,692 records)",
                "metric_name": "ROC-AUC",
                "metric_value": "0.8192",
                "accuracy": "74.8%",
                "features": ["HighBP", "HighChol", "BMI", "Smoker", "PhysActivity", "Fruits", "Veggies", "HvyAlcohol", "GenHlth", "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age"],
                "clinical_rationale": "Identifies early insulin resistance without requiring invasive venous blood draw."
            },
            {
                "id": "circadian",
                "name": "Circadian Sleep Latency, Fatigue & Sleep Debt",
                "algorithm": "Multi-Output HistGradientBoosting (Regressor + Classifier)",
                "dataset": "Bedtime Screen Time & Circadian Sleep Cohort (8,500 records)",
                "metric_name": "Latency RMSE",
                "metric_value": "6.84 mins",
                "secondary_metric": "Fatigue RMSE: 1.02 / 10 | Debt Acc: 89.2%",
                "features": ["bedtime_phone_minutes", "primary_bedtime_app", "screen_brightness_pct", "blue_light_filter", "caffeine_post_5pm", "physical_activity", "chronotype"],
                "clinical_rationale": "Models dopamine arousal and blue-light melatonin suppression curves."
            },
            {
                "id": "apnea",
                "name": "Clinical Sleep Pathology: Sleep Apnea vs Insomnia",
                "algorithm": "Balanced Random Forest Classifier (100 Estimators)",
                "dataset": "Sleep Health & Lifestyle (simulated Kaggle dataset, 374 rows)",
                "metric_name": "Weighted F1-Score",
                "metric_value": "0.8933",
                "accuracy": "89.3%",
                "features": ["Age", "Sleep Duration", "Sleep Quality", "Activity Level", "Stress Level", "Heart Rate", "Daily Steps", "Systolic BP", "Diastolic BP"],
                "clinical_rationale": "Differentiates behavioral sleep latency from obstructive anatomical airway hypopnea."
            },
            {
                "id": "burnout",
                "name": "Digital Screen Stress & Burnout Screener",
                "algorithm": "HistGradientBoosting Regressor & Classifier Ensemble",
                "dataset": "Student Lifestyle & Digital Wellbeing (100,000 records)",
                "metric_name": "Stress Score RMSE",
                "metric_value": "1.48 / 10",
                "secondary_metric": "Depression Classification Accuracy: 86.4%",
                "features": ["Sleep_Duration", "Social_Media_Hours", "Physical_Activity", "Age"],
                "clinical_rationale": "Predicts subjective burnout and academic/workplace cognitive exhaustion."
            }
        ]
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


@app.post("/api/what-if")
def what_if_simulation(req: WhatIfRequest):
    """
    Re-runs the trained ML models on a modified copy of the profile
    (less bedtime phone use, more steps, earlier caffeine cutoff)
    and returns before/after values for the What-If simulator.
    """
    try:
        engine = orchestrator.ml_engine
        before = req.profile
        after = before.model_copy(update={
            "bedtime_phone_minutes": max(before.bedtime_phone_minutes - req.phone_reduction_min, 0),
            "daily_steps": min(before.daily_steps + req.extra_steps, 50000),
            "hours_caffeine_before_bed": min(before.hours_caffeine_before_bed + req.caffeine_cutoff_earlier_hours, 24.0),
        })

        lat0, fat0, _ = engine.predict_circadian_sleep(before)
        lat1, fat1, debt1 = engine.predict_circadian_sleep(after)
        heart0 = engine.predict_cardiovascular_risk(before)
        heart1 = engine.predict_cardiovascular_risk(after)

        return {
            "latency_reduction_minutes": round(max(lat0 - lat1, 0.0), 1),
            "projected_latency_minutes": lat1,
            "fatigue_score_reduction": round(max(fat0 - fat1, 0.0), 1),
            "projected_fatigue_score": fat1,
            "projected_sleep_debt_category": debt1,
            "cardio_risk_reduction_pct": round(max(heart0 - heart1, 0.0), 1),
            "projected_cardio_risk_pct": heart1,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"What-if error: {str(e)}")


@app.post("/api/consultation")
def generate_consultation(payload: ComprehensiveDiagnosticPayload):
    """
    Sends the computed diagnostic payload to local Qwen (via Ollama on GPU).
    If Ollama is offline, gracefully executes the deterministic clinical synthesizer.
    """
    try:
        report, mode = advisor.generate_consultation(payload)
        return {
            "report": report,
            "mode": mode,
            "model": advisor.model_name if mode == "qwen_gpu" else "Deterministic Clinical Synthesizer (Offline Zero-Crash Mode)"
        }
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
