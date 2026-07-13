from agents.planner_agent import planner_agent


class PlannerService:

    def execute(
        self,
        question: str
    ):

        return planner_agent(
            question
        )