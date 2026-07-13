from crewai import Crew
from crewai import Process

from crew_ai.tasks import CrewTaskFactory


class CrewBuilder:

    @staticmethod
    def build(workflow: str, question: str):

        workflow = workflow.lower()

        if workflow == "policy":

            tasks = [

                CrewTaskFactory.hr_policy_task(question),

                CrewTaskFactory.report_task(question)

            ]

        elif workflow == "sql":

            tasks = [

                CrewTaskFactory.sql_task(question),

                CrewTaskFactory.report_task(question)

            ]

        elif workflow == "analysis":

            tasks = [

                CrewTaskFactory.hr_policy_task(question),

                CrewTaskFactory.sql_task(question),

                CrewTaskFactory.analysis_task(question),

                CrewTaskFactory.report_task(question)

            ]

        else:

            raise ValueError(
                f"Unsupported workflow : {workflow}"
            )

        crew = Crew(

            agents=[task.agent for task in tasks],

            tasks=tasks,

            process=Process.sequential,

            verbose=True

        )

        return crew