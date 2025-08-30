from utils.logger import logger
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

def analyze(df, analysis_plan):
    logger.info("[Analyzer] Analyzing based on LLM strategy...")
    stats = {}

    # Basic Trend Analysis (if trend_column is present)
    target = analysis_plan.get("trend_column")
    if target and target in df.columns:
        stats['description'] = df[target].describe().to_dict()

        df["Index"] = range(len(df))
        slope = df[[target, "Index"]].corr().iloc[0, 1]
        trend = "increasing" if slope > 0.1 else "decreasing" if slope < -0.1 else "stable"
        stats["trend"] = trend
        stats["correlation_to_time"] = round(slope, 3)

        window = analysis_plan.get("rolling_window", 10)
        df["RollingMean"] = df[target].rolling(window=window).mean()
        
        df.plot(y=[target, "RollingMean"], title=f"{target} with Rolling Average")
        plt.xlabel("Index (time)")
        plt.tight_layout()
        plt.savefig("output/trend_plot.png")
        plt.close()

    # Advanced Analysis
    advanced_analysis = analysis_plan.get("advanced_analysis", {})
    analysis_type = list(advanced_analysis.keys())[0] if advanced_analysis else None

    if analysis_type == "correlation":
        numeric_df = df.select_dtypes(include='number')
        if len(numeric_df.columns) > 1:
            plt.figure(figsize=(10, 8))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
            plt.title('Correlation Matrix')
            plt.savefig("output/correlation_matrix.png")
            plt.close()
            stats['correlation_matrix'] = numeric_df.corr().to_dict()

    elif analysis_type == "regression":
        reg_details = advanced_analysis.get("regression", {})
        target_col, feature_cols = reg_details.get("target"), reg_details.get("features", [])
        
        valid_features = [f for f in feature_cols if f in df.columns and pd.api.types.is_numeric_dtype(df[f])]
        
        if target_col in df.columns and pd.api.types.is_numeric_dtype(df[target_col]) and valid_features:
            X = df[valid_features]
            y = df[target_col]
            model = LinearRegression()
            model.fit(X, y)
            stats['regression_results'] = {
                'coefficients': dict(zip(valid_features, model.coef_)),
                'intercept': model.intercept_,
                'r_squared': model.score(X, y)
            }

    elif analysis_type == "clustering":
        cluster_details = advanced_analysis.get("clustering", {})
        n_clusters = cluster_details.get("n_clusters", 3)
        feature_cols = cluster_details.get("features", [])
        
        valid_features = [f for f in feature_cols if f in df.columns and pd.api.types.is_numeric_dtype(df[f])]
        
        if len(valid_features) > 1: 
            X = df[valid_features]
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            df['cluster'] = kmeans.fit_predict(X)
            stats['clustering_results'] = df.groupby('cluster')[valid_features].mean().to_dict()
            
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x=valid_features[0], y=valid_features[1], hue='cluster', palette='viridis')
            plt.title('Cluster Analysis')
            plt.savefig("output/cluster_plot.png")
            plt.close()

    logger.info("Analysis Complete")
    return stats