import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from agents.fin_genie_advisor import FinGenieAdvisorAgent
from streamlit_app.utils.pdf_generator import generate_pdf
import base64
import plotly.graph_objects as go
import io
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import requests
from datetime import datetime


# Load environment variables
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)


# App Config
st.set_page_config(page_title="FinGenie", layout="centered")

# Sidebar
with st.sidebar:
    st.title("🤖 FinGenie")
    st.markdown("Your AI-Powered Portfolio Guide 💼")
    st.markdown("---")
    st.markdown("🔒 *Demo only. Not financial advice.*")
    st.markdown("Made with ❤️ by Krushnali Biradar")

# Main Title
st.title("📈 FinGenie – Your AI Financial Advisor")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f4f4f9; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #4CAF50; color: white; }
    </style>
""", unsafe_allow_html=True)

# Form
with st.form("advisor_form"):
    age = st.number_input("Your Age", min_value=18, max_value=100, step=1)
    goal = st.text_input("Your Investment Goal (e.g., buying a house, retirement)")
    horizon = st.slider("Investment Horizon (in years)", 1, 30, 5)
    submit = st.form_submit_button("Generate Advice")

if submit:
    st.info("⏳ Analyzing your profile and current market...")
    advisor = FinGenieAdvisorAgent()
    result = advisor.generate_advice(age, goal, horizon)

    st.session_state.age = age
    st.session_state.goal = goal
    st.session_state.horizon = horizon
    st.session_state.result = result

    # --- Log user data to Firebase ---
    firebase_url = os.getenv("FIREBASE_URL")
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "age": age,
        "goal": goal,
        "horizon": horizon,
        "risk_level": result["risk_level"]
    }
    try:
        requests.post(f"{firebase_url}/user_logs.json", json=log_data)
    except Exception as e:
        st.warning(f"⚠️ Could not log data to Firebase: {e}")

    # --- Display Risk Profile ---
    st.subheader("📊 Risk Profile")
    st.write(f"**Risk Level:** `{result['risk_level'].capitalize()}`")
    st.markdown(result['risk_explanation'])

    # --- Display News Summary ---
    st.subheader("📰 Market Summary")
    st.markdown(result['news_summary'])

    # --- Asset Allocation Chart ---
    allocations = {
        "low": {"Equity": 20, "Debt": 60, "Alternatives": 20},
        "medium": {"Equity": 40, "Debt": 40, "Alternatives": 20},
        "high": {"Equity": 60, "Debt": 20, "Alternatives": 20}
    }
    risk_level = result["risk_level"]
    allocation = allocations.get(risk_level, allocations["medium"])
    labels = list(allocation.keys())
    values = list(allocation.values())
    
    colors = ['#2ca02c', '#1f77b4', '#ff7f0e']  # Green, Blue, Orange

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+percent'
    )])
    fig.update_layout(paper_bgcolor='white')
    fig.update_layout(title="📊 Recommended Asset Allocation", legend=dict(orientation="h"))
    st.subheader("📉 Asset Allocation Chart")
    st.plotly_chart(fig, use_container_width=True)

    # --- PDF Download ---
    img_buffer = io.BytesIO()
    fig.write_image(img_buffer, format="png")
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")
    img_html = f'<img src="data:image/png;base64,{img_base64}" width="500"/>'

    html_content = f"""
    <h2>📊 Risk Profile</h2>
    <p><strong>Risk Level:</strong> {result['risk_level'].capitalize()}</p>
    <p>{result['risk_explanation']}</p>
    <h2>📰 Market Summary</h2>
    <p>{result['news_summary']}</p>
    <h2>📉 Asset Allocation Chart</h2>
    {img_html}
    """
    pdf_path = generate_pdf(html_content)

    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="FinGenie_Report.pdf">📄 Download Report</a>'
    st.markdown(href, unsafe_allow_html=True)

if "result" in st.session_state:
    st.subheader("🤔 Ask About Your Plan")
    user_question = st.text_input("Type a question related to your investment plan:")

    if user_question:
        prompt = f"""
You are a financial advisor AI. Answer the user’s question based on the following context:

Age: {st.session_state.age}
Investment Goal: {st.session_state.goal}
Investment Horizon: {st.session_state.horizon} years
Risk Level: {st.session_state.result['risk_level']}
Risk Explanation: {st.session_state.result['risk_explanation']}
Market Summary: {st.session_state.result['news_summary']}

User Question: {user_question}

Provide a clear, concise, helpful answer.
"""
        try:
            st.info("Generating answer...")
            response = llm.invoke([HumanMessage(content=prompt)])
            st.markdown(f"**Answer:** {response.content.strip()}")
        except Exception as e:
            st.error(f"⚠️ Error while generating answer: {e}")
