import time

from execution.execution_engine import ExecutionEngine
from utils.logger import logger


def execution_agent(state):

    start_time = time.time()

    print("\n========== EXECUTION AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("EXECUTION AGENT")

    logger.info(
        "Execution Plan : %s",
        state["execution_plan"]
    )

    try:

        logger.info("Executing Execution Engine...")

        response = ExecutionEngine.execute(

            plan=state["execution_plan"],

            state=state

        )

        logger.info("Execution Engine Completed")

        logger.info(
            "Execution Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("Execution Agent Completed Successfully")
        logger.info("=" * 60)

        return response

    except Exception:

        logger.exception("Execution Agent Failed")

        logger.info(
            "Execution Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise