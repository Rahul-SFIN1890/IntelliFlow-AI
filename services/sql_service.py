import time

from services.sql_router import SQLRouter
from utils.logger import logger

from tools.sql.employee_tool import EmployeeTool
from tools.sql.finance_tool import FinanceTool
from tools.sql.attendance_tool import AttendanceTool
from tools.sql.payroll_tool import PayrollTool
from tools.sql.leave_tool import LeaveTool
from tools.sql.project_tool import ProjectTool


class SQLService:

    def __init__(self):

        self.router = SQLRouter()

        self.tool_map = {

            "employee": {
                "tool": EmployeeTool(),
                "name": "Employee",
                "ignore": "finance, attendance, payroll, leave and project"
            },

            "finance": {
                "tool": FinanceTool(),
                "name": "Finance",
                "ignore": "employee, attendance, payroll, leave and project"
            },

            "attendance": {
                "tool": AttendanceTool(),
                "name": "Attendance",
                "ignore": "employee, finance, payroll, leave and project"
            },

            "payroll": {
                "tool": PayrollTool(),
                "name": "Payroll",
                "ignore": "employee, finance, attendance, leave and project"
            },

            "leave": {
                "tool": LeaveTool(),
                "name": "Leave",
                "ignore": "employee, finance, attendance, payroll and project"
            },

            "project": {
                "tool": ProjectTool(),
                "name": "Project",
                "ignore": "employee, finance, attendance, payroll and leave"
            }

        }

    def execute(
        self,
        question: str,
        history: str = ""
    ):

        start_time = time.time()

        print("\n========== SQL SERVICE ==========\n")

        logger.info("=" * 60)
        logger.info("SQL SERVICE")
        logger.info("Question : %s", question)

        if history:
            logger.debug(
                "History : %s",
                history
            )

        try:

            logger.info(
                "Routing question to SQL Router..."
            )

            plan = self.router.route(question)

            logger.info(
                "SQL Router completed."
            )

            logger.info(
                "Execution Plan : %s",
                plan.get("tools", [])
            )

            print("\n========== SQL ROUTER ==========")
            print(plan)
            print("================================")

            results = {}

            for tool_name in plan.get("tools", []):

                if tool_name not in self.tool_map:
                    continue

                tool_info = self.tool_map[tool_name]

                logger.info(
                    "Executing Tool : %s",
                    tool_info["name"]
                )

                print("\n========== EXECUTING TOOL ==========")
                print(tool_info["name"])
                print("====================================")

                tool_question = f"""
You are the {tool_info['name']} Tool.

Ignore {tool_info['ignore']}.

Return ONLY {tool_info['name'].lower()} related information.

Original Question:

{question}
"""

                response = tool_info["tool"].run(
                    tool_question,
                    history
                )

                logger.info(
                    "%s Tool Execution Completed",
                    tool_info["name"]
                )

                logger.info(
                    "%s Tool Status : %s",
                    tool_info["name"],
                    response.get(
                        "status",
                        "unknown"
                    )
                )

                # Store using tool name
                results[tool_name] = response

            logger.info(
                "Preparing SQL response..."
            )

            final_answer = ""

            sql_queries = {}

            for tool_name, result in results.items():

                sql_queries[tool_name] = result.get(
                    "query",
                    ""
                )

                final_answer += "=" * 60
                final_answer += f"\n{tool_name.upper()} TOOL OUTPUT\n"
                final_answer += "=" * 60
                final_answer += "\n\n"

                if result["status"] == "success":

                    final_answer += "Generated SQL\n"
                    final_answer += "-" * 30 + "\n"
                    final_answer += result.get("query", "")
                    final_answer += "\n\n"

                    final_answer += "Query Result\n"
                    final_answer += "-" * 30 + "\n"

                    rows = result.get(
                        "rows",
                        []
                    )

                    columns = result.get(
                        "columns",
                        []
                    )

                    if rows:

                        for row in rows:

                            for column, value in zip(columns, row):

                                column = column.replace(
                                    "_",
                                    " "
                                ).title()

                                final_answer += (
                                    f"{column:<22}: {value}\n"
                                )

                            final_answer += "\n"

                    else:

                        final_answer += "No records found.\n"

                else:

                    final_answer += "Generated SQL\n"
                    final_answer += "-" * 30 + "\n"

                    final_answer += result.get(
                        "query",
                        ""
                    )

                    final_answer += "\n\n"

                    final_answer += "SQL Error\n"
                    final_answer += "-" * 30 + "\n"

                    final_answer += result.get(
                        "error",
                        "Unknown Error"
                    )

                    final_answer += "\n"

                    logger.info(
                "SQL Service Execution Time : %.3f sec",
                time.time() - start_time
            )

            logger.info(
                "SQL Service Completed Successfully"
            )

            logger.info("=" * 60)

            return {

                "answer": final_answer,

                "sql_response": sql_queries,

                "structured_results": results

            }

        except Exception:

            logger.exception(
                "SQL Service Failed"
            )

            logger.info(
                "SQL Service Execution Time : %.3f sec",
                time.time() - start_time
            )

            logger.info("=" * 60)

            raise