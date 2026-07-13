import os

from langchain_community.document_loaders import PyPDFLoader

from utils.logger import logger


def load_documents(folder_path):

    logger.info(
        "Loading documents from : %s",
        folder_path
    )

    documents = []

    try:

        for file in os.listdir(folder_path):

            if file.endswith(".pdf"):

                logger.info(
                    "Loading PDF : %s",
                    file
                )

                pdf_path = os.path.join(
                    folder_path,
                    file
                )

                loader = PyPDFLoader(
                    pdf_path
                )

                loaded_docs = loader.load()

                logger.info(
                    "Loaded %d pages from %s",
                    len(loaded_docs),
                    file
                )

                documents.extend(
                    loaded_docs
                )

        logger.info(
            "Total Documents Loaded : %d",
            len(documents)
        )

        return documents

    except Exception:

        logger.exception(
            "Document Loading Failed"
        )

        raise