import os
from dotenv import load_dotenv
import requests

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def write_report(stats):
    print("[Reporter] Using Groq to write natural language report...")

    prompt = f"""
You are a data analyst assistant. Based on the following statistics, write a brief natural language summary of the dataset trend.

Stats:
{stats}

Make it concise, clear, and insightful (3–5 sentences max).
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
    )

    result = response.json()["choices"][0]["message"]["content"]

    
    with open("output/report.md", "w") as f:
        f.write("# Data Analysis Report\n\n")
        f.write("## Summary\n")
        f.write(result.strip())
        f.write("\n\n---\n![Trend Plot](trend_plot.png)\n")
    
    print("Groq summary written to report.md")
