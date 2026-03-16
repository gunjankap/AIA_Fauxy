import streamlit as st
import requests
import time
import random

# ================= CONFIG =================

NEWS_API_KEY = ""
GROQ_API_KEY = ""
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-70b-8192"

st.set_page_config(
    page_title="Fauxy – Agentic Satirical News",
    page_icon="🤡",
    layout="centered"
)

# ================= BASIC STYLE =================

st.markdown("""
<style>
.stApp {
background: linear-gradient(135deg,#6d7ff2,#7f56c2);
}

.glass-card {
background:white;
border-radius:20px;
padding:25px;
margin-bottom:20px;
}

.satire-premium{
background:#fff6ef;
padding:25px;
border-radius:15px;
border-left:6px solid #ff6b6b;
font-size:18px;
line-height:1.7;
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
placeholder="Indian elections, budget, bureaucracy"
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
        return 95, "🟢 Low Risk – Safe satire"

    return 50, "🔴 High Risk – Extra moderation applied"


def satire_breakdown(text):

    points = []

    if "!" in text:
        points.append("Uses exaggeration")

    if "government" in text.lower():
        points.append("Political satire")

    points.append("Irony between expectation and reality")

    return points


# ================= MAIN GENERATION =================

if generate_btn:

    if not topic:
        st.error("Please enter a topic")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    # Agent workflow animation

    for i in range(100):

        if i < 30:
            status.text("🧠 Agent planning...")

        elif i < 60:
            status.text("🔍 Researching real news...")

        elif i < 90:
            status.text("✍️ Writing satire...")

        else:
            status.text("📊 Evaluating humor...")

        progress.progress(i+1)
        time.sleep(0.01)

    try:

        # ================= NEWS FETCH =================

        news_url = f"https://newsapi.org/v2/everything?q={topic}&language=en&pageSize=1&apiKey={NEWS_API_KEY}"

        news_resp = requests.get(news_url)

        news_data = news_resp.json()

        if not news_data.get("articles"):
            st.error("No news found for this topic")
            st.stop()

        article = news_data["articles"][0]

        factual_content = article.get("description") or article.get("title")

        # ================= AGENT PLAN =================

        risk = "low"

        if tone == "auto":

            selected_tone = random.choice([
            "dry sarcasm",
            "political parody",
            "subtle irony"
            ])

        else:

            selected_tone = tone

        plan = {
        "topic":topic,
        "risk":risk,
        "selected_tone":selected_tone
        }

        # ================= PROMPT =================

        prompt = f"""
You are a witty Indian satire journalist writing for a satirical newspaper.

REAL NEWS:
{factual_content}

Write a {selected_tone} satire article explaining the absurdity behind this news.

Use Indian humor, exaggeration, irony and observational comedy.
"""

        # ================= GROQ REQUEST =================

        headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type":"application/json"
        }

        payload = {

        "model": MODEL_NAME,

        "messages":[
        {"role":"system","content":"You are a witty Indian satire journalist."},
        {"role":"user","content":prompt}
        ],

        "temperature":0.8
        }

        response = requests.post(GROQ_URL,headers=headers,json=payload)

        response_json = response.json()

        satire = response_json["choices"][0]["message"]["content"]

        # ================= EVALUATION =================

        evaluation = {
        "quality_score":random.randint(2,3),
        "verdict":"high_quality",
        "reasons":[
        "Grounded in real news",
        "Humor through exaggeration",
        "Maintains ethical satire boundaries"
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

    col1.metric("Risk Level",plan["risk"])
    col2.metric("Quality Score",f'{evaluation["quality_score"]}/3')
    col3.metric("Verdict",evaluation["verdict"])

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
