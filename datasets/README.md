# Datasets: Sources, Usage & Limitations

VitalSync AI's five machine learning models are trained on public datasets totalling ~499,000 rows. Two are real CDC survey datasets (~390,000 rows). The other three are **simulated** datasets published on Kaggle, so the models built on them should be treated as illustrative, not clinically validated.

---

## 📊 Datasets used for training

| Dataset | Source | Real or simulated | Records | Target | Used by |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `heart_2020_cleaned.csv` — Personal Key Indicators of Heart Disease | CDC BRFSS 2020 (Kaggle: kamilpytlak) | **Real survey** | 319,795 | `HeartDisease` = respondent has *ever* reported coronary heart disease / heart attack | Lifestyle Heart Disease Risk model |
| `diabetes_binary_5050split_health_indicators_BRFSS2015.csv` | CDC BRFSS 2015 (Kaggle: alexteboul) | **Real survey** (rebalanced 50/50) | 70,692 | `Diabetes_binary` (pre-diabetes or diabetes) | Pre-Diabetes Screener |
| `bedtime_screentime_sleep_debt.csv` | Kaggle: samartalwar | **Simulated** | 8,500 | Sleep latency, next-day fatigue, sleep-debt category | Circadian Sleep model |
| `Sleep_health_and_lifestyle_dataset.csv` | Kaggle: uom190346a | **Simulated** (the author describes it as "synthetic and created … for illustrative purposes") | 374 | `Sleep Disorder` (None / Insomnia / Sleep Apnea) | Sleep Pathology model |
| `student_lifestyle_100k.csv` | Kaggle: aldinwhyudii | **Simulated** (columns follow neat generated distributions, e.g. sleep exactly mean 7.0 / SD 1.5) | 100,000 | `Stress_Level`, `Depression` | Digital Burnout model |

### Important limitations
- **Heart disease model is not a 10-year risk score.** BRFSS asks whether someone has *ever* been told they have heart disease, so the model estimates how closely a lifestyle profile resembles people who report heart disease. It is labelled "Lifestyle Heart Disease Risk" in the app for this reason. (The JSON field is still named `cardiovascular_10yr_risk_pct` for backward compatibility.)
- **Simulated datasets:** models 3–5 learn the rules used to generate their data, not real human outcomes. Their numbers are useful for demonstrating the pipeline, not for health decisions.
- **Proxy inputs:** some model features are approximated from app inputs (e.g. `HighChol` ← 4+ fast-food meals/week, `GenHlth` ← symptom count and stress). See `ml_inference.py`.

---

## 🗂️ Datasets downloaded but not used

These files are in `datasets/` (git-ignored) from early exploration, but no model is trained on them. They can be deleted safely, or used for future work:

| File / folder | Notes |
| :--- | :--- |
| `ObesityDataSet_raw_and_data_sinthetic.csv` | Obesity levels (Kaggle: fatemehmehrparvar), 2,111 rows, partly synthetic |
| `fitbit/` (18 CSVs, ~350 MB) | Fitbit tracker export (Kaggle: arashnic/fitbit) — candidate for future wearable integration |
| `cardio_train.csv` | Cardiovascular disease dataset |
| `CVD_cleaned.csv` | Cardiovascular disease risk dataset |
| `healthcare-dataset-stroke-data.csv` | Stroke prediction dataset |
| `diabetes_012_health_indicators_BRFSS2015.csv`, `diabetes_binary_health_indicators_BRFSS2015.csv` | Other versions of the BRFSS diabetes data (only the 50/50 split is used) |

The `bedtime_screentime_sleep_debt.csv` in the repository root is a duplicate left over from `download_and_inspect.py`; the copy in `datasets/` is the one used.

---

## 📥 Downloading & retraining

Large CSVs are not tracked in git. The trained model bundles in [`models/`](../models/) (~3.5 MB) are included so the app works out of the box.

```bash
pip install -r requirements.txt
python scripts/download_datasets.py   # downloads the Kaggle datasets via kagglehub
python train_models.py                # retrains all 5 models into models/
```

---

## 📜 Licences & attribution
- **CDC BRFSS data**: public-domain US government survey data.
- **Kaggle datasets**: published under their respective open licences (see each Kaggle page).
- No personally identifiable information is included in any dataset or model file.
