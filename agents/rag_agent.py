import time

from retriever.retriever import (
    get_retriever
)

from llms.grok_llm import llm

from prompts.rag_prompt import (
    RAG_PROMPT
)

from utils.logger import logger

retriever = get_retriever(
    "data/company_docs"
)


def rag_agent(state):

    start_time = time.time()

    print("\n========== RAG AGENT ==========\n")

    logger.info("=" * 60)
    logger.info("RAG AGENT")
    logger.info("Question : %s", state["question"])

    if state.get("chat_history"):
        logger.debug(
            "Chat History : %s",
            state.get("chat_history", [])
        )

    try:

        question = state["question"]

        history = "\n".join(
            state.get("chat_history", [])
        )

        logger.info("Retrieving relevant documents...")

        docs = retriever.get_relevant_documents(
            question
        )

        logger.info(
            "Documents Retrieved : %d",
            len(docs)
        )

        context = "\n".join(
            [doc.page_content for doc in docs]
        )

        logger.debug(
            "Context Length : %d characters",
            len(context)
        )

        logger.info("Generating response using LLM...")

        response = llm.invoke(
            RAG_PROMPT.format(
                history=history,
                context=context,
                question=question
            )
        )

        logger.info("LLM response received.")

        logger.info(
            "RAG Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("RAG Agent Completed Successfully")
        logger.info("=" * 60)

        return {

            "documents": context,

            "answer": response.content

        }

    except Exception:

        logger.exception("RAG Agent Failed")

        logger.info(
            "RAG Execution Time : %.3f sec",
            time.time() - start_time
        )

        logger.info("=" * 60)

        raise