import time

from llms.grok_llm import llm
from utils.logger import logger


def analyst_agent(state):

    start_time = time.time()

    print("\n========== ANALYST AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("ANALYST AGENT")
    logger.info("Question : %s", state["question"])

    sql_results = state.get(
        "sql",
        {}
    )

    rag_results = state.get(
        "rag",
        ""
    )

    logger.debug(
        "SQL Result Length : %d characters",
        len(str(sql_results))
    )

    logger.debug(
        "RAG Result Length : %d characters",
        len(str(rag_results))
    )

    prompt = f"""
You are a Senior Enterprise HR Business Analyst.

Your ONLY responsibility is to analyze the provided information.

You NEVER generate the final response.

==================================================
USER QUESTION
==================================================

{state["question"]}

==================================================
STRUCTURED SQL DATA
==================================================

{sql_results}

==================================================
RAG KNOWLEDGE
==================================================

{rag_results}

==================================================
YOUR RESPONSIBILITIES
==================================================

1. Analyze ONLY the provided information.

2. Never invent facts.

3. Never guess missing values.

4. Never assume information.

5. Never mention

- SQL
- Database
- Tables
- AI
- LLM
- RAG
- Agents
- Internal implementation

6. Preserve every numerical value exactly.

7. Use ONLY information available.

8. Ignore empty sections.

9. If SQL and RAG are both available,
combine them naturally.

10. If SQL contradicts RAG,
explicitly mention the inconsistency.

11. If the question asks for

- comparison

highlight ONLY the important differences.

12. If the question asks for

- report

organize information professionally.

13. If the question asks for

- profile

organize into logical HR sections.

14. If the question asks for

- summary

focus only on key highlights.

15. Never recommend actions.

16. Never speculate.

17. Never create fake information.

18. Never mention unavailable sections.

19. Return ONLY analysis.

==================================================
OUTPUT STYLE
==================================================

Use professional headings.

Use bullet points whenever appropriate.

Keep the analysis concise.

Highlight only important insights supported by data.

==================================================
ANALYSIS
==================================================
"""

    try:

        logger.info("Generating analysis using LLM...")

        response = llm.invoke(prompt)

        logger.info("LLM response received.")

        analysis = response.content.strip()

        logger.info(
            "Analysis Length : %d characters",
            len(analysis)
        )

        logger.info(
            "Analyst Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("Analyst Agent Completed Successfully")
        logger.info("=" * 60)

        return {

            "analysis": analysis

        }

    except Exception:

        logger.exception("Analyst Agent Failed")

        logger.info(
            "Analyst Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise