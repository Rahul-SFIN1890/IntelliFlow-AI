from agents.sql_agent import sql_agent
from agents.rag_agent import rag_agent
from agents.tool_agent import tool_agent
from agents.reasoning_agent import reasoning_agent
from agents.websearch_agent import websearch_agent
from agents.analyst_agent import analyst_agent
from agents.writer_agent import writer_agent
from agents.summarizer_agent import summarizer_agent


AGENT_REGISTRY = {

    "sql": sql_agent,

    "rag": rag_agent,

    "tool": tool_agent,

    "reasoning": reasoning_agent,

    "websearch": websearch_agent,

    "analyst": analyst_agent,

    "writer": writer_agent,

    "summary": summarizer_agent

}