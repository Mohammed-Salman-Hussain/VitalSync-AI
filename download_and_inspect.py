import os
import shutil
import kagglehub
import pandas as pd

print("Downloading dataset from Kaggle...")
path = kagglehub.dataset_download("samartalwar/sleep-debt-and-screen-time-late-night-phone-habits")
print("Downloaded to:", path)

files = os.listdir(path)
print("Files in downloaded dataset:", files)

# Copy files to local directory for easy access
for f in files:
    src = os.path.join(path, f)
    dst = os.path.join(os.getcwd(), f)
    if os.path.isfile(src):
        shutil.copy(src, dst)
        print(f"Copied {f} to {dst}")

# Find csv files
csv_files = [f for f in files if f.endswith(".csv")]
for csv_file in csv_files:
    print("\n" + "="*50)
    print(f"Inspecting: {csv_file}")
    print("="*50)
    df = pd.read_csv(csv_file)
    print("\n--- SHAPE ---")
    print(df.shape)
    print("\n--- COLUMNS & DTYPES ---")
    print(df.dtypes)
    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())
    print("\n--- HEAD (5 rows) ---")
    print(df.head())
    print("\n--- SUMMARY STATISTICS ---")
    print(df.describe(include='all'))
