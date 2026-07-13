import time

from llms.grok_llm import llm

from prompts.question_rewriter_prompt import (
    QUESTION_REWRITER_PROMPT
)

from utils.logger import logger


def question_rewriter_agent(state):

    start_time = time.time()

    print("\n========== QUESTION REWRITER ==========\n")

    logger.info("=" * 60)
    logger.info("QUESTION REWRITER AGENT")
    logger.info("Question : %s", state["question"])

    question = state["question"]

    history = state.get(
        "history",
        ""
    )

    try:

        logger.info("Rewriting question using LLM...")

        prompt = QUESTION_REWRITER_PROMPT.format(

            history=history,

            question=question

        )

        response = llm.invoke(
            prompt
        )

        logger.info("LLM response received.")

        rewritten_question = response.content.strip()

        logger.info(
            "Rewritten Question Length : %d characters",
            len(rewritten_question)
        )

        print("\n========== QUESTION REWRITER ==========")
        print("Original Question :")
        print(question)
        print()
        print("Rewritten Question :")
        print(rewritten_question)
        print("=======================================\n")

        logger.info(
            "Question Rewriter Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("Question Rewriter Completed Successfully")
        logger.info("=" * 60)

        return {

            "rewritten_question": rewritten_question

        }

    except Exception:

        logger.exception("Question Rewriter Failed")

        logger.info(
            "Question Rewriter Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise