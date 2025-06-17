from agents.fin_genie_advisor import FinGenieAdvisorAgent

advisor = FinGenieAdvisorAgent()
result = advisor.generate_advice(age=30, goal="buying a house", horizon=6)

print(f"📊 Risk Level: {result['risk_level']}")
print(f"\n🧠 Investment Guidance:\n{result['risk_explanation']}")
print(f"\n📰 Market Summary:\n{result['news_summary']}")