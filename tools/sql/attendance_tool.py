import re

from sqlalchemy import create_engine
from sqlalchemy import text

from llms.grok_llm import llm
from utils.logger import logger


class AttendanceTool:

    def __init__(self):

        self.engine = create_engine(
            "sqlite:///database/company.db"
        )

        self.schema = """
Table Name : attendance

Columns

employee_id
name
present_days
absent_days
work_from_home
"""

    def run(
        self,
        question: str,
        history: str = ""
    ):

        logger.info("=" * 60)
        logger.info("Attendance Tool Started")
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
5. Never use any table except attendance.
6. There is NO table called employee_attendance.
7. Always use attendance table.

Never answer

- employee questions
- finance questions
- payroll questions
- leave questions
- project questions

Never retrieve information owned by another table.

Only answer questions for your own table.

If another table contains the requested information,
ignore it.

Generate SQL ONLY for your assigned table.

Examples

Question:
Show Rahul's attendance.

SQL

SELECT *
FROM attendance
WHERE name='Rahul';

--------------------------------

Question:
How many days was Rahul present?

SQL

SELECT present_days
FROM attendance
WHERE name='Rahul';

--------------------------------

Question:
How many days was Rahul absent?

SQL

SELECT absent_days
FROM attendance
WHERE name='Rahul';

--------------------------------

Question:
How many work from home days did Rahul have?

SQL

SELECT work_from_home
FROM attendance
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
            logger.info("Attendance Tool Completed Successfully")
            logger.info("=" * 60)

            return {

                "status": "success",

                "query": query,

                "columns": columns,

                "rows": rows

            }

        except Exception as e:

            logger.exception("Attendance Tool execution failed.")
            logger.info("=" * 60)

            return {

                "status": "error",

                "query": query,

                "rows": [],

                "columns": [],

                "error": str(e)

            }