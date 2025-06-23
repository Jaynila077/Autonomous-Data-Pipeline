import pandas as pd
import matplotlib.pyplot as plt

def analyze(df, target_column):
    print("[Analyzer] Analyzing data...")

    stats = df[target_column].describe().to_dict()

    
    df = df.copy()
    df = df.dropna(subset=[target_column])
    df["Index"] = range(len(df))
    slope = df[[target_column, "Index"]].corr().iloc[0, 1]

    trend = "increasing" if slope > 0.1 else "decreasing" if slope < -0.1 else "stable"
    stats["trend"] = trend
    stats["correlation_to_time"] = round(slope, 3)

    
    plt.figure(figsize=(8, 4))
    df.plot(x="Index", y=target_column, title=f"{target_column} Trend", legend=False)
    plt.xlabel("Index (time)")
    plt.ylabel(target_column)
    plt.tight_layout()
    plt.savefig("output/trend_plot.png")
    plt.close()

    return stats
