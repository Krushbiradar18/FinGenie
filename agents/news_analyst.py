import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_community.utilities.serpapi import SerpAPIWrapper
load_dotenv()

# Set up Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)

class NewsAnalystAgent:
    def __init__(self):
        self.serp_tool = SerpAPIWrapper()

    def fetch_news(self, query="financial markets today"):
        return self.serp_tool.run(query)

    def summarize_news(self, raw_news):
        prompt = (
            "You're a financial analyst. Based on the following news summary, explain any "
            "market risks, opportunities, or changes in investor sentiment in simple, beginner-friendly language. "
            "Avoid jargon and keep it concise.\n\n"
            f"{raw_news}\n\n"
            "Summarize 3-5 key insights for someone with no finance background."
            )
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content.strip()
        except Exception as e:
            return f"Error during summary: {str(e)}"