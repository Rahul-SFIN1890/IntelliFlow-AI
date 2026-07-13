from agents.question_rewriter_agent import question_rewriter_agent

history = """
User:
What is Rahul's salary?

Assistant:
Rahul's salary is 72688.
"""

state = {

    "question": "Compare it with his department's highest salary.",

    "history": history

}

print(

    question_rewriter_agent(state)

)