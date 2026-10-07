"""
tests/test_phase3_4.py - Validation Suite for Central Orchestrator & Safety Engine

Validates:
1. HealthOrchestrator pipeline execution end-to-end
2. Safety Triage boundary conditions (Green vs Yellow vs Red)
3. Emergency override triggered on Hypertensive Crisis BP
4. Doctor Briefing Markdown export formatting
5. Qwen Health Advisor prompt construction
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from schemas import (
    UserHealthProfile,
    BiologicalSex,
    GoalType,
    AppCategory,
    Chronotype,
    TriageLevel,
    BloodPressureCategory,
    ComprehensiveDiagnosticPayload
)
from orchestrator import HealthOrchestrator
from llm_advisor import QwenHealthAdvisor


@pytest.fixture
def green_profile():
    return UserHealthProfile(
        age=26,
        sex=BiologicalSex.FEMALE,
        height_cm=168.0,
        weight_kg=62.0,
        systolic_bp=116,
        diastolic_bp=74,
        resting_hr_bpm=65,
        actual_sleep_hours=7.5,
        daily_steps=9000,
        symptoms=["brain_fog"],
        goal_type=GoalType.MAINTENANCE_RECOMP
    )


@pytest.fixture
def yellow_profile():
    return UserHealthProfile(
        age=52,
        sex=BiologicalSex.MALE,
        height_cm=178.0,
        weight_kg=96.0,
        systolic_bp=146,  # Stage 2 Hypertension
        diastolic_bp=94,
        resting_hr_bpm=82,
        actual_sleep_hours=5.5,
        daily_steps=3500,
        snoring_frequent=True,
        gasping_choking_nocturnal=True,  # Severe apnea indicator
        symptoms=["night_calf_cramps", "chronic_fatigue"],
        goal_type=GoalType.FAT_LOSS_MODERATE
    )


@pytest.fixture
def red_crisis_profile():
    return UserHealthProfile(
        age=58,
        sex=BiologicalSex.MALE,
        height_cm=175.0,
        weight_kg=88.0,
        systolic_bp=188,  # Hypertensive Crisis (>=180)
        diastolic_bp=124,
        resting_hr_bpm=102,
        actual_sleep_hours=4.0,
        symptoms=["chest_pain_radiating"]  # Emergency red flag
    )


def test_orchestrator_pipeline_green(green_profile):
    orchestrator = HealthOrchestrator()
    payload = orchestrator.process_health_profile(green_profile)
    
    assert isinstance(payload, ComprehensiveDiagnosticPayload)
    assert payload.math_metrics.bmr_kcal > 1000
    assert payload.ml_metrics is not None
    assert payload.triage.level == TriageLevel.GREEN
    assert payload.triage.emergency_override is False


def test_orchestrator_pipeline_yellow(yellow_profile):
    orchestrator = HealthOrchestrator()
    payload = orchestrator.process_health_profile(yellow_profile)
    
    assert payload.triage.level == TriageLevel.YELLOW
    assert payload.triage.doctor_consultation_recommended is True
    assert payload.triage.emergency_override is False
    assert len(payload.triage.triggers) >= 1


def test_orchestrator_pipeline_red_crisis(red_crisis_profile):
    orchestrator = HealthOrchestrator()
    payload = orchestrator.process_health_profile(red_crisis_profile)
    
    assert payload.triage.level == TriageLevel.RED
    assert payload.triage.emergency_override is True
    assert "Hypertensive Crisis" in payload.triage.triggers[0]


def test_doctor_briefing_export(green_profile):
    orchestrator = HealthOrchestrator()
    payload = orchestrator.process_health_profile(green_profile)
    briefing = orchestrator.generate_doctor_briefing_markdown(payload)
    
    assert "# CLINICAL SUMMARY BRIEFING" in briefing
    assert str(green_profile.age) in briefing
    assert str(green_profile.systolic_bp) in briefing
    assert "Cardiovascular" in briefing


def test_qwen_advisor_prompt_building(green_profile):
    orchestrator = HealthOrchestrator()
    payload = orchestrator.process_health_profile(green_profile)
    
    advisor = QwenHealthAdvisor()
    prompt = advisor._build_consultation_prompt(payload)
    
    assert "ANTI-CYBERCHONDRIA" in prompt
    assert str(green_profile.height_cm) in prompt
    assert str(payload.math_metrics.tdee_kcal) in prompt
    assert "Top 3 High-Impact Action Levers" in prompt
