import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

class RiskProfilerAgent:
    def __init__(self):
        self.risk_levels = {
            "low": "Low risk: safe investments like bonds, large-cap ETFs.",
            "medium": "Medium risk: balanced investments like index funds, blue-chip stocks.",
            "high": "High risk: aggressive investments like crypto, small-cap stocks."
        }

    def assess(self, age, goal, horizon):
        if age > 50 or horizon < 3:
            risk = "low"
        elif 30 <= age <= 50 or 3 <= horizon <= 5:
            risk = "medium"
        else:
            risk = "high"

        explanation = self.generate_explanation(age, goal, horizon, risk)
        return risk, explanation

    def generate_explanation(self, age, goal, horizon, risk_level):
        prompt = (
            f"A user aged {age} wants to invest for '{goal}' with a horizon of {horizon} years.\n"
            f"The risk level is '{risk_level}'.\n"
            "As a friendly AI financial advisor, explain this clearly and simply using beginner-friendly terms.\n"
            "Avoid financial jargon. Then suggest ideal investment options with reasons in simple language."
        )
        if risk_level not in self.risk_levels:
            return "Invalid risk level."
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content.strip()
        except Exception as e:
            return f"Error generating explanation: {str(e)}"