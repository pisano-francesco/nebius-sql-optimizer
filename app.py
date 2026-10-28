import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# Load environment variables (.env)
load_dotenv()
api_key = os.getenv("NEBIUS_API_KEY")

st.set_page_config(
    page_title="AI SQL Optimizer & Agent", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS per rifinire lo stile dell'interfaccia
st.markdown("""
    <style>
    /* Styling pulsante principale */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF1A1A 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
    }
    /* Badge styling */
    .tech-badge {
        background-color: #1E293B;
        color: #38BDF8;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.82rem;
        font-weight: 500;
        border: 1px solid #334155;
        display: inline-block;
        margin-right: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar - Settings & About
with st.sidebar:
    st.title("⚙️ Control Panel")
    
    language = st.selectbox(
        "🌐 Response Language",
        ["English", "Italiano", "Español", "Français", "Deutsch", "Português"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📌 System Info")
    st.markdown("<span class='tech-badge'>Model</span> NVIDIA Nemotron-3.5", unsafe_allow_html=True)
    st.markdown("<span class='tech-badge'>Provider</span> Nebius Token Factory", unsafe_allow_html=True)
    st.markdown("<span class='tech-badge'>Track</span> Agentic Engineering", unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("🚀 Built for Nebius x NVIDIA Hackathon 2026")

# Header Section
st.title("⚡ AI SQL Optimizer & Index Advisor")
st.markdown("""
<div style='margin-bottom: 20px;'>
    <span class='tech-badge'>🟢 API Status: Active</span>
    <span class='tech-badge'>⚡ Low Latency Inference</span>
</div>
""", unsafe_allow_html=True)

if not api_key:
    st.error("API Key not found in .env file! Please set NEBIUS_API_KEY correctly.")
    st.stop()

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/", api_key=api_key
)

# Initialize session state
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Language instruction mapping
language_instructions = {
    "English": "You MUST generate ALL your responses and analyses EXCLUSIVELY IN ENGLISH.",
    "Italiano": "Devi rispondere ed elaborare QUALSIASI testo, analisi o risposta ESCLUSIVAMENTE IN ITALIANO.",
    "Español": "Debes generar TODAS tus respuestas y análisis EXCLUSIVAMENTE EN ESPAÑOL.",
    "Français": "Vous devez générer TOUTES vos réponses et analyses EXCLUSIVEMENT EN FRANÇAIS.",
    "Deutsch": "Du musst ALLE deine Antworten und Analysen AUSSCHLIESSLICH AUF DEUTSCH verfassen.",
    "Português": "Você deve gerar TODAS as suas respostas e análises EXCLUSIVAMENTE EM PORTUGUÊS."
}

chat_placeholders = {
    "English": "e.g., Why did you choose a composite index instead of single indexes?",
    "Italiano": "Es: Perché hai scelto un indice composito invece di due indici singoli?",
    "Español": "Ej: ¿Por qué elegiste un índice compuesto en lugar de índices simples?",
    "Français": "Ex: Pourquoi avez-vous choisi un index composé au lieu d'index simples ?",
    "Deutsch": "z. B. Warum hast du einen zusammengesetzten Index statt einzelner Indizes gewählt?",
    "Português": "Ex: Por que você escolheu um índice composto em vez de índices simples?"
}

system_prompt = f"""You are a Senior Database Administrator (DBA) and Data Architecture Expert.

STRICT LANGUAGE MANDATE:
- {language_instructions[language]}
- Do not use any other language for explanations, output formatting, or greetings.

CORE RESPONSIBILITIES:
1. Analyze database schemas and SQL queries to identify bottlenecks, suggest optimal indexes (B-Tree, Hash), and rewrite queries for maximum performance.
2. Answer technical questions about SQL, relational/NoSQL databases, indexing, execution plans, ORMs, and database integration in programming languages.

SCOPE & CONTEXT BOUNDARIES:
- ACCEPT: Any questions regarding databases, SQL, NoSQL, data modeling, query optimization, database engine internals, and software integration.
- REJECT ONLY: Inputs completely unrelated to IT, software development, or databases."""

# Default inputs
default_schema = """CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    created_at TIMESTAMP,
    status VARCHAR(50),
    total_amount DECIMAL(10,2)
);"""

default_query = """SELECT * FROM orders 
WHERE user_id = 42 
  AND status = 'COMPLETED' 
ORDER BY created_at DESC;"""

# Input Layout with Containers
with st.container(border=True):
    col_input1, col_input2 = st.columns(2)

    with col_input1:
        schema_input = st.text_area(
            "1. Database Schema (CREATE TABLE...)", value=default_schema, height=180
        )

    with col_input2:
        query_input = st.text_area(
            "2. SQL Query to Optimize", value=default_query, height=180
        )

    btn_click = st.button("🚀 Analyze & Optimize with Nemotron", use_container_width=True)

if btn_click:
    if not query_input.strip():
        st.warning("Please enter at least one SQL query to analyze.")
    else:
        with st.spinner("Analyzing schema and query via NVIDIA Nemotron-3.5..."):
            user_content = f"DATABASE SCHEMA:\n{schema_input}\n\nQUERY TO OPTIMIZE:\n{query_input}"

            try:
                response = client.chat.completions.create(
                    model="nvidia/Nemotron-3_5-Lightning",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content},
                    ],
                    temperature=0.2,
                )

                st.session_state.analysis_result = response.choices[0].message.content
                st.session_state.chat_history = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": st.session_state.analysis_result},
                ]

            except Exception as e:
                st.error(f"API Request Error: {e}")

# Output Section
if st.session_state.analysis_result:
    st.markdown("### 📊 Analysis & Recommendations")
    
    with st.container(border=True):
        st.markdown(st.session_state.analysis_result)

    st.markdown("### 💬 Interactive DBA Agent")
    
    with st.container(border=True):
        if st.session_state.chat_history:
            st.session_state.chat_history[0] = {"role": "system", "content": system_prompt}

        for msg in st.session_state.chat_history[3:]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if user_question := st.chat_input(chat_placeholders[language]):
            st.session_state.chat_history.append({"role": "user", "content": user_question})

            with st.spinner("Agent Nemotron is thinking..."):
                try:
                    chat_response = client.chat.completions.create(
                        model="nvidia/Nemotron-3_5-Lightning",
                        messages=st.session_state.chat_history,
                        temperature=0.3,
                    )
                    answer = chat_response.choices[0].message.content
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.rerun()
                except Exception as e:
                    st.error(f"Chat Error: {e}")