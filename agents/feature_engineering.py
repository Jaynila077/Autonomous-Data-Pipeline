from utils.logger import logger
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

def engineer_features(df, analysis_plan):
    logger.info("[Feature Engineer] Applying LLM feature engineering plan...")
    feature_plan = analysis_plan.get("feature_engineering", [])

    for step in feature_plan:
        transformation = step.get("transformation")
        if transformation == "date_part":
            col = step.get("column")
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df[f'{col}_year'] = df[col].dt.year
                df[f'{col}_month'] = df[col].dt.month
                df[f'{col}_day'] = df[col].dt.day
                df[f'{col}_dayofweek'] = df[col].dt.dayofweek
        
        elif transformation == "polynomial":
            col = step.get("column")
            degree = step.get("degree", 2)
            if col in df.columns:
                poly = PolynomialFeatures(degree=degree, include_bias=False)
                poly_features = poly.fit_transform(df[[col]])
                poly_df = pd.DataFrame(poly_features, columns=[f"{col}^{i+1}" for i in range(degree)])
                df = pd.concat([df.drop(columns=[col]), poly_df], axis=1)

        elif transformation == "interaction":
            cols = step.get("columns_to_interact", [])
            if all(c in df.columns for c in cols) and len(cols) == 2:
                df[f'{cols[0]}_x_{cols[1]}'] = df[cols[0]] * df[cols[1]]

                ##More should added later

    logger.info("Feature engineering complete.")
    return df