import os, pandas as pd

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_csv(df: pd.DataFrame, path: str):
    ensure_dir(os.path.dirname(path))
    df.to_csv(path, index=False)
