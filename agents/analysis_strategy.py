from utils.logger import logger
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import os, re, json
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model_name="openai/gpt-oss-20b", groq_api_key=os.getenv("GROQ_API_KEY"))

prompt = PromptTemplate.from_template("""
You are a data analyst assistant.

Given this dataset profile:
{profile}

Suggest a JSON object for a comprehensive analysis plan. The plan should include:
- trend_column: (pick the best numeric column to track over time)
- anomaly_method: ("IQR", "Z-score", or "none")
- rolling_window: an integer window size for smoothing
- optional_plot: list of plots to include (like "histogram", "boxplot", "scatter")
- feature_engineering: a list of dictionaries for feature creation (e.g., "date_part", "polynomial", "interaction").
- advanced_analysis: A dictionary specifying ONE advanced analysis to perform. Choose the most relevant from "correlation", "regression", or "clustering".
  - For "correlation", include a "heatmap_columns" key with a list of numeric columns.
  - For "regression", include a "target" and a list of "features".
  - For "clustering", include "n_clusters" and a list of "features".

Respond ONLY with the JSON.
""")

def get_analysis_plan(profile):
    logger.info("[Analysis Strategy Agent] Querying LLM for analysis plan...")
    result = llm.invoke([HumanMessage(content=prompt.format(profile=profile))])
    match = re.search(r"\{.*\}", result.content, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return {}