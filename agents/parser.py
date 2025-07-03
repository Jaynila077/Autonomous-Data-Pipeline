import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import re


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"
)

prompt = PromptTemplate.from_template("""
You are a helpful assistant that extracts structured data pipeline task info from user input.

User input: "{user_input}"

Respond ONLY with a valid Python dictionary like:
{{"file_path": "data/sample.csv", "goal": "trend_analysis", "target_column": "Rainfall"}}
""")


def parse(user_input):
    print("[LangChain Parser] Using Groq via LangChain...")

    formatted_prompt = prompt.format(user_input=user_input)
    response = llm.invoke([HumanMessage(content=formatted_prompt)])
    result = response.content.strip()

    print("LLM Raw Output:", result)

    try:
        match = re.search(r"\{.*\}", result, re.DOTALL)
        if match:
            parsed_dict = eval(match.group(0), {"__builtins__": {}})
            print("Parsed Dict:", parsed_dict)
            return parsed_dict
        else:
            print("Could not find dictionary in output.")
            return {}
    except Exception as e:
        print("Error parsing dictionary:", e)
        return {}
