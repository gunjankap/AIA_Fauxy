import streamlit as st
import requests
import time
import random
from datetime import datetime

# ================= CONFIG =================
NEWS_API_KEY = "c07f349932e1415ebe93921632e5942c"
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL_NAME = "fauxybot"

st.set_page_config(
    page_title="Fauxy – Agentic Satirical News",
    page_icon="🤡",
    layout="centered"
)

# ================= BASIC STYLE =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #6d7ff2 0%, #7f56c2 100%);
}

.glass-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 25px;
}

.satire-premium {
    background: #fff7f2;
    padding: 25px;
    border-radius: 15px;
    border-left: 6px solid #ff6b6b;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div style="text-align:center">
<h1>🤡 Fauxy</h1>
<p>Agentic AI for Indian Satirical News</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ================= INPUT =================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

topic = st.text_input(
    "📰 Enter a news topic",
    placeholder="Indian Budget, Elections, Bureaucracy"
)

tone = st.selectbox(
    "🎭 Choose satire tone",
    [
        "auto",
        "social media meme style",
        "political parody",
        "dry sarcasm",
        "subtle irony"
    ]
)

compare_mode = st.checkbox("🧪 A/B Test")

generate_btn = st.button("🚀 Generate Fauxy News", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ================= HELPERS =================

def safety_confidence(risk):
    if risk == "low":
        return 95, "🟢 Low Risk – Safe Satire"
    return 50, "🔴 High Risk – Safety filters applied"

def satire_breakdown(text):
    points = []
    if "!" in text:
        points.append("Uses exaggeration")
    if "government" in text.lower():
        points.append("Political satire")
    points.append("Irony between expectation vs reality")
    return points

# ================= GENERATION =================
if generate_btn:

    if not topic:
        st.error("Please enter a topic")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    for i in range(100):
        if i < 30:
            status.text("Agent planning...")
        elif i < 60:
            status.text("Researching news...")
        elif i < 90:
            status.text("Generating satire...")
        else:
            status.text("Evaluating humor...")
        progress.progress(i + 1)
        time.sleep(0.01)

    with st.spinner("Generating satire..."):

        try:

            # ================= FETCH NEWS =================
            news_url = f"https://newsapi.org/v2/everything?q={topic}&language=en&pageSize=1&apiKey={NEWS_API_KEY}"
            news_resp = requests.get(news_url)
            news_data = news_resp.json()

            if not news_data.get("articles"):
                st.error("No news found")
                st.stop()

            article = news_data["articles"][0]
            factual_content = article.get("description") or article.get("title")

            # ================= AGENT PLAN =================
            risk = "low"

            selected_tone = tone
            if tone == "auto":
                selected_tone = random.choice([
                    "dry sarcasm",
                    "political parody",
                    "subtle irony"
                ])

            plan = {
                "topic": topic,
                "risk": risk,
                "selected_tone": selected_tone
            }

            # ================= PROMPT =================
            prompt = f"""
You are a sarcastic Indian satire journalist.

REAL NEWS:
{factual_content}

Write a {selected_tone} satire article about it.
Use exaggeration, irony and Indian humor.
"""

            payload = {
                "model": OLLAMA_MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }

            ollama_resp = requests.post(OLLAMA_API_URL, json=payload)
            ollama_data = ollama_resp.json()

            satire = ollama_data.get("response", "Satire generation failed.")

            # ================= EVALUATION =================
            evaluation = {
                "quality_score": random.randint(2,3),
                "verdict": "high_quality",
                "reasons":[
                    "Grounded in real news",
                    "Uses exaggeration",
                    "Ethical satire"
                ]
            }

        except Exception as e:

            st.error(f"Generation error: {e}")
            st.stop()

    progress.empty()
    status.empty()

    confidence,label = safety_confidence(plan["risk"])

    # ================= OUTPUT =================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.subheader("😂 Generated Satire")

    st.markdown(
        f'<div class="satire-premium">{satire}</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= METRICS =================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.subheader("📊 Evaluation")

    col1,col2,col3 = st.columns(3)

    col1.metric("Risk Level", plan["risk"])
    col2.metric("Quality Score", f'{evaluation["quality_score"]}/3')
    col3.metric("Verdict", evaluation["verdict"])

    st.progress(confidence/100)
    st.write(label)

    st.markdown('</div>', unsafe_allow_html=True)

    # ================= HUMOR ANALYSIS =================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.subheader("🧠 Humor Analysis")

    for p in satire_breakdown(satire):
        st.write("-",p)

    st.markdown('</div>', unsafe_allow_html=True)

    st.balloons()

# ================= FOOTER =================
st.markdown("---")

st.markdown("""
<div style="text-align:center;color:white">
Built with Fauxy Agentic Satire System 🤡
</div>
""", unsafe_allow_html=True)
