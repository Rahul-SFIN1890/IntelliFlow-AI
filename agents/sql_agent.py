import time

from services.sql_service import SQLService
from utils.logger import logger

service = SQLService()


def sql_agent(state):

    start_time = time.time()

    print("\n========== SQL AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("SQL AGENT")
    logger.info("Question : %s", state["question"])

    if state.get("chat_history"):
        logger.debug(
            "Chat History : %s",
            state.get("chat_history", [])
        )

    logger.info("Executing SQL Service...")

    try:

        response = service.execute(
            state["question"],
            "\n".join(
                state.get("chat_history", [])
            )
        )

        logger.info("SQL Service Execution Completed")

        logger.info(
            "SQL Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("SQL Agent Completed Successfully")
        logger.info("=" * 60)

        return response

    except Exception:

        logger.exception("SQL Agent Failed")

        logger.info(
            "SQL Agent Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise