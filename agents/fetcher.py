from utils.logger import logger
import pandas as pd

def fetch(file_path):
    logger.info(f"[Fetcher] Loading {file_path}...")
    return pd.read_csv(file_path)
