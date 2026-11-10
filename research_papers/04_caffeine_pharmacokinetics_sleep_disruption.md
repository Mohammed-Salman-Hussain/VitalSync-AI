# Research Paper 04: Pharmacokinetics of Caffeine and Bedtime Sleep Disruption

## 📄 Bibliographic Citation
* **Title:** Caffeine effects on sleep taken 0, 3, or 6 hours before going to bed
* **Authors:** Christopher Drake, Timothy Roehrs, John Shambroom, Thomas Roth
* **Journal / Venue:** *Journal of Clinical Sleep Medicine (JCSM)*, Vol. 9, No. 11, pp. 1195–1200, 2013.
* **DOI:** [10.5664/jcsm.3170](https://doi.org/10.5664/jcsm.3170)
* **Physiological Domain:** First-order elimination pharmacokinetics and adenosine receptor blockade.

---

## 🎯 Executive Summary & Core Objectives
Caffeine (1,3,7-trimethylxanthine) is the most widely consumed psychoactive stimulant in the world. While consumers recognize that coffee taken directly before bed disrupts sleep, many believe afternoon or early evening consumption is harmless. This double-blind, placebo-controlled clinical trial systematically quantified sleep disruption when a standard moderate-to-large dose of caffeine (400 mg) was consumed at 0, 3, and 6 hours prior to bedtime.

---

## 🔬 Clinical Methodology & Key Findings
* **Trial Design:** Double-blind, placebo-controlled crossover study on 12 healthy sleepers. Tracked via at-home polysomnography and sleep diaries.
* **Objective Findings:**
  1. Consuming caffeine even **6 hours before bed** objectively reduced total sleep time by **over 1 full hour** ($p < 0.05$).
  2. Increased sleep onset latency and doubled nocturnal wake time (WASO).
  3. **The "Unaware" Factor:** While objective sensors confirmed severe sleep fragmentation, participants' subjective diaries frequently failed to perceive the disruption, indicating an insidious, sub-conscious loss of slow-wave sleep.

---

## ⚙️ Pharmacokinetic Modeling in VitalSync AI
Caffeine follows **first-order linear elimination kinetics** in healthy adult livers via cytochrome P450 1A2 (CYP1A2) enzymes:
$$C(t) = C_0 \cdot \left(\frac{1}{2}\right)^{\frac{t}{t_{1/2}}}$$
Where:
* $C_0$ = Initial caffeine dose (mg).
* $t_{1/2}$ = Biological elimination half-life ($\approx 5.5\text{ hours}$ in non-pregnant adults).
* $t$ = Elapsed time from last cup to bedtime (hours).

### Clinical Disruption Threshold:
If $C(\text{bedtime}) > 25\text{ mg}$, active serum caffeine continues to antagonize central adenosine $A_1$ and $A_{2A}$ receptors, suppressing slow-wave delta power and elevating heart rate.

---

## 🧬 Direct Integration in VitalSync AI Codebase
* **Mathematical Implementation:** Encoded in [`health_models.py`](file:///c:/Users/salman/Desktop/projects/p2/health_models.py) within `HealthMathEngine.calculate_circadian_caffeine_metrics()`.
* **Dynamic Canvas Rendering:** In **Tab 3: Circadian Clock**, [`charts.js`](file:///c:/Users/salman/Desktop/projects/p2/web/js/charts.js) renders a 60fps high-DPI canvas showing the continuous 24-hour decay curve, a dashed red $25\text{ mg}$ disruption floor, and the exact bedtime point marker.
* **Automated Curfew Recommendation:** Computes the exact time of day after which no further coffee/tea should be consumed to guarantee $<20\text{ mg}$ residual caffeine by habitual bedtime.

