import matplotlib.pyplot as plt

def analyze(df, column):
    print(f"[Analyzer] Analyzing '{column}'...")
    stats = df[column].describe().to_dict()
    df[column].plot(title=f"{column} Trend")
    plt.savefig("output/chart.png")
    return stats
