import time

from llms.grok_llm import llm
from utils.logger import logger


def writer_agent(state):

    start_time = time.time()

    print("\n========== WRITER AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("WRITER AGENT")
    logger.info("Question : %s", state["question"])

    analysis = state.get(
        "analysis",
        ""
    )

    logger.debug(
        "Analysis Length : %d characters",
        len(analysis)
    )

    prompt = f"""
You are a Professional Enterprise HR Report Writer.

Your ONLY responsibility is to convert the analysis
into a professional business report.

You NEVER invent information.

==================================================
USER QUESTION
==================================================

{state["question"]}

==================================================
ANALYSIS
==================================================

{analysis}

==================================================
INSTRUCTIONS
==================================================

1. Use ONLY the provided analysis.

2. Never invent facts.

3. Never change numerical values.

4. Never assume missing information.

5. Never mention

- SQL
- Database
- RAG
- AI
- LLM
- Agents
- Internal implementation

6. Remove duplicate information.

7. Never repeat the same section.

8. Use professional HR formatting.

9. Use Markdown headings.

10. Use bullet points whenever appropriate.

11. If the user asked for

- comparison

highlight only the important differences.

12. If the user asked for

- report

produce a professional report.

13. If the user asked for

- profile

produce a complete employee profile.

14. If the user asked for

- summary

keep the report concise.

15. Never recommend actions.

16. Never speculate.

17. Never create empty headings.

18. Return ONLY the final report.

==================================================
OUTPUT FORMAT
==================================================

# Title

## Section

• Item

## Section

• Item

==================================================
FINAL REPORT
==================================================
"""

    try:

        logger.info("Generating final report using LLM...")

        response = llm.invoke(prompt)

        logger.info("LLM response received.")

        final_response = response.content.strip()

        logger.info(
            "Final Response Length : %d characters",
            len(final_response)
        )

        logger.info(
            "Writer Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("Writer Agent Completed Successfully")
        logger.info("=" * 60)

        return {

            "final_response": final_response

        }

    except Exception:

        logger.exception("Writer Agent Failed")

        logger.info(
            "Writer Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise