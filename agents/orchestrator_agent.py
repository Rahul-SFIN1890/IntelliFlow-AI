import json
import re
import time

from llms.grok_llm import llm
from utils.logger import logger

def extract_json(text: str):

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if match:

        try:

            return json.loads(match.group())

        except Exception:

            pass

    return {

        "plan": [

            "reasoning"

        ]

    }


def orchestrator_agent(state):

    start_time = time.time()

    print("\n========== ORCHESTRATOR AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("ORCHESTRATOR AGENT")
    logger.info("Question : %s", state["question"])

    if state.get("chat_history"):
        logger.debug(
            "Chat History : %s",
            state.get("chat_history", [])
        )

    question = state["question"]

    history = "\n".join(
        state.get(
            "chat_history",
            []
        )
    )


    prompt = f"""
You are an Enterprise AI Orchestrator.

Your ONLY responsibility is to decide which agents should execute.

You NEVER answer the user's question.

==================================================
AVAILABLE AGENTS
==================================================

1. sql

Use for

- employee information
- salary
- attendance
- finance
- payroll
- leave balance
- projects

--------------------------------------------------

2. rag

Use for

- HR policy
- company policy
- leave policy
- reimbursement policy
- insurance policy
- handbook
- manuals
- PDFs
- company documents

--------------------------------------------------

3. tool

Use for

- weather
- currency
- calculations
- utilities

--------------------------------------------------

4. websearch

Use for

- latest news
- internet search
- current information

--------------------------------------------------

5. reasoning

Use for

- greetings
- casual conversation
- general reasoning

--------------------------------------------------

6. analyst

Use when

- comparison
- report
- dashboard
- recommendation
- insights
- profile generation
- business analysis

--------------------------------------------------

7. writer

Always execute AFTER analyst.

The writer prepares the final report.

--------------------------------------------------

8. summary

Use ONLY when the user explicitly asks for

- summarize
- summary
- brief
- concise
- executive summary
- TLDR

Summary ALWAYS executes AFTER writer.

==================================================
EXECUTION RULES
==================================================

Rule 1

If SQL data alone is sufficient,

DO NOT use RAG.

Example

What is Rahul's salary?

Plan

{{
    "plan":[
        "sql",
        "writer"
    ]
}}

--------------------------------------------------

Rule 2

If company documents alone are sufficient,

DO NOT use SQL.

Example

What is the company leave policy?

Plan

{{
    "plan":[
        "rag",
        "writer"
    ]
}}

--------------------------------------------------

Rule 3

If both SQL data and company documents are required,

use BOTH SQL and RAG.

Example

Compare Rahul's leave balance with company leave policy.

Plan

{{
    "plan":[
        "sql",
        "rag",
        "analyst",
        "writer"
    ]
}}

--------------------------------------------------

Rule 4

If the user asks for comparison,
analysis,
profile,
report,
or recommendations,

always execute

analyst

before

writer.

--------------------------------------------------

Rule 5

If the user explicitly asks to summarize,

always execute

summary

AFTER

writer.

==================================================
EXAMPLES
==================================================

Question

Compare Rahul and Aman salaries.

Plan

{{
    "plan":[
        "sql",
        "analyst",
        "writer"
    ]
}}

--------------------------------------------------

Question

Generate Rahul's complete employee profile.

Plan

{{
    "plan":[
        "sql",
        "analyst",
        "writer"
    ]
}}

--------------------------------------------------

Question

Generate Rahul's report and summarize it.

Plan

{{
    "plan":[
        "sql",
        "analyst",
        "writer",
        "summary"
    ]
}}

--------------------------------------------------

Question

Summarize Leave Policy.pdf.

Plan

{{
    "plan":[
        "rag",
        "writer",
        "summary"
    ]
}}

--------------------------------------------------

Question

Compare Rahul's leave balance with company leave policy.

Plan

{{
    "plan":[
        "sql",
        "rag",
        "analyst",
        "writer"
    ]
}}

--------------------------------------------------

Question

Is Rahul eligible according to company leave policy?

Plan

{{
    "plan":[
        "sql",
        "rag",
        "analyst",
        "writer"
    ]
}}

--------------------------------------------------

Question

Explain reimbursement policy.

Plan

{{
    "plan":[
        "rag",
        "writer"
    ]
}}

--------------------------------------------------

Question

Show Rahul's attendance.

Plan

{{
    "plan":[
        "sql",
        "writer"
    ]
}}

--------------------------------------------------

Return ONLY valid JSON.

Never explain.

Never add markdown.

Never add comments.

Never add text before or after the JSON.

Conversation

{history}

Current Question

{question}
"""
    logger.info("Generating execution plan using LLM...")

    response = llm.invoke(prompt)

    logger.info("LLM response received.")

    raw_response = response.content.strip()

    logger.debug(
        "Raw Orchestrator Response:\n%s",
        raw_response
    )

    print("\n========== RAW ORCHESTRATOR RESPONSE ==========")
    print(raw_response)
    print("===============================================\n")

    plan = extract_json(raw_response)

    logger.info("Execution plan extracted successfully.")
    logger.debug("Execution Plan : %s", plan)

    # ==================================================
    # Validate Execution Plan
    # ==================================================

    valid_agents = {

        "sql",

        "rag",

        "tool",

        "websearch",

        "reasoning",

        "analyst",

        "writer",

        "summary"

    }

    execution_plan = []

    for agent in plan.get("plan", []):

        if agent in valid_agents:

            execution_plan.append(agent)

    if not execution_plan:

        logger.warning(
            "No valid execution plan found. Falling back to reasoning."
        )

        execution_plan = [

            "reasoning"

        ]
    # ==================================================
    # Remove Duplicate Agents
    # ==================================================

    execution_plan = list(
        dict.fromkeys(
            execution_plan
        )
    )

    logger.info(
        "Validated Execution Plan : %s",
        execution_plan
    )

    # ==================================================
    # Writer Ordering
    # ==================================================

    if "writer" in execution_plan:

        execution_plan.remove(
            "writer"
        )

        execution_plan.append(
            "writer"
        )

    # ==================================================
    # Summary Ordering
    # ==================================================

    if "summary" in execution_plan:

        execution_plan.remove(
            "summary"
        )

        execution_plan.append(
            "summary"
        )

    print("\n========== EXECUTION PLAN ==========")
    print(execution_plan)
    print("====================================\n")

    logger.info(
        "Orchestrator Execution Time : %.3f sec",
        time.time() - start_time
    )

    logger.info("Orchestrator Agent Completed Successfully")
    logger.info("=" * 60)

    return {

        "execution_plan": execution_plan,

        "answer": ""

    }