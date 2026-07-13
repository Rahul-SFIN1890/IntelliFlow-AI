from crewai import Task

from crew_ai.agents import CrewAgentFactory


class CrewTaskFactory:

    @staticmethod
    def hr_policy_task(question: str):

        return Task(

            description=f"""
            Answer the following HR policy question.

            Question:
            {question}

            Use only the HR Policy Tool.

            If the answer is unavailable,
            clearly mention it.
            """,

            expected_output="""
            Accurate HR policy answer
            with supporting explanation.
            """,

            agent=CrewAgentFactory.hr_policy_agent()
        )

    @staticmethod
    def sql_task(question: str):

        return Task(

            description=f"""
            Retrieve employee information
            from database.

            User Question:

            {question}

            Always use SQL Database Tool.
            """,

            expected_output="""
            Employee data
            retrieved from SQL.
            """,

            agent=CrewAgentFactory.sql_agent()
        )

    @staticmethod
    def analysis_task(question: str):

        return Task(

            description=f"""
            Analyze all available
            information.

            User Question:

            {question}

            Compare structured
            and unstructured data.

            Generate insights.
            """,

            expected_output="""
            Business insights
            and recommendations.
            """,

            agent=CrewAgentFactory.business_analyst()
        )

    @staticmethod
    def report_task(question: str):

        return Task(

            description=f"""
            Prepare a professional report
            for the HR manager.

            User Question:

            {question}
            """,

            expected_output="""
            Executive report
            including

            Summary

            Findings

            Recommendations

            Action Items
            """,

            agent=CrewAgentFactory.report_writer()
        )