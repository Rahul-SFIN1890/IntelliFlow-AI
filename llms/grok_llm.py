import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)
def get_llm():
    return llm

# model_name="llama-3.3-70b-versatile",
# model_name = "llama-3.1-8b-instant",