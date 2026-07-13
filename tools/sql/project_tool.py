import re

from sqlalchemy import create_engine
from sqlalchemy import text

from llms.grok_llm import llm
from utils.logger import logger


class ProjectTool:

    def __init__(self):

        self.engine = create_engine(
            "sqlite:///database/company.db"
        )

        self.schema = """
Table Name : projects

Columns

employee_id
name
project_name
project_status
client
rating
"""

    def run(
        self,
        question: str,
        history: str = ""
    ):

        logger.info("=" * 60)
        logger.info("Project Tool Started")
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

IMPORTANT

Return ONLY SQLite query.

Never use

employees

finance

attendance

payroll

leave_balance

Only use

projects

Never retrieve information owned by another table.

Only answer questions for your own table.

If another table contains the requested information,
ignore it.

Generate SQL ONLY for your assigned table.

Examples

Question:
Which project is Rahul working on?

SQL

SELECT project_name
FROM projects
WHERE name='Rahul';

--------------------------------

Question:
Show Rahul's project status.

SQL

SELECT project_status
FROM projects
WHERE name='Rahul';

--------------------------------

Question:
Who is Rahul's client?

SQL

SELECT client
FROM projects
WHERE name='Rahul';

--------------------------------

Question:
What is Rahul's project rating?

SQL

SELECT rating
FROM projects
WHERE name='Rahul';

IMPORTANT

Return ONLY a SQLite query.

Never explain.

Never think aloud.

Never say "Here is the SQL query".

Never say "To retrieve...".

Never write English sentences.

Never return markdown.

Never return ```sql.

Return ONLY the SQL query.

Correct Example

SELECT *
FROM projects
WHERE name='Rahul';

Wrong Example

To retrieve Rahul's project details...

SELECT *
FROM projects
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
            logger.info("Project Tool Completed Successfully")
            logger.info("=" * 60)

            return {

                "status": "success",

                "query": query,

                "columns": columns,

                "rows": rows

            }

        except Exception as e:

            logger.exception("Project Tool execution failed.")
            logger.info("=" * 60)

            return {

                "status": "error",

                "query": query,

                "rows": [],

                "columns": [],

                "error": str(e)

            }