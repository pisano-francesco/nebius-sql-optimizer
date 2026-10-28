# ⚡ AI SQL Optimizer & Index Advisor

An intelligent, interactive DBA Agent built for the **Nebius x NVIDIA Hackathon 2026** under the **Coding and Agentic Engineering** track.

Powered by **NVIDIA Nemotron-3.5-Lightning** via **Nebius Token Factory**.

---

## 🚀 Overview

**AI SQL Optimizer** is an agentic developer tool designed to bridge the gap between application development and database performance engineering. It analyzes database schemas alongside raw or incomplete SQL queries, identifies execution bottlenecks, suggests optimal B-tree compound indexes, rewrites queries for efficiency, and offers an interactive DBA chat agent to explain database internal mechanics in real time.

---

## ✨ Key Features

- **Co-Analysis of Schema & Query:** Evaluates table structures and filtering/sorting predicates together to catch full table scans, filesorts, and IO overhead.
- **Fault-Tolerant Input Processing:** Gracefully handles incomplete SQL syntax or partial statements without failing.
- **Automated Index Recommendations:** Generates precise `CREATE INDEX` DDL statements tailored to query filtering, join, and sorting conditions.
- **Interactive Agentic Q&A:** Maintains a multi-turn persistent conversation session allowing developers to ask follow-up questions about B-tree mechanics, leftmost prefix rules, and execution plans.
- **Strict Domain Boundary Guardrails:** Built-in system instructions ensure the agent remains focused on database, SQL, ORM, and IT architecture topics while politely rejecting off-topic inputs.
- **Multilingual Support:** Dynamic sidebar selector enabling real-time language switching across 6 languages (**English, Italian, Spanish, French, German, Portuguese**) for both chat placeholders and agent responses.

---

## 🛠️ Tech Stack

- **LLM Model:** `nvidia/Nemotron-3_5-Lightning` (NVIDIA Nemotron-3.5-Lightning)
- **Inference Platform:** Nebius Token Factory (Serverless OpenAI-compatible API)
- **Frontend / UI Framework:** Streamlit
- **Runtime Environment:** Python 3.12+
- **SDKs & Libraries:** OpenAI Python SDK, `python-dotenv`

---

## ⚡ Quickstart & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/pisano-francesco/nebius-sql-optimizer.git
cd nebius-sql-optimizer
