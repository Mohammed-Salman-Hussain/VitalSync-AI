"""
orchestrator.py - Central Health Intelligence Orchestrator

The central nervous system of the All-in-One Health Platform:
- Ingests a validated UserHealthProfile.
- Executes scientific mathematical engines (BMR, TDEE, macros, caffeine clearance).
- Runs functional medicine symptom-to-deficiency mappings.
- Runs all 5 calibrated machine learning models.
- Executes the clinical safety & red-flag triage engine.
- Bundles everything into a homogeneous ComprehensiveDiagnosticPayload.
- Provides a clean 'Doctor Visit Briefing' Markdown generator for clinical sharing.
"""

from datetime import datetime, timezone
from schemas import (
    UserHealthProfile,
    ComprehensiveDiagnosticPayload,
    TriageLevel
)
from calculators import compute_all_mathematical_metrics
from deficiency_matrix import analyze_symptom_deficiencies
from ml_inference import MLInferenceEngine
from safety_triage import evaluate_clinical_safety_triage


class HealthOrchestrator:
    """
    Central pipeline orchestrator linking user profiles to calculators,
    ML models, deficiency knowledge graphs, and safety triage.
    """
    def __init__(self):
        self.ml_engine = MLInferenceEngine()

    def process_health_profile(self, profile: UserHealthProfile) -> ComprehensiveDiagnosticPayload:
        """
        Executes the full homogeneous diagnostic pipeline in <30ms.
        """
        # 1. Validated Scientific Calculations
        math_metrics = compute_all_mathematical_metrics(profile)

        # 2. Functional Micronutrient Deficiency Analysis
        deficiency_analysis = analyze_symptom_deficiencies(profile)

        # 3. Multi-Model ML Statistical Inference
        ml_metrics = self.ml_engine.compute_all_ml_metrics(profile)

        # 4. Clinical Safety & Red-Flag Triage
        triage = evaluate_clinical_safety_triage(profile, math_metrics, ml_metrics)

        return ComprehensiveDiagnosticPayload(
            profile=profile,
            math_metrics=math_metrics,
            deficiency_analysis=deficiency_analysis,
            triage=triage,
            ml_metrics=ml_metrics,
            generated_at=datetime.now(timezone.utc)
        )

    def generate_doctor_briefing_markdown(self, payload: ComprehensiveDiagnosticPayload) -> str:
        """
        Generates a clean, professional, 1-page summary markdown designed to be
        printed or shown directly to a primary care physician.
        """
        p = payload.profile
        m = payload.math_metrics
        ml = payload.ml_metrics
        t = payload.triage

        lines = [
            "# CLINICAL SUMMARY BRIEFING: LIFESTYLE & VITALS LOG",
            f"**Generated On:** {payload.generated_at.strftime('%Y-%m-%d %H:%M UTC')} | **Triage Status:** {t.badge_title}",
            "",
            "---",
            "### 1. Patient Demographics & Baseline Vitals",
            f"- **Age / Biological Sex:** {p.age} years | {p.sex.value.capitalize()}",
            f"- **Height / Weight:** {p.height_cm} cm | {p.weight_kg} kg (BMI: {p.bmi} kg/m²)",
            f"- **Resting Blood Pressure:** {p.systolic_bp}/{p.diastolic_bp} mmHg ({m.bp_category.value})",
            f"- **Resting Heart Rate:** {p.resting_hr_bpm} BPM",
            f"- **Daily Activity:** ~{p.daily_steps:,} steps/day | Resistance: {p.resistance_training_days_per_week}x/wk | Cardio: {p.cardio_sessions_per_week}x/wk",
            "",
            "### 2. Circadian & Sleep Architecture",
            f"- **Reported Sleep Duration:** {p.actual_sleep_hours} hours | Bedtime Phone Usage: {p.bedtime_phone_minutes} min ({p.bedtime_app.value})",
            f"- **Predicted Sleep Latency:** ~{ml.predicted_sleep_latency_min} minutes",
            f"- **Sleep Debt Assessment:** {ml.sleep_debt_category} (Next-Day Fatigue: {ml.predicted_fatigue_score_1_to_10}/10)",
            f"- **Sleep Pathology Screen:** {ml.sleep_apnea_probability_pct}% Apnea Risk (Snoring: {'Yes' if p.snoring_frequent else 'No'}, Gasping: {'Yes' if p.gasping_choking_nocturnal else 'No'})",
            "",
            "### 3. Epidemiological Risk Screeners (CDC BRFSS Models)",
            f"- **10-Year Cardiovascular Lifestyle Risk:** {ml.cardiovascular_10yr_risk_pct}%",
            f"- **Pre-Diabetes Non-Invasive Risk:** {ml.prediabetes_risk_pct}%",
            "",
            "### 4. Active Patient-Reported Symptoms",
            f"- **Reported Symptoms:** {', '.join(p.symptoms) if p.symptoms else 'None reported'}",
            f"- **Subjective Stress Rating:** {p.stress_level_1_to_10} / 10",
            "",
            "### 5. Nutrition & Substance Intake",
            f"- **Estimated TDEE:** {m.tdee_kcal} kcal | Target: {m.target_calories_kcal} kcal (Protein: {m.target_protein_g}g, Fat: {m.target_fat_g}g, Carbs: {m.target_carbs_g}g)",
            f"- **Daily Caffeine:** {p.daily_caffeine_mg} mg (Est. Active at Bedtime: {m.caffeine_active_at_bedtime_mg} mg)",
            f"- **Alcohol:** {p.alcohol_drinks_per_week} drinks/week",
            "",
            "### 6. Clinical Triage Notes & Triggers",
            f"- **Status Level:** {t.level.value.upper()}",
            f"- **Identified Triggers:** {'; '.join(t.triggers)}",
            f"- **Recommended Clinical Actions:** {'; '.join(t.actions_required)}",
            "",
            "---",
            "*(This summary was automatically compiled by the user's local wellness tracking platform. It is provided for informational and clinical review purposes only.)*"
        ]
        return "\n".join(lines)
