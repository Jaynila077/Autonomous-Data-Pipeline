from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import os, re, json
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model_name="llama3-8b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))

prompt = PromptTemplate.from_template("""
You are a data analyst assistant.

Given this dataset profile:
{profile}

Suggest a JSON object with:
- trend_column: (pick the best numeric column to track over time)
- anomaly_method: ("IQR", "Z-score", or "none")
- rolling_window: an integer window size for smoothing
- optional_plot: list of plots to include (like "histogram", "boxplot", "scatter")

Respond ONLY with the JSON.
""")

def get_analysis_plan(profile):
    print("[Analysis Strategy Agent] Querying LLM for analysis plan...")
    result = llm.invoke([HumanMessage(content=prompt.format(profile=profile))])
    match = re.search(r"\{.*\}", result, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return {}
