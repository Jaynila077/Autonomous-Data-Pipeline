import pandas as pd
import matplotlib.pyplot as plt

def analyze(df, analysis_plan):
    print("[Analyzer] Analyzing based on LLM strategy...")

    target = analysis_plan.get("trend_column")
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not in DataFrame")

    stats = df[target].describe().to_dict()

    df["Index"] = range(len(df))
    slope = df[[target, "Index"]].corr().iloc[0, 1]
    trend = "increasing" if slope > 0.1 else "decreasing" if slope < -0.1 else "stable"
    stats["trend"] = trend
    stats["correlation_to_time"] = round(slope, 3)

    window = analysis_plan.get("rolling_window", 10)
    df["RollingMean"] = df[target].rolling(window=window).mean()

    method = analysis_plan.get("anomaly_method", "none")
    if method == "IQR":
        Q1 = df[target].quantile(0.25)
        Q3 = df[target].quantile(0.75)
        IQR = Q3 - Q1
        anomalies = df[(df[target] < Q1 - 1.5*IQR) | (df[target] > Q3 + 1.5*IQR)]
    elif method == "Z-score":
        z_scores = (df[target] - df[target].mean()) / df[target].std()
        anomalies = df[abs(z_scores) > 3]
    else:
        anomalies = pd.DataFrame()

    stats["num_anomalies"] = len(anomalies)

   
    df.plot(y=[target, "RollingMean"], title=f"{target} with Rolling Average")
    plt.xlabel("Index (time)")
    plt.tight_layout()
    plt.savefig("output/trend_plot.png")
    plt.close()

    
    for plot_type in analysis_plan.get("optional_plot", []):
        if plot_type == "histogram":
            df[target].plot(kind="hist", bins=20, title="Histogram")
            plt.savefig("output/histogram.png")
            plt.close()
        elif plot_type == "boxplot":
            df[[target]].plot(kind="box", title="Boxplot")
            plt.savefig("output/boxplot.png")
            plt.close()

    return stats
