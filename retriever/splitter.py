from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.logger import logger


def split_documents(documents):

    logger.info(
        "Document Splitting Started"
    )

    logger.info(
        "Input Documents : %d",
        len(documents)
    )

    try:

        splitter = RecursiveCharacterTextSplitter(

            chunk_size=1000,

            chunk_overlap=200

        )

        logger.info(
            "Chunk Size : %d | Chunk Overlap : %d",
            1000,
            200
        )

        chunks = splitter.split_documents(
            documents
        )

        logger.info(
            "Chunks Created : %d",
            len(chunks)
        )

        logger.info(
            "Document Splitting Completed Successfully"
        )

        return chunks

    except Exception:

        logger.exception(
            "Document Splitting Failed"
        )

        raise