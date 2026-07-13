import time

from llms.grok_llm import llm
from utils.logger import logger


def websearch_agent(state):

    start_time = time.time()

    print("\n========== WEBSEARCH AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("WEBSEARCH AGENT")
    logger.info("Question : %s", state["question"])

    if state.get("chat_history"):
        logger.debug(
            "Chat History : %s",
            state.get("chat_history", [])
        )

    question = state["question"]

    history = "\n".join(
        state.get("chat_history", [])
    )

    prompt = f"""
Previous Conversation:
{history}

Current Question:
{question}

Answer directly and concisely.
"""

    try:

        logger.info("Generating response using LLM...")

        response = llm.invoke(prompt)

        logger.info("LLM response received.")

        answer = response.content.strip()

        logger.info(
            "Response Length : %d characters",
            len(answer)
        )

        logger.info(
            "WebSearch Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("WebSearch Agent Completed Successfully")
        logger.info("=" * 60)

        return {
            "answer": answer
        }

    except Exception:

        logger.exception("WebSearch Agent Failed")

        logger.info(
            "WebSearch Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise