import re
import time
from urllib import response

from graph import state
from llms.grok_llm import llm
from utils.logger import logger


AVAILABLE_ROUTES = [

    "rag",

    "summary",

    "websearch",

    "reasoning",

    "tool",

    "sql",

    "orchestrator"

]
# ==========================================================
# ROUTER LOGGER
# ==========================================================

def log_route(route: str, elapsed: float):

    logger.info("=" * 60)
    logger.info("ROUTER AGENT")
    logger.info("Selected Route : %s", route)
    logger.info("Execution Time : %.3f sec", elapsed)
    logger.info("=" * 60)


def router_agent(state):

    start_time = time.time()

    print("\n========== ROUTER AGENT ==========\n")

    question = state["question"]

    logger.info("=" * 60)
    logger.info("Incoming Request")
    logger.info("Question : %s", question)

    if state.get("chat_history"):
        logger.debug(
            "Chat History : %s",
            state.get("chat_history", [])
        )

    history = "\n".join(
        state.get(
            "chat_history",
            []
        )
    )

    question_lower = question.lower()

    employee_names = [

        "rahul",

        "aman",

        "bhavna",
    
        "rohit",

        "priya"

    ]

    has_employee = any(

        name in question_lower

        for name in employee_names

    )

    # ==========================================================
    # SQL KEYWORDS
    # ==========================================================

    sql_keywords = [

        # Employee

        "employee",

        "employee id",

        "department",

        "designation",

        "experience",

        "city",

        "profile",

        # Salary

        "salary",

        "gross salary",

        "net salary",

        "ctc",

        # Finance

        "bonus",

        "tax",

        "loan",

        "reimbursement",

        "incentive",

        # Attendance

        "attendance",

        "present",

        "absent",

        "work from home",

        "wfh",

        # Payroll

        "payroll",

        "pf",

        "esi",

        "deduction",

        "gross",

        "net pay",

        # Leave

        "leave balance",

        "remaining leave",

        "paid leave",

        "casual leave",

        "sick leave",

        # Projects

        "project",

        "project status",

        "project rating",

        "client",

        "working on",

        # Ranking

        "highest salary",

        "lowest salary",

        "top salary",

        "maximum salary",

        "minimum salary"

    ]

    # ==========================================================
    # RAG KEYWORDS
    # ==========================================================

    rag_keywords = [

        "policy",

        "leave policy",

        "company policy",

        "company leave policy",

        "hr policy",

        "insurance",

        "insurance policy",

        "travel policy",

        "reimbursement policy",

        "handbook",

        "employee handbook",

        "manual",

        "guideline",

        "guidelines",

        "faq",

        "pdf",

        "document"

    ]

    # ==========================================================
    # TOOL KEYWORDS
    # ==========================================================

    tool_keywords = [

        "weather",

        "currency",

        "calculate",

        "conversion",

        "convert"

    ]

    # ==========================================================
    # WEB SEARCH
    # ==========================================================

    web_keywords = [

        "latest",

        "today",

        "current",

        "internet",

        "news"

    ]

    # ==========================================================
    # SUMMARY KEYWORDS
    # ==========================================================

    summary_keywords = [

        "summarize",

        "summary",

        "brief",

        "short",

        "concise",

        "executive summary",

        "tldr"

    ]

    # ==========================================================
    # ANALYSIS KEYWORDS
    # ==========================================================

    analysis_keywords = [

        "compare",

        "analysis",

        "analyze",

        "report",

        "dashboard",

        "recommend",

        "insight",

        "generate"

    ]

    # ==========================================================
    # HYBRID SQL + RAG
    # ==========================================================

    has_sql = any(
        keyword in question_lower
        for keyword in sql_keywords
    )

    has_rag = any(
        keyword in question_lower
        for keyword in rag_keywords
    )

    has_summary = any(
        keyword in question_lower
        for keyword in summary_keywords
    )

    has_analysis = any(
        keyword in question_lower
        for keyword in analysis_keywords
    )

    has_tool = any(
        keyword in question_lower
        for keyword in tool_keywords
    )

    has_web = any(
        keyword in question_lower
        for keyword in web_keywords
    )

    logger.debug(
        "Keyword Detection | SQL=%s | RAG=%s | TOOL=%s | WEB=%s | SUMMARY=%s | ANALYSIS=%s",
        has_sql,
        has_rag,
        has_tool,
        has_web,
        has_summary,
        has_analysis
    )

    # ==========================================================
    # REPORT / PROFILE DETECTION
    # ==========================================================

    report_keywords = [

        "report",

        "profile",

        "dashboard",

        "analysis",

        "analyze",

        "compare",

        "recommend",

        "generate"

    ]

    if (

        any(

            keyword in question_lower

            for keyword in report_keywords

        )

        and

        has_employee

    ):

        elapsed = time.time() - start_time

        log_route(
            "orchestrator",
            elapsed
        )

        return {
            "route": "orchestrator"
        }
    # ==========================================================
    # SQL + RAG
    # ==========================================================

    if has_sql and has_rag:

       elapsed = time.time() - start_time

       log_route(
            "orchestrator",
            elapsed
        )

       return {
            "route": "orchestrator"
        }

    # ==========================================================
    # SQL + Analysis + Summary
    # ==========================================================

    if (

        has_analysis

        and

        (

            has_sql

            or

            has_employee

        )

    ):

        elapsed = time.time() - start_time

        log_route(
            "orchestrator",
            elapsed
        )

        return {

            "route": "orchestrator"

        }

    # ==========================================================
    # RAG + Summary
    # ==========================================================

    if has_rag and has_summary:

        elapsed = time.time() - start_time

        log_route(
            "orchestrator",
            elapsed
        )

        return {

            "route": "orchestrator"

        }

    # ==========================================================
    # SQL
    # ==========================================================

    if has_sql:

        elapsed = time.time() - start_time

        log_route(
            "sql",
            elapsed
        )

        return {
            "route": "sql"
        }

    # ==========================================================
    # RAG
    # ==========================================================

    if has_rag:

        elapsed = time.time() - start_time

        log_route(
            "rag",
            elapsed
        )

        return {

            "route": "rag"

        }

    # ==========================================================
    # TOOL
    # ==========================================================

    if has_tool:

        elapsed = time.time() - start_time

        log_route(
            "tool",
            elapsed
        )

        return {
            "route": "tool"
        }

    # ==========================================================
    # WEB SEARCH
    # ==========================================================

    if has_web:

        elapsed = time.time() - start_time

        log_route(
            "websearch",
            elapsed
        )

        return {
            "route": "websearch"
        }
    # ==========================================================
    # LLM FALLBACK
    # ==========================================================

    prompt = f"""
You are an Enterprise AI Router.

Your job is to select ONLY ONE route.

Conversation

{history}

Current Question

{question}

Available Routes

1. sql

Use for

- employee information
- salary
- attendance
- payroll
- finance
- leave balance
- projects

--------------------------------------------

2. rag

Use for

- company policy
- leave policy
- HR policy
- handbook
- PDF
- documents
- manuals

--------------------------------------------

3. orchestrator

Use when MULTIPLE agents are required.

Examples

- Compare Rahul and Aman salaries.
- Compare Rahul's leave balance with company leave policy.
- Generate Rahul's report and summarize it.
- Compare reimbursement with reimbursement policy.

--------------------------------------------

4. tool

Use for

- weather
- calculations
- currency conversion

--------------------------------------------

5. websearch

Use for

- latest news
- internet search
- current events

--------------------------------------------

6. reasoning

Use for

- greetings
- casual conversation
- follow-up questions
- general reasoning

--------------------------------------------

7. summary

Use ONLY when the user explicitly wants to summarize
already available content.

Return ONLY ONE route.

Never explain.

Never justify.

Never write JSON.

Return only one of

sql
rag
orchestrator
tool
websearch
reasoning
summary
"""
    
    logger.info("No rule-based match found.")
    logger.info("Invoking LLM Router...")

    response = llm.invoke(prompt)

    logger.info("LLM Router Response Received")
    logger.debug(
        "Raw Route Response : %s",
        response.content
    )

    route = response.content.strip().lower()

    match = re.search(
        r"\b(sql|rag|orchestrator|tool|websearch|reasoning|summary)\b",
        route
    )

    if match:

        route = match.group(1)

    else:

        route = "reasoning"

    logger.warning(
        "Unable to extract valid route. Falling back to reasoning."
    )

    elapsed = time.time() - start_time

    log_route(
        route,
        elapsed
    )

    logger.info("Router Agent Completed Successfully")
    logger.info("=" * 60)
    
    return {
        "route": route
    }