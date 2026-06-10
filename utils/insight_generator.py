import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()


def generate_insight(question, answer):
    """
    Takes the user's question and the agent's answer,
    returns a 2-sentence plain English business insight.
    """
    if not answer or "error" in answer.lower():
        return None

    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            api_key=os.getenv("GROQ_API_KEY")
        )

        prompt = f"""You are a business analyst writing for a non-technical audience.

The user asked: "{question}"
The data shows: "{answer}"

Write exactly 2 sentences:
1. What the data shows in plain English with specific numbers
2. What action or conclusion the business should consider

Be specific, concise, and avoid technical jargon.
Do not say "the data shows" or "based on the data".
Just write the insight directly."""

        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()

    except Exception:
        return None