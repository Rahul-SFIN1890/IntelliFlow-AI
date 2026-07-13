import json
import re
import time
from urllib import response
from llms.grok_llm import llm
from utils.logger import logger


class SQLRouter:

    def route(self, question: str):
        start_time = time.time()
        logger.info("=" * 60)
        logger.info("SQL ROUTER")
        logger.info("Question : %s", question)
        logger.info("=" * 60)

        prompt = f"""
You are an Enterprise SQL Router.

Your ONLY responsibility is to determine which SQL tools are required to answer the user's question.

You NEVER answer the question.
You NEVER generate SQL.
You NEVER explain your reasoning.

==================================================
QUESTION
==================================================

{question}

==================================================
AVAILABLE TOOLS
==================================================

employee
Owns:
- employee_id
- name
- department
- designation
- experience
- salary
- city

finance
Owns:
- bonus
- tax
- reimbursement
- incentive
- loan

attendance
Owns:
- present days
- absent days
- work from home
- attendance

payroll
Owns:
- gross salary
- net salary
- pf
- esi
- deductions

leave
Owns:
- paid leave
- casual leave
- sick leave
- remaining leave

project
Owns:
- project
- client
- project status
- project rating
- assigned project

==================================================
ROUTING RULES
==================================================

Rule 1

Select ONLY the minimum required tools.

--------------------------------------------------

Rule 2

Never select duplicate tools.

--------------------------------------------------

Rule 3

Multiple employees do NOT imply multiple tools.

Example

Compare Rahul and Aman salaries

Return

{{
    "tools":[
        "employee"
    ]
}}

--------------------------------------------------

Rule 4

Comparison questions still require only the relevant tools.

--------------------------------------------------

Rule 5

If multiple domains are requested, include all relevant tools.

Example

Compare Rahul salary and bonus.

Return

{{
    "tools":[
        "employee",
        "finance"
    ]
}}

==================================================
DOMAIN OWNERSHIP
==================================================

Salary
employee

Gross Salary
payroll

Net Salary
payroll

PF
payroll

ESI
payroll

Bonus
finance

Tax
finance

Loan
finance

Incentive
finance

Attendance
attendance

Present Days
attendance

Absent Days
attendance

WFH
attendance

Leave
leave

Remaining Leave
leave

Paid Leave
leave

Casual Leave
leave

Sick Leave
leave

Project
project

Client
project

Project Rating
project

Department
employee

Designation
employee

Experience
employee

City
employee

==================================================
REPORT TYPES
==================================================

Employee Report

Return

{{
    "tools":[
        "employee"
    ]
}}

--------------------------------------------------

Attendance Report

Return

{{
    "tools":[
        "attendance"
    ]
}}

--------------------------------------------------

Leave Report

Return

{{
    "tools":[
        "leave"
    ]
}}

--------------------------------------------------

Finance Report

Return

{{
    "tools":[
        "finance"
    ]
}}

--------------------------------------------------

Payroll Report

Return

{{
    "tools":[
        "payroll"
    ]
}}

--------------------------------------------------

Project Report

Return

{{
    "tools":[
        "project"
    ]
}}

--------------------------------------------------

Complete Report

Full Report

Complete Employee Profile

360 Report

Complete Employee Report

Return

{{
    "tools":[
        "employee",
        "attendance",
        "leave",
        "finance",
        "payroll",
        "project"
    ]
}}

==================================================
EXAMPLES
==================================================

Question

What is Rahul's salary?

Return

{{
    "tools":[
        "employee"
    ]
}}

------------------------------------------

Question

What is Rahul's bonus?

Return

{{
    "tools":[
        "finance"
    ]
}}

------------------------------------------

Question

Show Rahul attendance.

Return

{{
    "tools":[
        "attendance"
    ]
}}

------------------------------------------

Question

Show Rahul leave balance.

Return

{{
    "tools":[
        "leave"
    ]
}}

------------------------------------------

Question

Show Rahul payroll.

Return

{{
    "tools":[
        "payroll"
    ]
}}

------------------------------------------

Question

Show Rahul project.

Return

{{
    "tools":[
        "project"
    ]
}}

------------------------------------------

Question

Compare Rahul and Aman salaries.

Return

{{
    "tools":[
        "employee"
    ]
}}

------------------------------------------

Question

Compare Rahul salary with Aman's bonus.

Return

{{
    "tools":[
        "employee",
        "finance"
    ]
}}

------------------------------------------

Question

Generate Rahul employee report.

Return

{{
    "tools":[
        "employee"
    ]
}}

------------------------------------------

Question

Generate Rahul attendance report.

Return

{{
    "tools":[
        "attendance"
    ]
}}

------------------------------------------

Question

Generate Rahul finance report.

Return

{{
    "tools":[
        "finance"
    ]
}}

------------------------------------------

Question

Generate Rahul payroll report.

Return

{{
    "tools":[
        "payroll"
    ]
}}
------------------------------------------

Question

Generate Rahul project report.

Return

{{
    "tools":[
        "project"
    ]
}}

------------------------------------------

Question

Generate Rahul leave report.

Return

{{
    "tools":[
        "leave"
    ]
}}
------------------------------------------

Question

Generate a report for Rahul.

Return

{{
    "tools":[
        "employee",
        "attendance",
        "leave",
        "finance",
        "payroll",
        "project"
    ]
}}

------------------------------------------

Question

Generate Rahul's complete employee profile.

Return

{{
    "tools":[
        "employee",
        "attendance",
        "leave",
        "finance",
        "payroll",
        "project"
    ]
}}

------------------------------------------

Question

Generate Rahul's 360 report.

Return

{{
    "tools":[
        "employee",
        "attendance",
        "leave",
        "finance",
        "payroll",
        "project"
    ]
}}

------------------------------------------

Question

Compare Rahul's full report with Aman.

Return

{{
    "tools":[
        "employee",
        "attendance",
        "leave",
        "finance",
        "payroll",
        "project"
    ]
}}

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

Example

{{
    "tools":[
        "employee"
    ]
}}

Never return explanations.

Never return markdown.

Never return SQL.

Never return comments.

Never return text before or after the JSON.

If unsure, return the minimum set of tools required.
"""
        logger.info("Generating SQL execution plan using LLM...")
        response = llm.invoke(prompt)
        logger.info("LLM response received.")
        logger.debug("Raw LLM Response:\n%s", response.content)

        text = response.content.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )
        if match:
            logger.info("Execution plan extracted successfully.")
        else:
            logger.warning("No valid JSON execution plan found.")

        try:

            if match:

                plan = json.loads(
                    match.group()
                )

                plan["tools"] = list(
                    dict.fromkeys(
                        plan.get(
                            "tools",
                            []
                        )
                    )
                )
                print("\n========== SQL ROUTER ==========")
                print(plan)
                print("================================\n")

                logger.info("Selected SQL Tools : %s", plan["tools"])

                logger.info(
                    "SQL Router Execution Time : %.3f sec",
                    time.time() - start_time
                )
                logger.info("SQL Router Completed Successfully")
                logger.info("=" * 60)
                return plan

        except Exception as e:
            
            logger.exception("SQL Router Failed")
            logger.warning(
            "Fallback Triggered. Default Tool : employee"
        )

        logger.info(
            "SQL Router Execution Time : %.3f sec",
            time.time() - start_time
        )
        logger.info("Returning fallback execution plan.")
        logger.info("SQL Router Completed With Fallback")
        logger.info("=" * 60)
        return {

            "tools":[

                "employee"  

            ]

        }