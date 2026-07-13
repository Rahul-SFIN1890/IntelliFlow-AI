# 🚀 IntelliFlow AI

> Enterprise Multi-Agent AI Assistant powered by **LangGraph**, **LangChain**, **CrewAI**, **ChromaDB**, **SQLite**, and **Groq LLM**.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-green)
![LangChain](https://img.shields.io/badge/LangChain-Framework-success)
![CrewAI](https://img.shields.io/badge/CrewAI-Orchestration-orange)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple)
![License](https://img.shields.io/badge/License-MIT-red)

---

# 📖 Overview

IntelliFlow AI is an **enterprise-grade Multi-Agent AI Assistant** designed to answer both **structured** and **unstructured** business queries using intelligent routing, planning, Retrieval-Augmented Generation (RAG), SQL querying, reasoning, memory, and enterprise tools.

Unlike traditional chatbots that rely on a single LLM prompt, IntelliFlow AI employs multiple specialized AI agents working together to determine the best strategy for answering a user's request.

The system intelligently decides whether the answer should come from:

- Enterprise SQL Database
- Company Policy Documents
- Enterprise Tools
- Web Search
- Multiple Data Sources

This architecture closely resembles production-grade enterprise AI systems.

---

# ✨ Key Features

## 🤖 Multi-Agent Architecture

- Router Agent
- Planner Agent
- SQL Agent
- RAG Agent
- Question Rewriter Agent
- Reasoning Agent
- Execution Agent
- Tool Agent
- Analyst Agent
- Writer Agent
- Summarizer Agent
---

## 🧠 Intelligent Query Routing

Automatically detects whether a user query should be answered using:

- SQL Database
- Company Documents
- Enterprise Tools
- Web Search
- Hybrid Workflow

---

## 🗄 Enterprise SQL Assistant

Supports enterprise data including:

- Employee Details
- Payroll
- Leave Management
- Attendance
- Finance
- Projects

Natural language questions are converted into SQL automatically.

Example:

> How many leaves does Rahul have?

> Generate Rahul's employee profile.

> Who earns more than ₹10 LPA?

---

## 📄 Retrieval-Augmented Generation (RAG)

The system performs semantic search over company documents using ChromaDB.

Supported documents include:

- HR Policies
- Leave Policies
- Insurance Policies
- Company Handbook

Pipeline:

Document → Chunking → Embedding → ChromaDB → Retrieval → LLM

---

## 📋 Intelligent Planning

Complex queries are decomposed into multiple executable steps using the Planner Agent.

Example:

> Compare Rahul's payroll with his attendance and summarize the findings.

Planner automatically breaks the task into:

- Attendance Retrieval
- Payroll Retrieval
- Analysis
- Final Summary

---

## 💬 Conversation Memory

Supports:

- Chat Memory
- Conversation History
- Context-Aware Responses

Users can ask follow-up questions naturally.

---

## 🛠 Enterprise Tools

Integrated tools include:

- SQL Tools
- Calculator
- Email Tool
- Slack Tool
- Currency Converter
- Weather Tool
- Web Search
- News Search

---

## 📊 Enterprise Logging

Production-ready logging captures:

- Agent Routing
- Tool Execution
- SQL Queries
- Planner Decisions
- Errors
- Execution Flow

Useful for debugging and production monitoring.

---

# 🏗 High-Level Architecture

```
                      User
                        │
                        ▼
               Question Rewriter
                        │
                        ▼
                 Router Agent
                        │
      ┌─────────────────┼──────────────────┐
      │                 │                  │
      ▼                 ▼                  ▼
 SQL Agent         RAG Agent          Tool Agent
      │                 │                  │
      ▼                 ▼                  ▼
 SQLite DB        Chroma Vector DB   Enterprise Tools
      │                 │                  │
      └─────────────────┴──────────────────┘
                        │
                        ▼
                 Planner Agent
                        │
                        ▼
               Execution Agent
                        │
                        ▼
              Summarizer Agent
                        │
                        ▼
                  Final Response
```

---

# 🧩 Project Workflow

1. User submits a question.
2. Question Rewriter improves clarity.
3. Router Agent identifies the best execution path.
4. Planner Agent creates an execution strategy.
5. SQL Agent or RAG Agent retrieves relevant information.
6. Tool Agent invokes enterprise tools if required.
7. Execution Agent combines all outputs.
8. Summarizer Agent generates the final response.
9. Conversation Memory stores context for future interactions.

---

# 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| LLM | Groq |
| AI Framework | LangChain |
| Workflow | LangGraph |
| Multi-Agent | CrewAI |
| Vector Database | ChromaDB |
| Database | SQLite |
| Embeddings | HuggingFace |
| Logging | Python Logging |
| Memory | Conversation Buffer |
| Document Loader | LangChain |
| Text Splitter | Recursive Character Splitter |

---

# 📂 Project Structure

```
IntelliFlow-AI
│
├── agents/
├── crew_ai/
├── data/
├── database/
├── execution/
├── graph/
├── llms/
├── memory/
├── prompts/
├── retriever/
├── services/
├── tests/
├── tools/
├── utils/
├── vector_db/
│
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/IntelliFlow-AI.git

cd IntelliFlow-AI
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=YOUR_API_KEY
```

Run

```bash
python run.py
```

---

# 💬 Example Questions

## SQL

- Generate Rahul's employee profile
- Show attendance of Rahul
- How many leaves does Rahul have?
- Compare payroll of Rahul and Aman
- Show all employees working in Finance

## RAG

- Summarize the leave policy
- Explain the insurance policy
- What is the company's HR policy?
- Explain the reimbursement process


---

# 📈 Production Features

- Modular Architecture
- Prompt Engineering
- Multi-Agent Workflow
- Enterprise Logging
- Memory Management
- Tool Calling
- SQL Generation
- RAG Pipeline
- Semantic Search
- Extensible Architecture
- Error Handling
- Reusable Services

---

# 🔮 Future Enhancements

- FastAPI Backend
- Streamlit Dashboard
- Authentication & Authorization
- Role-Based Access Control (RBAC)
- Docker Support
- Kubernetes Deployment
- PostgreSQL Integration
- Redis Memory
- API Gateway
- CI/CD Pipeline
- Monitoring with Prometheus & Grafana
- Multi-LLM Support
- Voice Assistant Integration

---

# 👨‍💻 Author

**Rahul Jha**

AI/ML Engineer

---

# ⭐ If you found this project useful

Please consider giving it a ⭐ on GitHub.

It motivates further development and helps others discover the project.
