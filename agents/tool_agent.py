import time

from tools.search_tool import (
    search_tool
)

from tools.calculator_tool import (
    calculator_tool
)

from prompts.tool_prompt import (
    TOOL_PROMPT
)

from llms.grok_llm import llm
from utils.logger import logger


def tool_agent(state):

    start_time = time.time()

    print("\n========== TOOL AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("TOOL AGENT")
    logger.info("Question : %s", state["question"])

    question = state["question"].lower()

    math_keywords = [
        "+", "-", "*", "/", "%",
        "calculate",
        "multiply",
        "divide",
        "add",
        "subtract"
    ]

    try:

        # -----------------------------
        # CALCULATOR TOOL
        # -----------------------------
        if any(word in question for word in math_keywords):

            print("CALCULATOR TOOL SELECTED")

            logger.info("Selected Tool : Calculator")

            output = calculator_tool.invoke(question)

            logger.info("Calculator execution completed.")

            logger.info(
                "Tool Agent Execution Time : %.3f sec",
                time.time() - start_time
            )

            logger.info("Tool Agent Completed Successfully")
            logger.info("=" * 60)

            return {
                "tool_output": str(output),
                "answer": str(output)
            }

        # -----------------------------
        # SEARCH TOOL
        # -----------------------------
        else:

            print("SEARCH TOOL SELECTED")

            logger.info("Selected Tool : Search")

            output = search_tool.invoke(question)

            logger.info("Search Tool execution completed.")

            final_prompt = TOOL_PROMPT.format(
                question=question,
                tool_results=output
            )

            logger.info("Generating final response using LLM...")

            response = llm.invoke(final_prompt)

            logger.info("LLM response received.")

            final_answer = response.content

            logger.info(
                "Response Length : %d characters",
                len(final_answer)
            )

            logger.info(
                "Tool Agent Execution Time : %.3f sec",
                time.time() - start_time
            )

            logger.info("Tool Agent Completed Successfully")
            logger.info("=" * 60)

            return {
                "tool_output": str(output),
                "answer": final_answer
            }

    except Exception:

        logger.exception("Tool Agent Failed")

        logger.info(
            "Tool Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise