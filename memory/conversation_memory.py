from collections import deque

from utils.logger import logger


class ConversationMemory:

    def __init__(

        self,

        max_history=10

    ):

        self.history = deque(

            maxlen=max_history

        )

        logger.info(
            "Conversation Memory Initialized (Max History : %d)",
            max_history
        )

    def add_user_message(

        self,

        message: str

    ):

        self.history.append(

            {

                "role": "user",

                "content": message

            }

        )

        logger.info(
            "User message added to memory."
        )

        logger.debug(
            "Current Memory Size : %d",
            len(self.history)
        )

    def add_assistant_message(

        self,

        message: str

    ):

        self.history.append(

            {

                "role": "assistant",

                "content": message

            }

        )

        logger.info(
            "Assistant message added to memory."
        )

        logger.debug(
            "Current Memory Size : %d",
            len(self.history)
        )

    def get_history(self):

        logger.debug(

            "Conversation History Requested (Messages : %d)",

            len(self.history)

        )

        return list(

            self.history

        )

    def get_history_text(self):

        conversation = []

        for item in self.history:

            conversation.append(

                f"{item['role'].title()}: {item['content']}"

            )

        logger.debug(

            "Conversation History Text Generated"

        )

        return "\n".join(

            conversation

        )

    def clear(self):

        self.history.clear()

        logger.info(

            "Conversation Memory Cleared"

        )