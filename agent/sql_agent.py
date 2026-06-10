import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()


def get_sql_agent(db_path="data.db", table_name=None, columns=None):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    )

    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    if table_name and columns:
        prefix = f"""You are a data analyst assistant. You have access to a SQLite database.
The database has ONE table called '{table_name}' with these columns: {', '.join(columns)}.
ALWAYS query the '{table_name}' table. Never guess other table names.
Always return a clear, specific answer with the actual numbers."""
    else:
        prefix = """You are a data analyst assistant with access to a SQLite database.
Always use sql_db_list_tables first to find the correct table name.
Always return a clear specific answer."""

    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=20,
        prefix=prefix
    )

    return agent


def ask_agent(agent, question, chat_history=None):
    try:
        if chat_history:
            history_text = ""
            for msg in chat_history[-4:]:
                role = "Human" if msg["role"] == "user" else "AI"
                history_text += f"{role}: {msg['content']}\n"

            full_question = f"""Previous conversation:
{history_text}
Current question: {question}"""
        else:
            full_question = question

        result = agent.invoke({"input": full_question})
        return result["output"]

    except Exception as e:
        return f"I encountered an error: {str(e)}. Please try rephrasing your question."


if __name__ == "__main__":
    print("SQL agent module loaded successfully.")
    print("Run the Streamlit app to test: streamlit run app.py")