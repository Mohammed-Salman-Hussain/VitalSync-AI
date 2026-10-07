"""
safety_triage.py - Three-Tier Clinical Safety & Red-Flag Triage Engine

Enforces Rule 1 (Ethical Medical Safety & Non-Diagnostic Scope).
Evaluates biometrics, symptom constellations, and machine-learning risk outputs
to assign a definitive, deterministic clinical triage level:
- LEVEL 1 (🟢 Green): Lifestyle modifiable, safe for self-directed optimization.
- LEVEL 2 (🟡 Yellow): Persistent anomaly; recommend scheduling a routine PCP appointment.
- LEVEL 3 (🔴 Red): Critical red flag; emergency override, immediate clinical care.
"""

from typing import List
from schemas import (
    UserHealthProfile,
    MathematicalMetrics,
    MLRiskMetrics,
    TriageLevel,
    TriageAssessment,
    BloodPressureCategory
)


def evaluate_clinical_safety_triage(
    profile: UserHealthProfile,
    math_metrics: MathematicalMetrics,
    ml_metrics: MLRiskMetrics
) -> TriageAssessment:
    """
    Evaluates clinical safety triggers across biometrics, symptoms, and ML probabilities.
    Assigns the highest applicable triage level and generates appropriate clinical banners.
    """
    triggers: List[str] = []
    actions: List[str] = []
    emergency = False
    doctor_needed = False

    # -----------------------------------------------------------------------
    # 1. Level 3 (RED): Critical Emergency Red Flags
    # -----------------------------------------------------------------------
    # A. Hypertensive Crisis (>= 180 / >= 120 mmHg)
    if math_metrics.bp_category == BloodPressureCategory.CRISIS:
        emergency = True
        triggers.append(f"Hypertensive Crisis BP reading ({profile.systolic_bp}/{profile.diastolic_bp} mmHg).")
        actions.append("Re-check BP after 5 minutes of quiet rest. If still >=180/120, call emergency services (911/112) or go to the nearest emergency department.")

    # B. Acute Cardiac / Neurological Symptoms
    critical_symptoms = {
        "chest_pain_radiating": "Chest discomfort or pain radiating to the jaw, neck, or left arm.",
        "sudden_numbness_weakness": "Sudden numbness or weakness in face, arm, or leg (especially one side).",
        "acute_shortness_of_breath": "Severe shortness of breath at rest.",
        "severe_suicidal_crisis": "Active thoughts of self-harm or severe psychological crisis."
    }
    for sym_key, desc in critical_symptoms.items():
        if sym_key in profile.symptoms:
            emergency = True
            triggers.append(desc)
            actions.append("Seek immediate emergency medical evaluation. Do not drive yourself if experiencing acute cardiac or neurological symptoms.")

    if emergency:
        return TriageAssessment(
            level=TriageLevel.RED,
            badge_title="EMERGENCY MEDICAL ATTENTION REQUIRED",
            triggers=triggers,
            actions_required=actions,
            doctor_consultation_recommended=True,
            emergency_override=True,
            banner_message=(
                "CRITICAL CLINICAL ALERT: One or more of your indicators cross emergency safety thresholds. "
                "Lifestyle advice has been suppressed. Please seek immediate professional medical or emergency care."
            )
        )

    # -----------------------------------------------------------------------
    # 2. Level 2 (YELLOW): Routine Clinical Review Recommended
    # -----------------------------------------------------------------------
    # A. Stage 1 or Stage 2 Hypertension confirmed
    if math_metrics.bp_category in [BloodPressureCategory.STAGE_1, BloodPressureCategory.STAGE_2]:
        doctor_needed = True
        triggers.append(f"Elevated blood pressure ({math_metrics.bp_category.value}).")
        actions.append("Log your blood pressure twice daily for 7 days and schedule a routine consultation with your primary care physician.")

    # B. Elevated Sleep Apnea Risk (>60% probability or gasping)
    if ml_metrics.sleep_apnea_probability_pct >= 60.0 or profile.gasping_choking_nocturnal:
        doctor_needed = True
        triggers.append(f"High indicators of obstructive sleep apnea ({ml_metrics.sleep_apnea_probability_pct}% risk with nocturnal gasping/snoring).")
        actions.append("Request an overnight home sleep apnea test (HST) or polysomnography from an ear, nose, and throat (ENT) or sleep medicine specialist.")

    # C. Elevated Pre-Diabetes Risk (>65%)
    if ml_metrics.prediabetes_risk_pct >= 65.0:
        doctor_needed = True
        triggers.append(f"Elevated non-invasive pre-diabetes risk index ({ml_metrics.prediabetes_risk_pct}%).")
        actions.append("Ask your doctor for a routine fasting glucose or HbA1c blood test during your next regular checkup.")

    # D. Severe Chronic Sleep Debt with daytime fatigue > 8.0
    if ml_metrics.predicted_fatigue_score_1_to_10 >= 8.0 and ml_metrics.sleep_debt_category == "Severe Sleep Debt":
        doctor_needed = True
        triggers.append("Severe cumulative sleep deficit accompanied by acute daytime fatigue score >= 8/10.")
        actions.append("Evaluate whether shift work, medications, or untreated sleep architecture issues require clinical support.")

    if doctor_needed:
        return TriageAssessment(
            level=TriageLevel.YELLOW,
            badge_title="ROUTINE MEDICAL CONSULTATION RECOMMENDED",
            triggers=triggers,
            actions_required=actions,
            doctor_consultation_recommended=True,
            emergency_override=False,
            banner_message=(
                "HEALTHCARE PROVIDER CONSULTATION RECOMMENDED: Your data reflects persistent biometric or metabolic patterns "
                "that warrant a routine checkup with a primary care doctor. Bring this summary to your next appointment."
            )
        )

    # -----------------------------------------------------------------------
    # 3. Level 1 (GREEN): Lifestyle Modifiable
    # -----------------------------------------------------------------------
    return TriageAssessment(
        level=TriageLevel.GREEN,
        badge_title="LIFESTYLE MODIFIABLE & SAFE FOR BEHAVIORAL OPTIMIZATION",
        triggers=["All primary vitals within acceptable lifestyle baseline ranges."],
        actions_required=[
            "Optimize bedtime screen curfew and blue-light exposure.",
            "Maintain your targeted daily protein and hydration allocations.",
            "Continue tracking daily steps and active recovery."
        ],
        doctor_consultation_recommended=False,
        emergency_override=False,
        banner_message=(
            "LIFESTYLE OPTIMIZATION PROFILE: Your vitals and risk scores indicate your current symptoms are primarily "
            "responsive to behavioral, nutritional, and sleep hygiene modifications."
        )
    )
