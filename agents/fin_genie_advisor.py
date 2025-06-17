from agents.risk_profiler import RiskProfilerAgent
from agents.news_analyst import NewsAnalystAgent

class FinGenieAdvisorAgent:
    def __init__(self):
        self.risk_agent = RiskProfilerAgent()
        self.news_agent = NewsAnalystAgent()

    def generate_advice(self, age, goal, horizon):
        # Step 1: Get risk profile and explanation
        risk_level, risk_explanation = self.risk_agent.assess(age, goal, horizon)

        # Step 2: Fetch and analyze market news
        raw_news = self.news_agent.fetch_news()
        news_summary = self.news_agent.summarize_news(raw_news)

        # Step 3: Combine outputs
        return {
            "risk_level": risk_level,
            "risk_explanation": risk_explanation,
            "news_summary": news_summary
        }