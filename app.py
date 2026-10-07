"""
app.py - All-in-One AI Health & Lifestyle Advice Platform
Homogeneous Localhost Interface running on Streamlit + Local Python ML + Local Qwen (Ollama GPU)
"""

import streamlit as st
import pandas as pd
import numpy as np
from schemas import (
    UserHealthProfile,
    BiologicalSex,
    GoalType,
    AppCategory,
    Chronotype,
    TriageLevel,
    BloodPressureCategory
)
from orchestrator import HealthOrchestrator
from llm_advisor import QwenHealthAdvisor


# ---------------------------------------------------------------------------
# Page Configuration & Modern Theme Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="VitalSync AI - Holistic Health Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished, dark-mode, glassmorphism aesthetics
st.markdown("""
<style>
    .reportview-container {
        background: #0f172a;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        backdrop-filter: blur(8px);
    }
    .triage-green {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #10b981;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
    }
    .triage-yellow {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid #f59e0b;
        color: #f59e0b;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 600;
    }
    .triage-red {
        background: rgba(239, 68, 68, 0.2);
        border: 2px solid #ef4444;
        color: #ef4444;
        padding: 16px 20px;
        border-radius: 8px;
        font-weight: 700;
        animation: pulse 2s infinite;
    }
    .disclaimer-box {
        background: rgba(30, 41, 59, 0.5);
        border-left: 4px solid #3b82f6;
        padding: 10px 14px;
        font-size: 0.85rem;
        color: #94a3b8;
        border-radius: 4px;
        margin-bottom: 18px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Pipeline Initialization (Cached Singletons)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_orchestrator():
    return HealthOrchestrator()

@st.cache_resource
def get_advisor():
    return QwenHealthAdvisor()

orchestrator = get_orchestrator()
advisor = get_advisor()


# ---------------------------------------------------------------------------
# Sidebar: User Profile & Health Questionnaire
# ---------------------------------------------------------------------------
st.sidebar.title("🧬 User Health Profile")
intake_mode = st.sidebar.radio("Intake Depth", ["⚡ 2-Minute Quick Pulse", "🔬 Comprehensive Deep Checkup"])

# 1. Baseline Biometrics
st.sidebar.subheader("1. Vitals & Body Metrics")
age = st.sidebar.number_input("Age", min_value=18, max_value=95, value=32, step=1)
sex_val = st.sidebar.selectbox("Biological Sex", ["Male", "Female"])
sex = BiologicalSex.MALE if sex_val == "Male" else BiologicalSex.FEMALE

col_w, col_h = st.sidebar.columns(2)
weight_kg = col_w.number_input("Weight (kg)", min_value=35.0, max_value=220.0, value=78.0, step=0.5)
height_cm = col_h.number_input("Height (cm)", min_value=120.0, max_value=230.0, value=178.0, step=1.0)

col_bp1, col_bp2 = st.sidebar.columns(2)
systolic_bp = col_bp1.number_input("Systolic BP", min_value=80, max_value=230, value=124, step=1)
diastolic_bp = col_bp2.number_input("Diastolic BP", min_value=50, max_value=140, value=78, step=1)
resting_hr = st.sidebar.slider("Resting Heart Rate (BPM)", min_value=40, max_value=130, value=68)

body_fat_pct = None
waist_cm = None
if intake_mode == "🔬 Comprehensive Deep Checkup":
    col_bf, col_wst = st.sidebar.columns(2)
    bf_input = col_bf.number_input("Body Fat % (Optional)", min_value=0.0, max_value=60.0, value=0.0, step=0.5)
    body_fat_pct = bf_input if bf_input > 0 else None
    waist_input = col_wst.number_input("Waist (cm, Optional)", min_value=0.0, max_value=160.0, value=0.0, step=1.0)
    waist_cm = waist_input if waist_input > 0 else None

# 2. Sleep & Screen Time
st.sidebar.subheader("2. Sleep & Bedtime Screens")
actual_sleep = st.sidebar.slider("Actual Sleep Duration (hrs)", min_value=3.0, max_value=12.0, value=6.5, step=0.5)
bedtime_phone = st.sidebar.slider("Bedtime Phone Use (minutes)", min_value=0, max_value=180, value=45, step=5)

app_choice = st.sidebar.selectbox(
    "Primary Bedtime App",
    ["TikTok / Reels / Shorts", "Streaming (Netflix/YouTube)", "Messaging / Chat", "News / Reading / Audio"]
)
app_map = {
    "TikTok / Reels / Shorts": AppCategory.SHORT_FORM_VIDEO,
    "Streaming (Netflix/YouTube)": AppCategory.LONG_FORM_STREAMING,
    "Messaging / Chat": AppCategory.SOCIAL_MESSAGING,
    "News / Reading / Audio": AppCategory.READING_AUDIO
}
bedtime_app = app_map[app_choice]

blue_light = st.sidebar.checkbox("Blue Light Filter Active (Night Shift)", value=False)
snoring = st.sidebar.checkbox("Frequent Loud Snoring", value=False)
gasping = st.sidebar.checkbox("Nocturnal Gasping or Choking reported", value=False)

# 3. Stimulants, Diet & Activity
st.sidebar.subheader("3. Nutrition & Stimulants")
caffeine_mg = st.sidebar.slider("Daily Caffeine Intake (mg)", min_value=0, max_value=800, value=200, step=25)
caffeine_hours_before_bed = st.sidebar.slider("Hours between last coffee and bed", min_value=0.0, max_value=16.0, value=5.0, step=0.5)
daily_water = st.sidebar.slider("Daily Plain Water (Liters)", min_value=0.5, max_value=6.0, value=2.0, step=0.25)
steps = st.sidebar.slider("Daily Steps", min_value=1000, max_value=25000, value=7500, step=500)

goal_choice = st.sidebar.selectbox(
    "Primary Goal",
    ["Moderate Fat Loss (-15%)", "Aggressive Fat Loss (-25%)", "Maintenance & Recomposition", "Lean Muscle Bulk (+10%)"]
)
goal_map = {
    "Moderate Fat Loss (-15%)": GoalType.FAT_LOSS_MODERATE,
    "Aggressive Fat Loss (-25%)": GoalType.FAT_LOSS_AGGRESSIVE,
    "Maintenance & Recomposition": GoalType.MAINTENANCE_RECOMP,
    "Lean Muscle Bulk (+10%)": GoalType.LEAN_BULK
}
goal_type = goal_map[goal_choice]

# 4. Functional Everyday Symptoms
st.sidebar.subheader("4. Everyday Bodily Signals")
available_symptoms = [
    ("Brain Fog / Forgetfulness", "brain_fog"),
    ("Afternoon Energy Crash (2-4 PM)", "afternoon_crash"),
    ("Eyelid or Facial Twitching", "eyelid_twitch"),
    ("Nighttime Calf / Foot Cramps", "night_calf_cramps"),
    ("Restless Legs at Bedtime", "restless_legs"),
    ("Heart Flutter / Thumping after Coffee", "heart_flutter_post_coffee"),
    ("Cold Hands & Cold Feet", "cold_hands_feet"),
    ("Brittle Nails / Hair Shedding", "brittle_nails"),
    ("Post-Meal Bloating", "bloating"),
    ("Frequent Tension Headaches", "tension_headaches"),
    ("Difficulty Switching Off Brain", "difficulty_switching_off_brain")
]

selected_symptoms = []
for label, code in available_symptoms:
    if st.sidebar.checkbox(label, value=(code in ["afternoon_crash", "eyelid_twitch"])):
        selected_symptoms.append(code)

stress_rating = st.sidebar.slider("Perceived Stress Rating (1-10)", min_value=1, max_value=10, value=6)

# Construct Unified Profile State
profile = UserHealthProfile(
    age=age,
    sex=sex,
    height_cm=height_cm,
    weight_kg=weight_kg,
    waist_cm=waist_cm,
    body_fat_pct=body_fat_pct,
    systolic_bp=int(systolic_bp),
    diastolic_bp=int(diastolic_bp),
    resting_hr_bpm=int(resting_hr),
    actual_sleep_hours=float(actual_sleep),
    bedtime_phone_minutes=int(bedtime_phone),
    bedtime_app=bedtime_app,
    screen_brightness_pct=60,
    blue_light_filter_active=blue_light,
    snoring_frequent=snoring,
    gasping_choking_nocturnal=gasping,
    daily_caffeine_mg=int(caffeine_mg),
    hours_caffeine_before_bed=float(caffeine_hours_before_bed),
    daily_water_liters=float(daily_water),
    daily_steps=int(steps),
    resistance_training_days_per_week=3,
    cardio_sessions_per_week=1,
    goal_type=goal_type,
    symptoms=selected_symptoms,
    stress_level_1_to_10=int(stress_rating)
)


# ---------------------------------------------------------------------------
# Run Homogeneous Orchestration Pipeline
# ---------------------------------------------------------------------------
payload = orchestrator.process_health_profile(profile)
math_m = payload.math_metrics
ml_m = payload.ml_metrics
triage = payload.triage


# ---------------------------------------------------------------------------
# Main View Header & Safety Triage Banner
# ---------------------------------------------------------------------------
st.title("🧬 VitalSync AI: All-in-One Health & Lifestyle Platform")

st.markdown("""
<div class="disclaimer-box">
    <strong>⚖️ ETHICAL NOTICE & MEDICAL SAFETY:</strong> This platform provides lifestyle, wellness, and behavioral analysis designed to eliminate everyday health anxiety. 
    <strong>IT DOES NOT PROVIDE MEDICAL ADVICE OR MEDICAL DIAGNOSIS.</strong> Statistical probabilities are predictive indicators, not clinical determinations. 
    Always consult a qualified healthcare provider for medical concerns.
</div>
""", unsafe_allow_html=True)

# Render Dynamic Clinical Triage Status
if triage.level == TriageLevel.RED:
    st.markdown(f'<div class="triage-red">🚨 {triage.badge_title}<br>{triage.banner_message}</div>', unsafe_allow_html=True)
elif triage.level == TriageLevel.YELLOW:
    st.markdown(f'<div class="triage-yellow">⚠️ {triage.badge_title}<br>{triage.banner_message}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="triage-green">✅ {triage.badge_title}<br>{triage.banner_message}</div>', unsafe_allow_html=True)

st.write("")


# ---------------------------------------------------------------------------
# Interactive Platform Navigation Tabs
# ---------------------------------------------------------------------------
tabs = st.tabs([
    "📊 Master Health Dashboard",
    "🥗 Nutrition & Macro Architect",
    "☕ Circadian & Caffeine Clock",
    "🧩 Micronutrient Detective",
    "🔮 'What-If' Habit Simulator",
    "🧘 'Am I Okay?' De-escalator",
    "🩺 Dr. Qwen AI Consultation",
    "📄 Doctor Briefing Export"
])


# ---------------------------------------------------------------------------
# TAB 1: Master Health Dashboard
# ---------------------------------------------------------------------------
with tabs[0]:
    st.subheader("Biological Overview & Pre-Trained Risk Ensembles")
    
    # Top Row: Key Biometrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Body Mass Index (BMI)", f"{profile.bmi} kg/m²", "Healthy Range: 18.5 - 24.9")
    col2.metric("Resting Blood Pressure", f"{profile.systolic_bp}/{profile.diastolic_bp} mmHg", math_m.bp_category.value)
    col3.metric("BMR (Basal Metabolism)", f"{math_m.bmr_kcal} kcal/day", math_m.bmr_formula_used)
    col4.metric("TDEE (Daily Burn)", f"{math_m.tdee_kcal} kcal/day", f"Target: {math_m.target_calories_kcal} kcal")

    st.write("---")
    st.markdown("#### Machine Learning Predictive Ensembles (Calibrated on CDC & Kaggle Datasets)")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown("**10-Year Cardiovascular Risk**")
        st.metric("Cardio Odds", f"{ml_m.cardiovascular_10yr_risk_pct}%", "Trained on CDC 319k")
        st.progress(min(ml_m.cardiovascular_10yr_risk_pct / 100.0, 1.0))
        st.caption("CDC BRFSS epidemiological logistic regression pipeline.")

    with col_m2:
        st.markdown("**Pre-Diabetes Non-Invasive Screener**")
        st.metric("Pre-Diabetes Risk", f"{ml_m.prediabetes_risk_pct}%", "Trained on CDC 70k 50/50")
        st.progress(min(ml_m.prediabetes_risk_pct / 100.0, 1.0))
        st.caption("Gradient boosted dietary & vitals screener.")

    with col_m3:
        st.markdown("**Circadian Sleep Debt & Latency**")
        st.metric("Predicted Latency", f"~{ml_m.predicted_sleep_latency_min} min", ml_m.sleep_debt_category)
        st.metric("Next-Day Fatigue", f"{ml_m.predicted_fatigue_score_1_to_10} / 10")
        st.caption("Trained on 8,500 bedtime screen habits records.")

    with col_m4:
        st.markdown("**Sleep Apnea Triage**")
        st.metric("Apnea Probability", f"{ml_m.sleep_apnea_probability_pct}%", "Clinical Cohort")
        st.metric("Digital Burnout Index", f"{ml_m.digital_burnout_stress_score_1_to_10} / 10", "100k Student Data")
        st.caption("Random Forest classifier on clinical vitals.")


# ---------------------------------------------------------------------------
# TAB 2: Nutrition & Macro Architect
# ---------------------------------------------------------------------------
with tabs[1]:
    st.subheader("Precision Macronutrient Architect & Caloric Deficit Planner")
    
    col_n1, col_n2, col_n3, col_n4 = st.columns(4)
    col_n1.metric("Daily Calorie Target", f"{math_m.target_calories_kcal} kcal", f"{math_m.deficit_or_surplus_kcal} kcal deficit/surplus")
    col_n2.metric("Target Protein", f"{math_m.target_protein_g} g", f"~{(math_m.target_protein_g*4/math_m.target_calories_kcal*100):.1f}% calories")
    col_n3.metric("Dietary Fat Floor", f"{math_m.target_fat_g} g", f"~{(math_m.target_fat_g*9/math_m.target_calories_kcal*100):.1f}% calories")
    col_n4.metric("Carbohydrates", f"{math_m.target_carbs_g} g", f"~{(math_m.target_carbs_g*4/math_m.target_calories_kcal*100):.1f}% calories")

    st.write("---")
    col_plan1, col_plan2 = st.columns(2)
    with col_plan1:
        st.markdown("#### 🎯 Projected Weekly Progress")
        st.write(f"- **Weekly Projected Fat Loss/Gain:** `{math_m.weekly_weight_change_kg} kg/week`")
        st.write(f"- **30-Day Estimated Trajectory:** `{round(math_m.weekly_weight_change_kg * 4.3, 1)} kg`")
        st.write("- **Protein Strategy:** Preserves metabolically active lean muscle tissue during caloric reduction.")
        st.write("- **Fat Floor Safety:** Guarantees hormonal synthesis and fat-soluble vitamin absorption.")

    with col_plan2:
        st.markdown("#### ⚖️ Scale Weight Fluctuation Demystification (Anti-Anxiety)")
        st.info(
            f"**Normal 24-48h Scale Fluctuation Range:** `±{math_m.expected_daily_scale_swing_min_kg} to {math_m.expected_daily_scale_swing_max_kg} kg`\n\n"
            f"- **Estimated Glycogen Bound Water:** `{math_m.glycogen_water_bound_g / 1000.0:.1f} Liters` of intracellular water.\n"
            "- **The Science:** Gaining 1 kg of adipose tissue requires eating 7,700 kcal *above* your maintenance calories. Overnight scale jumps are almost entirely water shifts from sodium, carbohydrate glycogen binding, or digestive transit."
        )


# ---------------------------------------------------------------------------
# TAB 3: Circadian & Caffeine Clock
# ---------------------------------------------------------------------------
with tabs[2]:
    st.subheader("24-Hour Circadian Screen Latency & Caffeine Clearance Engine")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    col_c1.metric("Active Caffeine at Bedtime", f"{math_m.caffeine_active_at_bedtime_mg} mg", f"Consumed: {profile.daily_caffeine_mg} mg")
    col_c2.metric("Sleep Disruption Risk", "HIGH (Delayed Onset)" if math_m.caffeine_sleep_disruption_flag else "OPTIMAL (<25 mg)", "")
    col_c3.metric("Hours to Complete Clearance (<20mg)", f"~{math_m.caffeine_clearance_hours_needed} hours", "From last cup")

    st.write("---")
    st.markdown("#### Bedtime App Genre vs Sleep Latency Impact")
    st.write(f"- **Your Selected App:** `{profile.bedtime_app.value}` for `{profile.bedtime_phone_minutes} minutes`.")
    st.write(f"- **Predicted Sleep Latency:** `~{ml_m.predicted_sleep_latency_min} minutes` before actual sleep onset.")
    if profile.bedtime_app == AppCategory.SHORT_FORM_VIDEO:
        st.warning("⚠️ Short-form algorithmic feeds (TikTok/Reels) stimulate variable dopamine spikes, extending sleep latency by up to 25-40 minutes compared to static reading.")
    elif profile.bedtime_app == AppCategory.READING_AUDIO:
        st.success("✅ Low-stimulation reading or audio allows natural adenosine accumulation, promoting faster sleep onset.")


# ---------------------------------------------------------------------------
# TAB 4: Micronutrient Detective
# ---------------------------------------------------------------------------
with tabs[3]:
    st.subheader("Functional Medicine: Bidirectional Symptom-to-Deficiency Matrix")
    
    def_data = payload.deficiency_analysis
    if def_data.flagged_deficiencies:
        for match in def_data.flagged_deficiencies:
            with st.expander(f"🔍 {match.nutrient_name} (Confidence Match: {int(match.confidence_score*100)}%)"):
                st.write(f"**Biological Function:** {match.biological_function}")
                st.write(f"**Matching User Symptoms:** `{', '.join(match.matched_symptoms)}`")
                
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    st.markdown("**Top Whole-Food Dietary Sources:**")
                    for food in match.top_whole_food_sources:
                        st.write(f"- {food}")
                with col_f2:
                    st.markdown("**Crucial Absorption Rules:**")
                    st.write(f"- **Cofactors:** {', '.join(match.absorption_cofactors)}")
                    st.write(f"- **Inhibitors:** {', '.join(match.absorption_inhibitors)}")
                st.caption(f"💡 Safety Note: {match.safety_supplement_note}")
    else:
        st.success("No significant micronutrient shortfalls flagged based on your reported symptoms!")


# ---------------------------------------------------------------------------
# TAB 5: What-If Habit Simulator
# ---------------------------------------------------------------------------
with tabs[4]:
    st.subheader("Interactive Counterfactual Lifestyle Simulator")
    st.write("Simulate how behavioral modifications immediately lower your statistical health risks.")
    
    cf = ml_m.counterfactual_scenarios
    st.info(f"**Tested Scenario:** {cf.get('intervention_description')}")
    
    col_sim1, col_sim2, col_sim3 = st.columns(3)
    col_sim1.metric("Sleep Latency Drop", f"-{cf.get('latency_reduction_minutes')} min", f"New Latency: {cf.get('projected_latency_minutes')} min")
    col_sim2.metric("Fatigue Score Reduction", f"-{cf.get('fatigue_score_reduction')} pts", f"New Fatigue: {cf.get('projected_fatigue_score')}/10")
    col_sim3.metric("Cardio Risk Reduction", f"-{cf.get('cardio_risk_reduction_pct')}%", f"New Odds: {cf.get('projected_cardio_risk_pct')}%")


# ---------------------------------------------------------------------------
# TAB 6: Am I Okay? De-escalator
# ---------------------------------------------------------------------------
with tabs[5]:
    st.subheader("🧘 'Am I Okay?' 60-Second Symptom De-escalator")
    st.write("Click any common bodily sensation to receive instant, calm physiological demystification:")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("💓 Why is my heart pounding after coffee or in bed?"):
            st.info(
                "**The Reassurance:** In 95%+ of healthy adults, post-caffeine or bedtime heart thumping is a benign autonomic response. "
                "Caffeine temporarily blocks adenosine receptors, heightening adrenaline sensitivity. In the quiet of night, resting chest sensations feel magnified. "
                "As long as resting heart rate is <100 BPM and there is no chest pain or shortness of breath, this is an autonomic arousal response, not a cardiac emergency."
            )
        if st.button("⚖️ Why did the scale jump 2 kg (4.5 lbs) overnight?"):
            st.info(
                "**The Reassurance:** Gaining 1 kg of true adipose fat requires consuming ~7,700 kcal *above* maintenance in a single day. "
                "A rapid scale jump is almost always harmless water retention: each gram of stored dietary carbohydrate binds 3 to 4 grams of water in muscle tissue, "
                "and sodium shifts hold temporary fluid. Your body weight will normalize naturally over 48-72 hours."
            )

    with col_b2:
        if st.button("👁️ Why is my eyelid or calf twitching?"):
            st.info(
                "**The Reassurance:** Benign eyelid flutter (myokymia) and calf twitches are hallmark bodily signals of **Magnesium depletion, elevated stress/cortisol, and stimulant overconsumption**. "
                "Magnesium is required for neuromuscular relaxation; when depleted by stress or high caffeine, tiny involuntary twitches fire. "
                "Hydrating with electrolytes and eating a handful of pumpkin seeds or dark chocolate usually resolves it."
            )
        if st.button("📉 Why do I crash every day at 3:00 PM?"):
            st.info(
                "**The Reassurance:** An afternoon energy slump is a biological combination of your body's natural circadian core body temperature dip "
                "coupled with high-glycemic lunch insulin clearance. Ensuring your lunch contains 30g+ of protein and taking a brisk 10-minute walk offsets this slump."
            )


# ---------------------------------------------------------------------------
# TAB 7: Dr. Qwen AI Consultation
# ---------------------------------------------------------------------------
with tabs[6]:
    st.subheader("🩺 Local 'Dr. Qwen' AI Consultation (Ollama GPU)")
    st.write("Generates a grounded, empathetic, clinician-grade synthesis based strictly on your computed diagnostic payload.")
    
    if st.button("Generate Full Consultation Report with Local Qwen", type="primary"):
        with st.spinner("Local Qwen (qwen3.5:0.8b on GPU) is analyzing your multi-model metrics..."):
            report_placeholder = st.empty()
            
            def stream_updater(chunk):
                pass  # Streamlit update
                
            report = advisor.generate_consultation(payload)
            report_placeholder.markdown(report)

    st.write("---")
    st.markdown("#### Ask Dr. Qwen a Specific Everyday Health Query")
    user_q = st.text_input("Ask about any health question, myth, or symptom (e.g., 'Is cold plunging good for cortisol?'):")
    if st.button("Ask Qwen"):
        if user_q:
            with st.spinner("Qwen is formulating an evidence-based biological explanation..."):
                answer = advisor.answer_health_question(user_q, payload)
                st.markdown(answer)


# ---------------------------------------------------------------------------
# TAB 8: Doctor Briefing Export
# ---------------------------------------------------------------------------
with tabs[7]:
    st.subheader("📄 Clinical Summary Briefing for Primary Care Physician")
    st.write("Download or print a standardized, clean 1-page clinical log to share with your real-life doctor.")
    
    briefing_md = orchestrator.generate_doctor_briefing_markdown(payload)
    st.markdown(briefing_md)
    
    st.download_button(
        label="📥 Download Doctor Briefing (Markdown)",
        data=briefing_md,
        file_name=f"clinical_briefing_{profile.age}_{profile.sex.value}.md",
        mime="text/markdown"
    )
