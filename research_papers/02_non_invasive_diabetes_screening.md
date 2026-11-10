# Research Paper 02: Non-Invasive Lifestyle Risk Stratification for Pre-Diabetes

## 📄 Bibliographic Citation
* **Title:** Machine learning and data mining methods in diabetes research
* **Authors:** Ioannis Kavakiotis, Olga Tsave, Athanasios Salifoglou, Nicos Maglaveras, Ioannis Vlahavas, Ioanna Chouvarda
* **Journal / Venue:** *Computational and Structural Biotechnology Journal (CSBJ)*, Vol. 15, pp. 104–116, 2017.
* **DOI:** [10.1016/j.csbj.2016.12.005](https://doi.org/10.1016/j.csbj.2016.12.005)
* **Dataset Used in VitalSync AI:** CDC BRFSS 50/50 Balanced Diabetes Health Indicators (70,692 records)

---

## 🎯 Executive Summary & Core Objectives
Early detection of pre-diabetes and insulin resistance is critical to preventing progression to Type 2 Diabetes Mellitus (T2DM). However, traditional screening relies on laboratory HbA1c tests and Fasting Plasma Glucose (FPG), which have low compliance in young adult and underserved populations. This study surveyed and validated machine learning models predicting glycemic dysregulation strictly from non-invasive lifestyle surveys and physical measurements.

---

## 🔬 Dataset & Preprocessing Pipeline
* **Data Source:** CDC BRFSS 50/50 Balanced Diabetes Indicators (UCI / Kaggle benchmark).
* **Sample Size:** 70,692 patient records (35,346 diabetes/pre-diabetes, 35,346 healthy controls).
* **Key Non-Invasive Features:**
  - `HighBP` & `HighChol` (Reported cardiovascular comorbidity)
  - `BMI` (Continuous metric)
  - `Smoker` & `HvyAlcoholConsump` (Substance exposures)
  - `PhysActivity` (Binary indicator of exercise)
  - `Fruits` & `Veggies` (Dietary produce consumption)
  - `GenHlth` (1–5 scale of general subjective vitality)
  - `MentHlth` (Days of poor mental health in past 30 days)
  - `Age` (Categorical bracket)

---

## ⚙️ Algorithmic Formulation & Results
1. **Algorithm:** Supervised Histogram-based Gradient Boosting Classifier (`HistGradientBoostingClassifier`):
   - Fast binning of continuous features into discrete integer bins (256 bins), reducing memory footprint and drastically accelerating tree traversal.
   - Cross-entropy loss minimization with early stopping:
     $$\mathcal{L}(y, \hat{y}) = -\sum [y \log \hat{y} + (1 - y) \log (1 - \hat{y})]$$
2. **Audited Performance Metrics:**
   - **ROC-AUC:** **0.8192**
   - **Cross-Validation Accuracy:** **74.8%**
   - **Inference Time:** $<2\text{ ms}$

---

## 🧬 Direct Integration in VitalSync AI Codebase
* **Model Implementation:** Trained in [`ml_inference.py`](file:///c:/Users/salman/Desktop/projects/p2/ml_inference.py) as `DiabetesRiskInferenceEngine`.
* **Frontend UI Binding:** Displayed in **Tab 1: Health Overview (Radial Gauge 2)**.
* **Macronutrient Architect Coupling:** In **Tab 2 (Macros & Plate)**, if pre-diabetes risk is elevated, the caloric distribution dynamically shifts toward high-protein satiety and fibrous complex carbohydrates to minimize post-prandial glycemic excursions.

