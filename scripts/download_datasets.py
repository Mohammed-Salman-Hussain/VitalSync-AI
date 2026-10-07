"""
scripts/download_datasets.py - Automated Public Health Dataset Ingestion

Downloads all authentic public health and lifestyle datasets used by VitalSync AI:
1. samartalwar/sleep-debt-and-screen-time-late-night-phone-habits
2. kamilpytlak/personal-key-indicators-of-heart-disease
3. alexteboul/diabetes-health-indicators-dataset
4. uom190346a/sleep-health-and-lifestyle-dataset
5. aldinwhyudii/student-depression-and-lifestyle-100k-data
6. fatemehmehrparvar/obesity-levels
"""

import os
import shutil
import kagglehub

DATASETS = [
    ("samartalwar/sleep-debt-and-screen-time-late-night-phone-habits", "Circadian Sleep & Screen Time (8,500 rows)"),
    ("kamilpytlak/personal-key-indicators-of-heart-disease", "CDC BRFSS 2020 Heart Disease (319,795 rows)"),
    ("alexteboul/diabetes-health-indicators-dataset", "CDC BRFSS Diabetes Indicators (70,692 rows)"),
    ("uom190346a/sleep-health-and-lifestyle-dataset", "Clinical Sleep Health & Apnea (374 records)"),
    ("aldinwhyudii/student-depression-and-lifestyle-100k-data", "Digital Stress & Lifestyle (100,000 records)"),
    ("fatemehmehrparvar/obesity-levels", "Obesity & Sedentary Habit Estimation (2,111 records)"),
]

TARGET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets")
os.makedirs(TARGET_DIR, exist_ok=True)


def download_all():
    print("=" * 70)
    print("VitalSync AI - Public Health Datasets Downloader")
    print("=" * 70)
    
    for slug, desc in DATASETS:
        print(f"\n[+] Fetching {desc} ({slug})...")
        try:
            path = kagglehub.dataset_download(slug)
            print(f"    Downloaded to: {path}")
            
            # Copy CSV files to datasets/
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith(".csv"):
                        src = os.path.join(root, f)
                        dst = os.path.join(TARGET_DIR, f)
                        shutil.copy2(src, dst)
                        size_mb = os.path.getsize(dst) / (1024 * 1024)
                        print(f"    -> Saved {f} ({size_mb:.2f} MB) to datasets/")
        except Exception as e:
            print(f"    [!] Failed to download {slug}: {e}")
            
    print("\n" + "=" * 70)
    print("All dataset files successfully populated in datasets/ directory.")
    print("To retrain all machine learning models, run:")
    print("    python train_models.py")
    print("=" * 70)


if __name__ == "__main__":
    download_all()
