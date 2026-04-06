import streamlit as st
from groq import Groq
import plotly.graph_objects as go
from datetime import datetime
import re

st.set_page_config(
    page_title="Serenova – AI Mental Health Companion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* White background everywhere */
.stApp { background-color: #ffffff !important; }
section[data-testid="stSidebar"] { background-color: #fcfaf7 !important; border-right: 1px solid #f0ede8; }

/* Header */
.mhc-header {
    display: flex; align-items: center; gap: 12px;
    padding: 0 0 18px 0; border-bottom: 1px solid #f0ede8; margin-bottom: 20px;
}
.mhc-title { font-family: 'DM Serif Display', serif; font-size: 26px; color: #2d4a3e; margin: 0; }
.mhc-sub { font-size: 12px; color: #8a9e96; margin: 0; }

/* Chat bubbles */
.bubble-ai {
    background: #f7f4ef; border-radius: 16px 16px 16px 4px;
    padding: 13px 16px; margin: 6px 0; font-size: 14px;
    color: #2a2a2a; line-height: 1.65; max-width: 82%;
}
.bubble-user {
    background: #2d4a3e; border-radius: 16px 16px 4px 16px;
    padding: 13px 16px; margin: 6px 0; font-size: 14px;
    color: #f0ede8; line-height: 1.65; max-width: 82%;
    margin-left: auto;
}
.msg-row-ai  { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px; }
.msg-row-user { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px; flex-direction: row-reverse; }
.avatar-ai   { width:34px;height:34px;background:linear-gradient(135deg,#c8dfc9,#a8c5b5);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0; }
.avatar-user { width:34px;height:34px;background:linear-gradient(135deg,#e8d5c4,#d4b896);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#5a3e28;flex-shrink:0; }
.meta        { font-size: 10px; color: #bbb; margin-top: 4px; }
.meta-user   { text-align: right; }

/* Mood badge */
.badge { display:inline-block; font-size:11px; font-weight:600; padding:3px 9px; border-radius:12px; margin-left:6px; }
.badge-positive { background:#e8f5e9; color:#2e7d32; }
.badge-negative { background:#fce4ec; color:#c62828; }
.badge-neutral  { background:#f3f0e8; color:#6d6044; }
.badge-anxious  { background:#fff3e0; color:#e65100; }

/* Stat cards */
.stat-card  { background:#f7f4ef; border-radius:12px; padding:12px; text-align:center; }
.stat-val   { font-size:22px; font-weight:600; color:#2d4a3e; }
.stat-lbl   { font-size:10px; color:#9a8f82; font-weight:500; margin-top:2px; }

/* Coping card */
.coping-card { background:#ffffff; border:1px solid #f0ede8; border-radius:12px; padding:14px; margin-top:10px; }
.coping-item { display:flex; gap:8px; align-items:flex-start; padding:6px 0; border-bottom:1px solid #f7f4ef; font-size:13px; color:#4a4a4a; }
.coping-item:last-child { border-bottom:none; }
.c-icon { width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;flex-shrink:0; }

/* Input */
.stTextArea textarea { border-radius: 14px !important; border: 1.5px solid #e0dbd5 !important; font-family: 'DM Sans', sans-serif !important; font-size:14px !important; background: #fdfcfa !important; }
.stTextArea textarea:focus { border-color: #7c9a92 !important; box-shadow: none !important; }

/* Buttons */
.stButton > button { border-radius: 22px !important; border: 1.5px solid #e0dbd5 !important; background: #fdfcfa !important; color: #6d6a65 !important; font-size: 13px !important; padding: 5px 14px !important; font-family: 'DM Sans', sans-serif !important; transition: all 0.2s; }
.stButton > button:hover { border-color: #7c9a92 !important; color: #2d4a3e !important; background: #f0f7f4 !important; }

div[data-testid="stHorizontalBlock"] { gap: 8px !important; }

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Disclaimer */
.disclaimer { font-size:11px; color:#aaa; text-align:center; padding:12px; border-top:1px solid #f0ede8; margin-top:16px; line-height:1.6; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────
if "messages"       not in st.session_state: st.session_state.messages = []
if "mood_history"   not in st.session_state: st.session_state.mood_history = []
if "coping_tips"    not in st.session_state: st.session_state.coping_tips = [
    ("🌬️", "#e8f5e9", "#2e7d32", "4-7-8 breathing: inhale 4s, hold 7s, exhale 8s"),
    ("📔", "#e3f2fd", "#1565c0", "Journal 3 things you're grateful for today"),
    ("🚶", "#fff3e0", "#e65100", "A 10-minute walk can meaningfully shift your mood"),
]
if "msg_count"      not in st.session_state: st.session_state.msg_count = 0

MOOD_MAP = {
    "positive":    ("Positive",    75,  "#7ec8a0", "badge-positive"),
    "happy":       ("Happy",       88,  "#7ec8a0", "badge-positive"),
    "hopeful":     ("Hopeful",     70,  "#a8c5b5", "badge-positive"),
    "calm":        ("Calm",        65,  "#a8c5b5", "badge-positive"),
    "neutral":     ("Neutral",     50,  "#c8b88a", "badge-neutral"),
    "sad":         ("Sad",         28,  "#ef9f9f", "badge-negative"),
    "angry":       ("Frustrated",  22,  "#ef9f9f", "badge-negative"),
    "anxious":     ("Anxious",     32,  "#ffb74d", "badge-anxious"),
    "stressed":    ("Stressed",    30,  "#ffb74d", "badge-anxious"),
    "overwhelmed": ("Overwhelmed", 25,  "#ffb74d", "badge-anxious"),
}

SYSTEM_PROMPT = """You are Serenova, a warm, compassionate AI mental health companion.
Your role:
- Listen actively and respond with deep empathy and understanding
- Detect emotional tone from messages
- Provide supportive, non-judgmental responses
- Offer evidence-based coping strategies when relevant
- Keep responses concise (3–5 sentences) but meaningful
- Use a warm, gentle tone — like a caring friend who also understands psychology
- Occasionally ask one open-ended question to encourage reflection
- Gently mention professional help when the situation warrants it

MANDATORY: At the very end of every response include EXACTLY:
MOOD_TAG:[mood_word]
COPING_STRATEGIES:[strategy1]|[strategy2]|[strategy3]

Where mood_word is one of: positive, happy, hopeful, calm, neutral, sad, angry, anxious, stressed, overwhelmed
And strategies are short, specific, actionable suggestions relevant to what was shared."""

def parse_response(raw: str):
    text = raw
    mood_key = "neutral"
    coping = []

    m = re.search(r"MOOD_TAG:\[?(\w+)\]?", raw, re.IGNORECASE)
    if m:
        mood_key = m.group(1).lower()
        text = text[:m.start()].strip()

    c = re.search(r"COPING_STRATEGIES:(.+?)(?:\n|$)", raw, re.IGNORECASE)
    if c:
        coping = [s.strip() for s in c.group(1).split("|") if s.strip()]
        text = re.sub(r"COPING_STRATEGIES:.+?(?:\n|$)", "", text, flags=re.IGNORECASE).strip()

    if mood_key not in MOOD_MAP:
        mood_key = "neutral"
    return text, mood_key, coping

def call_claude(messages):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    all_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=900,
        messages=all_messages
    )
    return response.choices[0].message.content

def mood_chart():
    if not st.session_state.mood_history:
        return None
    scores = [m["score"] for m in st.session_state.mood_history]
    labels = [f"#{i+1}" for i in range(len(scores))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=labels, y=scores,
        mode="lines+markers",
        line=dict(color="#7c9a92", width=2.5, shape="spline"),
        marker=dict(size=7, color="#7c9a92"),
        fill="tozeroy",
        fillcolor="rgba(124,154,146,0.08)"
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=4, b=0),
        plot_bgcolor="white", paper_bgcolor="white",
        height=160,
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#bbb"), linecolor="#f0ede8"),
        yaxis=dict(range=[0, 100], showgrid=True, gridcolor="#f7f4ef",
                   tickfont=dict(size=9, color="#bbb"), tickvals=[0,25,50,75,100]),
        showlegend=False
    )
    return fig

# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:\'DM Serif Display\',serif;font-size:20px;color:#2d4a3e;margin-bottom:16px;">🌿 Dashboard</p>', unsafe_allow_html=True)

    # Mood meter
    hist = st.session_state.mood_history
    if hist:
        latest = hist[-1]
        score  = latest["score"]
        label  = latest["label"]
        color  = latest["color"]
    else:
        score, label, color = 0, "Waiting…", "#c8dfc9"

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #f0ede8;border-radius:14px;padding:16px;margin-bottom:12px;text-align:center;">
      <div style="font-size:11px;font-weight:600;color:#9a8f82;text-transform:uppercase;letter-spacing:.8px;margin-bottom:8px;">Current Mood</div>
      <div style="font-family:'DM Serif Display',serif;font-size:44px;color:#2d4a3e;line-height:1;">{score if score else "—"}</div>
      <div style="font-size:13px;color:#8a9e96;margin-top:4px;font-weight:500;">{label}</div>
      <div style="height:6px;background:#f0ede8;border-radius:3px;margin-top:12px;overflow:hidden;">
        <div style="height:100%;width:{score}%;background:{color};border-radius:3px;transition:width .7s ease;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    scores   = [m["score"] for m in hist]
    avg_mood = round(sum(scores)/len(scores)) if scores else "—"
    peak     = max(scores) if scores else "—"
    if len(scores) >= 2:
        trend = "↑" if scores[-1] > scores[-2] else ("↓" if scores[-1] < scores[-2] else "→")
    else:
        trend = "—"

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-val">{st.session_state.msg_count}</div><div class="stat-lbl">Messages</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-card" style="margin-top:8px;"><div class="stat-val">{peak}</div><div class="stat-lbl">Peak Mood</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-val">{avg_mood}</div><div class="stat-lbl">Avg Mood</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-card" style="margin-top:8px;"><div class="stat-val">{trend}</div><div class="stat-lbl">Trend</div></div>', unsafe_allow_html=True)

    # Chart
    st.markdown('<div style="margin-top:14px;font-size:11px;font-weight:600;color:#9a8f82;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px;">Mood History</div>', unsafe_allow_html=True)
    fig = mood_chart()
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div style="font-size:12px;color:#bbb;text-align:center;padding:20px 0;">Chart appears after first message</div>', unsafe_allow_html=True)

    # Coping strategies
    st.markdown('<div style="margin-top:6px;font-size:11px;font-weight:600;color:#9a8f82;text-transform:uppercase;letter-spacing:.8px;margin-bottom:6px;">Coping Strategies</div>', unsafe_allow_html=True)
    icons = [("🌬️","#e8f5e9","#2e7d32"),("💭","#e3f2fd","#1565c0"),("🌿","#f3e5f5","#6a1b9a")]
    tips_html = '<div class="coping-card">'
    for i, tip in enumerate(st.session_state.coping_tips[:3]):
        ic, bg, col = icons[i]
        tips_html += f'<div class="coping-item"><div class="c-icon" style="background:{bg};color:{col};">{ic}</div><span>{tip[3] if len(tip)>3 else tip}</span></div>'
    tips_html += '</div>'
    st.markdown(tips_html, unsafe_allow_html=True)

    st.markdown('<div class="disclaimer">Serenova is an AI companion, not a substitute for professional mental health care.<br><strong>iCall: 9152987821</strong></div>', unsafe_allow_html=True)

# ── MAIN CHAT ──────────────────────────────────────────────────
st.markdown("""
<div class="mhc-header">
  <span style="font-size:30px;">🌿</span>
  <div>
    <p class="mhc-title">Serenova</p>
    <p class="mhc-sub">AI Mental Health Companion &nbsp;·&nbsp; Safe, private, always here</p>
  </div>
</div>
""", unsafe_allow_html=True)

# Welcome message
if not st.session_state.messages:
    st.markdown("""
    <div class="msg-row-ai">
      <div class="avatar-ai">🌿</div>
      <div>
        <div class="bubble-ai">
          Hello, I'm Serenova — your personal mental health companion. 🌿<br><br>
          This is a safe, judgment-free space where you can share whatever's on your mind —
          stress, anxiety, sadness, or just the need to talk. I'm here to listen, understand,
          and support you.<br><br>
          <strong>How are you feeling today?</strong>
        </div>
        <div class="meta">Just now</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Render chat history
for msg in st.session_state.messages:
    ts = msg.get("time", "")
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-row-user">
          <div class="avatar-user">You</div>
          <div>
            <div class="bubble-user">{msg["content"]}</div>
            <div class="meta meta-user">{ts}</div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        mood_info = MOOD_MAP.get(msg.get("mood","neutral"), MOOD_MAP["neutral"])
        badge = f'<span class="badge {mood_info[3]}">{mood_info[0]}</span>'
        st.markdown(f"""
        <div class="msg-row-ai">
          <div class="avatar-ai">🌿</div>
          <div>
            <div class="bubble-ai">{msg["content"].replace(chr(10),'<br>')}</div>
            <div class="meta">{ts} {badge}</div>
          </div>
        </div>""", unsafe_allow_html=True)

# Quick prompts
if st.session_state.msg_count == 0:
    st.markdown("<div style='margin: 8px 0 4px; font-size:12px; color:#bbb;'>Quick starters</div>", unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    prompts = [
        (q1, "Feeling anxious"),
        (q2, "Can't sleep"),
        (q3, "Feeling sad"),
        (q4, "Need coping tips"),
    ]
    full = [
        "I've been feeling really anxious lately and I don't know how to deal with it.",
        "I'm struggling to sleep and feeling completely overwhelmed.",
        "I'm feeling sad and I don't really know why.",
        "Can you share some coping strategies for managing stress?"
    ]
    for (col, label), text in zip(prompts, full):
        with col:
            if st.button(label, key=f"qp_{label}"):
                st.session_state._quick_send = text
                st.rerun()

# Handle quick send
if hasattr(st.session_state, "_quick_send"):
    quick_text = st.session_state._quick_send
    del st.session_state._quick_send
    ts = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "content": quick_text, "time": ts})
    st.session_state.msg_count += 1

    with st.spinner("Serenova is thinking…"):
        api_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        raw = call_claude(api_msgs)

    text, mood_key, coping = parse_response(raw)
    mood_info = MOOD_MAP[mood_key]
    st.session_state.messages.append({"role": "assistant", "content": text, "mood": mood_key, "time": datetime.now().strftime("%I:%M %p")})
    st.session_state.mood_history.append({"label": mood_info[0], "score": mood_info[1], "color": mood_info[2]})
    if coping:
        st.session_state.coping_tips = [(None,None,None,s) for s in coping]
    st.rerun()

# Input
st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area(
        "Your message",
        placeholder="Share what's on your mind… (Shift+Enter for new line)",
        height=80,
        label_visibility="collapsed"
    )
    col_send, col_clear = st.columns([5, 1])
    with col_send:
        submitted = st.form_submit_button("Send message ➤", use_container_width=True)
    with col_clear:
        if st.form_submit_button("Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.mood_history = []
            st.session_state.msg_count = 0
            st.rerun()

if submitted and user_input.strip():
    ts = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "content": user_input.strip(), "time": ts})
    st.session_state.msg_count += 1

    with st.spinner("Serenova is thinking…"):
        api_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        raw = call_claude(api_msgs)

    text, mood_key, coping = parse_response(raw)
    mood_info = MOOD_MAP[mood_key]
    st.session_state.messages.append({"role": "assistant", "content": text, "mood": mood_key, "time": datetime.now().strftime("%I:%M %p")})
    st.session_state.mood_history.append({"label": mood_info[0], "score": mood_info[1], "color": mood_info[2]})
    if coping:
        st.session_state.coping_tips = [(None,None,None,s) for s in coping]
    st.rerun()
