# VitalSync AI: REST API Documentation

The **VitalSync AI API** is a high-performance, asynchronous REST backend built on FastAPI. It connects modern web applications to validated biophysical calculations, machine learning ensembles, a functional deficiency knowledge graph, clinical safety triage, and local GPU LLMs via Ollama.

---

## 🌐 Base URL & Server Launch

- **Base URL**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Specification**: `http://localhost:8000/redoc`

### Starting the Server
```bash
uvicorn api_server:app --host 127.0.0.1 --port 8000 --reload
```

---

## 📋 Endpoints Overview

| Method | Endpoint | Description | Latency |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | System status, active models count, and Ollama connectivity | $< 5\,\text{ms}$ |
| `POST` | `/api/analyze` | Ingests `UserHealthProfile`, executes math, ML, triage, and deficiency analysis | $< 30\,\text{ms}$ |
| `POST` | `/api/consultation`| Sends payload to local Qwen LLM on GPU and streams consultation report | $1\text{--}3\,\text{s}$ |
| `POST` | `/api/ask` | Answers everyday health query or de-escalates panic, grounded in user metrics | $1\text{--}2\,\text{s}$ |
| `POST` | `/api/export-doctor-briefing`| Generates standardized 1-page clinical Markdown for physician consultation | $< 15\,\text{ms}$ |

---

## 🔍 Detailed Endpoint Reference

### 1. `GET /api/health`
Returns system status, active machine learning model count, and local Ollama GPU configuration.

#### Response (`200 OK`)
```json
{
  "status": "healthy",
  "models_loaded": 5,
  "ollama_model": "qwen3.5:0.8b",
  "ollama_url": "http://localhost:11434"
}
```

#### Example cURL
```bash
curl -X GET "http://localhost:8000/api/health"
```

---

### 2. `POST /api/analyze`
Executes the full homogeneous diagnostic pipeline in a single roundtrip. Computes BMR, TDEE, dynamic macro distribution, first-order caffeine pharmacokinetics, 5 machine learning models, functional deficiency matches, and clinical triage.

#### Request Body (`application/json`)
```json
{
  "age": 32,
  "sex": "male",
  "height_cm": 178.0,
  "weight_kg": 78.0,
  "waist_cm": 84.0,
  "body_fat_pct": 18.5,
  "systolic_bp": 124,
  "diastolic_bp": 78,
  "resting_hr_bpm": 68,
  "bedtime_hour": 23.5,
  "wake_hour": 7.5,
  "actual_sleep_hours": 7.0,
  "chronotype": "intermediate",
  "snooze_count": 1,
  "snoring_frequent": false,
  "gasping_choking_nocturnal": false,
  "total_screen_time_hours": 6.5,
  "social_media_hours": 2.5,
  "bedtime_phone_minutes": 45,
  "bedtime_app": "short_form_video",
  "screen_brightness_pct": 50,
  "blue_light_filter_active": true,
  "daily_water_liters": 2.2,
  "fruit_veg_servings": 3,
  "fast_food_meals_per_week": 2,
  "hours_last_meal_to_bed": 2.5,
  "daily_caffeine_mg": 180,
  "hours_caffeine_before_bed": 7.0,
  "alcohol_drinks_per_week": 2,
  "alcohol_near_bedtime": false,
  "smoker_or_vaper": false,
  "daily_steps": 7500,
  "resistance_training_days_per_week": 3,
  "cardio_sessions_per_week": 2,
  "desk_job_sedentary": true,
  "symptoms": ["eyelid_twitch", "afternoon_crash"],
  "goal_type": "maintenance_recomp",
  "stress_level_1_to_10": 5
}
```

#### Response (`200 OK`)
Returns a `ComprehensiveDiagnosticPayload` object:
```json
{
  "profile": { ... },
  "math_metrics": {
    "bmr_kcal": 1738.4,
    "bmr_formula_used": "Katch-McArdle",
    "tdee_kcal": 2520.7,
    "target_calories_kcal": 2520.7,
    "target_protein_g": 140.4,
    "target_fat_g": 70.0,
    "target_carbs_g": 332.2,
    "deficit_or_surplus_kcal": 0.0,
    "weekly_weight_change_kg": 0.0,
    "caffeine_active_at_bedtime_mg": 43.6,
    "caffeine_sleep_disruption_flag": true,
    "caffeine_clearance_hours_needed": 15.6,
    "water_recommended_liters": 2.73,
    "water_deficit_liters": 0.53,
    "expected_daily_scale_swing_min_kg": -1.5,
    "expected_daily_scale_swing_max_kg": 1.5,
    "glycogen_water_bound_g": 1400.0,
    "bp_category": "Elevated (120-129 and <80)"
  },
  "deficiency_analysis": {
    "flagged_deficiencies": [
      {
        "nutrient_name": "Magnesium",
        "confidence_score": 0.85,
        "matched_symptoms": ["eyelid_twitch"],
        "biological_function": "Neuromuscular relaxation and ATP cofactor",
        "top_whole_food_sources": ["Pumpkin seeds", "Dark leafy greens", "Almonds"],
        "absorption_cofactors": ["Vitamin B6"],
        "absorption_inhibitors": ["High supplemental zinc", "Phytates"],
        "safety_supplement_note": "Prefer Magnesium Glycinate or Malate (200-400mg) before bed."
      }
    ],
    "total_symptoms_evaluated": 2,
    "primary_lifestyle_levers": [
      "Target 300-400mg dietary magnesium from whole foods.",
      "Stabilize afternoon blood sugar with protein/fiber snacks."
    ]
  },
  "triage": {
    "level": "green",
    "badge_title": "Lifestyle Optimization Profile",
    "triggers": [],
    "actions_required": ["Optimize hydration and sleep hygiene."],
    "doctor_consultation_recommended": false,
    "emergency_override": false,
    "banner_message": "All biometrics within manageable lifestyle ranges."
  },
  "ml_metrics": {
    "cardiovascular_10yr_risk_pct": 3.8,
    "prediabetes_risk_pct": 8.4,
    "sleep_debt_category": "Mild Sleep Debt",
    "predicted_sleep_latency_min": 24.2,
    "predicted_fatigue_score_1_to_10": 4.1,
    "sleep_apnea_probability_pct": 4.2,
    "digital_burnout_stress_score_1_to_10": 4.6,
    "counterfactual_scenarios": { ... }
  },
  "generated_at": "2026-10-07T17:30:00Z"
}
```

---

### 3. `POST /api/consultation`
Transmits the pre-computed `ComprehensiveDiagnosticPayload` to local Qwen LLM on GPU and streams back an empathetic, clinically grounded lifestyle consultation report.

#### Request Body
The JSON object returned by `/api/analyze`.

#### Response (`200 OK`)
```json
{
  "report": "### 🧬 Your Personalized Health & Lifestyle Synthesis\n\n**1. Welcome & Reassurance**\nYour baseline cardiovascular and metabolic indicators are strong..."
}
```

---

### 4. `POST /api/ask`
Submits an everyday health query or viral myth (e.g., *"Why does my eye twitch after espresso?"*). If a profile is provided, the response is grounded in the user's specific metrics.

#### Request Body
```json
{
  "question": "Is an eyelid twitch a sign of a stroke or heart disease?",
  "profile": { ... }
}
```

#### Response (`200 OK`)
```json
{
  "answer": "No. An isolated eyelid twitch (myokymia) is a benign neuromuscular fasciculation of the orbicularis oculi muscle..."
}
```

---

### 5. `POST /api/export-doctor-briefing`
Generates a clean 1-page standardized Markdown clinical summary briefing formatted for clinical review by a physician.

#### Request Body
The `UserHealthProfile` JSON object.

#### Response (`200 OK`, `text/plain`)
```markdown
# CLINICAL SUMMARY BRIEFING: LIFESTYLE & VITALS LOG
**Generated On:** 2026-10-07 17:30 UTC | **Triage Status:** Lifestyle Optimization Profile

---
### 1. Patient Demographics & Baseline Vitals
- **Age / Biological Sex:** 32 years | Male
- **Height / Weight:** 178.0 cm | 78.0 kg (BMI: 24.62 kg/m²)
- **Resting Blood Pressure:** 124/78 mmHg (Elevated (120-129 and <80))
- **Resting Heart Rate:** 68 BPM
...
```

---

## 🐍 Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

profile = {
    "age": 32,
    "sex": "male",
    "height_cm": 178,
    "weight_kg": 78,
    "systolic_bp": 124,
    "diastolic_bp": 78,
    "resting_hr_bpm": 68,
    "daily_steps": 7500,
    "actual_sleep_hours": 7.0,
    "daily_caffeine_mg": 180,
    "symptoms": ["eyelid_twitch"]
}

# 1. Run diagnostic analysis (<30ms)
resp = requests.post(f"{BASE_URL}/api/analyze", json=profile)
diagnostic_payload = resp.json()

print(f"BMR: {diagnostic_payload['math_metrics']['bmr_kcal']} kcal")
print(f"Cardio 10-Yr Risk: {diagnostic_payload['ml_metrics']['cardiovascular_10yr_risk_pct']}%")
print(f"Triage Level: {diagnostic_payload['triage']['level']}")

# 2. Generate Doctor Briefing
briefing = requests.post(f"{BASE_URL}/api/export-doctor-briefing", json=profile).text
print("\nDoctor Briefing Generated:\n", briefing[:300])
```
