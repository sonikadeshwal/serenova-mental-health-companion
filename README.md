# 🌿 Serenova — AI Mental Health Companion

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white"/>
  <img src="https://img.shields.io/badge/LLaMA_3.3_70B-blueviolet?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Live-Deployed-brightgreen?style=for-the-badge"/>
</p>

<p align="center">
  <b>A conversational AI chatbot that understands how you feel — not just what you say.</b><br/>
  Detects emotional tone, responds with empathy, and tracks your mood across the session.
</p>

<p align="center">
  <a href="https://serenova-mental-health-companion-79u5ebfcykwmhnkhcuetwk.streamlit.app/">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit"/>
  </a>
</p>

---

## 🧠 What is Serenova?

Serenova is an **AI-powered mental health companion** built as a full-stack NLP project. It goes beyond simple chatbots by combining **real-time sentiment analysis**, **LLM-driven empathetic responses**, and **session-based mood tracking with visual analytics** — all wrapped in a clean, calming interface designed for emotional safety.

This project was built to explore how Large Language Models can be applied responsibly in the mental wellness space, combining NLP, data visualization, and accessible UI design.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **Empathetic AI Responses** | Powered by LLaMA 3.3 70B via Groq — context-aware, warm, non-judgmental replies |
| 🎭 **Real-time Mood Detection** | Classifies emotional tone from every message (happy, sad, anxious, calm, etc.) |
| 📊 **Session Mood Tracking** | Live Plotly chart tracking your mood score across the conversation |
| 💡 **Dynamic Coping Strategies** | Sidebar updates with relevant strategies based on what you share |
| 📈 **Session Analytics** | Message count, average mood, peak mood, and trend indicator |
| ⚡ **Fast Inference** | Groq's LPU hardware gives near-instant response times |
| 🎨 **Calming White UI** | Custom-styled Streamlit with DM Serif Display typography and sage green accents |

---

## 🛠️ Tech Stack

```
Frontend     →  Streamlit (custom CSS + Google Fonts)
AI Backend   →  Groq API  (LLaMA 3.3 70B Versatile)
NLP          →  Prompt engineering for sentiment classification + response generation
Visualization→  Plotly (interactive mood history line chart)
Deployment   →  Streamlit Cloud
```

---

## 📁 Project Structure

```
serenova-mental-health-companion/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md
├── .gitignore
└── .streamlit/
    ├── config.toml         # Theme configuration
    └── secrets.toml        # API key (NOT pushed to GitHub)
```

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/sonikadeshwal/serenova-mental-health-companion.git
cd serenova-mental-health-companion
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Groq API key**

Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```
Get a free key at [console.groq.com](https://console.groq.com) — no credit card needed.

**4. Run**
```bash
streamlit run app.py
```

---

## 🌐 Live Demo

👉 **[serenova-mental-health-companion.streamlit.app](https://serenova-mental-health-companion-79u5ebfcykwmhnkhcuetwk.streamlit.app/)**

---

## 💡 How It Works

```
User types a message
        ↓
Message sent to LLaMA 3.3 70B (via Groq API)
with a system prompt that instructs the model to:
  • Respond empathetically
  • Classify mood  →  MOOD_TAG
  • Generate coping strategies  →  COPING_STRATEGIES
        ↓
Response parsed → mood tag extracted → score mapped (0–100)
        ↓
UI updates: chat bubble + mood meter + chart + coping sidebar
```

---

## ⚠️ Disclaimer

Serenova is an AI project built for educational and portfolio purposes. It is **not a substitute for professional mental health care**.

If you or someone you know is in crisis, please reach out:
- 🇮🇳 **iCall (India):** 9152987821
- 🌍 **Crisis Text Line:** Text HOME to 741741

---

## 👩‍💻 Author

**Sonika Deshwal**  
B.Tech CSE (AI & ML) — Lovely Professional University

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/sonikadeshwal)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/sonikadeshwal)
[![Portfolio](https://img.shields.io/badge/Portfolio-2d4a3e?style=flat&logo=google-chrome&logoColor=white)](https://sonikadeshwal.netlify.app)

---

<p align="center">Made with 🌿 and a lot of empathy</p>
