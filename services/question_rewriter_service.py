from agents.question_rewriter_agent import (
    question_rewriter_agent
)


class QuestionRewriterService:

    def execute(

        self,

        question: str,

        history: str

    ):

        state = {

            "question": question,

            "history": history

        }

        response = question_rewriter_agent(
            state
        )

        return response