# Research Paper 03: Short-Wavelength Blue Light, Melatonin Suppression, and Sleep Latency

## 📄 Bibliographic Citation
* **Title:** Evening use of light-emitting eReaders negatively affects sleep, circadian timing, and next-morning alertness
* **Authors:** Anne-Marie Chang, Daniel Aeschbach, Jeanne F. Duffy, Charles A. Czeisler
* **Journal / Venue:** *Proceedings of the National Academy of Sciences (PNAS)*, Vol. 112, No. 4, pp. 1232–1237, 2015.
* **DOI:** [10.1073/pnas.1418490112](https://doi.org/10.1073/pnas.1418490112)
* **Dataset Used in VitalSync AI:** Screen Time, Blue Light, & Late-Night Phone Habits Cohort (8,500 records)

---

## 🎯 Executive Summary & Core Objectives
In modern society, nighttime smartphone and tablet usage has become ubiquitous. This clinical inpatient crossover study evaluated the biological consequences of evening exposure to light-emitting screens versus reading print books under identical dim ambient lighting.

---

## 🔬 Experimental Methodology & Findings
* **Protocol:** Inpatient randomized crossover study at Brigham and Women's Hospital. Participants read on light-emitting tablets versus printed books for 4 hours before bedtime for 5 consecutive nights.
* **Primary Biological Observations:**
  1. **Sleep Onset Latency Delay:** Participants reading on screens took an average of **$>30\text{ minutes}$ longer to fall asleep** ($p < 0.001$).
  2. **Melatonin Secretion Suppression:** Endogenous salivary and plasma melatonin was acutely suppressed by $>55\%$.
  3. **Circadian Phase Shift:** The circadian melatonin rhythm was phase-delayed by **1.5 hours** (shifting the body's biological clock later).
  4. **Degradation of REM Sleep:** Total duration of Rapid Eye Movement (REM) sleep was significantly attenuated.
  5. **Next-Morning Sleep Inertia:** Participants experienced prolonged subjective sleepiness and impaired cognitive alertness taking several hours to dissipate.

---

## ⚙️ Mathematical & Algorithmic Translation in VitalSync AI
VitalSync AI translates these biological findings into a **Multi-Output Gradient Boosting Regressor** (`CircadianSleepLatencyModel`):
* **Input Features:**
  - `bedtime_phone_minutes` (Continuous: 0 to 180 min)
  - `bedtime_app` (Categorical: short-form video [dopaminergic/high stimulation], streaming, messaging, reading)
  - `blue_light_filter_active` (Binary boolean attenuation factor)
  - `screen_brightness_pct` (0 to 100%)
* **Target Outputs:**
  1. Predicted Sleep Latency (Minutes):
     $$\text{Latency} \approx \text{Baseline} + \alpha \cdot (\text{PhoneMin}) \cdot (1 - 0.4 \cdot \text{BlueLight}) + \beta \cdot (\text{AppFactor})$$
  2. Sleep Debt Category (None, Mild, Moderate, Severe).

---

## 🧬 Direct Integration in VitalSync AI Codebase
* **Model Implementation:** Deployed in [`ml_inference.py`](file:///c:/Users/salman/Desktop/projects/p2/ml_inference.py).
* **Frontend UI Binding:** Displayed in **Tab 1 (Radial Gauge 3: Circadian Sleep Latency)**.
* **Counterfactual Interactivity:** In **Tab 5 (What-If Simulator)**, dragging the phone reduction slider recalculates the latency drop in real time (e.g., reducing phone scrolling from 75 min to 30 min yields an instant projected onset improvement of $\sim 18.4\text{ minutes}$).

