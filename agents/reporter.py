import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-8b-8192"
)

prompt_template = PromptTemplate.from_template("""
You are a data analyst assistant. Given the following dictionary of summary statistics:

{stats}

Write a concise, insightful markdown report (3-5 sentences max) explaining the trend, key values, and what the data indicates.
Avoid any generic disclaimers.
""")

def write_report(stats):
    print("[Reporter] Using LangChain + Groq to write summary...")

    prompt = prompt_template.format(stats=stats)

    response = llm([HumanMessage(content=prompt)])
    summary = response.content.strip()

    with open("output/report.md", "w", encoding="utf-8") as f:
        f.write("# Data Analysis Report\n\n")
        f.write("## Summary\n\n")
        f.write(summary)
        f.write("\n\n---\n![Trend Plot](trend_plot.png)\n")

    print("Summary written to `output/report.md`")
