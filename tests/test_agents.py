from agents.analyst_agent import analyst_agent
from agents.writer_agent import writer_agent


sample = {

    "question": "Compare Rahul salary with leave policy",

    "results": {

        "sql": "Rahul Salary = 8 LPA",

        "rag": "Leave Policy = 18 Paid Leaves"

    }

}

print(

    analyst_agent(sample)

)

print()

print(

    writer_agent(sample)

)