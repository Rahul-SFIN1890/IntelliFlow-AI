from unittest import result
from utils.logger import logger
from sqlalchemy import create_engine
from sqlalchemy import text
import re

from llms.grok_llm import llm


class LeaveTool:

    def __init__(self):

        self.engine = create_engine(
            "sqlite:///database/company.db"
        )

        self.schema = """
Table Name : leave_balance

Columns

employee_id
name
paid_leave
casual_leave
sick_leave
remaining_leave
"""

    def run(
        self,
        question: str,
        history: str = ""
    ):
        logger.info("=" * 60)
        logger.info("Leave Tool Started")
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
Return ONLY the SQL statement.

Do NOT write:
- "Here is the SQL"
- "The SQL query is"
- "To answer your question"
- Explanations
- Markdown
- ```sql

The FIRST word of your response must be SELECT.
Never use

employees

finance

attendance

payroll

projects

Only use

leave_balance

Never retrieve information owned by another table.

Only answer questions for your own table.

If another table contains the requested information,
ignore it.

Generate SQL ONLY for your assigned table.

Examples

Question:
How many leaves does Rahul have?

SQL

SELECT remaining_leave
FROM leave_balance
WHERE name='Rahul';

--------------------------------

Question:
Show Rahul's paid leave.

SQL

SELECT paid_leave
FROM leave_balance
WHERE name='Rahul';

--------------------------------

Question:
Show Rahul's casual leave.

SQL

SELECT casual_leave
FROM leave_balance
WHERE name='Rahul';
"""

        logger.info("Generating SQL using LLM...")
        response = llm.invoke(prompt)
        logger.info("LLM response received.")
        logger.debug(f"Raw LLM Response:\n{response.content}")

        query = response.content

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
            logger.info("Leave Tool Completed Successfully")
            logger.info("=" * 60)

            return {

                "status": "success",

                "query": query,

                "columns": columns,

                "rows": rows

            }
        except Exception as e:

            logger.exception("Leave Tool execution failed.")
            logger.info("=" * 60)

            return {

                "status": "error",

                "query": query,

                "rows": [],

                "columns": [],

                "error": str(e)

            }