import logging
import re

from sqlalchemy import create_engine
from sqlalchemy import text

from llms.grok_llm import llm

logger = logging.getLogger(__name__)


class EmployeeTool:

    def __init__(self):

        self.engine = create_engine(
            "sqlite:///database/company.db"
        )

        self.schema = """
Table Name : employees

Columns

employee_id
name
department
designation
experience
salary
city
"""

    def run(
        self,
        question: str,
        history: str = ""
    ):

        logger.info("=" * 60)
        logger.info("Employee Tool Started")
        logger.info(f"Question: {question}")

        if history:
            logger.debug(f"Conversation History: {history}")

        prompt = f"""
You are an Enterprise Employee SQL Generator.

Your responsibility is to generate ONLY valid SQLite SQL queries
for the employees table.

====================================================
DATABASE SCHEMA
====================================================

employees(

employee_id,
name,
department,
designation,
experience,
salary,
city

)

====================================================
TABLE OWNERSHIP
====================================================

You own ONLY the employees table.

Never use

finance
attendance
payroll
leave_balance
projects

Never join with another table.

====================================================
QUESTION
====================================================

{question}

====================================================
PREVIOUS CONVERSATION
====================================================

{history}

====================================================
RULES
====================================================

1. Return EXACTLY ONE valid SQLite SQL query.

2. The first word of your response MUST be SELECT.

3. The response MUST end with a semicolon (;).

4. Never explain the SQL.

5. Never think aloud.

6. Never say:

- Here is the SQL query
- To answer your question
- This query will
- I will use
- The following SQL
- SQL Query

7. Never return markdown.

8. Never return ```sql.

9. Never return comments.

10. Never return English sentences.

11. Never generate multiple SELECT statements.

12. Never use another table.

13. Never use JOIN.

14. Never use UNION unless explicitly requested.

15. Never use EXCEPT.

16. Never use INTERSECT.

17. Use SQLite syntax only.

18. If ONE employee is requested

Use

WHERE name='EmployeeName'

19. If MULTIPLE employees are requested

Use

WHERE name IN ('Rahul','Aman')

20. If comparison is requested

Always include the name column.

21. If the user asks for

- employee profile
- employee details
- employee report
- HR profile
- complete employee profile
- complete employee details

return every employee column.

22. Use SELECT * ONLY when the user explicitly requests the complete employee profile.

23. Otherwise retrieve ONLY the required columns.

24. Always generate EXACTLY ONE SQL statement.

====================================================
QUERY PATTERNS
====================================================

Question

What is Rahul's salary?

SQL

SELECT salary
FROM employees
WHERE name='Rahul';

--------------------------------------------

Question

Which department does Rahul work in?

SQL

SELECT department
FROM employees
WHERE name='Rahul';

--------------------------------------------

Question

What is Rahul's designation?

SQL

SELECT designation
FROM employees
WHERE name='Rahul';

--------------------------------------------

Question

How much experience does Rahul have?

SQL

SELECT experience
FROM employees
WHERE name='Rahul';

--------------------------------------------

Question

Which city does Rahul belong to?

SQL

SELECT city
FROM employees
WHERE name='Rahul';

--------------------------------------------

Question

Show Rahul's employee details.

SQL

SELECT
name,
department,
designation,
experience,
salary,
city
FROM employees
WHERE name='Rahul';

--------------------------------------------

Question

Generate Rahul's employee report.

SQL

SELECT *
FROM employees
WHERE name='Rahul';

--------------------------------------------

Question

Generate Rahul's complete employee profile.

SQL

SELECT *
FROM employees
WHERE name='Rahul';

--------------------------------------------

Question

Compare Rahul and Aman salaries.

SQL

SELECT
name,
salary
FROM employees
WHERE name IN ('Rahul','Aman');

--------------------------------------------

Question

Compare Rahul and Aman employee details.

SQL

SELECT
name,
department,
designation,
experience,
salary,
city
FROM employees
WHERE name IN ('Rahul','Aman');

--------------------------------------------

Question

Compare Rahul and Aman complete employee profiles.

SQL

SELECT *
FROM employees
WHERE name IN ('Rahul','Aman');

--------------------------------------------

Question

Compare Rahul, Aman and Priya salaries.

SQL

SELECT
name,
salary
FROM employees
WHERE name IN ('Rahul','Aman','Priya');

--------------------------------------------

Question

Show salary of all employees.

SQL

SELECT
name,
salary
FROM employees;

--------------------------------------------

Question

Show all employee details.

SQL

SELECT *
FROM employees;

"""
        logger.info("Generating SQL using LLM...")
        response = llm.invoke(prompt)
        logger.info("LLM response received.")
        logger.debug(f"Raw LLM Response:\n{response.content}")

        # ==========================================
        # Extract SQL from LLM Response
        # ==========================================

        query = response.content.strip()

        query = query.replace("```sql", "")
        query = query.replace("```", "")
        query = query.strip()

        # Extract ONLY the SQL statement
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

        # ============================
        # Validate SQL
        # ============================

        logger.info("Validating generated SQL...")

        if not query.upper().startswith("SELECT"):

            logger.error("Invalid SQL generated. Expected a SELECT statement.")

            return {

                "status": "error",

                "query": query,

                "columns": [],

                "rows": [],

                "error": "Invalid SQL generated. Expected a SELECT statement."

            }

        logger.info("SQL validation successful.")

        # ==========================================
        # Execute SQL
        # ==========================================

        try:

            logger.info("Executing SQL query...")

            with self.engine.connect() as conn:

                result = conn.execute(text(query))

                rows = result.fetchall()

                columns = list(result.keys())

            logger.info(f"Query executed successfully. Rows returned: {len(rows)}")

            return {

                "status": "success",

                "query": query,

                "columns": columns,

                "rows": rows

            }

        except Exception as e:

            logger.exception("Employee Tool execution failed.")
            logger.info("=" * 60)
            return {

                "status": "error",

                "query": query,

                "columns": [],

                "rows": [],

                "error": str(e)

            }