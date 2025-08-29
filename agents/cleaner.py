from utils.logger import logger
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder

def clean(df, cleaning_plan):
    logger.info("[Cleaner] Applying LLM cleaning strategy...")

    for col in cleaning_plan.get("drop_columns", []):
        if col in df.columns:
            df = df.drop(columns=[col])

    for col, method in cleaning_plan.get("fill_missing", {}).items():
        if col in df.columns:
            if method == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif method == "median":
                df[col] = df[col].fillna(df[col].median())
            elif method == "mode":
                df[col] = df[col].fillna(df[col].mode()[0])

    scaler = MinMaxScaler()
    scale_cols = [col for col in cleaning_plan.get("scale_columns", []) if col in df.columns]
    if scale_cols:
        df[scale_cols] = scaler.fit_transform(df[scale_cols])

    for col in cleaning_plan.get("encode_columns", []):
        if col in df.columns:
            dummies = pd.get_dummies(df[col], prefix=col)
            df = pd.concat([df.drop(columns=[col]), dummies], axis=1)

    logger.info("Cleaning complete.")
    return df
