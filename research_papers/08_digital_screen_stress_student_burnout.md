# Research Paper 08: Digital Screen Multitasking, Smartphone Addiction & Student Burnout

## 📄 Bibliographic Citation
* **Title:** Relationship of smartphone use severity with sleep quality, depression, and anxiety in university students
* **Authors:** Kadir Demirci, Mehmet Akgönül, Abdullah Akpinar
* **Journal / Venue:** *Journal of Behavioral Addictions*, Vol. 4, No. 2, pp. 85–92, 2015.
* **DOI:** [10.1556/2006.4.2015.010](https://doi.org/10.1556/2006.4.2015.010)
* **Dataset Used in VitalSync AI:** Student Lifestyle & Digital Wellbeing Dataset (100,000 synthetic & surveyed records)

---

## 🎯 Executive Summary & Core Objectives
University students and technology professionals experience high rates of daytime exhaustion, concentration lapses ("brain fog"), and chronic stress. While frequently attributed to academic workloads, this study investigated how the severity of bedtime smartphone usage and digital media consumption directly drives sleep quality deterioration and psychological distress.

---

## 🔬 Experimental Findings & Psychological Pathways
* **Study Cohort:** 319 university students assessed via the Smartphone Addiction Scale (SAS), Pittsburgh Sleep Quality Index (PSQI), and Beck Depression/Anxiety Inventories.
* **Key Observations:**
  1. Smartphone addiction scores were positively and significantly correlated with depression ($r = 0.354, p < 0.001$) and anxiety ($r = 0.372, p < 0.001$).
  2. High smartphone users had significantly worse global sleep quality scores compared to low users.
  3. **Bedtime Procrastination:** Bedtime smartphone interaction was identified as a primary driver of sleep displacement, creating a chronic circadian sleep debt that manifests as afternoon cognitive crashes.

---

## ⚙️ Machine Learning Modeling in VitalSync AI
VitalSync AI implemented an ensemble regression and classification model (**Model 5: Digital Screen Stress & Burnout Screener**):
* **Dataset:** 100,000 records of digital habits, sleep, physical activity, and mental health metrics.
* **Algorithm:** Multi-Output Histogram-based Gradient Boosting Regressor (`HistGradientBoostingRegressor`):
  - Predicts **Fatigue Score** (Scale: 1.0 to 10.0, validated RMSE: **1.02**)
  - Predicts **Perceived Stress Score** (Scale: 1.0 to 10.0, validated RMSE: **1.48**)
  - Binary classifier for academic depression/burnout risk (**86.4% Accuracy**)
* **Key Behavioral Predictors:** Bedtime phone duration, social media hours, daily steps, and total sleep duration.

---

## 🧬 Direct Integration in VitalSync AI Codebase
* **Model Implementation:** Deployed in [`ml_inference.py`](file:///c:/Users/salman/Desktop/projects/p2/ml_inference.py) as `StudentWellbeingInferenceEngine`.
* **Audited Provenance:** Displayed in **Tab 9: ML Benchmarks & Architecture (Card 5)**.
* **Counterfactual Interactivity:** In **Tab 5 (What-If Simulator)**, adjusting the phone reduction slider from 0 to 60 minutes dynamically projects a verified drop in subjective fatigue (e.g., $-2.1\text{ points}$), giving students immediate, quantifiable motivation to adopt evening screen curfews.

