import os
import re
from dotenv import load_dotenv
import requests

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def parse(user_input):
    print("[Groq Parser] Calling Groq API...")

    prompt = f"""
You are a helpful assistant that extracts structured data pipeline task info from user input.

User says: "{user_input}"

Respond ONLY with a Python dictionary like:
{{"file_path": "data/sample.csv", "goal": "trend_analysis", "target_column": "Rainfall"}}
"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",  
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=data)
    raw_result = response.json()["choices"][0]["message"]["content"]
    print("🧾 Raw LLM Response:", raw_result)

    try:
        match = re.search(r"\{.*?\}", raw_result, re.DOTALL)
        if match:
            result_str = match.group(0)
            parsed_dict = eval(result_str, {"__builtins__": {}})
            print("Parsed dict:", parsed_dict)
            return parsed_dict
        else:
            print("No dictionary found in LLM response.")
            return {}
    except Exception as e:
        print("Parsing failed:", e)
        return {}
