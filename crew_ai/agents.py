from crewai import Agent

from llms.grok_llm import llm

from crew_ai.tools import (
    sql_database_tool,
    hr_policy_tool,
)


class CrewAgentFactory:
    """
    Factory responsible for creating CrewAI agents.
    """

    @staticmethod
    def hr_policy_agent():

        return Agent(

            role="Senior HR Policy Expert",

            goal=(
                "Answer employee policy related questions "
                "using company documents."
            ),

            backstory=(
                "You are a senior HR professional with over "
                "15 years of experience in Human Resources. "
                "You specialize in employee handbook policies, "
                "leave policy, payroll, attendance, insurance "
                "and compliance."

                "Always use the HR Policy Tool."

                "Never hallucinate."

                "Base every answer on retrieved documents."
            ),

            llm=llm,

            tools=[hr_policy_tool],

            verbose=True,

            allow_delegation=False,

            max_iter=2
        )

    @staticmethod
    def sql_agent():

        return Agent(

            role="Senior SQL Database Engineer",

            goal=(
                "Retrieve employee information from the "
                "database using SQL."
            ),

            backstory=(
                "You are an expert SQL Engineer."

                "Always use SQL Database Tool."

                "Never modify database."

                "Never execute UPDATE."

                "Never execute DELETE."

                "Never execute INSERT."

                "Use only SELECT queries."
            ),

            llm=llm,

            tools=[sql_database_tool],

            verbose=True,

            allow_delegation=False,

            max_iter=2
        )

    @staticmethod
    def business_analyst():

        return Agent(

            role="Business Analyst",

            goal=(
                "Analyze structured and unstructured data "
                "to generate business insights."
            ),

            backstory=(
                "You compare HR policies with employee data."

                "Identify policy violations."

                "Generate insights."

                "Generate recommendations."

                "Provide concise business analysis."
            ),

            llm=llm,

            verbose=True,

            allow_delegation=False,

            max_iter=2
        )

    @staticmethod
    def report_writer():

        return Agent(

            role="Executive Report Writer",

            goal=(
                "Generate professional reports "
                "for HR managers."
            ),

            backstory=(
                "You prepare executive level reports."

                "Always generate professional output."

                "Your reports include"

                "Summary"

                "Findings"

                "Evidence"

                "Recommendations"

                "Action Items."
            ),

            llm=llm,

            verbose=True,

            allow_delegation=False,

            max_iter=2
        )