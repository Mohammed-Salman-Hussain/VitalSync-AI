# VitalSync AI: Software & Technologies Specification

**Author:** Mohammed Salman Hussain  
**Project:** VitalSync AI  

---

## 1. Full Technology Stack Overview

| Layer | Technology | Version | Purpose in VitalSync AI |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | **FastAPI** | `0.115+` | High-performance asynchronous REST API routing and request handling |
| **ASGI Server** | **Uvicorn** | `0.30+` | Lightning-fast ASGI production server |
| **Data Validation** | **Pydantic v2** | `2.8+` | Strict schema validation, data serialization, and type safety |
| **Machine Learning** | **Scikit-Learn** | `1.4+` | HistGradientBoosting, Balanced Logistic Regression, Random Forest classifiers |
| **Scientific Computing** | **NumPy & Pandas** | `2.0+` | Matrix operations, tabular data wrangling, and statistical feature scaling |
| **Local LLM Engine** | **Ollama / Qwen** | `qwen3.5:0.8b` | Quantized local generative language model for edge clinical consultation |
| **Frontend Framework** | **Vanilla HTML5 & CSS3** | Modern ES6+ | Zero-dependency, lightweight, high-performance glassmorphic UI |
| **Data Visualization** | **HTML5 Canvas & SVG** | 60fps Native | High-DPI radial progress gauges, 24h caffeine curves, and macro donut charts |
| **Testing Harness** | **Pytest** | `8.0+` | Automated regression testing across 24 unit test suites |
| **Version Control** | **Git & GitHub** | `2.40+` | Source code management, semantic commit history, and release distribution |

---

## 2. Machine Learning Architecture Details

### 1. Cardiovascular Risk Model
* **Algorithm**: Balanced Logistic Regression with Standard Scaler Pipeline
* **Training Dataset**: CDC BRFSS 2020 (319,795 records)
* **Optimization**: Class-weighted inverse frequency loss to resolve positive case rarity
* **Metrics**: ROC-AUC: **0.8170**, Accuracy: **76.4%**

### 2. Pre-Diabetes Non-Invasive Screener
* **Algorithm**: Histogram-based Gradient Boosting Classifier (`HistGradientBoostingClassifier`)
* **Training Dataset**: CDC BRFSS 50/50 Balanced Diabetes Indicators (70,692 records)
* **Optimization**: Binned continuous splits (256 bins) for sub-2ms inference
* **Metrics**: ROC-AUC: **0.8192**, Cross-Validation Accuracy: **74.8%**

### 3. Circadian Sleep Latency Model
* **Algorithm**: Multi-Output Ensemble Regressor + Classifier
* **Training Dataset**: Screen Time & Late-Night Phone Habits Cohort (8,500 records)
* **Metrics**: Latency RMSE: **6.84 min**, Debt Category Accuracy: **89.2%**

### 4. Sleep Apnea Clinical Pathology Classifier
* **Algorithm**: Balanced Random Forest (100 estimators)
* **Training Dataset**: Clinical Polysomnography Sleep Health Cohort (374 patient rows)
* **Metrics**: Weighted F1-Score: **0.8933**, Accuracy: **89.3%**

### 5. Digital Screen Stress & Burnout Screener
* **Algorithm**: Ensemble Regressor on Student Lifestyle (100,000 records)
* **Metrics**: Fatigue RMSE: **1.02 / 10**, Perceived Stress RMSE: **1.48 / 10**

---

## 3. Mathematical Foundations & Clinical Equations

1. **Basal Metabolic Rate (Mifflin-St Jeor, 1990)**:
   $$\text{BMR} = 10 \cdot W_{\text{kg}} + 6.25 \cdot H_{\text{cm}} - 5 \cdot A_{\text{years}} \pm s$$
2. **Lean Mass Metabolism (Katch-McArdle, 1996)**:
   $$\text{BMR} = 370 + (21.6 \cdot \text{LBM}_{\text{kg}})$$
3. **Caffeine Elimination Kinetics (Drake et al., 2013)**:
   $$C(t) = C_0 \cdot (0.5)^{\frac{t}{5.5}}$$
4. **Glycogen Hydration Dynamics (Olsson & Saltin, 1970)**:
   $$\text{Bound Water (g)} \approx 3.5 \times \text{Glycogen (g)}$$
