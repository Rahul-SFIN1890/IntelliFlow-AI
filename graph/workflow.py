from langgraph.graph import StateGraph
from langgraph.graph import END

from graph.state import AgentState

from agents.router_agent import router_agent
from agents.rag_agent import rag_agent
from agents.summarizer_agent import summarizer_agent
from agents.websearch_agent import websearch_agent
from agents.reasoning_agent import reasoning_agent
from agents.tool_agent import tool_agent
from agents.sql_agent import sql_agent

# New Agents
from agents.orchestrator_agent import orchestrator_agent
from agents.execution_agent import execution_agent


builder = StateGraph(AgentState)

# ==========================
# Nodes
# ==========================

builder.add_node(
    "router",
    router_agent
)

builder.add_node(
    "rag",
    rag_agent
)

builder.add_node(
    "summary",
    summarizer_agent
)

builder.add_node(
    "websearch",
    websearch_agent
)

builder.add_node(
    "reasoning",
    reasoning_agent
)

builder.add_node(
    "tool",
    tool_agent
)

builder.add_node(
    "sql",
    sql_agent
)

# New Nodes
builder.add_node(
    "orchestrator",
    orchestrator_agent
)

builder.add_node(
    "execution",
    execution_agent
)

# ==========================
# Entry Point
# ==========================

builder.set_entry_point(
    "router"
)

# ==========================
# Router Decision
# ==========================

def route_decision(state):

    return state["route"]


# ==========================
# Conditional Routing
# ==========================

builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "rag": "rag",

        "summary": "summary",

        "websearch": "websearch",

        "reasoning": "reasoning",

        "tool": "tool",

        "sql": "sql",

        "orchestrator": "orchestrator"
    }
)

# ==========================
# Existing Routes
# ==========================

builder.add_edge(
    "rag",
    END
)

builder.add_edge(
    "summary",
    END
)

builder.add_edge(
    "websearch",
    END
)

builder.add_edge(
    "reasoning",
    END
)

builder.add_edge(
    "tool",
    END
)

builder.add_edge(
    "sql",
    END
)

# ==========================
# Multi-Agent Flow
# ==========================

builder.add_edge(
    "orchestrator",
    "execution"
)

builder.add_edge(
    "execution",
    END
)

# ==========================
# Compile
# ==========================

app = builder.compile()