from utils.logger import logger
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import os, re, json
from dotenv import load_dotenv


load_dotenv()
llm = ChatGroq(model_name="llama3-8b-8192", groq_api_key=os.getenv("GROQ_API_KEY"))

prompt = PromptTemplate.from_template("""
You are a data cleaning planner bot.

Based on this dataset profile:
{profile}

Return a JSON object with:
- drop_columns: list of column names
- fill_missing: dict of column: method ("mean", "median", "mode")
- scale_columns: list of numeric columns to normalize
- encode_columns: list of categorical columns to one-hot encode

Respond ONLY with the JSON.
""")

def get_cleaning_plan(profile):
    logger.info("[Cleanig Strategy Agent] Querying LLM for cleaning strategy...")
    result = llm.invoke([HumanMessage(content=prompt.format(profile=profile))])  
    match = re.search(r"\{.*\}", result.content, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return {}
