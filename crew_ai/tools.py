from crewai.tools import tool

from agents.sql_agent import sql_agent
from agents.rag_agent import rag_agent


@tool("SQL Database Tool")
def sql_database_tool(question: str) -> str:
    """
    Execute SQL queries using the existing SQL agent.
    """

    state = {
        "question": question,
        "chat_history": []
    }

    try:
        result = sql_agent(state)
        return result["answer"]

    except Exception as e:
        return f"SQL Tool Error: {str(e)}"


@tool("HR Policy Tool")
def hr_policy_tool(question: str) -> str:
    """
    Search HR policies using the existing RAG pipeline.
    """

    state = {
        "question": question,
        "chat_history": []
    }

    try:
        result = rag_agent(state)
        return result["answer"]

    except Exception as e:
        return f"RAG Tool Error: {str(e)}"