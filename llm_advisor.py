"""
llm_advisor.py - Local Qwen AI Medical Interpreter & Prompt Engine

Connects to local Ollama instance (qwen3.5:0.8b on GPU via http://localhost:11434).
Synthesizes the ComprehensiveDiagnosticPayload into a calm, empathetic,
scientifically grounded, and non-alarmist health consultation report.
"""

import sys
import json
import requests
from typing import Optional, Callable, Dict, Any
from schemas import ComprehensiveDiagnosticPayload, TriageLevel


OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen3.5:0.8b"


class QwenHealthAdvisor:
    """
    Client for local Qwen inference on GPU.
    Grounds all generated responses in the structured diagnostic payload.
    """
    def __init__(self, model_name: str = DEFAULT_MODEL, api_url: str = OLLAMA_API_URL):
        self.model_name = model_name
        self.api_url = api_url

    def _build_consultation_prompt(self, payload: ComprehensiveDiagnosticPayload) -> str:
        p = payload.profile
        m = payload.math_metrics
        ml = payload.ml_metrics
        t = payload.triage
        deficiencies = payload.deficiency_analysis.flagged_deficiencies

        def_summary = ", ".join([f"{d.nutrient_name} (Confidence: {int(d.confidence_score*100)}%)" for d in deficiencies[:3]]) or "None identified"
        
        prompt = f"""You are an empathetic, world-class preventive health physician and clinical lifestyle strategist.
Your mission is to provide calm, reassuring, scientifically grounded, and actionable lifestyle advice to an everyday individual who is seeking clarity about their bodily signals.

CRITICAL INSTRUCTIONS:
1. ANTI-CYBERCHONDRIA: De-escalate health anxiety. Do NOT speculate on rare, catastrophic illnesses. Explain harmless physiological mechanisms calmly.
2. ZERO HALLUCINATIONS: Base all advice strictly on the provided quantitative diagnostic data below.
3. ETHICAL DISCLAIMER: Reiterate that this is lifestyle and behavioral analysis, NOT medical advice.
4. ACTIONABLE FOCUS: Conclude with exactly the Top 3 High-Impact Habits for the user to implement this week.

PATIENT DIAGNOSTIC DATA:
- Age: {p.age} | Sex: {p.sex.value} | Height: {p.height_cm} cm | Weight: {p.weight_kg} kg | BMI: {p.bmi} kg/m²
- Resting Blood Pressure: {p.systolic_bp}/{p.diastolic_bp} mmHg ({m.bp_category.value}) | Resting HR: {p.resting_hr_bpm} BPM
- Daily Activity: {p.daily_steps:,} steps/day | Workouts: {p.resistance_training_days_per_week} resistance + {p.cardio_sessions_per_week} cardio per week
- Nutrition: TDEE {m.tdee_kcal} kcal | Target: {m.target_calories_kcal} kcal | Protein: {m.target_protein_g}g | Fat: {m.target_fat_g}g | Carbs: {m.target_carbs_g}g
- Sleep: Reported {p.actual_sleep_hours} hrs/night | Bedtime Phone: {p.bedtime_phone_minutes} mins ({p.bedtime_app.value})
- Circadian Metrics: Predicted Latency ~{ml.predicted_sleep_latency_min} mins | Debt: {ml.sleep_debt_category} | Next-Day Fatigue: {ml.predicted_fatigue_score_1_to_10}/10
- Caffeine: {p.daily_caffeine_mg} mg daily | Estimated Active at Bedtime: {m.caffeine_active_at_bedtime_mg} mg (Disruption Flag: {m.caffeine_sleep_disruption_flag})
- CDC Epidemiological Risks: 10-Year Cardiovascular Risk: {ml.cardiovascular_10yr_risk_pct}% | Pre-Diabetes Index: {ml.prediabetes_risk_pct}% | Sleep Apnea Risk: {ml.sleep_apnea_probability_pct}%
- Active Symptoms Reported: {', '.join(p.symptoms) if p.symptoms else 'None'} | Stress Rating: {p.stress_level_1_to_10}/10
- Suspected Micronutrient Shortfalls: {def_summary}
- Clinical Triage Level: {t.level.value.upper()} ({t.badge_title})

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:
### 1. Compassionate Health Overview & Demystification
(Explain how their sleep, screen time, caffeine, and symptoms interconnect without causing panic.)

### 2. Biological Breakdown of Symptoms
(Explain the exact biological mechanisms behind their reported symptoms—e.g. why caffeine blocks adenosine, why magnesium affects twitches, or why daily scale weight jumps are water, not fat.)

### 3. Your Top 3 High-Impact Action Levers for This Week
1. **Lever 1 (Sleep / Digital Detox)**: Specific, measurable action.
2. **Lever 2 (Nutrition / Micronutrient)**: Specific whole-food additions.
3. **Lever 3 (Movement / Stress)**: Realistic physical target.

### 4. Safety & Medical Next Steps
(State the triage status clearly and guide them on whether a routine physician checkup or immediate care is appropriate.)
"""
        return prompt

    def generate_consultation(
        self,
        payload: ComprehensiveDiagnosticPayload,
        stream_callback: Optional[Callable[[str], None]] = None
    ) -> str:
        """
        Sends the diagnostic payload to local Qwen via Ollama.
        Supports live token streaming via stream_callback.
        """
        prompt = self._build_consultation_prompt(payload)
        
        request_body = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": stream_callback is not None,
            "options": {
                "temperature": 0.4,  # Lower temperature for grounded medical advice
                "top_p": 0.9,
                "num_ctx": 4096
            }
        }
        
        try:
            if stream_callback:
                response = requests.post(self.api_url, json=request_body, stream=True, timeout=120)
                full_text = []
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode("utf-8")).get("response", "")
                        stream_callback(chunk)
                        full_text.append(chunk)
                return "".join(full_text)
            else:
                response = requests.post(self.api_url, json=request_body, timeout=120)
                return response.json().get("response", "").strip()
        except Exception as e:
            error_msg = f"[Local LLM Connection Error]: Could not reach Ollama at {self.api_url}: {e}"
            print(error_msg, file=sys.stderr)
            return (
                "### ⚠️ Local AI Interpreter Unavailable\n\n"
                "The mathematical metrics and ML risk scores were calculated successfully above, "
                f"but the local Qwen LLM did not respond. Error details: `{e}`.\n"
                "Please verify that Ollama is running (`ollama serve`)."
            )

    def answer_health_question(
        self,
        question: str,
        payload: Optional[ComprehensiveDiagnosticPayload] = None
    ) -> str:
        """
        Answers general everyday health queries or social media claims
        (e.g., 'Is ice bathing good for cortisol?'), grounded in user context if provided.
        """
        user_context = ""
        if payload:
            user_context = (
                f"User Profile Context: Age {payload.profile.age}, Sex {payload.profile.sex.value}, "
                f"BMI {payload.profile.bmi}, Sleep {payload.profile.actual_sleep_hours}h, "
                f"Symptoms: {', '.join(payload.profile.symptoms) or 'None'}."
            )
            
        prompt = f"""You are a calm, evidence-based preventive health educator.
Answer the following everyday health query directly, cutting through viral social media marketing myths.
{user_context}

Question: {question}

Explain the physiology simply in 2-3 concise paragraphs. End with an ethical reminder that this is wellness information, not medical advice.
"""
        try:
            res = requests.post(
                self.api_url,
                json={"model": self.model_name, "prompt": prompt, "stream": False},
                timeout=60
            )
            return res.json().get("response", "").strip()
        except Exception as e:
            return f"Error contacting local AI: {e}"
