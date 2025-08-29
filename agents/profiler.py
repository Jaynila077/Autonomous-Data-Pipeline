from utils.logger import logger

def profile(df):
    logger.info("[Profiler] Profiling dataset...")
    
    summary = {
        "head": df.head(3).to_dict(),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum().to_dict()
    }
    return summary
