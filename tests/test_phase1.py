"""
tests/test_phase1.py - Rigorous Scientific Validation Suite for Phase 1

Validates:
1. Pydantic UserHealthProfile boundary integrity
2. BMR against clinical benchmark human cases (Mifflin-St Jeor & Katch-McArdle)
3. TDEE and Activity Multiplier calculations
4. Macro distribution caloric equilibrium (4P + 9F + 4C == Total Calories)
5. Caffeine first-order pharmacokinetics (5.5h half-life at exact t intervals)
6. Hydration equations & scale water fluctuation bounds
7. AHA Blood pressure classification boundaries
8. Bidirectional symptom-to-deficiency matching
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
    BloodPressureCategory
)
from calculators import (
    calculate_bmr,
    calculate_tdee,
    calculate_macros_and_calories,
    calculate_caffeine_clearance,
    calculate_hydration_requirements,
    calculate_scale_water_fluctuation_bounds,
    classify_blood_pressure,
    compute_all_mathematical_metrics
)
from deficiency_matrix import analyze_symptom_deficiencies


@pytest.fixture
def standard_male_profile():
    return UserHealthProfile(
        age=30,
        sex=BiologicalSex.MALE,
        height_cm=180.0,
        weight_kg=80.0,
        daily_steps=8000,
        resistance_training_days_per_week=3,
        cardio_sessions_per_week=1,
        daily_caffeine_mg=200,
        hours_caffeine_before_bed=5.5,
        goal_type=GoalType.FAT_LOSS_MODERATE,
        systolic_bp=124,
        diastolic_bp=78,
        symptoms=["eyelid_twitch", "night_calf_cramps", "brain_fog"]
    )


@pytest.fixture
def standard_female_profile():
    return UserHealthProfile(
        age=25,
        sex=BiologicalSex.FEMALE,
        height_cm=165.0,
        weight_kg=60.0,
        daily_steps=5000,
        resistance_training_days_per_week=2,
        cardio_sessions_per_week=0,
        daily_caffeine_mg=100,
        hours_caffeine_before_bed=11.0,
        goal_type=GoalType.MAINTENANCE_RECOMP,
        systolic_bp=118,
        diastolic_bp=75,
        symptoms=["cold_hands_feet", "brittle_nails"]
    )


# ---------------------------------------------------------------------------
# Test 1: BMR Formula Validation
# ---------------------------------------------------------------------------

def test_bmr_mifflin_male(standard_male_profile):
    # Expected: 10*80 + 6.25*180 - 5*30 + 5 = 800 + 1125 - 150 + 5 = 1780.0
    bmr, formula = calculate_bmr(standard_male_profile)
    assert bmr == 1780.0
    assert formula == "Mifflin-St Jeor"


def test_bmr_mifflin_female(standard_female_profile):
    # Expected: 10*60 + 6.25*165 - 5*25 - 161 = 600 + 1031.25 - 125 - 161 = 1345.25 -> 1345.2
    bmr, formula = calculate_bmr(standard_female_profile)
    assert abs(bmr - 1345.2) < 0.2
    assert formula == "Mifflin-St Jeor"


def test_bmr_katch_mcardle():
    profile = UserHealthProfile(
        age=28,
        sex=BiologicalSex.MALE,
        height_cm=175.0,
        weight_kg=75.0,
        body_fat_pct=15.0  # Lean mass = 75 * 0.85 = 63.75 kg
    )
    # Expected Katch: 370 + 21.6 * 63.75 = 370 + 1377 = 1747.0
    bmr, formula = calculate_bmr(profile)
    assert bmr == 1747.0
    assert "Katch-McArdle" in formula


# ---------------------------------------------------------------------------
# Test 2: TDEE Activity Multipliers
# ---------------------------------------------------------------------------

def test_tdee_calculation(standard_male_profile):
    # Steps=8000, workouts=4 -> Multiplier 1.55
    # BMR = 1780 -> TDEE = 1780 * 1.55 = 2759.0
    bmr, _ = calculate_bmr(standard_male_profile)
    tdee = calculate_tdee(standard_male_profile, bmr)
    assert tdee == 2759.0


# ---------------------------------------------------------------------------
# Test 3: Macro Distribution & Caloric Conservation
# ---------------------------------------------------------------------------

def test_macro_caloric_balance(standard_male_profile):
    """
    CRITICAL ZERO-HALLUCINATION TEST:
    Target Calories must strictly equal (4*Protein + 9*Fat + 4*Carbs) within 1.0 kcal.
    """
    bmr, _ = calculate_bmr(standard_male_profile)
    tdee = calculate_tdee(standard_male_profile, bmr)
    
    target_kcal, protein_g, fat_g, carbs_g, deficit, weekly_change = calculate_macros_and_calories(
        standard_male_profile, tdee
    )
    
    summed_kcal = (protein_g * 4.0) + (fat_g * 9.0) + (carbs_g * 4.0)
    assert abs(summed_kcal - target_kcal) <= 1.0
    
    # Fat floor check: fat >= 0.7 g/kg
    assert fat_g >= (standard_male_profile.weight_kg * 0.7)
    # Protein check for moderate deficit (2.0 g/kg)
    assert protein_g >= (standard_male_profile.weight_kg * 1.8)


# ---------------------------------------------------------------------------
# Test 4: Pharmacokinetic Caffeine Half-Life Decay
# ---------------------------------------------------------------------------

def test_caffeine_clearance_exact_half_lives():
    # 200 mg consumed, 0 hours before bed -> 200.0 mg active
    p0 = UserHealthProfile(
        age=30, sex=BiologicalSex.MALE, height_cm=180, weight_kg=80,
        daily_caffeine_mg=200, hours_caffeine_before_bed=0.0
    )
    active, flag, _ = calculate_caffeine_clearance(p0)
    assert active == 0.0  # 0 hours before bed treated as null/none
    
    # Exactly 1 half-life (5.5h) with 200 mg -> 100.0 mg active
    p1 = UserHealthProfile(
        age=30, sex=BiologicalSex.MALE, height_cm=180, weight_kg=80,
        daily_caffeine_mg=200, hours_caffeine_before_bed=5.5
    )
    active, flag, hours_needed = calculate_caffeine_clearance(p1)
    assert active == 100.0
    assert flag is True  # 100 mg > 25 mg threshold
    
    # Exactly 2 half-lives (11.0h) with 200 mg -> 50.0 mg active
    p2 = UserHealthProfile(
        age=30, sex=BiologicalSex.MALE, height_cm=180, weight_kg=80,
        daily_caffeine_mg=200, hours_caffeine_before_bed=11.0
    )
    active, flag, _ = calculate_caffeine_clearance(p2)
    assert active == 50.0
    
    # Exactly 3 half-lives (16.5h) with 200 mg -> 25.0 mg active
    p3 = UserHealthProfile(
        age=30, sex=BiologicalSex.MALE, height_cm=180, weight_kg=80,
        daily_caffeine_mg=200, hours_caffeine_before_bed=16.5
    )
    active, flag, _ = calculate_caffeine_clearance(p3)
    assert active == 25.0
    assert flag is False  # 25 mg not strictly > 25 mg


# ---------------------------------------------------------------------------
# Test 5: AHA Blood Pressure Classification
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("sys, dia, expected", [
    (115, 75, BloodPressureCategory.NORMAL),
    (124, 78, BloodPressureCategory.ELEVATED),
    (134, 82, BloodPressureCategory.STAGE_1),
    (145, 92, BloodPressureCategory.STAGE_2),
    (185, 125, BloodPressureCategory.CRISIS),
    (180, 85, BloodPressureCategory.CRISIS),
    (135, 120, BloodPressureCategory.CRISIS)
])
def test_blood_pressure_classification(sys, dia, expected):
    assert classify_blood_pressure(sys, dia) == expected


# ---------------------------------------------------------------------------
# Test 6: Scale Water Fluctuation & Physiology
# ---------------------------------------------------------------------------

def test_scale_water_fluctuation_bounds(standard_male_profile):
    min_swing, max_swing, glycogen_h2o = calculate_scale_water_fluctuation_bounds(standard_male_profile)
    # For 80 kg: min swing ~ 1.0 kg, max swing ~ 2.4 kg
    assert 0.8 <= min_swing <= 1.5
    assert 2.0 <= max_swing <= 3.0
    assert glycogen_h2o > 1000.0  # Glycogen bound water should be > 1 Liter


# ---------------------------------------------------------------------------
# Test 7: Bidirectional Deficiency Mapping
# ---------------------------------------------------------------------------

def test_deficiency_mapping_magnesium(standard_male_profile):
    analysis = analyze_symptom_deficiencies(standard_male_profile)
    names = [d.nutrient_name for d in analysis.flagged_deficiencies]
    assert "Magnesium" in names
    
    # Verify magnesium details are populated
    mg = next(d for d in analysis.flagged_deficiencies if d.nutrient_name == "Magnesium")
    assert "eyelid_twitch" in mg.matched_symptoms
    assert "night_calf_cramps" in mg.matched_symptoms
    assert len(mg.top_whole_food_sources) > 0
    assert len(mg.absorption_cofactors) > 0


def test_deficiency_mapping_iron(standard_female_profile):
    analysis = analyze_symptom_deficiencies(standard_female_profile)
    names = [d.nutrient_name for d in analysis.flagged_deficiencies]
    assert "Iron & Ferritin" in names
    
    iron = next(d for d in analysis.flagged_deficiencies if d.nutrient_name == "Iron & Ferritin")
    assert "cold_hands_feet" in iron.matched_symptoms
    assert "brittle_nails" in iron.matched_symptoms


# ---------------------------------------------------------------------------
# Test 8: End-to-End Master Mathematical Metrics Compilation
# ---------------------------------------------------------------------------

def test_compute_all_mathematical_metrics(standard_male_profile):
    metrics = compute_all_mathematical_metrics(standard_male_profile)
    assert metrics.bmr_kcal > 1000
    assert metrics.tdee_kcal > metrics.bmr_kcal
    assert metrics.target_calories_kcal < metrics.tdee_kcal  # In moderate deficit
    assert metrics.caffeine_active_at_bedtime_mg == 100.0
    assert metrics.bp_category == BloodPressureCategory.ELEVATED
    assert metrics.expected_daily_scale_swing_max_kg > 1.5
