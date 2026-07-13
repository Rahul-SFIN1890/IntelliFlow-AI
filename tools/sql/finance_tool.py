import re

from sqlalchemy import create_engine
from sqlalchemy import text

from llms.grok_llm import llm
from utils.logger import logger


class FinanceTool:

    def __init__(self):

        self.engine = create_engine(
            "sqlite:///database/company.db"
        )

        self.schema = """
Table Name : finance

Columns

employee_id
name
bonus
tax
reimbursement
loan
incentive
"""

    def run(
        self,
        question: str,
        history: str = ""
    ):

        logger.info("=" * 60)
        logger.info("Finance Tool Started")
        logger.info(f"Question: {question}")

        if history:
            logger.debug(f"Conversation History: {history}")

        prompt = f"""
You are an Enterprise SQLite Expert.

You are ONLY allowed to use the following table.

{self.schema}

Previous Conversation

{history}

Question

{question}

IMPORTANT RULES

1. Return ONLY SQLite query.
2. Never return markdown.
3. Never return explanation.
4. Never return ```sql.
5. Never use any table except finance.
6. There is NO table called salary.
7. There is NO table called employee.
8. There is NO table called finance_data.
9. Always use finance table.
10. The finance table DOES NOT contain salary.

11. Never generate:

SELECT salary
FROM finance

12. Salary exists ONLY in the employees table.

13. The finance table contains ONLY:

bonus
tax
loan
reimbursement
incentive

Never answer

- employee questions
- attendance questions
- payroll questions
- leave questions
- project questions

Never retrieve information owned by another table.

Only answer questions for your own table.

If another table contains the requested information,
ignore it.

Generate SQL ONLY for your assigned table.

14. Generate exactly ONE SQL statement.

15. Never generate multiple SELECT statements.

16. If multiple finance fields are requested,
retrieve them in a SINGLE SELECT.

17. Prefer

SELECT *
FROM finance

or

SELECT bonus, tax, reimbursement, loan, incentive
FROM finance

instead of multiple queries.

Examples

Question:
Generate Rahul's complete finance profile.

SQL

SELECT
    bonus,
    tax,
    reimbursement,
    loan,
    incentive
FROM finance
WHERE name='Rahul';

--------------------------------

Question:
Generate Rahul's complete employee profile.

SQL

SELECT
    bonus,
    tax,
    reimbursement,
    loan,
    incentive
FROM finance
WHERE name='Rahul';

--------------------------------

Question:
Show Rahul's finance details.

SQL

SELECT
    bonus,
    tax,
    reimbursement,
    loan,
    incentive
FROM finance
WHERE name='Rahul';

--------------------------------

Question:
What is Rahul's bonus?

SQL

SELECT bonus
FROM finance
WHERE name='Rahul';

--------------------------------

Question:
What is Rahul's tax?

SQL

SELECT tax
FROM finance
WHERE name='Rahul';
"""

        logger.info("Generating SQL using LLM...")

        response = llm.invoke(prompt)

        logger.info("LLM response received.")
        logger.debug(f"Raw LLM Response:\n{response.content}")

        query = response.content.strip()

        query = query.replace("```sql", "")
        query = query.replace("```", "")
        query = query.strip()

        match = re.search(
            r"(SELECT[\s\S]*?;)",
            query,
            re.IGNORECASE
        )

        if match:
            query = match.group(1).strip()
        else:
            query = query.strip()

        logger.info(f"Extracted SQL: {query}")

        logger.info("Validating generated SQL...")

        if not query.upper().startswith("SELECT"):

            logger.error("Invalid SQL generated. Expected SELECT statement.")

            return {

                "status": "error",

                "query": query,

                "columns": [],

                "rows": [],

                "error": "Invalid SQL generated. Expected a SELECT statement."

            }

        logger.info("SQL validation successful.")

        try:

            logger.info("Executing SQL query...")

            with self.engine.connect() as conn:

                result = conn.execute(
                    text(query)
                )

                rows = result.fetchall()

                columns = list(result.keys())

            logger.info(f"Query executed successfully. Rows returned: {len(rows)}")
            logger.info("Finance Tool Completed Successfully")
            logger.info("=" * 60)

            return {

                "status": "success",

                "query": query,

                "columns": columns,

                "rows": rows

            }

        except Exception as e:

            logger.exception("Finance Tool execution failed.")
            logger.info("=" * 60)

            return {

                "status": "error",

                "query": query,

                "rows": [],

                "columns": [],

                "error": str(e)

            }