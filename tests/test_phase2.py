"""
tests/test_phase2.py - Validation Suite for Machine Learning Models & Inference Pipeline

Validates:
1. All 5 serialized model bundles exist in models/
2. MLInferenceEngine loads and executes cleanly
3. Calibrated probability bounds (0.0 <= prob <= 100.0%)
4. Continuous score bounds (Fatigue: 1-10, Stress: 1-10)
5. Counterfactual simulations produce logical, non-negative health improvements
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
    MLRiskMetrics
)
from ml_inference import MLInferenceEngine


@pytest.fixture
def sample_user_profile():
    return UserHealthProfile(
        age=45,
        sex=BiologicalSex.MALE,
        height_cm=175.0,
        weight_kg=92.0,  # BMI ~30 (Obese class 1)
        systolic_bp=138,
        diastolic_bp=88,
        resting_hr_bpm=78,
        actual_sleep_hours=6.0,
        bedtime_phone_minutes=60,
        bedtime_app=AppCategory.SHORT_FORM_VIDEO,
        screen_brightness_pct=70,
        blue_light_filter_active=False,
        daily_steps=4000,
        social_media_hours=3.5,
        daily_caffeine_mg=250,
        hours_caffeine_before_bed=4.0,
        fruit_veg_servings=1,
        fast_food_meals_per_week=4,
        stress_level_1_to_10=7,
        snoring_frequent=True
    )


def test_models_exist_on_disk():
    expected_models = [
        "cardio_risk_model.joblib",
        "prediabetes_screener_model.joblib",
        "circadian_sleep_models.joblib",
        "sleep_pathology_model.joblib",
        "digital_burnout_model.joblib"
    ]
    for model_file in expected_models:
        path = os.path.join("models", model_file)
        assert os.path.exists(path), f"Missing model bundle: {path}"


def test_ml_inference_engine_predictions(sample_user_profile):
    engine = MLInferenceEngine()
    metrics = engine.compute_all_ml_metrics(sample_user_profile)
    
    assert isinstance(metrics, MLRiskMetrics)
    
    # 1. Cardio Risk Check
    assert 0.0 <= metrics.cardiovascular_10yr_risk_pct <= 100.0
    
    # 2. Pre-Diabetes Risk Check
    assert 0.0 <= metrics.prediabetes_risk_pct <= 100.0
    
    # 3. Circadian Latency & Fatigue Check
    assert metrics.predicted_sleep_latency_min >= 5.0
    assert 1.0 <= metrics.predicted_fatigue_score_1_to_10 <= 10.0
    assert metrics.sleep_debt_category in [
        "Optimal Recovery", "Mild Deficit", "Moderate Debt", "Severe Sleep Debt"
    ]
    
    # 4. Sleep Apnea Probability
    assert 0.0 <= metrics.sleep_apnea_probability_pct <= 100.0
    
    # 5. Burnout Stress Index
    assert 1.0 <= metrics.digital_burnout_stress_score_1_to_10 <= 10.0
    
    # 6. Counterfactual Verification
    cf = metrics.counterfactual_scenarios
    assert "latency_reduction_minutes" in cf
    assert cf["latency_reduction_minutes"] >= 0.0
    assert cf["fatigue_score_reduction"] >= 0.0
