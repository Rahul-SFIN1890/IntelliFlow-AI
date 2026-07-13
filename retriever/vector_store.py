from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

from utils.logger import logger


def create_vectorstore(chunks):

    logger.info("=" * 60)
    logger.info("VECTOR STORE")
    logger.info("Creating Vector Store...")

    try:

        logger.info(
            "Loading Embedding Model..."
        )

        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        logger.info(
            "Embedding Model Loaded Successfully"
        )

        logger.info(
            "Embedding Model : sentence-transformers/all-MiniLM-L6-v2"
        )

        logger.info(
            "Creating Chroma Vector Store..."
        )

        vectorstore = Chroma.from_documents(

            documents=chunks,

            embedding=embedding,

            persist_directory="vector_db"

        )

        logger.info(
            "Vector Store Created Successfully"
        )

        logger.info(
            "Chunks Indexed : %d",
            len(chunks)
        )

        logger.info("=" * 60)

        return vectorstore

    except Exception:

        logger.exception(
            "Vector Store Creation Failed"
        )

        logger.info("=" * 60)

        raise