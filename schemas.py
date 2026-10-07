"""
schemas.py - Unified Pydantic Models for All-in-One AI Health Platform

Ensures homogeneous state across scientific mathematical engines,
machine learning models, functional deficiency matrices, clinical safety triage,
and local Qwen LLM synthesis.
"""

from enum import Enum
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field, model_validator


class BiologicalSex(str, Enum):
    MALE = "male"
    FEMALE = "female"


class GoalType(str, Enum):
    FAT_LOSS_AGGRESSIVE = "fat_loss_aggressive"    # -25% caloric deficit
    FAT_LOSS_MODERATE = "fat_loss_moderate"        # -15% caloric deficit
    MAINTENANCE_RECOMP = "maintenance_recomp"      # Caloric maintenance, high protein
    LEAN_BULK = "lean_bulk"                        # +10% caloric surplus


class AppCategory(str, Enum):
    SHORT_FORM_VIDEO = "short_form_video"   # TikTok, IG Reels, YT Shorts (highest dopamine/latency)
    LONG_FORM_STREAMING = "streaming"       # Netflix, Hulu, YouTube essays
    SOCIAL_MESSAGING = "messaging"          # WhatsApp, Discord, iMessage
    READING_AUDIO = "reading_audio"         # E-reader, Podcasts, Audiobooks (lowest latency)


class Chronotype(str, Enum):
    MORNING_LARK = "morning_lark"
    INTERMEDIATE = "intermediate"
    NIGHT_OWL = "night_owl"


class TriageLevel(str, Enum):
    GREEN = "green"    # Lifestyle modifiable, safe for self-directed behavioral optimization
    YELLOW = "yellow"  # Routine clinical review recommended (PCP appointment)
    RED = "red"        # Emergency clinical warning, immediate medical care required


class BloodPressureCategory(str, Enum):
    NORMAL = "Normal (<120 and <80)"
    ELEVATED = "Elevated (120-129 and <80)"
    STAGE_1 = "Stage 1 Hypertension (130-139 or 80-89)"
    STAGE_2 = "Stage 2 Hypertension (140+ or 90+)"
    CRISIS = "Hypertensive Crisis (>=180 or >=120)"


# ---------------------------------------------------------------------------
# Core User Profile Schema (Unified Input Contract)
# ---------------------------------------------------------------------------

class UserHealthProfile(BaseModel):
    """
    Central user state ingested by all platform engines.
    Covers biometrics, circadian sleep habits, digital habits, nutrition,
    stimulants, physical movement, everyday functional symptoms, and goals.
    """
    # 1. Demographics & Body Vitals
    age: int = Field(..., ge=12, le=120, description="Age in years")
    sex: BiologicalSex = Field(..., description="Biological sex for metabolic baseline")
    height_cm: float = Field(..., ge=80.0, le=250.0, description="Height in centimeters")
    weight_kg: float = Field(..., ge=30.0, le=350.0, description="Weight in kilograms")
    waist_cm: Optional[float] = Field(None, ge=40.0, le=200.0, description="Waist circumference in cm")
    body_fat_pct: Optional[float] = Field(None, ge=3.0, le=70.0, description="Body fat percentage if known")
    
    systolic_bp: int = Field(120, ge=70, le=260, description="Resting systolic blood pressure (mmHg)")
    diastolic_bp: int = Field(80, ge=40, le=160, description="Resting diastolic blood pressure (mmHg)")
    resting_hr_bpm: int = Field(70, ge=35, le=220, description="Resting heart rate in beats per minute")

    # 2. Sleep & Circadian Mechanics
    bedtime_hour: float = Field(23.5, ge=0.0, lt=24.0, description="Bedtime in 24h format (e.g. 23.5 = 11:30 PM)")
    wake_hour: float = Field(7.5, ge=0.0, lt=24.0, description="Wake time in 24h format (e.g. 7.5 = 7:30 AM)")
    actual_sleep_hours: float = Field(7.0, ge=1.0, le=16.0, description="Self-reported actual sleep hours")
    chronotype: Chronotype = Field(Chronotype.INTERMEDIATE, description="Circadian chronotype")
    snooze_count: int = Field(1, ge=0, le=10, description="Number of morning alarm snoozes")
    snoring_frequent: bool = Field(False, description="Does the user snore loudly most nights?")
    gasping_choking_nocturnal: bool = Field(False, description="Has anyone reported gasping or breathing pauses?")

    # 3. Digital Habits & Bedtime Screen Time
    total_screen_time_hours: float = Field(6.0, ge=0.0, le=20.0, description="Total daily device screen time")
    social_media_hours: float = Field(2.5, ge=0.0, le=16.0, description="Daily hours on social media")
    bedtime_phone_minutes: int = Field(45, ge=0, le=240, description="Phone use minutes in bed before sleep")
    bedtime_app: AppCategory = Field(AppCategory.SHORT_FORM_VIDEO, description="Primary app used before sleep")
    screen_brightness_pct: int = Field(50, ge=10, le=100, description="Bedtime screen brightness percentage")
    blue_light_filter_active: bool = Field(False, description="Is Night Shift / blue light filter enabled?")

    # 4. Nutrition, Hydration & Eating Patterns
    daily_water_liters: float = Field(2.0, ge=0.2, le=10.0, description="Daily plain water intake in liters")
    fruit_veg_servings: int = Field(2, ge=0, le=15, description="Daily servings of fresh fruits and vegetables")
    fast_food_meals_per_week: int = Field(2, ge=0, le=21, description="Fast food / fried meals per week")
    hours_last_meal_to_bed: float = Field(2.0, ge=0.0, le=8.0, description="Hours between last food intake and bed")

    # 5. Stimulants & Substances
    daily_caffeine_mg: int = Field(150, ge=0, le=1200, description="Total daily caffeine in milligrams")
    hours_caffeine_before_bed: float = Field(6.0, ge=0.0, le=24.0, description="Hours between last caffeine and bedtime")
    alcohol_drinks_per_week: int = Field(2, ge=0, le=60, description="Alcoholic beverages per week")
    alcohol_near_bedtime: bool = Field(False, description="Consumed alcohol within 3 hours of sleep")
    smoker_or_vaper: bool = Field(False, description="Active cigarette smoker or e-cigarette user")

    # 6. Physical Activity & Movement
    daily_steps: int = Field(6500, ge=500, le=50000, description="Average daily step count")
    resistance_training_days_per_week: int = Field(2, ge=0, le=7, description="Days doing resistance/weight training")
    cardio_sessions_per_week: int = Field(2, ge=0, le=14, description="Cardiovascular / aerobic exercise sessions")
    desk_job_sedentary: bool = Field(True, description="Spends 7+ hours seated for work/study")

    # 7. Functional Bodily Symptoms & Subjective Signals (Multi-select)
    symptoms: List[str] = Field(
        default_factory=list,
        description="Active everyday symptoms (e.g. brain_fog, eyelid_twitch, afternoon_crash, bloating, etc.)"
    )

    # 8. Goals & Stress Load
    goal_type: GoalType = Field(GoalType.MAINTENANCE_RECOMP, description="Primary body composition / health goal")
    stress_level_1_to_10: int = Field(5, ge=1, le=10, description="Subjective perceived stress rating (1-10)")

    @property
    def bmi(self) -> float:
        """Body Mass Index (kg/m^2)"""
        height_m = self.height_cm / 100.0
        return round(self.weight_kg / (height_m ** 2), 2)


# ---------------------------------------------------------------------------
# Output Schemas: Calculated Scientific Metrics
# ---------------------------------------------------------------------------

class MathematicalMetrics(BaseModel):
    """Rigorous, unit-tested biological and mathematical outputs."""
    bmr_kcal: float
    bmr_formula_used: str  # 'Mifflin-St Jeor' or 'Katch-McArdle'
    tdee_kcal: float
    target_calories_kcal: float
    target_protein_g: float
    target_fat_g: float
    target_carbs_g: float
    deficit_or_surplus_kcal: float
    weekly_weight_change_kg: float
    
    # Caffeine Pharmacokinetics
    caffeine_active_at_bedtime_mg: float
    caffeine_sleep_disruption_flag: bool
    caffeine_clearance_hours_needed: float

    # Hydration
    water_recommended_liters: float
    water_deficit_liters: float

    # Water Fluctuation Physiology (Anti-Anxiety Explainer)
    expected_daily_scale_swing_min_kg: float
    expected_daily_scale_swing_max_kg: float
    glycogen_water_bound_g: float

    # Blood Pressure Classification
    bp_category: BloodPressureCategory


# ---------------------------------------------------------------------------
# Output Schemas: Functional Deficiency & Nutrient Detective
# ---------------------------------------------------------------------------

class MicronutrientMatch(BaseModel):
    nutrient_name: str
    confidence_score: float  # 0.0 to 1.0 based on matching symptom count
    matched_symptoms: List[str]
    biological_function: str
    top_whole_food_sources: List[str]
    absorption_cofactors: List[str]
    absorption_inhibitors: List[str]
    safety_supplement_note: str


class NutrientDeficiencyAnalysis(BaseModel):
    flagged_deficiencies: List[MicronutrientMatch]
    total_symptoms_evaluated: int
    primary_lifestyle_levers: List[str]


# ---------------------------------------------------------------------------
# Output Schemas: Safety & Clinical Red-Flag Triage
# ---------------------------------------------------------------------------

class TriageAssessment(BaseModel):
    level: TriageLevel
    badge_title: str
    triggers: List[str]
    actions_required: List[str]
    doctor_consultation_recommended: bool
    emergency_override: bool
    banner_message: str


# ---------------------------------------------------------------------------
# Output Schemas: Machine Learning Preventive Risk Indicators
# ---------------------------------------------------------------------------

class MLRiskMetrics(BaseModel):
    """Calibrated statistical risks from Kaggle & CDC models."""
    cardiovascular_10yr_risk_pct: float
    prediabetes_risk_pct: float
    sleep_debt_category: str
    predicted_sleep_latency_min: float
    predicted_fatigue_score_1_to_10: float
    sleep_apnea_probability_pct: float
    digital_burnout_stress_score_1_to_10: float
    counterfactual_scenarios: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# The Master Diagnostic Payload (Homogeneous State passed to Qwen & UI)
# ---------------------------------------------------------------------------

class ComprehensiveDiagnosticPayload(BaseModel):
    profile: UserHealthProfile
    math_metrics: MathematicalMetrics
    deficiency_analysis: NutrientDeficiencyAnalysis
    triage: TriageAssessment
    ml_metrics: Optional[MLRiskMetrics] = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
