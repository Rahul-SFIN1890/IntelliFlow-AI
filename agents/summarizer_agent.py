import time

from llms.grok_llm import llm

from prompts.summary_prompt import (
    SUMMARY_PROMPT
)

from utils.logger import logger


def summarizer_agent(state):

    start_time = time.time()

    print("\n========== SUMMARY AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("SUMMARY AGENT")
    logger.info("Question : %s", state["question"])

    report = state.get(
        "content",
        ""
    )

    logger.debug(
        "Report Length : %d characters",
        len(report)
    )

    prompt = SUMMARY_PROMPT.format(

        question=state["question"],

        report=report

    )

    try:

        logger.info("Generating summary using LLM...")

        response = llm.invoke(prompt)

        logger.info("LLM response received.")

        summary = response.content.strip()

        logger.info(
            "Summary Length : %d characters",
            len(summary)
        )

        logger.info(
            "Summary Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("Summary Agent Completed Successfully")
        logger.info("=" * 60)

        return {

            "summary": summary

        }

    except Exception:

        logger.exception("Summary Agent Failed")

        logger.info(
            "Summary Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise