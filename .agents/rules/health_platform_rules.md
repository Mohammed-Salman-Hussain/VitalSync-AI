# Project Constitution & Agent Environment Rules: All-in-One AI Health Platform

## 1. Ethical Transparency & Medical Disclaimer Rule
- **Non-Diagnostic Scope**: This platform provides lifestyle, wellness, and behavioral analysis. It is explicitly NOT medical advice, medical diagnosis, or medical treatment.
- **Mandatory Disclaimers**: Every generated report, UI view, and agent response dealing with health data MUST include prominent, unambiguous disclaimers advising users to consult a licensed medical professional for clinical concerns.
- **Three-Tier Safety Triage System**:
  - `LEVEL 1 (Green / Lifestyle)`: Modifiable behavioral factors (hydration, screen time, macro splits, sleep hygiene).
  - `LEVEL 2 (Yellow / Medical Review)`: Persistent anomalous patterns (Stage 1/2 Hypertension, suspected Sleep Apnea, elevated Pre-Diabetes risk). Prompt the user to schedule a routine clinical appointment.
  - `LEVEL 3 (Red / Emergency Triage)`: Critical red flags (Hypertensive Crisis BP $\ge 180/120$, chest pressure, sudden numbness/slurred speech, severe depression crisis). Immediately halt lifestyle advice and display emergency protocols.

## 2. Zero-Hallucination & Rigorous Scientific Validation Rule
- **No Made-Up Metrics**: Every health indicator, risk percentage, and recommendation must be mathematically or statistically grounded.
- **Validated Formulas Only**:
  - BMR & TDEE: Mifflin-St Jeor and Katch-McArdle equations only.
  - Pharmacokinetics: Caffeine clearance modeled on a validated first-order elimination curve ($t_{1/2} \approx 5.5\text{ hours}$).
  - Macronutrients: Evidence-based guidelines (e.g., $1.6\text{--}2.2\,\text{g/kg}$ protein for resistance training / muscle retention; minimum $0.6\,\text{g/kg}$ fat for endocrine health).
- **Tested & Validated ML Models**:
  - Models must be trained on authentic datasets (CDC BRFSS 2020, BRFSS 50/50 Diabetes, Clinical Sleep Health, Kaggle Screentime).
  - All models must record cross-validated performance metrics (ROC-AUC, F1-score, accuracy, calibration).
  - Models must output calibrated probabilities rather than raw uncalibrated heuristics.
- **Grounded LLM Role**: Local Qwen (via Ollama) must act purely as an *interpreter* of the pre-computed mathematical and ML diagnostic payload. Qwen is never asked to guess numbers or diagnose conditions; it synthesizes provided metrics into empathetic, plain-English guidance.

## 3. Homogeneous System Architecture Rule
- **Unified Health State**: The entire platform must operate on a single, shared data schema (`UserHealthProfile` Pydantic / dataclass object). No independent, orphaned scripts or siloed state.
- **Centralized Orchestrator**: A single `HealthOrchestrator` ingests the user profile, runs all scientific calculators, executes the ML ensemble, screens for safety red-flags, and packages the complete diagnostic payload for Qwen.
- **Interconnected Insights**: Features must cross-pollinate. (e.g., Bedtime screen time links to sleep latency, which feeds sleep debt, which impacts morning blood pressure and daytime carbohydrate cravings, which alters the macro recommendations).

## 4. Anti-Cyberchondria & Anxiety De-escalation Rule
- **Tone Mandate**: Empathetic, calm, reassuring, and educational.
- **Deconstruct Panic Sensations**: Demystify common harmless sensations (e.g., post-coffee heart thumping, benign eyelid twitches, daily 2kg scale water fluctuations) with physiology rather than alarmist disease lists.
- **Actionable Levers**: Focus on the top 3 highest-leverage, easily achievable behavioral changes rather than overwhelming the user with 50 rules.

## 5. Local-First Privacy & Zero Data Leakage Rule
- **100% Localhost Operation**: Biometrics, health questionnaires, and symptom logs must never leave the user's machine.
- **Local Compute**: ML inference runs locally in Python; LLM inference runs locally on the user's GPU via Ollama (`http://localhost:11434`).

## 6. High Feature Density with Non-Destructive Modularity Rule
- Build as many valuable modules, sub-calculators, and metrics as possible into the system.
- Every feature must be toggleable or modularly suppressible in the UI so the user can easily switch between a "Fast 2-Minute Pulse" and a "Comprehensive Deep Dive" without code breaking.

## 7. Counterfactual "What-If" Simulation Capability
- The system must allow users to test lifestyle changes interactively (e.g., "What if I cut bedtime phone use by 30 mins and increase steps by 4,000?") and watch their risk scores update dynamically in real time.
