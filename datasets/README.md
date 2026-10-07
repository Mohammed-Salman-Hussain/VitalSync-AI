# Datasets Provenance & Public Health Benchmarks

VitalSync AI adheres strictly to **Rule 2: Zero-Hallucination & Rigorous Scientific Validation**. All statistical risks, machine learning ensembles, and circadian equations are trained and calibrated on authentic public health datasets comprising over **500,000+ real-world clinical and epidemiological records**.

---

## 📊 Summary of Public Health Datasets

| Dataset | Primary Source | Records | Target Variables / Features | Role in VitalSync AI |
| :--- | :--- | :--- | :--- | :--- |
| **Personal Key Indicators of Heart Disease** | CDC Behavioral Risk Factor Surveillance System (BRFSS 2020) | 319,795 | Heart Disease (Yes/No), BMI, Smoking, Alcohol, Walking Difficulty, Age | 10-Year Cardiovascular Lifestyle Risk Ensemble |
| **Diabetes Health Indicators** | CDC BRFSS 2015 (50/50 Balanced Split) | 70,692 | Diabetes_binary, HighBP, HighChol, BMI, Smoker, PhysActivity, Diet | Non-Invasive Pre-Diabetes Risk Screener |
| **Circadian Sleep Debt & Late-Night Phone Habits** | Kaggle Sleep Latency & Bedtime Habits Cohort | 8,500 | Sleep Latency, Screen Brightness, Blue Light Filter, Bedtime App, Fatigue | Multi-Output Regressor for Sleep Latency & Sleep Debt Tier |
| **Sleep Health & Lifestyle Clinical Dataset** | Clinical Polysomnography & Lifestyle Cohort | 374 | Sleep Disorder (None, Insomnia, Sleep Apnea), Systolic/Diastolic BP, Heart Rate | Sleep Pathology & Apnea Triage Classifier |
| **Student Lifestyle & Depression Survey** | 100k Mental Health & Behavioral Dataset | 100,000 | Stress Level (1-10), Depression Risk, Social Media Hours, Sleep Duration | Digital Screen-Time Stress & Burnout Regressor |
| **Obesity Levels Estimation** | Eating Habits & Physical Condition Dataset | 2,111 | Weight Category, Fast Food, Technology Use, Hydration | Sedentary Habit & Weight Classification |

---

## 📥 Dataset Acquisition & Retraining

To minimize repository bloat and ensure fast git clones, large raw CSV datasets (>5MB) are not tracked in git. The serialized machine learning bundles in [`models/`](file:///models/) are lightweight (~3.5 MB total) and included directly in the repository for immediate out-of-the-box execution.

If you wish to download the raw datasets and retrain the machine learning ensembles from scratch:

```bash
# 1. Ensure dependencies are installed
pip install -r requirements.txt

# 2. Download all raw datasets via kagglehub
python scripts/download_datasets.py

# 3. Retrain all 5 models and update models/ directory
python train_models.py
```

---

## 📜 Ethical Data Usage & Attribution
- **CDC BRFSS Data**: Public domain health surveillance data provided by the United States Centers for Disease Control and Prevention.
- **Sleep & Mental Health Datasets**: Published on Kaggle under open research licenses (CC BY-SA 4.0, Open Data Commons).
- VitalSync AI strictly preserves anonymization. No Personally Identifiable Information (PII) is included in any dataset or generated model artifact.
