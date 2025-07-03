def profile(df):
    print("[Profiler] Profiling dataset...")
    
    summary = {
        "head": df.head(3).to_dict(),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum().to_dict()
    }
    return summary
