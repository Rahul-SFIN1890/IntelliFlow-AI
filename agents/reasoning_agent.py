import time

from llms.grok_llm import llm
from utils.logger import logger


def reasoning_agent(state):

    start_time = time.time()

    print("\n========== REASONING AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("REASONING AGENT")
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
You are an intelligent conversational assistant.

Conversation History:
{history}

Current Question:
{question}

Instructions:
- Use conversation history when needed
- Answer contextually
- Handle follow-up questions correctly
- Be concise and accurate
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
            "Reasoning Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("Reasoning Agent Completed Successfully")
        logger.info("=" * 60)

        return {

            "answer": answer

        }

    except Exception:

        logger.exception("Reasoning Agent Failed")

        logger.info(
            "Reasoning Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise