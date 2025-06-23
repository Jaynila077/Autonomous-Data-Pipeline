import pandas as pd

def fetch(file_path):
    print(f"[Fetcher] Loading {file_path}...")
    return pd.read_csv(file_path)
