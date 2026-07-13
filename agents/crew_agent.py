from crew_ai.crew import CrewBuilder


def crew_agent(state):
    """
    LangGraph node responsible for executing CrewAI workflows.
    """

    print("\nCREW AI AGENT EXECUTED\n")

    question = state["question"]

    workflow = state.get(
        "crew_workflow",
        "analysis"
    )

    try:

        crew = CrewBuilder.build(
            workflow=workflow,
            question=question
        )

        response = crew.kickoff()

        answer = str(response)

    except Exception as e:

        answer = f"CrewAI Error : {str(e)}"

    return {
        "answer": answer
    }