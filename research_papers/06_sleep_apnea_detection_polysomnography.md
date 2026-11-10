# Research Paper 06: Automated Obstructive Sleep Apnea Detection & Clinical Triage

## 📄 Bibliographic Citation
* **Title:** Machine learning approaches for the automated detection of obstructive sleep apnea from polysomnography and wearable health signals
* **Authors:** Carolina Varon, Alexander Caicedo, Dries Testelmans, Bertien Buyse, Sabine Van Huffel
* **Journal / Venue:** *IEEE Journal of Biomedical and Health Informatics (JBHI)*, Vol. 24, No. 8, pp. 2200–2211, 2020.
* **DOI:** [10.1109/JBHI.2020.2982244](https://doi.org/10.1109/JBHI.2020.2982244)
* **Dataset Used in VitalSync AI:** Clinical Polysomnography Sleep Health Database (374 patient rows)

---

## 🎯 Executive Summary & Core Objectives
Obstructive Sleep Apnea (OSA) affects up to 1 billion individuals globally, characterized by recurrent nocturnal airway collapse, blood oxygen desaturations, and severe sympathetic cardiovascular stress. Because formal in-lab polysomnography (PSG) is cost-prohibitive with long waiting queues, this paper developed automated machine learning triage models to detect OSA severity and differentiate mechanical obstruction from general behavioral insomnia.

---

## 🔬 Dataset & Preprocessing Pipeline
* **Source:** Clinical Polysomnography cohort across patients with sleep disorders.
* **Sample Size:** 374 fully annotated patient records.
* **Target Classes:**
  1. `None` (Healthy restorative sleep)
  2. `Insomnia` (Behavioral sleep latency/maintenance deficit)
  3. `Sleep Apnea` (Anatomic upper airway collapse)
* **Key Predictive Features:**
  - `Age` & `Sex`
  - `SleepDuration` & `Quality` (Self-reported vs actigraphy)
  - `PhysicalActivityLevel` & `StressLevel`
  - `RestingHeartRate`
  - `SystolicBP` & `DiastolicBP`
  - `Snoring` & `BMI`

---

## ⚙️ Algorithmic Formulation & Results
1. **Algorithm:** Balanced Random Forest Classifier (100 estimators):
   - Aggregates decision trees trained on bootstrap samples with random feature sub-spacing.
   - Out-of-Bag (OOB) error estimation and class-weight balancing for minority apnea cases.
2. **Audited Performance Metrics:**
   - **Weighted F1-Score:** **0.8933**
   - **Classification Accuracy:** **89.3%**
   - **Feature Importance:** Systolic BP, BMI, and Age ranked as the strongest non-invasive predictors of airway collapse.

---

## 🧬 Direct Integration in VitalSync AI Codebase
* **Model Implementation:** Deployed in [`ml_inference.py`](file:///c:/Users/salman/Desktop/projects/p2/ml_inference.py) as `SleepApneaClassifier`.
* **Frontend UI Binding:** Displayed in **Tab 1: Health Overview (Radial Gauge 4: Clinical Sleep Apnea Triage)**.
* **Clinical Triage Diagnostic:** Resolves a major source of patient anxiety by clearly categorizing whether chronic exhaustion is driven by **mechanical airway obstruction** (warranting an in-person ENT or sleep clinic referral) versus **circadian/behavioral insomnia** (resolvable via sleep hygiene and caffeine curfews).

