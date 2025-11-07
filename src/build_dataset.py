import os
import pandas as pd
from extract_features import extract_features
 
RAW_DIR = "data/raw/"
 
LABEL_FILE = "data/labels.csv"
 
OUTPUT_FILE = "data/processed/features.csv"
 
def build_dataset():
    labels_df = pd.read_csv(LABEL_FILE)
 
    all_rows = []
 
    for _, row in labels_df.iterrows():
        filename = row["filename"]
        label = row["label"]
        gpx_path = os.path.join(RAW_DIR, filename)
 
        if not os.path.exists(gpx_path):
            print(f"⚠️ File not found: {gpx_path}")
            continue
 
        try:
            # Extract features from GPX
            features = extract_features(gpx_path)
            features["filename"] = filename
            features["label"] = label
            all_rows.append(features)
            print(f"Processed {filename}")
 
        except Exception as e:
            print(f"Error processing {filename}: {e}")
 
    # Convert to DataFrame & save
    df = pd.DataFrame(all_rows)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print("\nSaved dataset to:", OUTPUT_FILE)
    print(df.head())
 
if __name__ == "__main__":
    build_dataset()
