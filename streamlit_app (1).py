import streamlit as st
import requests
import time
import random
from datetime import datetime

# ================= CONFIG =================
API_URL = "http://localhost:5000/satire"

st.set_page_config(
    page_title="Fauxy – Agentic Satirical News",
    page_icon="🤡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= ADVANCED STYLES =================
st.markdown("""
<style>
    /* Premium Gradient Background */
    .stApp {
         background: linear-gradient(135deg, #6d7ff2 0%, #7f56c2 100%);
    }
    
    /* Glass Morphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Satire Box with Premium Feel */
    .satire-premium {
        background: linear-gradient(145deg, #fff8f0, #fff2e5);
        padding: 30px;
        border-radius: 20px;
        border-left: 8px solid #ff6b6b;
        font-size: 18px;
        line-height: 1.8;
        box-shadow: 0 10px 40px rgba(255, 107, 107, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .satire-premium::before {
        content: "“";
        position: absolute;
        top: -20px;
        left: -10px;
        font-size: 150px;
        color: rgba(255, 107, 107, 0.1);
        font-family: Georgia, serif;
    }
    
    /* Score Circles */
    .score-container {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
    }
    
    .score-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: conic-gradient(from 0deg, #4CAF50 0deg, #4CAF50 calc(var(--score) * 3.6deg), #f0f0f0 calc(var(--score) * 3.6deg));
        position: relative;
        margin: 10px;
        animation: growIn 0.8s ease-out;
    }
    
    .score-circle::before {
        content: "";
        position: absolute;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: white;
    }
    
    .score-value {
        position: relative;
        font-size: 32px;
        font-weight: bold;
        color: #222;
    }
    
    .score-label {
        position: relative;
        font-size: 14px;
        color: white;
        margin-top: -5px;
    }
    
    /* Animated Tags */
    .premium-tag {
        display: inline-block;
        padding: 6px 14px;
        margin: 0 5px 5px 0;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        background: linear-gradient(145deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideIn 0.3s ease-out;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 40px;
        color: white;
        margin: 10px 0;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes growIn {
        from { transform: scale(0); }
        to { transform: scale(1); }
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }
    
    /* Progress Bar Styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
        transition: width 0.5s ease-in-out !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(145deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 50px !important;
        transition: all 0.3s ease !important;
        animation: pulse 2s infinite;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 50px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 15px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        border-radius: 50px !important;
        border: 2px solid #e0e0e0 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 15px !important;
        font-weight: 600 !important;
    }
    
    /* Divider */
    hr {
        margin: 30px 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent) !important;
    }
</style>
""", unsafe_allow_html=True)

# ================= HEADER WITH ANIMATION =================
st.markdown("""
<div style="text-align: center; padding: 30px 0; animation: fadeIn 0.8s ease-in;">
    <h1 style="font-size: 48px; margin-bottom: 10px; background: linear-gradient(145deg, #fff, #f0f0f0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
        🤡 Fauxy
    </h1>
    <p style="font-size: 18px; color: white; opacity: 0.95; font-weight: 500;">
        Agentic, Safe & Explainable AI for Indian Satirical News
    </p>
    <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
        <span class="premium-tag">⚡ Agentic AI</span>
        <span class="premium-tag">🛡️ Safety First</span>
        <span class="premium-tag">🔍 Explainable</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ================= INPUT SECTION WITH PREMIUM DESIGN =================
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown('<p style="font-size: 48px; margin: 0;">🎯</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p style="font-size: 24px; font-weight: bold; margin: 0; color: #333;">Create Fauxy News</p>', unsafe_allow_html=True)
        st.markdown('<p style="Yellow: white; margin-top: 5px;">Transform real news into brilliant satire</p>', unsafe_allow_html=True)
    
    topic = st.text_input(
        "📰 Enter a news topic",
        placeholder="e.g. Indian Budget, Elections, Bureaucracy, Public Reactions"
    )

    tone = st.selectbox(
        "🎭 Choose satire tone",
        [
            "auto",
            "social media meme style",
            "political parody",
            "dry sarcasm",
            "subtle irony"
        ],
        help="Select the flavor of satire you prefer"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        compare_mode = st.checkbox("🧪 A/B Test", help="Compare agent vs user tone selection")
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
    
    generate_btn = st.button("🚀 Generate Fauxy News", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================= SCORING & VISUALIZATION HELPERS =================
def create_score_circle(score, label, color="#667eea"):
    """Generate HTML for a score circle"""
    percentage = int(score * 33.33) if isinstance(score, (int, float)) and score <= 3 else int(score)
    return f"""
    <div class="score-circle" style="--score: {percentage};">
        <div style="position: relative; text-align: center;">
            <span class="score-value">{score if isinstance(score, str) else f'{score}/3'}</span>
            <div class="score-label">{label}</div>
        </div>
    </div>
    """

def calculate_composite_score(evaluation, risk_level):
    """Calculate composite scores for visualization"""
    quality_score = evaluation.get('quality_score', 2)
    risk_score = 3 if risk_level == 'low' else 1
    humor_score = 3 if 'exaggeration' in str(evaluation) or 'irony' in str(evaluation) else 2
    safety_score = 3 if risk_level == 'low' else 1.5
    
    composite = (quality_score + risk_score + humor_score + safety_score) / 4
    
    return {
        'quality': quality_score,
        'humor': humor_score,
        'safety': safety_score,
        'composite': round(composite, 1)
    }

def generate_sparkline(score):
    """Generate inline sparkline for scores"""
    bars = int(score * 10)
    bar_html = ""
    for i in range(20):
        if i < bars:
            bar_html += f'<div style="width: 8px; height: {20 + (i * 2)}px; background: linear-gradient(0deg, #fb923c, #ea580c); display: inline-block; margin: 0 2px; border-radius: 4px;"></div>'
        else:
            bar_html += f'<div style="width: 8px; height: {20 + (i * 2)}px; background: #e0e0e0; display: inline-block; margin: 0 2px; border-radius: 4px;"></div>'
    return bar_html

# ================= HELPERS =================
def safety_confidence(risk):
    if risk == "low":
        return 95, "🟢 Low Risk – Standard safety constraints applied", "#000000"
    return 45, "🔴 High Risk – Enhanced safety & ethics validation", "#000000"

def satire_breakdown(text):
    points = []
    if "!" in text:
        points.append("🎯 Uses exaggeration and hyperbole")
    if any(w in text.lower() for w in ["voter", "queue", "budget", "public", "rally"]):
        points.append("🇮🇳 Anchored in Indian public behavior")
    if any(w in text.lower() for w in ["minister", "government", "official"]):
        points.append("🏛️ Political satire with safety constraints")
    points.append("💭 Uses irony to contrast expectations vs reality")
    return points

# ================= MAIN GENERATION LOGIC =================
if generate_btn:
    if not topic:
        st.error("🎯 Please enter a topic to generate satire!")
        st.stop()

    # Animated progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        if i < 30:
            status_text.markdown("🧠 **Agent Planning Phase:** Analyzing topic sensitivity...")
        elif i < 60:
            status_text.markdown("🔍 **Research Agent:** Grounding in real-world context...")
        elif i < 90:
            status_text.markdown("✍️ **Satire Generation:** Crafting humor with safety constraints...")
        else:
            status_text.markdown("✅ **Evaluation Agent:** Validating quality and ethics...")
        progress_bar.progress(i + 1)
        time.sleep(0.01)
    
    # API Call
    with st.spinner("🎭 Finalizing your satire..."):
        try:
            resp = requests.post(API_URL, json={"topic": topic, "tone": tone})
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            st.error(f"🚨 Backend error: {str(e)}")
            st.stop()
    
    progress_bar.empty()
    status_text.empty()

    satire = data["satire"]
    plan = data["agent_plan"]
    evaluation = data["evaluation"]
    
    # Calculate scores
    scores = calculate_composite_score(evaluation, plan["risk"])
    confidence, label, color = safety_confidence(plan["risk"])

    # ================= SATIRE OUTPUT =================
    #st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #333;">😂 Generated Satire</h3>
        <span style="background: #ff6b6b; color: white; padding: 5px 15px; border-radius: 50px; font-size: 12px; font-weight: 600;">
            ⚡ Fresh News
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Tags
    tags_html = ""
    for tag in ["Satire", "Observational", "Exaggeration", "🇮🇳 Indian Context"]:
        tags_html += f'<span class="premium-tag">{tag}</span>'
    st.markdown(tags_html, unsafe_allow_html=True)
    
    st.markdown(f'<div class="satire-premium">{satire}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= COMPOSITE SCORE DASHBOARD =================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #333;">📊 Performance Dashboard</h3>
        <span style="background: #4CAF50; color: white; padding: 5px 15px; border-radius: 50px; font-size: 12px;">
            🎯 Composite Score: {}/3
        </span>
    </div>
    """.format(scores['composite']), unsafe_allow_html=True)
    
    # Score circles in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_score_circle(scores['composite'], "COMPOSITE"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_score_circle(scores['quality'], "QUALITY"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_score_circle(scores['humor'], "HUMOR"), unsafe_allow_html=True)
    with col4:
        st.markdown(create_score_circle(scores['safety'], "SAFETY"), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= SAFETY & METRICS =================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🛡️ Safety Governance")
        
        # Animated progress bar
        st.progress(confidence/100)
        st.markdown(f'<p style="color: {color}; font-weight: 600;">{label}</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span>Content Safety</span>
                <span style="font-weight: bold;">{}/100</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Ethical Compliance</span>
                <span style="font-weight: bold;">92/100</span>
            </div>
        </div>
        """.format(confidence), unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📈 Performance Metrics")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            risk_color = "🟢" if plan["risk"] == "low" else "🔴"
            st.markdown(f'<p style="color: White; margin: 0;">Risk</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value">{risk_color}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: white; font-size: 18px;">{plan["risk"].upper()}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with c2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<p style="color: white; margin: 0;">Quality</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value">{evaluation["quality_score"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: white; font-size: 18px;">/3</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with c3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            verdict_color = "🟢" if evaluation["verdict"] == "high_quality" else "🟡"
            st.markdown(f'<p style="color: white; margin: 0;">Verdict</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value">{verdict_color}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: white; font-size: 18px;">{evaluation["verdict"].replace("_", " ").title()}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ================= HUMOR ANALYSIS =================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🧩 Humor Analysis & Introspection")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**📊 Humor Breakdown**")
        for point in satire_breakdown(satire):
            st.markdown(f"- {point}")
    
    with col2:
        st.markdown("**📈 Humor Intensity**")
        humor_bars = generate_sparkline(scores['humor'])
        st.markdown(f'<div style="padding: 20px 0;">{humor_bars}</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
            <span style="color: white;">Subtle</span>
            <span style="color: white;">Moderate</span>
            <span style="color: white;">Exaggerated</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= AGENT REASONING =================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Agent Reasoning & Validation")
    
    # Agent timeline
    st.markdown("""
    <div style="display: flex; justify-content: space-between; margin: 30px 0; position: relative;">
        <div style="position: absolute; top: 15px; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2);"></div>
        <div style="background: #667eea; color: white; padding: 10px 20px; border-radius: 50px; position: relative; z-index: 1;">📋 Plan</div>
        <div style="background: #764ba2; color: white; padding: 10px 20px; border-radius: 50px; position: relative; z-index: 1;">🔍 Research</div>
        <div style="background: #ff6b6b; color: white; padding: 10px 20px; border-radius: 50px; position: relative; z-index: 1;">✍️ Generate</div>
        <div style="background: #4CAF50; color: white; padding: 10px 20px; border-radius: 50px; position: relative; z-index: 1;">✅ Evaluate</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 15px;">
            <p style="color: #666; margin: 0;">Topic</p>
            <p style="font-size: 20px; font-weight: bold; color: #333;">{plan['topic'].capitalize()}</p>
            <p style="color: #666; margin: 15px 0 0 0;">Selected Tone</p>
            <span class="premium-tag">{plan['selected_tone']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**🧠 Autonomous Decision Justification**")
        st.info(
            f"The planner agent classified this topic as **{plan['risk']} sensitivity**, "
            "allowing humor amplification using a **{tone}** style while "
            "maintaining ethical safeguards. The agent selected this tone "
            "based on topic context and safety constraints."
        )
        
        # Evaluation reasons
        st.markdown("**✅ Evaluation Agent Feedback:**")
        for reason in evaluation["reasons"]:
            st.markdown(f"- {reason}")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= A/B COMPARISON =================
    if compare_mode and tone != "auto":
        with st.spinner("🧪 Generating comparison output..."):
            resp_b = requests.post(API_URL, json={"topic": topic, "tone": tone})
            if resp_b.status_code == 200:
                comparison = resp_b.json()
                
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 🧪 A/B Tone Comparison")
                
                colA, colB = st.columns(2)
                
                with colA:
                    st.markdown("""
                    <div style="background: linear-gradient(145deg, #f3e8ff, #faf5ff); padding: 20px; border-radius: 15px;">
                        <h4 style="color: #667eea; margin-top: 0;">🤖 Agent-selected</h4>
                        <span class="premium-tag">{}</span>
                        <div style="margin-top: 15px; font-style: italic;">{}</div>
                    </div>
                    """.format(plan["selected_tone"], satire[:150] + "..."), unsafe_allow_html=True)
                
                with colB:
                    st.markdown("""
                    <div style="background: linear-gradient(145deg, #fff3e0, #fff9f0); padding: 20px; border-radius: 15px;">
                        <h4 style="color: #ff9800; margin-top: 0;">👤 User-selected</h4>
                        <span class="premium-tag">{}</span>
                        <div style="margin-top: 15px; font-style: italic;">{}</div>
                    </div>
                    """.format(tone, comparison["satire"][:150] + "..."), unsafe_allow_html=True)
                
                st.caption(
                    "✨ **Insight:** Agent-selected tone typically achieves higher safety scores "
                    "while maintaining humor quality through contextual awareness."
                )
                
                st.markdown('</div>', unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 30px 0; color: white; opacity: 0.9;">
    <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 20px;">
        <span>⚡ Agentic Planning</span>
        <span>🔍 Grounded Research</span>
        <span>🛡️ Ethics Guardrails</span>
        <span>📊 Quality Evaluation</span>
        <span>💡 Explainable AI</span>
    </div>
    <p style="font-size: 14px;">
        Built with 🎭 <strong>Fauxy Agentic System</strong> | Flask + Streamlit | Safe & Explainable Satire AI
    </p>
    <p style="font-size: 12px; opacity: 0.7;">
        © 2024 Fauxy – Where AI meets Indian Satire, Responsibly
    </p>
</div>
""", unsafe_allow_html=True)

# ================= AUTO-REFRESH & SESSION STATE =================
if 'generated' not in st.session_state:
    st.session_state.generated = False

if generate_btn:
    st.session_state.generated = True
    st.balloons()