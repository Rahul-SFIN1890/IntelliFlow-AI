from retriever.loader import load_documents
from retriever.splitter import split_documents
from retriever.vector_store import create_vectorstore

from utils.logger import logger


def get_retriever(folder_path):

    logger.info("=" * 60)
    logger.info("RETRIEVER INITIALIZATION")
    logger.info("Folder Path : %s", folder_path)

    try:

        logger.info(
            "Loading Documents..."
        )

        docs = load_documents(folder_path)

        logger.info(
            "Documents Loaded : %d",
            len(docs)
        )

        logger.info(
            "Splitting Documents..."
        )

        chunks = split_documents(docs)

        logger.info(
            "Chunks Created : %d",
            len(chunks)
        )

        logger.info(
            "Creating Vector Store..."
        )

        vectorstore = create_vectorstore(chunks)

        logger.info(
            "Vector Store Ready"
        )

        logger.info(
            "Creating Retriever..."
        )

        retriever = vectorstore.as_retriever(

            search_kwargs={

                "k": 5

            }

        )

        logger.info(
            "Retriever Created Successfully"
        )

        logger.info(
            "Search Top K : %d",
            5
        )

        logger.info("=" * 60)

        return retriever

    except Exception:

        logger.exception(
            "Retriever Initialization Failed"
        )

        logger.info("=" * 60)

        raise