# Master Project Plan: All-in-One AI Health & Lifestyle Platform
### *A Homogeneous, Scientifically Grounded, Local-First Health Advisory System*

---

> ### ⚖️ ETHICAL CONSTITUTION & MEDICAL DISCLAIMER
> **THIS SOFTWARE PROVIDES LIFESTYLE, BEHAVIORAL, AND WELLNESS ANALYSIS DESIGNED TO CREATE A GROUNDED, EDUCATIONAL, AND ANXIETY-REDUCING EXPERIENCE THAT IS FAR SUPERIOR TO GENERIC SEARCH ENGINES OR ALARMIST ONLINE HEALTH ARTICLES.**
>
> **THIS PLATFORM DOES NOT PROVIDE MEDICAL DIAGNOSES, CLINICAL TREATMENT, PRESCRIPTIONS, OR THERAPY. IT IS NOT A SUBSTITUTE FOR PROFESSIONAL MEDICAL ADVICE, DIAGNOSIS, OR CLINICAL JUDGMENT.**
>
> All machine-learning probabilities and health indices are statistical risk indicators, not definitive diagnoses. If you experience severe, persistent, or worsening symptoms—or urgent red-flag warning signs (e.g., crushing chest pressure, sudden numbness or speech difficulty, severe shortness of breath)—seek immediate emergency medical care or consult a licensed healthcare professional.

---

## 1. Chat Trajectory & Context Analysis

Our project evolved through a focused, user-guided progression:

```
                                  PROJECT EVOLUTION
                                          │
    ┌─────────────────────────────────────┼─────────────────────────────────────┐
    ▼                                     ▼                                     ▼
1. Initial Inception:                 2. Scope Expansion:                   3. Platform Vision:
   Bedtime screentime dataset &          Downloaded & verified 6 Kaggle        All-in-one AI health advice
   UN SDG 3 (Good Health &               datasets (Heart, Diabetes, Sleep,     software with local Qwen
   Well-being) focus.                    Fitbit, Depression, Obesity).         Ollama on GPU.
                                          │
                                          ▼
                             4. Philosophy & Architecture:
                                Anti-Cyberchondria (breaking health anxiety),
                                exhaustive input taxonomy, zero hallucinations,
                                validated science, homogeneous orchestration.
```

1. **Phase 0 (Initial Seed)**: Started with the Kaggle dataset `samartalwar/sleep-debt-and-screen-time-late-night-phone-habits` to examine sleep latency, bedtime phone usage, and UN Sustainable Development Goal 3 (Target 3.4: Mental health and non-communicable disease prevention).
2. **Phase 1 (Dataset Gathering & Verification)**: Broadened scope to gather authentic, high-impact public health data. Downloaded and verified all 6 key datasets into [`datasets/`](file:///c:/Users/salman/Desktop/p2/datasets):
   - `kamilpytlak/personal-key-indicators-of-heart-disease` (319,795 CDC BRFSS records)
   - `alexteboul/diabetes-health-indicators-dataset` (70,692 balanced BRFSS records)
   - `uom190346a/sleep-health-and-lifestyle-dataset` (374 clinical records)
   - `aldinwhyudii/student-depression-and-lifestyle-100k-data` (100,000 records)
   - `arashnic/fitbit` (18 sensor time-series CSVs)
   - `fatemehmehrparvar/obesity-levels` (2,111 records)
   - `samartalwar/sleep-debt-and-screen-time-late-night-phone-habits` (8,500 records)
3. **Phase 2 (Hardware & Local AI Verification)**: Confirmed local Ollama running `qwen3.5:0.8b` on 100% GPU with UTF-8 support and fast response times.
4. **Phase 3 (Anti-Cyberchondria & Holistic Mission)**: Recognized that the average person is overwhelmed by health anxiety from alarmist search results. Shifted mission from disconnected ML toy models to a **homogeneous, reassuring, and evidence-grounded health advisory platform**.

---

## 2. Homogeneous System Architecture

Rather than isolated, disconnected scripts, the entire platform runs as a **single, unified pipeline** centered around a shared data schema:

```
                                  UNIFIED USER INPUT
       (Demographics, Vitals, Sleep, Screentime, Nutrition, Stimulants, Symptoms)
                                          │
                                          ▼
                          [ Central UserHealthProfile State ]
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            ▼                             ▼                             ▼
   [ Scientific Calculators ]     [ Pre-Trained ML Ensembles ]    [ Functional Matrices ]
   • BMR & TDEE (Mifflin)         • 10-Yr Cardio Risk (CDC 319k)  • Symptom ⟷ Deficiency
   • Dynamic Macro Allocator      • Pre-Diabetes Screener (70k)   • Food & Cofactor Map
   • Caffeine 5.5h Half-Life      • Circadian Sleep Debt (8.5k)   • Water & Electrolytes
   • Caloric Deficit Forecaster   • Sleep Apnea Triage (374)
   • Weight Fluctuation Bounds    • Screen Stress & Burnout (100k)
            │                             │                             │
            └─────────────────────────────┼─────────────────────────────┘
                                          │
                                          ▼
                        [ Clinical Red-Flag Triage Engine ]
                          (🟢 Green, 🟡 Yellow, 🔴 Red)
                                          │
                                          ▼
                      [ ComprehensiveDiagnosticPayload Object ]
                       (All numbers, risks, scores, flags)
                                          │
                                          ▼
                     [ Local Qwen AI Engine (Ollama GPU) ]
                    "Empathetic Clinical & Lifestyle Co-Pilot"
                                          │
                                          ▼
                    [ Homogeneous Interactive Local Web UI ]
         (Live Gauges, What-If Simulator, Am-I-Okay De-escalator, Export)
```

---

## 3. The 6 Core Subsystems (Deep Dive)

### Subsystem 1: Validated Scientific Mathematical Engine
Every formula is strictly grounded in peer-reviewed physiological literature:
1. **Basal Metabolic Rate (BMR)**:
   - **Mifflin-St Jeor Equation** (Gold standard for normal and overweight individuals):
     $$\text{BMR}_{\text{male}} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age} + 5$$
     $$\text{BMR}_{\text{female}} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age} - 161$$
   - **Katch-McArdle Equation** (Applied when body fat percentage is provided):
     $$\text{BMR} = 370 + (21.6 \times \text{Lean Body Mass in kg})$$
2. **Total Daily Energy Expenditure (TDEE)**:
   - Calculated via verified physical activity multipliers ($1.20$ to $1.90$) cross-verified with daily step counts and structured exercise days.
3. **Target Macronutrient Architect**:
   - **Protein**: Target $1.6\text{--}2.2\,\text{g/kg}$ of body weight (or lean mass) based on goal (fat loss sparing vs hypertrophy).
   - **Fat Floor**: Minimum $0.6\text{--}0.8\,\text{g/kg}$ to prevent endocrine dysfunction.
   - **Carbohydrates**: Sized to fill remaining caloric budget, timed around activity.
4. **Caffeine Receptor Pharmacokinetics**:
   - First-order elimination curve with average $5.5\text{-hour}$ half-life:
     $$C(t) = C_0 \times \left(\frac{1}{2}\right)^{\frac{t}{5.5}}$$
   - Calculates remaining active caffeine at bedtime and flags latency disruption if $>25\,\text{mg}$.
5. **Scale Fluctuation & Glycogen Water Estimator**:
   - Accounts for $3\text{--}4\,\text{g}$ of water bound per gram of stored glycogen + sodium retention, explaining why $1\text{--}2.5\,\text{kg}$ overnight jumps are fluid shifts, not fat.

---

### Subsystem 2: Machine Learning Preventive Risk Ensembles
Trained on authentic public health datasets, calibrated with cross-validation:
1. **Cardiovascular Lifestyle Risk Model** (Trained on `heart_2020_cleaned.csv` - 319,795 rows):
   - Logistic Regression / LightGBM with Platt scaling for well-calibrated probabilities.
   - Evaluates age, BMI, smoking, alcohol, walking difficulty, physical activity, and sleep duration.
   - Computes baseline 10-year heart disease odds and enables counterfactual simulation.
2. **Pre-Diabetes Non-Invasive Screener** (Trained on `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` - 70,692 rows):
   - Predicts insulin resistance risk using diet (fruits/veggies), high blood pressure, high cholesterol, BMI, and physical inactivity.
3. **Circadian Sleep Debt & Latency Model** (Trained on `bedtime_screentime_sleep_debt.csv` - 8,500 rows):
   - Multi-output regressor & classifier predicting exact sleep latency (minutes), next-day fatigue score ($1\text{--}10$), and sleep debt tier based on bedtime phone minutes and app genre.
4. **Sleep Pathology & Apnea Triage Model** (Trained on `Sleep_health_and_lifestyle_dataset.csv` - 374 clinical records):
   - Classifies likelihood of *Sleep Apnea* vs *Insomnia* vs *None* using resting heart rate, blood pressure, BMI, and occupational stress.
5. **Digital Stress & Burnout Predictor** (Trained on `student_lifestyle_100k.csv` - 100,000 rows):
   - Maps social media hours and sleep duration to stress score ($1\text{--}10$) and depressive risk probability.
6. **Obesity & Sedentary Habit Stage Model** (Trained on `ObesityDataSet_raw_and_data_sinthetic.csv` - 2,111 rows):
   - Evaluates technology device usage (`TUE`), hydration, and meal frequency to classify weight category.

---

### Subsystem 3: Functional Medicine & Nutrient Deficiency Matrix
A bidirectional knowledge base connecting daily symptoms to nutritional cofactors:
- **Symptom ➔ Probable Deficiencies**:
  - *Brain fog + cold extremities + chronic fatigue* $\longrightarrow$ Iron/Ferritin, Vitamin B12, Thyroid iodine/selenium cofactors.
  - *Eyelid flutter + calf spasms + restless legs* $\longrightarrow$ Magnesium, Potassium, Calcium/Vitamin D.
  - *Tension headaches + afternoon crash* $\longrightarrow$ Hydration/Electrolyte imbalance, Reactive hypoglycemia, Caffeine withdrawal.
  - *Brittle nails + hair thinning* $\longrightarrow$ Iron/Ferritin, Biotin, Zinc, Protein insufficiency.
- **Deficiency ➔ Whole-Food Solutions & Safe Supplementation Guidelines**:
  - Highlights bioavailable whole foods first (pumpkin seeds for magnesium, lentils & spinach for iron, wild salmon for D3/Omega-3).
  - Explicitly states absorption rules (e.g., Vitamin C doubles non-heme iron absorption; tannins in coffee/tea inhibit iron absorption by up to 60%; Vitamin D3 requires K2 and magnesium for safe calcium handling).

---

### Subsystem 4: Clinical Safety & Three-Tier Red-Flag Triage Engine
Operates as an automated clinical guardrail running on every input payload:
- **Level 1 (Green / Lifestyle Modifiable)**: Routine variations in fatigue, sleep latency, macro ratios, or fluid retention. Fully addressed with lifestyle advice and reassurance.
- **Level 2 (Yellow / Medical Review)**: Persistent anomalous patterns:
  - Stage 1/2 Hypertension confirmed at rest ($140/90\text{ mmHg} \le \text{BP} < 180/120\text{ mmHg}$).
  - High probability of Sleep Apnea (snoring + choking/gasping + morning headaches + high BP).
  - High pre-diabetes risk score.
  - *Action*: Displays full lifestyle optimization alongside a clear, professional banner recommending a routine checkup with a primary care doctor.
- **Level 3 (Red / Emergency Clinical Warning)**: Critical red flags:
  - Hypertensive Crisis ($\text{Systolic} \ge 180\text{ mmHg}$ or $\text{Diastolic} \ge 120\text{ mmHg}$).
  - Acute chest pressure, radiating arm/jaw pain, acute shortness of breath.
  - Sudden focal neurological signs (facial droop, arm weakness, speech difficulty).
  - *Action*: **Immediate Interface Override**. Suppresses lifestyle tips and triggers a full-screen red emergency modal with direct instructions to call emergency services (911 / 112) or seek emergency room care immediately.

---

### Subsystem 5: Local Qwen AI Orchestrator & Prompt Engine
- **Localhost Execution**: Powered by `qwen3.5:0.8b` running on GPU via Ollama (`http://localhost:11434`). Zero cloud data leakage.
- **Role Definition**: Qwen acts strictly as a **sympathetic, plain-English translator and lifestyle strategist**. Qwen never invents numbers; it receives the structured JSON diagnostic payload containing all calculated metrics, risk percentages, and red-flag levels.
- **Prompt Guardrails**:
  - Explicit instruction to de-escalate anxiety.
  - Clear biological analogies (e.g., explaining adenosine as a sleep-pressure hourglass).
  - Limits advice to the **Top 3 High-Impact Behavioral Levers** to prevent cognitive overload.

---

### Subsystem 6: Interactive Localhost Web Interface
A responsive, modern interface built with Python (FastAPI/Streamlit or modern web stack):
1. **Intake Flow**:
   - Quick Mode: "2-Minute Health Pulse" (Age, Weight, Sleep, Bedtime Screentime, Caffeine, Top Symptoms).
   - Deep Mode: Full Biometrics, Diet, Exercise, and Vitals.
2. **Interactive Visual Dashboard**:
   - Color-coded risk dials (Cardio, Diabetes, Sleep Debt, Stress).
   - Dynamic 24-Hour Caffeine Clearance Clock.
   - Precision Macro Plate Visualizer (Grams + Real-food equivalents).
3. **"Am I Okay?" Quick Symptom De-escalator**:
   - One-click reassurance for sudden everyday worries (post-coffee heart thumping, bloated stomach, sudden scale jump, eyelid twitch).
4. **Interactive "What-If" Lifestyle Simulator**:
   - Live sliders: adjust screen time, steps, or sleep hours and see risk dials move dynamically.
5. **"Doctor Visit Briefing" Export**:
   - Single-click download of a clean Markdown/PDF summary for the user to share with their actual physician.

---

## 4. Phased Implementation Roadmap

```
                                  PHASED DELIVERY PLAN
                                           │
  ┌─────────────────┬──────────────────────┼──────────────────────┬─────────────────┐
  ▼                 ▼                      ▼                      ▼                 ▼
Phase 1:          Phase 2:               Phase 3:               Phase 4:          Phase 5:
Core Math &       ML Training &          Safety Triage &        Local Qwen        Local Web UI &
Schemas           Serialization          Orchestrator           Integration       What-If Engine
(Days 1-2)        (Days 2-3)             (Day 4)                (Day 5)           (Days 6-7)
```

### Phase 1: Core Schemas & Mathematical Engine (Days 1–2)
- Build `schemas.py`: Pydantic models for `UserHealthProfile`, `MathematicalMetrics`, `MLRiskMetrics`, `TriageAssessment`, and `DiagnosticPayload`.
- Build `calculators.py`: Unit-tested implementations of Mifflin-St Jeor, Katch-McArdle, TDEE, dynamic macro distribution, 1st-order caffeine half-life, water equations, and scale weight fluctuation bounds.
- Build `deficiency_matrix.py`: Bidirectional symptom-to-micronutrient dictionary with food sources and co-factor rules.

### Phase 2: Machine Learning Training & Serialization Pipeline (Days 2–3)
- Build `train_models.py`:
  - Train Logistic Regression & LightGBM on `heart_2020_cleaned.csv` (Calibrated probabilities).
  - Train Classifier on `diabetes_binary_5050split_health_indicators_BRFSS2015.csv`.
  - Train Multi-output Regressor & Classifier on `bedtime_screentime_sleep_debt.csv`.
  - Train Classifier on `Sleep_health_and_lifestyle_dataset.csv` (Insomnia vs Sleep Apnea).
  - Train Regressor on `student_lifestyle_100k.csv` (Social media screen hours to stress score).
- Save serialized model bundles and scaler preprocessors to `models/` as `.joblib` files.
- Generate and log validation reports (ROC-AUC, F1, Accuracy, Brier Calibration Score) to guarantee zero hallucinations.

### Phase 3: Central Orchestrator & Safety Red-Flag Triage Engine (Day 4)
- Build `safety_triage.py`: Deterministic rule engine detecting AHA blood pressure crises, severe mental distress, and sleep apnea indicators.
- Build `orchestrator.py`: The central engine that receives `UserHealthProfile`, executes all calculators, runs ML inference, evaluates triage level, and packages the complete `DiagnosticPayload`.

### Phase 4: Local Qwen Ollama Connector & Prompt Engine (Day 5)
- Build `llm_advisor.py`:
  - Connects to `http://localhost:11434` with UTF-8 streaming.
  - Constructs the scientifically grounded prompt containing the diagnostic payload.
  - Enforces prompt guardrails: calm anti-cyberchondria tone, biological demystification, top 3 action levers, and ethical disclaimers.

### Phase 5: Interactive Web Server & Responsive Dashboard (Days 6–7)
- Build `app.py`: A clean, modern local server UI (e.g. Streamlit or FastAPI + modern frontend):
  - Tab 1: Comprehensive Health Intake Form (Quick vs Deep dive).
  - Tab 2: Holistic Health Scorecard & Visual Risk Gauges.
  - Tab 3: Precision Nutrition, Macro Plate & Deficit Planner.
  - Tab 4: 24-Hour Caffeine Curfew Clock & Circadian Forecaster.
  - Tab 5: "Am I Okay?" 60-Second Symptom De-escalator.
  - Tab 6: Interactive "What-If" Lifestyle Simulator.
  - Tab 7: Streaming "Dr. Qwen" Holistic Health Consultation & Doctor Briefing Export.

### Phase 6: Verification, Testing & QA
- Comprehensive test suite (`pytest`) verifying mathematical boundary cases, model inference latencies, triage overrides, and Ollama connection stability.

---

## 5. Verification & Testing Standards

To adhere strictly to **Rule 3 (Zero Hallucinations & Rigorous Validation)**:
1. **Automated Unit Tests**:
   - BMR/TDEE test cases against benchmark human metabolism tables.
   - Caffeine decay formula tested at $t = 0, 5.5, 11, 16.5\text{ hours}$.
   - Macro splits validated to guarantee protein, carbs, and fats sum exactly to the caloric target ($\pm 2\text{ kcal}$).
2. **Machine Learning Model Validation**:
   - Minimum ROC-AUC threshold of $>0.75$ on held-out test splits for clinical classification tasks.
   - Probability calibration verified using Brier score and calibration plots.
3. **Safety Override Tests**:
   - Test inputs with BP $185/125$ to confirm that lifestyle tips are 100% suppressed and Level 3 emergency protocol is triggered.
4. **Offline Localhost Integrity**:
   - System verified to function with zero external internet access (offline-first).

---

### Project File Manifest in Workspace

- 📁 [`datasets/`](file:///c:/Users/salman/Desktop/p2/datasets) — All 6 Kaggle & CDC public health datasets verified and stored.
- 📄 [`.agents/rules/health_platform_rules.md`](file:///c:/Users/salman/Desktop/p2/.agents/rules/health_platform_rules.md) — Active agent constitution and project rules.
- 📄 [`AGENTS.md`](file:///c:/Users/salman/Desktop/p2/AGENTS.md) — Root agent entry point.
- 📄 [`all_possible_ideas_and_inputs.md`](file:///c:/Users/salman/Desktop/p2/all_possible_ideas_and_inputs.md) — Complete user inputs taxonomy and everyday health question mappings.
- 📄 [`PROJECT_MASTER_PLAN.md`](file:///c:/Users/salman/Desktop/p2/PROJECT_MASTER_PLAN.md) — Master architecture and phased delivery blueprint.
