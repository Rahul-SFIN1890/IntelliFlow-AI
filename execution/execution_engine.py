import time

from agents.sql_agent import sql_agent
from agents.rag_agent import rag_agent
from agents.tool_agent import tool_agent
from agents.websearch_agent import websearch_agent
from agents.reasoning_agent import reasoning_agent

from agents.analyst_agent import analyst_agent
from agents.writer_agent import writer_agent
from agents.summarizer_agent import summarizer_agent

from services.planner_service import PlannerService
from services.question_rewriter_service import (
    QuestionRewriterService
)

from memory.conversation_memory import (
    ConversationMemory
)

from utils.logger import logger


# ==========================================================
# Global Conversation Memory
# ==========================================================

memory = ConversationMemory()


class ExecutionEngine:

    @staticmethod
    def execute(plan, state):

        start_time = time.time()

        print("\n========== EXECUTION ENGINE ==========\n")

        logger.info("=" * 60)
        logger.info("EXECUTION ENGINE")
        logger.info("Question : %s", state["question"])
        logger.info("Execution Plan : %s", plan)

        try:

            execution_results = {}

            planner = PlannerService()

            rewriter = QuestionRewriterService()

            # ==================================================
            # Store User Question
            # ==================================================

            logger.info(
                "Adding user message to conversation memory..."
            )

            memory.add_user_message(
                state["question"]
            )

            # ==================================================
            # Conversation History
            # ==================================================

            history = memory.get_history_text()

            logger.info(
                "Conversation history loaded."
            )

            # ==================================================
            # Rewrite Question
            # ==================================================

            logger.info(
                "Executing Question Rewriter..."
            )

            rewrite_result = rewriter.execute(

                question=state["question"],

                history=history

            )

            rewritten_question = rewrite_result.get(

                "rewritten_question",

                state["question"]

            )

            logger.info(
                "Question rewritten successfully."
            )

            print("\n========== QUESTION REWRITER ==========")

            print("Original Question :")
            print(state["question"])
            print()

            print("Rewritten Question :")
            print(rewritten_question)

            print("=======================================\n")

            # ==================================================
            # Planner
            # ==================================================

            logger.info(
                "Executing Planner..."
            )

            planner_result = planner.execute(
                rewritten_question
            )

            logger.info(
                "Planner completed."
            )

            sql_question = planner_result.get(
                "sql_question",
                ""
            )

            rag_question = planner_result.get(
                "rag_question",
                ""
            )

            print("\n========== PLANNER ==========")
            print(planner_result)
            print("=============================\n")

            # ==================================================
            # Start Execution
            # ==================================================

            for step in plan:

                logger.info(
                    "Executing Agent : %s",
                    step.upper()
                )

                print(
                    f"\n========== Executing : {step.upper()} ==========\n"
                )

                # ===========================================
                # SQL AGENT
                # ===========================================

                if step == "sql":

                    if not sql_question:
                        continue

                    sql_state = {

                        **state,

                        "question": sql_question

                    }

                    try:

                        response = sql_agent(
                            sql_state
                        )

                        logger.info(
                            "SQL Agent Completed Successfully"
                        )

                        execution_results["sql"] = response.get(
                            "structured_results",
                            {}
                        )

                        execution_results["sql_debug"] = response.get(
                            "answer",
                            ""
                        )

                        execution_results["sql_queries"] = response.get(
                            "sql_response",
                            {}
                        )

                    except Exception as e:

                        logger.exception(
                            "SQL Agent Failed"
                        )

                        execution_results["sql"] = {}

                        execution_results["sql_error"] = str(
                            e
                        )

                        print("\n========== SQL ERROR ==========")
                        print(str(e))
                        print("===============================\n")

                # ===========================================
                # RAG AGENT
                # ===========================================

                elif step == "rag":

                    if not rag_question:
                        continue

                    rag_state = {

                        **state,

                        "question": rag_question

                    }

                    try:

                        response = rag_agent(
                            rag_state
                        )

                        logger.info(
                            "RAG Agent Completed Successfully"
                        )

                        execution_results["rag"] = response.get(
                            "answer",
                            ""
                        )

                    except Exception as e:

                        logger.exception(
                            "RAG Agent Failed"
                        )

                        execution_results["rag"] = ""

                        execution_results["rag_error"] = str(
                            e
                        )

                        print("\n========== RAG ERROR ==========")
                        print(str(e))
                        print("===============================\n")

                # ===========================================
                # TOOL AGENT
                # ===========================================

                elif step == "tool":

                    try:

                        response = tool_agent(
                            state
                        )

                        logger.info(
                            "Tool Agent Completed Successfully"
                        )

                        execution_results["tool"] = response.get(
                            "answer",
                            ""
                        )

                    except Exception as e:

                        logger.exception(
                            "Tool Agent Failed"
                        )

                        execution_results["tool_error"] = str(
                            e
                        )

                        print("\n========== TOOL ERROR ==========")
                        print(str(e))
                        print("================================\n")

                # ===========================================
                # WEB SEARCH AGENT
                # ===========================================

                elif step == "websearch":

                    try:

                        response = websearch_agent(
                            state
                        )

                        logger.info(
                            "WebSearch Agent Completed Successfully"
                        )

                        execution_results["websearch"] = response.get(
                            "answer",
                            ""
                        )

                    except Exception as e:

                        logger.exception(
                            "WebSearch Agent Failed"
                        )

                        execution_results["websearch_error"] = str(
                            e
                        )

                        print("\n========== WEBSEARCH ERROR ==========")
                        print(str(e))
                 
                        print("=====================================\n")

                # ===========================================
                # REASONING AGENT
                # ===========================================

                elif step == "reasoning":

                    try:

                        response = reasoning_agent(
                            state
                        )

                        logger.info(
                            "Reasoning Agent Completed Successfully"
                        )

                        execution_results["reasoning"] = response.get(
                            "answer",
                            ""
                        )

                    except Exception as e:

                        logger.exception(
                            "Reasoning Agent Failed"
                        )

                        execution_results["reasoning_error"] = str(
                            e
                        )

                        print("\n========== REASONING ERROR ==========")
                        print(str(e))
                        print("=====================================\n")

                # ===========================================
                # ANALYST AGENT
                # ===========================================

                elif step == "analyst":

                    analyst_state = {

                        "question": rewritten_question,

                        "sql": execution_results.get(
                            "sql",
                            {}
                        ),

                        "rag": execution_results.get(
                            "rag",
                            ""
                        )

                    }

                    try:

                        response = analyst_agent(
                            analyst_state
                        )

                        logger.info(
                            "Analyst Agent Completed Successfully"
                        )

                        print("\n========== ANALYST OUTPUT ==========")
                        print(response)
                        print("===================================\n")

                        execution_results["analysis"] = response.get(
                            "analysis",
                            ""
                        )

                    except Exception as e:

                        logger.exception(
                            "Analyst Agent Failed"
                        )

                        execution_results["analysis"] = ""

                        execution_results["analyst_error"] = str(
                            e
                        )

                        print("\n========== ANALYST ERROR ==========")
                        print(str(e))
                        print("===================================\n")

                # ===========================================
                # WRITER AGENT
                # ===========================================

                elif step == "writer":

                    writer_state = {

                        "question": rewritten_question,

                        "analysis": execution_results.get(
                            "analysis",
                            ""
                        )

                    }

                    try:

                        response = writer_agent(
                            writer_state
                        )

                        logger.info(
                            "Writer Agent Completed Successfully"
                        )

                        print("\n========== WRITER OUTPUT ==========")
                        print(response)
                        print("==================================\n")

                        execution_results["final_answer"] = response.get(
                            "final_response",
                            ""
                        )

                    except Exception as e:

                        logger.exception(
                            "Writer Agent Failed"
                        )

                        execution_results["final_answer"] = ""

                        execution_results["writer_error"] = str(
                            e
                        )

                        print("\n========== WRITER ERROR ==========")
                        print(str(e))
                        print("==================================\n")

                # ===========================================
                # SUMMARY AGENT
                # ===========================================

                elif step == "summary":

                    summary_state = {

                        "question": rewritten_question,

                        "content": execution_results.get(
                            "final_answer",
                            ""
                        )

                    }

                    try:

                        response = summarizer_agent(
                            summary_state
                        )

                        logger.info(
                            "Summary Agent Completed Successfully"
                        )

                        execution_results["final_answer"] = response.get(
                            "summary",
                            execution_results.get(
                                "final_answer",
                                ""
                            )
                        )

                    except Exception as e:

                        logger.exception(
                            "Summary Agent Failed"
                        )

                        execution_results["summary_error"] = str(
                            e
                        )

                        print("\n========== SUMMARY ERROR ==========")
                        print(str(e))
                        print("===================================\n")

                            # ==================================================
            # Store Assistant Response in Memory
            # ==================================================

            print("\n========== FINAL ANSWER ==========")
            print(execution_results.get("final_answer"))
            print("=================================\n")

            logger.info(
                "Saving assistant response to conversation memory..."
            )

            memory.add_assistant_message(

                execution_results.get(

                    "final_answer",

                    ""

                )

            )

            # ==================================================
            # Execution Summary
            # ==================================================

            logger.info(
                "Execution Summary Generated."
            )

            print("\n========== EXECUTION SUMMARY ==========")

            print("Executed Agents :")

            for agent in plan:

                print(f"✔ {agent}")

            print()

            print("Execution Result Keys :")

            for key in execution_results.keys():

                print(f"• {key}")

            print("=======================================\n")

            logger.info(
                "Execution Engine Time : %.3f sec",
                time.time() - start_time
            )

            logger.info(
                "Execution Engine Completed Successfully"
            )

            logger.info("=" * 60)

            # ==================================================
            # Return Response
            # ==================================================

            return {

                "answer": execution_results.get(

                    "final_answer",

                    ""

                ),

                "execution_results": execution_results,

                "planner": planner_result,

                "rewritten_question": rewritten_question,

                "chat_history": memory.get_history()

            }

        except Exception:

            logger.exception(
                "Execution Engine Failed"
            )

            logger.info(
                "Execution Engine Time : %.3f sec",
                time.time() - start_time
            )

            logger.info("=" * 60)

            raise