"""
ml_inference.py - Production Inference Engine for Machine Learning Ensembles

Ingests a homogeneous UserHealthProfile object, runs inference across
all 5 pre-trained statistical & machine learning models, executes counterfactual
habit simulations, and outputs a validated MLRiskMetrics schema.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from schemas import UserHealthProfile, MLRiskMetrics, BiologicalSex, AppCategory, Chronotype


MODELS_DIR = "models"


class MLInferenceEngine:
    """
    Singleton inference orchestrator that loads all trained models once
    into memory and provides rapid (<10ms) risk scoring and counterfactual simulation.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLInferenceEngine, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _load_models(self):
        print("Loading serialized ML models into memory...")
        self.cardio_bundle = joblib.load(os.path.join(MODELS_DIR, "cardio_risk_model.joblib"))
        self.prediabetes_bundle = joblib.load(os.path.join(MODELS_DIR, "prediabetes_screener_model.joblib"))
        self.circadian_bundle = joblib.load(os.path.join(MODELS_DIR, "circadian_sleep_models.joblib"))
        self.pathology_bundle = joblib.load(os.path.join(MODELS_DIR, "sleep_pathology_model.joblib"))
        self.burnout_bundle = joblib.load(os.path.join(MODELS_DIR, "digital_burnout_model.joblib"))
        print("All 5 models loaded successfully.")

    def _map_age_to_cdc_category(self, age: int) -> str:
        if age < 25:
            return "18-24"
        elif age < 30:
            return "25-29"
        elif age < 35:
            return "30-34"
        elif age < 40:
            return "35-39"
        elif age < 45:
            return "40-44"
        elif age < 50:
            return "45-49"
        elif age < 55:
            return "50-54"
        elif age < 60:
            return "55-59"
        elif age < 65:
            return "60-64"
        elif age < 70:
            return "65-69"
        elif age < 75:
            return "70-74"
        elif age < 80:
            return "75-79"
        else:
            return "80 or older"

    def predict_cardiovascular_risk(self, profile: UserHealthProfile) -> float:
        """Computes calibrated 10-year lifestyle cardiovascular risk percentage (0-100%)."""
        features_df = pd.DataFrame([{
            "BMI": profile.bmi,
            "Smoking": 1 if profile.smoker_or_vaper else 0,
            "AlcoholDrinking": 1 if profile.alcohol_drinks_per_week >= 7 else 0,
            "PhysicalActivity": 1 if (profile.resistance_training_days_per_week + profile.cardio_sessions_per_week >= 2 or profile.daily_steps >= 7000) else 0,
            "SleepTime": profile.actual_sleep_hours,
            "DiffWalking": 1 if profile.daily_steps < 3000 else 0,
            "Sex": 1 if profile.sex == BiologicalSex.MALE else 0,
            "AgeCategory": self._map_age_to_cdc_category(profile.age)
        }])
        
        prob = self.cardio_bundle["pipeline"].predict_proba(features_df)[0, 1]
        return round(float(prob * 100.0), 1)

    def predict_prediabetes_risk(self, profile: UserHealthProfile) -> float:
        """Computes non-invasive pre-diabetes risk probability (0-100%)."""
        high_bp = 1 if (profile.systolic_bp >= 130 or profile.diastolic_bp >= 80) else 0
        high_chol = 1 if profile.fast_food_meals_per_week >= 4 else 0
        phys_act = 1 if (profile.daily_steps >= 6000 or profile.cardio_sessions_per_week >= 1) else 0
        fruits = 1 if profile.fruit_veg_servings >= 2 else 0
        veggies = 1 if profile.fruit_veg_servings >= 2 else 0
        hvy_alcohol = 1 if profile.alcohol_drinks_per_week >= 14 else 0
        
        # Map general health from symptoms and stress
        if len(profile.symptoms) >= 4 or profile.stress_level_1_to_10 >= 8:
            gen_hlth = 4  # Poor/Fair
        elif len(profile.symptoms) >= 2 or profile.stress_level_1_to_10 >= 6:
            gen_hlth = 3  # Good
        else:
            gen_hlth = 1  # Excellent

        # CDC age scale 1-13
        age_scale = min(max(int((profile.age - 18) / 5) + 1, 1), 13)

        features_df = pd.DataFrame([{
            "HighBP": high_bp,
            "HighChol": high_chol,
            "BMI": profile.bmi,
            "Smoker": 1 if profile.smoker_or_vaper else 0,
            "PhysActivity": phys_act,
            "Fruits": fruits,
            "Veggies": veggies,
            "HvyAlcoholConsump": hvy_alcohol,
            "GenHlth": gen_hlth,
            "MentHlth": profile.stress_level_1_to_10 * 3,  # days of poor mental health
            "PhysHlth": len(profile.symptoms) * 3,        # days of physical symptoms
            "DiffWalk": 1 if profile.daily_steps < 3000 else 0,
            "Sex": 1 if profile.sex == BiologicalSex.MALE else 0,
            "Age": age_scale
        }])
        
        prob = self.prediabetes_bundle["pipeline"].predict_proba(features_df)[0, 1]
        return round(float(prob * 100.0), 1)

    def predict_circadian_sleep(self, profile: UserHealthProfile) -> Tuple[float, float, str]:
        """
        Predicts:
        - sleep latency in minutes
        - next-day fatigue score (1-10)
        - sleep debt category ('Optimal Recovery', 'Mild Deficit', 'Moderate Debt', 'Severe Sleep Debt')
        """
        app_map = {
            AppCategory.SHORT_FORM_VIDEO: "TikTok / Reels",
            AppCategory.LONG_FORM_STREAMING: "Streaming (Netflix/Hulu)",
            AppCategory.SOCIAL_MESSAGING: "Messaging / Chat",
            AppCategory.READING_AUDIO: "News / Reading"
        }
        app_str = app_map.get(profile.bedtime_app, "TikTok / Reels")
        
        chrono_map = {
            Chronotype.MORNING_LARK: "Morning Lark",
            Chronotype.INTERMEDIATE: "Intermediate",
            Chronotype.NIGHT_OWL: "Night Owl"
        }
        chrono_str = chrono_map.get(profile.chronotype, "Intermediate")
        
        features_df = pd.DataFrame([{
            "bedtime_phone_minutes": profile.bedtime_phone_minutes,
            "primary_bedtime_app": app_str,
            "screen_brightness_pct": profile.screen_brightness_pct,
            "blue_light_filter_active": 1 if profile.blue_light_filter_active else 0,
            "caffeine_post_5pm_mg": profile.daily_caffeine_mg if profile.hours_caffeine_before_bed <= 6.0 else 0,
            "physical_activity_min": int((profile.daily_steps / 100.0) + (profile.cardio_sessions_per_week * 20)),
            "chronotype": chrono_str
        }])
        
        latency = float(self.circadian_bundle["latency_model"].predict(features_df)[0])
        fatigue = float(self.circadian_bundle["fatigue_model"].predict(features_df)[0])
        debt_cat = str(self.circadian_bundle["debt_classifier"].predict(features_df)[0])
        
        return round(max(latency, 5.0), 1), round(min(max(fatigue, 1.0), 10.0), 1), debt_cat

    def predict_sleep_pathology(self, profile: UserHealthProfile) -> float:
        """Computes clinical Sleep Apnea probability percentage (0-100%)."""
        features_df = pd.DataFrame([{
            "Age": profile.age,
            "Sleep Duration": profile.actual_sleep_hours,
            "Quality of Sleep": max(int(10 - (profile.snooze_count * 2)), 3),
            "Physical Activity Level": int(min(profile.daily_steps / 150.0, 100)),
            "Stress Level": profile.stress_level_1_to_10,
            "Heart Rate": profile.resting_hr_bpm,
            "Daily Steps": profile.daily_steps,
            "Systolic_BP": profile.systolic_bp,
            "Diastolic_BP": profile.diastolic_bp
        }])
        
        probs = self.pathology_bundle["pipeline"].predict_proba(features_df)[0]
        classes = self.pathology_bundle["classes"]
        
        apnea_idx = classes.index("Sleep Apnea") if "Sleep Apnea" in classes else -1
        apnea_prob = probs[apnea_idx] if apnea_idx != -1 else 0.0
        
        # Clinical adjustment if user confirms nocturnal gasping/choking
        if profile.gasping_choking_nocturnal:
            apnea_prob = min(apnea_prob + 0.35, 0.98)
            
        return round(float(apnea_prob * 100.0), 1)

    def predict_digital_burnout(self, profile: UserHealthProfile) -> float:
        """Predicts subjective stress/burnout score on a 1-10 scale."""
        features_df = pd.DataFrame([{
            "Sleep_Duration": profile.actual_sleep_hours,
            "Social_Media_Hours": profile.social_media_hours,
            "Physical_Activity": int(profile.daily_steps / 80.0),
            "Age": profile.age
        }])
        
        predicted_stress = float(self.burnout_bundle["stress_model"].predict(features_df)[0])
        return round(min(max(predicted_stress, 1.0), 10.0), 1)

    def run_counterfactual_simulation(self, profile: UserHealthProfile) -> Dict[str, Any]:
        """
        Counterfactual 'What-If' Simulation:
        Simulates what happens to sleep latency, next-day fatigue, and cardio risk
        if the user reduces bedtime screen time by 30 min and adds 3,000 steps.
        """
        # Create improved profile clone
        improved_profile = profile.model_copy(deep=True)
        improved_profile.bedtime_phone_minutes = max(profile.bedtime_phone_minutes - 30, 0)
        improved_profile.blue_light_filter_active = True
        improved_profile.daily_steps = profile.daily_steps + 3000
        improved_profile.bedtime_app = AppCategory.READING_AUDIO

        curr_lat, curr_fat, _ = self.predict_circadian_sleep(profile)
        new_lat, new_fat, _ = self.predict_circadian_sleep(improved_profile)
        
        curr_cardio = self.predict_cardiovascular_risk(profile)
        new_cardio = self.predict_cardiovascular_risk(improved_profile)

        return {
            "intervention_description": "Reduce bedtime screen time by 30 min, enable blue light filter, and add 3,000 daily steps",
            "latency_reduction_minutes": round(max(curr_lat - new_lat, 0.0), 1),
            "fatigue_score_reduction": round(max(curr_fat - new_fat, 0.0), 1),
            "cardio_risk_reduction_pct": round(max(curr_cardio - new_cardio, 0.0), 1),
            "projected_latency_minutes": new_lat,
            "projected_fatigue_score": new_fat,
            "projected_cardio_risk_pct": new_cardio
        }

    def compute_all_ml_metrics(self, profile: UserHealthProfile) -> MLRiskMetrics:
        """Master ML coordinator returning the unified MLRiskMetrics schema."""
        cardio_risk = self.predict_cardiovascular_risk(profile)
        prediabetes_risk = self.predict_prediabetes_risk(profile)
        latency, fatigue, debt_cat = self.predict_circadian_sleep(profile)
        apnea_risk = self.predict_sleep_pathology(profile)
        burnout_stress = self.predict_digital_burnout(profile)
        counterfactuals = self.run_counterfactual_simulation(profile)

        return MLRiskMetrics(
            cardiovascular_10yr_risk_pct=cardio_risk,
            prediabetes_risk_pct=prediabetes_risk,
            sleep_debt_category=debt_cat,
            predicted_sleep_latency_min=latency,
            predicted_fatigue_score_1_to_10=fatigue,
            sleep_apnea_probability_pct=apnea_risk,
            digital_burnout_stress_score_1_to_10=burnout_stress,
            counterfactual_scenarios=counterfactuals
        )
