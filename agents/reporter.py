from utils.logger import logger
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="openai/gpt-oss-20b"
)

prompt_template = PromptTemplate.from_template("""
You are a data analyst assistant. Given the following dictionary of summary statistics:

{stats}

Write a concise, insightful markdown report (5-7 sentences max). Explain the key trends, values, and insights from the analysis. 
If there are advanced analysis results (correlation, regression, or clustering), be sure to interpret them.
Avoid any generic disclaimers.
""")

def write_report(stats):
    logger.info("[Reporter] Using LangChain + Groq to write summary...")


    prompt = prompt_template.format(stats=stats)

    response = llm.invoke([HumanMessage(content=prompt)])
    summary = response.content.strip()

    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write("# Data Analysis Report\n\n")
        f.write("## Summary\n\n")
        f.write(summary)
        f.write("\n\n---\n![Trend Plot](trend_plot.png)\n")
        
        # Add links to new plots if they exist
        if os.path.exists("output/correlation_matrix.png"):
            f.write("![Correlation Matrix](correlation_matrix.png)\n")
        if os.path.exists("output/cluster_plot.png"):
            f.write("![Cluster Plot](cluster_plot.png)\n")


    logger.info("[Reporter] Summary written to `output/report.md`")