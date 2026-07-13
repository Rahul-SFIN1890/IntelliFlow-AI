import re
import time

from utils.logger import logger


def planner_agent(question: str):

    start_time = time.time()

    print("\n========== PLANNER ==========\n")

    logger.info("=" * 60)
    logger.info("PLANNER AGENT")
    logger.info("Question : %s", question)

    question_lower = question.lower()

    plan = {

        "sql_question": "",

        "rag_question": ""

    }

    # =====================================================
    # SQL Keywords
    # =====================================================

    sql_keywords = [

        # Employee

        "employee",

        "employee profile",

        "profile",

        "department",

        "designation",

        "experience",

        "city",

        "salary",

        "gross salary",

        "net salary",

        # Finance

        "bonus",

        "tax",

        "loan",

        "reimbursement",

        "incentive",

        # Attendance

        "attendance",

        "present",

        "absent",

        "work from home",

        "wfh",

        # Leave

        "leave balance",

        "remaining leave",

        "paid leave",

        "casual leave",

        "sick leave",

        # Payroll

        "payroll",

        "pf",

        "esi",

        "deduction",

        # Projects

        "project",

        "project status",

        "project rating",

        "client",

        "working on",

        # Analytics

        "highest salary",

        "lowest salary",

        "maximum salary",

        "minimum salary"

    ]

    # =====================================================
    # RAG Keywords
    # =====================================================

    rag_keywords = [

        "policy",

        "leave policy",

        "company policy",

        "company leave policy",

        "hr policy",

        "insurance",

        "insurance policy",

        "travel policy",

        "reimbursement policy",

        "work from home policy",

        "handbook",

        "manual",

        "guideline",

        "guidelines",

        "faq",

        "document",

        "pdf"

    ]

    # =====================================================
    # Summary Keywords
    # =====================================================

    summary_keywords = [

        "summarize",

        "summary",

        "brief",

        "concise",

        "executive summary",

        "tldr"

    ]

    has_sql = any(

        keyword in question_lower

        for keyword in sql_keywords

    )

    has_rag = any(

        keyword in question_lower

        for keyword in rag_keywords

    )

    has_summary = any(

        keyword in question_lower

        for keyword in summary_keywords

    )
    
    # =====================================================
    # Employee Name Extraction
    # =====================================================

    employee_match = re.search(

        r"\b([A-Z][a-z]+)\b",

        question

    )

    employee_name = ""

    if employee_match:

        employee_name = employee_match.group(1)

    # =====================================================
    # SQL + RAG
    # =====================================================

    if has_sql and has_rag:

        # Leave Balance + Policy

        if "leave" in question_lower:

            plan["sql_question"] = (

                f"Show {employee_name}'s leave balance."

            )

            plan["rag_question"] = (

                "What is the company leave policy?"

            )

            return plan

        # Reimbursement + Policy

        if "reimbursement" in question_lower:

            plan["sql_question"] = (

                f"Show {employee_name}'s reimbursement."

            )

            plan["rag_question"] = (

                "Explain reimbursement policy."

            )

            return plan

        # Insurance + Policy

        if "insurance" in question_lower:

            plan["sql_question"] = (

                f"Show {employee_name}'s insurance information."

            )

            plan["rag_question"] = (

                "Explain insurance policy."

            )

            return plan

        # Default Hybrid

        plan["sql_question"] = question

        plan["rag_question"] = question

        return plan

    # =====================================================
    # Report Generation
    # =====================================================

    if "report" in question_lower:

        plan["sql_question"] = question

        return plan

    # =====================================================
    # Profile Generation
    # =====================================================

    if "profile" in question_lower:

        plan["sql_question"] = question

        return plan

    # =====================================================
    # Comparison
    # =====================================================

    if "compare" in question_lower:

        plan["sql_question"] = question

        return plan

    # =====================================================
    # Summary
    # =====================================================

    if has_summary:

        plan["sql_question"] = question

        return plan

    # =====================================================
    # SQL Only
    # =====================================================

    if has_sql:

        plan["sql_question"] = question

        return plan

    # =====================================================
    # RAG Only
    # =====================================================

    if has_rag:

        plan["rag_question"] = question

        return plan
    
        # =====================================================
    # Better Employee Extraction
    # =====================================================

    ignore_words = {

        "what",
        "show",
        "compare",
        "generate",
        "who",
        "how",
        "which",
        "explain",
        "summarize",
        "report",
        "profile",
        "employee",
        "company"

    }

    if employee_name.lower() in ignore_words:

        employee_name = ""

    # =====================================================
    # Follow-up Questions
    # =====================================================

    follow_up_keywords = [

        "it",
        "his",
        "her",
        "that",
        "those",
        "same employee"

    ]

    if any(
        keyword in question_lower
        for keyword in follow_up_keywords
    ):

        plan["sql_question"] = question

        return plan

    # =====================================================
    # Default Planner
    # =====================================================

    if not plan["sql_question"] and not plan["rag_question"]:

        plan["sql_question"] = question

    # =====================================================
    # Planner Debug
    # =====================================================

    print("\n========== PLANNER ==========")
    print("SQL Question :", plan["sql_question"])
    print("RAG Question :", plan["rag_question"])
    print("=============================\n")

    return plan