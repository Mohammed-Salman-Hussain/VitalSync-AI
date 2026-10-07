"""
train_models.py - Multi-Model Training & Serialization Pipeline

Trains calibrated machine learning models on verified public health datasets:
1. Cardiovascular 10-Year Lifestyle Risk (CDC BRFSS 2020 - 319,795 rows)
2. Pre-Diabetes Non-Invasive Screener (BRFSS 50/50 - 70,692 rows)
3. Circadian Sleep Debt & Latency (8,500 rows)
4. Clinical Sleep Pathology: Sleep Apnea vs Insomnia (374 clinical records)
5. Digital Screen-Time Stress & Burnout (100,000 rows)

Saves all serialized pipelines and metadata to models/ directory.
"""

import os
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor, RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, mean_squared_error, f1_score


MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)


def train_cardiovascular_model():
    print("\n" + "="*60)
    print("Training 1: Cardiovascular 10-Year Lifestyle Risk (CDC 319k)")
    print("="*60)
    t0 = time.time()
    
    csv_path = os.path.join("datasets", "heart_2020_cleaned.csv")
    df = pd.read_csv(csv_path)
    
    # Target
    y = (df["HeartDisease"] == "Yes").astype(int)
    
    # Features
    features = [
        "BMI", "Smoking", "AlcoholDrinking", "PhysicalActivity", 
        "SleepTime", "DiffWalking", "Sex", "AgeCategory"
    ]
    X = df[features].copy()
    
    # Convert binary categoricals to 0/1
    for col in ["Smoking", "AlcoholDrinking", "PhysicalActivity", "DiffWalking"]:
        X[col] = (X[col] == "Yes").astype(int)
    X["Sex"] = (X["Sex"] == "Male").astype(int)
    
    # OneHotEncode AgeCategory
    categorical_cols = ["AgeCategory"]
    numeric_cols = ["BMI", "Smoking", "AlcoholDrinking", "PhysicalActivity", "SleepTime", "DiffWalking", "Sex"]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ["BMI", "SleepTime"]),
            ("cat", OneHotEncoder(drop="first", sparse_output=False), categorical_cols)
        ],
        remainder="passthrough"
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", C=1.0))
    ])
    
    model.fit(X_train, y_train)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"Cardio Model ROC-AUC: {auc:.4f} (Trained on {len(X_train):,} records in {time.time()-t0:.2f}s)")
    
    bundle = {
        "pipeline": model,
        "features": features,
        "auc_score": float(auc)
    }
    joblib.dump(bundle, os.path.join(MODELS_DIR, "cardio_risk_model.joblib"))
    print("Saved -> models/cardio_risk_model.joblib")


def train_prediabetes_model():
    print("\n" + "="*60)
    print("Training 2: Pre-Diabetes Non-Invasive Screener (CDC 70k 50/50)")
    print("="*60)
    t0 = time.time()
    
    csv_path = os.path.join("datasets", "diabetes_binary_5050split_health_indicators_BRFSS2015.csv")
    df = pd.read_csv(csv_path)
    
    y = df["Diabetes_binary"].astype(int)
    features = [
        "HighBP", "HighChol", "BMI", "Smoker", "PhysActivity", 
        "Fruits", "Veggies", "HvyAlcoholConsump", "GenHlth", 
        "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age"
    ]
    X = df[features].copy()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = HistGradientBoostingClassifier(max_iter=120, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Pre-Diabetes Model ROC-AUC: {auc:.4f}, Accuracy: {acc:.4f} (Trained on {len(X_train):,} records in {time.time()-t0:.2f}s)")
    
    bundle = {
        "pipeline": model,
        "features": features,
        "auc_score": float(auc),
        "accuracy": float(acc)
    }
    joblib.dump(bundle, os.path.join(MODELS_DIR, "prediabetes_screener_model.joblib"))
    print("Saved -> models/prediabetes_screener_model.joblib")


def train_circadian_sleep_models():
    print("\n" + "="*60)
    print("Training 3: Circadian Sleep Latency, Fatigue & Debt (8,500 rows)")
    print("="*60)
    t0 = time.time()
    
    csv_path = os.path.join("datasets", "bedtime_screentime_sleep_debt.csv")
    df = pd.read_csv(csv_path)
    
    # Feature inputs
    features = [
        "bedtime_phone_minutes", "primary_bedtime_app", "screen_brightness_pct",
        "blue_light_filter_active", "caffeine_post_5pm_mg", "physical_activity_min", "chronotype"
    ]
    X = df[features].copy()
    
    cat_cols = ["primary_bedtime_app", "chronotype"]
    num_cols = ["bedtime_phone_minutes", "screen_brightness_pct", "blue_light_filter_active", "caffeine_post_5pm_mg", "physical_activity_min"]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
        ]
    )
    
    # 1. Sleep Latency Regressor (minutes)
    y_latency = df["sleep_latency_min"].values
    X_train, X_test, y_train_lat, y_test_lat = train_test_split(X, y_latency, test_size=0.2, random_state=42)
    
    latency_pipe = Pipeline([
        ("prep", preprocessor),
        ("reg", HistGradientBoostingRegressor(max_iter=100, random_state=42))
    ])
    latency_pipe.fit(X_train, y_train_lat)
    rmse_lat = np.sqrt(mean_squared_error(y_test_lat, latency_pipe.predict(X_test)))
    print(f"Sleep Latency RMSE: {rmse_lat:.2f} minutes")
    
    # 2. Next-day Fatigue Regressor (1-10)
    y_fatigue = df["next_day_fatigue_score"].values
    fatigue_pipe = Pipeline([
        ("prep", preprocessor),
        ("reg", HistGradientBoostingRegressor(max_iter=100, random_state=42))
    ])
    fatigue_pipe.fit(X_train, y_fatigue[X_train.index])
    rmse_fat = np.sqrt(mean_squared_error(y_fatigue[X_test.index], fatigue_pipe.predict(X_test)))
    print(f"Fatigue Score RMSE: {rmse_fat:.2f} / 10")
    
    # 3. Sleep Debt Classifier (Optimal, Mild, Moderate, Severe)
    y_debt = df["sleep_debt_category"].values
    debt_pipe = Pipeline([
        ("prep", preprocessor),
        ("clf", HistGradientBoostingClassifier(max_iter=100, random_state=42))
    ])
    debt_pipe.fit(X_train, y_debt[X_train.index])
    acc_debt = accuracy_score(y_debt[X_test.index], debt_pipe.predict(X_test))
    print(f"Sleep Debt Category Accuracy: {acc_debt:.4f} (Finished in {time.time()-t0:.2f}s)")
    
    bundle = {
        "latency_model": latency_pipe,
        "fatigue_model": fatigue_pipe,
        "debt_classifier": debt_pipe,
        "features": features
    }
    joblib.dump(bundle, os.path.join(MODELS_DIR, "circadian_sleep_models.joblib"))
    print("Saved -> models/circadian_sleep_models.joblib")


def train_sleep_pathology_model():
    print("\n" + "="*60)
    print("Training 4: Clinical Sleep Pathology (Insomnia vs Sleep Apnea - 374 clinical rows)")
    print("="*60)
    t0 = time.time()
    
    csv_path = os.path.join("datasets", "Sleep_health_and_lifestyle_dataset.csv")
    df = pd.read_csv(csv_path)
    
    # Target: Sleep Disorder (None, Insomnia, Sleep Apnea)
    y = df["Sleep Disorder"].fillna("None")
    
    # Parse Blood Pressure '126/83' -> systolic, diastolic
    bp_split = df["Blood Pressure"].str.split("/", expand=True).astype(int)
    df["Systolic_BP"] = bp_split[0]
    df["Diastolic_BP"] = bp_split[1]
    
    features = [
        "Age", "Sleep Duration", "Quality of Sleep", "Physical Activity Level", 
        "Stress Level", "Heart Rate", "Daily Steps", "Systolic_BP", "Diastolic_BP"
    ]
    X = df[features].copy()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced"))
    ])
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    f1 = f1_score(y_test, model.predict(X_test), average="weighted")
    print(f"Sleep Pathology Accuracy: {acc:.4f}, Weighted F1: {f1:.4f} (Finished in {time.time()-t0:.2f}s)")
    
    bundle = {
        "pipeline": model,
        "features": features,
        "classes": list(model.named_steps["clf"].classes_),
        "accuracy": float(acc)
    }
    joblib.dump(bundle, os.path.join(MODELS_DIR, "sleep_pathology_model.joblib"))
    print("Saved -> models/sleep_pathology_model.joblib")


def train_digital_burnout_model():
    print("\n" + "="*60)
    print("Training 5: Digital Screen-Time Stress & Burnout (100,000 rows)")
    print("="*60)
    t0 = time.time()
    
    csv_path = os.path.join("datasets", "student_lifestyle_100k.csv")
    df = pd.read_csv(csv_path)
    
    # Target: Stress_Level (continuous 1-10) and Depression (bool)
    features = ["Sleep_Duration", "Social_Media_Hours", "Physical_Activity", "Age"]
    X = df[features].copy()
    
    y_stress = df["Stress_Level"].values
    y_dep = df["Depression"].astype(int).values
    
    X_train, X_test, y_train_s, y_test_s = train_test_split(X, y_stress, test_size=0.2, random_state=42)
    
    stress_model = HistGradientBoostingRegressor(max_iter=100, random_state=42)
    stress_model.fit(X_train, y_train_s)
    rmse_stress = np.sqrt(mean_squared_error(y_test_s, stress_model.predict(X_test)))
    print(f"Stress Score Model RMSE: {rmse_stress:.2f} / 10")
    
    dep_model = HistGradientBoostingClassifier(max_iter=100, random_state=42)
    dep_model.fit(X_train, y_dep[X_train.index])
    acc_dep = accuracy_score(y_dep[X_test.index], dep_model.predict(X_test))
    print(f"Depression Risk Classifier Accuracy: {acc_dep:.4f} (Finished in {time.time()-t0:.2f}s)")
    
    bundle = {
        "stress_model": stress_model,
        "depression_model": dep_model,
        "features": features
    }
    joblib.dump(bundle, os.path.join(MODELS_DIR, "digital_burnout_model.joblib"))
    print("Saved -> models/digital_burnout_model.joblib")


if __name__ == "__main__":
    print("Starting Multi-Model Training Pipeline for AI Health Platform...")
    t_start = time.time()
    
    train_cardiovascular_model()
    train_prediabetes_model()
    train_circadian_sleep_models()
    train_sleep_pathology_model()
    train_digital_burnout_model()
    
    print("\n" + "="*60)
    print(f"ALL 5 MACHINE LEARNING MODELS TRAINED & SAVED IN {time.time()-t_start:.2f}s")
    print("Model files in models/:", os.listdir(MODELS_DIR))
    print("="*60)
