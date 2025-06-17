

# 💰 FinGenie – Your AI Financial Advisor

FinGenie is an intelligent investment advisory assistant powered by LLaMA 3 via Groq and built with Streamlit. It analyzes your goals, risk appetite, and market trends to give you clear, actionable advice – complete with downloadable reports and a user-friendly dashboard.

---

## 🚀 Features

- 📊 Personalized risk assessment & asset allocation
- 📰 Real-time market sentiment analysis
- 🧠 GPT-powered Q&A about your financial plan
- 📄 PDF report generation with chart
- ☁️ Firebase logging for user analytics
- 🖥️ Admin dashboard with charts and downloads

---

## 🛠 Tech Stack

- Python 3.12
- Streamlit
- LangChain + Groq (LLaMA 3)
- Firebase Realtime DB
- Plotly
- PDFKit + wkhtmltopdf

---

## 📦 Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/Krushbiradar18/FinGenie.git
cd FinGenie

	2.	Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate

	3.	Install Dependencies

pip install -r requirements.txt

	4.	Configure Environment Variables

Create a .env file using the template below:

GROQ_API_KEY=your_groq_api_key
FIREBASE_URL=https://your-project.firebaseio.com

Or use .env.example as a reference.
	5.	Run the App

streamlit run streamlit_app/app.py


⸻

🧪 Firebase Admin Dashboard

To view user logs, run:

streamlit run streamlit_app/dashboard.py


⸻

🌐 Deployment

Deploy on Streamlit Cloud
	1.	Push your repo to GitHub
	2.	Go to Streamlit Cloud → New App
	3.	Set file path to: streamlit_app/app.py
	4.	Add secrets under Settings → Secrets:

GROQ_API_KEY=your_groq_api_key
FIREBASE_URL=https://your-project.firebaseio.com


⸻

📸 Screenshots

You can add screenshots or GIFs of the app UI here later for extra polish.

⸻

👩‍💻 Developer

Made with ❤️ by Krushnali Biradar
GitHub · LinkedIn


