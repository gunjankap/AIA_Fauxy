# =========================================================
# Fauxy Agentic Satirical News System (Final Polished)
# =========================================================

from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------- CONFIG --------------------

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


# -------------------- AGENTS --------------------

def planner_agent(topic, tone):
    plan = {
        "topic": topic,
        "user_tone": tone,
        "risk": "low",
        "needs_ethics_check": True,
        "needs_evaluation": True
    }

    # Autonomous tone selection
    if tone is None or tone.lower() == "auto":
        plan["selected_tone"] = "social media meme style"
    else:
        plan["selected_tone"] = tone

    # Risk-based override
    if any(k in topic.lower() for k in ["election", "politics", "government", "parliament"]):
        plan["risk"] = "high"
        plan["selected_tone"] = "subtle irony"

    return plan


def research_agent(topic):
    url = (
        "https://newsapi.org/v2/everything"
        f"?q={topic}&language=en&pageSize=1&apiKey={NEWS_API_KEY}"
    )

    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    if not data.get("articles"):
        raise ValueError("No relevant news articles found")

    article = data["articles"][0]
    factual = (
        article.get("description")
        or article.get("title")
        or "General public discussion around the topic."
    )

    return {
        "factual_content": factual,
        "satire_angle": "exaggerated Indian public reaction"
    }


def satire_agent(plan, research):
    prompt = f"""
You are a writer for 'The Fauxy', a satirical Indian news outlet.

STRICT CONSTRAINTS:
- The satire MUST focus ONLY on India
- Use Indian election culture: voters, rallies, slogans, bureaucracy, queues
- Do NOT mention foreign countries, cultures, or personalities
- Do NOT name real politicians directly
- Keep it humorous, fictional, and safe

Topic: {plan['topic']}
Tone: {plan['selected_tone']}
Risk Level: {plan['risk']}

FACTUAL CONTEXT:
{research['factual_content']}

Write ONE short satirical paragraph ending with a fake quote.
"""

    payload = {
        "model": GROQ_MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": "You write sharp but safe Indian political satire."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 220
    }

    resp = call_groq(payload)
    resp.raise_for_status()

    result = resp.json()
    return result["choices"][0]["message"]["content"].strip()


def ethics_agent(text, plan):
    banned_words = ["kill", "violence", "hate", "genocide"]

    for word in banned_words:
        if word in text.lower():
            return False

    # Extra safety for political topics
    if plan["risk"] == "high":
        forbidden = ["religion", "caste", "specific politician", "real name"]
        for word in forbidden:
            if word in text.lower():
                return False

    return True


def evaluator_agent(text):
    score = 0
    reasons = []

    if len(text) > 120:
        score += 1
        reasons.append("Adequate length")

    if any(w in text.lower() for w in ["voter", "rally", "election", "ballot", "queue"]):
        score += 1
        reasons.append("Strong election relevance")

    if "!" in text or "said" in text.lower():
        score += 1
        reasons.append("Clear satirical tone")

    return {
        "quality_score": score,
        "verdict": "high" if score >= 2 else "average",
        "reasons": reasons
    }


# -------------------- GROQ CALL --------------------

def call_groq(payload):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    return requests.post(
        GROQ_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )


# -------------------- API ENDPOINT --------------------

@app.route("/satire", methods=["POST"])
def generate_satire():
    data = request.get_json(force=True, silent=True)

    if not data or "topic" not in data:
        return jsonify({"error": "Missing 'topic' field"}), 400

    topic = data["topic"]
    tone = data.get("tone")

    try:
        # 1. Planning
        plan = planner_agent(topic, tone)

        # 2. Research
        research = research_agent(topic)

        # 3. Generation
        satire = satire_agent(plan, research)

        # 4. Ethics validation
        if plan["needs_ethics_check"] and not ethics_agent(satire, plan):
            return jsonify({"error": "Ethical validation failed"}), 400

        # 5. Evaluation
        evaluation = evaluator_agent(satire)

        return jsonify({
            "topic": topic,
            "satire": satire,
            "agent_plan": plan,
            "evaluation": evaluation
        })

    except Exception as e:
        print("BACKEND ERROR:", e)
        return jsonify({"error": str(e)}), 500


# -------------------- RUN --------------------

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
