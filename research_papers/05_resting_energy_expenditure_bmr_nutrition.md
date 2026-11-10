# Research Paper 05: Resting Energy Expenditure & Basal Metabolic Rate Calibration

## 📄 Bibliographic Citation
* **Title:** A new predictive equation for resting energy expenditure in healthy individuals
* **Authors:** M. D. Mifflin, S. T. St Jeor, L. A. Hill, B. J. Scott, S. A. Daugherty, Y. O. Koh
* **Journal / Venue:** *The American Journal of Clinical Nutrition (AJCN)*, Vol. 51, No. 2, pp. 241–247, 1990.
* **DOI:** [10.1093/ajcn/51.2.241](https://doi.org/10.1093/ajcn/51.2.241)
* **Domain:** Clinical indirect calorimetry, basal metabolism, and macronutrient architecture.

---

## 🎯 Executive Summary & Core Objectives
Accurately estimating Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) is foundational to preventive nutritional therapy, obesity management, and metabolic recomposition. For decades, the 1919 Harris-Benedict equation was the standard but systematically overestimated caloric burn in modern sedentary cohorts. This landmark study established the gold-standard modern predictive formula validated through indirect calorimetry.

---

## 🔬 Experimental Methodology & The Mifflin-St Jeor Equations
* **Subjects:** 498 healthy men and women aged 19 to 78 years, incorporating both normal weight and obese individuals.
* **Instrumentation:** Precision indirect calorimetry measuring resting oxygen consumption ($\text{VO}_2$) and carbon dioxide production ($\text{VCO}_2$).
* **Equations Derived:**
  - **For Males:**
    $$\text{BMR} = 10 \cdot W_{\text{kg}} + 6.25 \cdot H_{\text{cm}} - 5 \cdot A_{\text{years}} + 5$$
  - **For Females:**
    $$\text{BMR} = 10 \cdot W_{\text{kg}} + 6.25 \cdot H_{\text{cm}} - 5 \cdot A_{\text{years}} - 161$$
* **Validation:** Demonstrated within $\pm 10\%$ accuracy for $>82\%$ of subjects, outperforming older anthropometric equations by $\sim 5\%$.

---

## ⚙️ Advanced Lean Mass Extension: Katch-McArdle Formula
While Mifflin-St Jeor is the most reliable general equation, it relies solely on total body mass ($W_{\text{kg}}$). For athletic individuals with low body fat, fat-free lean body mass ($\text{LBM}$) is the true metabolic engine:
$$\text{LBM}_{\text{kg}} = W_{\text{kg}} \cdot \left(1 - \frac{\text{BodyFat}\%}{100}\right)$$
$$\text{BMR}_{\text{Katch}} = 370 + (21.6 \cdot \text{LBM}_{\text{kg}})$$

---

## 🧬 Direct Integration in VitalSync AI Codebase
* **Mathematical Implementation:** Encoded in [`health_models.py`](file:///c:/Users/salman/Desktop/projects/p2/health_models.py) within `HealthMathEngine.calculate_bmr_and_tdee()`.
* **Intelligent Dual-Engine Switch:**
  - If the user uses standard Quick intake, VitalSync AI computes BMR via **Mifflin-St Jeor**.
  - If the user switches to Deep mode and provides `body_fat_pct`, the system automatically activates the **Katch-McArdle Formula** and updates the UI tag to display `"Katch-McArdle (LBM)"`.
* **Total Daily Energy Expenditure (TDEE):** Computes activity multipliers based on daily steps ($1.2$ to $1.65$) plus specific resistance training sessions.
* **Macronutrient Equilibrium:** Powers **Tab 2 (Macros & Plate)**, ensuring that protein ($1.6\text{ to }2.2\text{ g/kg}$), fat ($0.7\text{ to }1.0\text{ g/kg}$), and carbohydrates perfectly equate to the targeted caloric deficit or surplus ($4\text{P} + 9\text{F} + 4\text{C} = \text{Target Kcal}$).

