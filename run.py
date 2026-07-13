import warnings
import time

warnings.filterwarnings("ignore")

from graph.workflow import app
from memory.chat_memory import chat_history

from utils.logger import logger
from utils.console_logger import (
    section,
    sub_section,
    info,
    success,
    error
)

# =====================================================
# Application Start
# =====================================================

section("🚀 INTELLIFLOW AI STARTED")

logger.info("Application Started Successfully")

request_count = 1

# =====================================================
# Main Loop
# =====================================================

while True:

    print()

    question = input("Ask Question : ").strip()

    if not question:
        continue

    if question.lower() in ["exit", "quit", "bye"]:

        section("👋 APPLICATION SHUTDOWN")

        success("IntelliFlow AI Stopped Successfully")

        logger.info("Application Shutdown Successfully")

        break

    start_time = time.time()

    logger.info("=" * 80)
    logger.info("Request %s Started", request_count)
    logger.info("Question : %s", question)

    sub_section("📝 User Question")

    info(question)

    try:

        response = app.invoke(
            {
                "question": question,
                "chat_history": chat_history
            }
        )

        answer = response.get(
            "answer",
            "No answer generated."
        )

        execution_time = time.time() - start_time

        chat_history.append(
            f"User : {question}"
        )

        chat_history.append(
            f"AI : {answer}"
        )

        section("✅ FINAL RESPONSE")

        print(answer)

        logger.info("Request Completed Successfully")
        logger.info("Execution Time : %.3f sec", execution_time)
        logger.info("Answer Length : %s", len(answer))
        logger.info("=" * 80)

        section("✅ REQUEST COMPLETED")

        info(
            f"Execution Time : {execution_time:.2f} sec"
        )

        request_count += 1

    except Exception as e:

        execution_time = time.time() - start_time

        logger.exception("Unhandled Exception")

        section("❌ ERROR")

        error(str(e))

        logger.info(
            "Execution Time : %.3f sec",
            execution_time
        )