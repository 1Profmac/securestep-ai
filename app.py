import streamlit as st
import anthropic
import os
from datetime import datetime

# Page setup
st.set_page_config(page_title="Ask Barb by SecureStep.ai", page_icon="🌟", layout="centered")

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@700;800&display=swap');

/* Root reset */
html, body, [class*="css"], .stApp {
    background-color: #0E1C2F !important;
    color: #C4CDD9 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 18px !important;
}

/* Remove Streamlit white containers */
.block-container {
    background-color: #0E1C2F !important;
    padding-top: 2rem !important;
}
section[data-testid="stSidebar"] {
    background-color: #162640 !important;
}
section[data-testid="stSidebar"] > div {
    background-color: #162640 !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Playfair Display', serif !important;
    color: #C8942E !important;
}
p, li, label, span, div {
    font-family: 'DM Sans', sans-serif !important;
    color: #C4CDD9 !important;
}

/* Buttons — gold filled */
.stButton > button {
    background-color: #C8942E !important;
    color: #0E1C2F !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 12px 24px !important;
    min-height: 48px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background-color 0.2s ease !important;
}
.stButton > button:hover {
    background-color: #E8B84B !important;
    color: #0E1C2F !important;
}

/* Outline buttons — pill buttons for example questions */
.pill-btn > button {
    background-color: #1E3A5F !important;
    color: #C8942E !important;
    border: 1.5px solid #C8942E !important;
    border-radius: 24px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
}
.pill-btn > button:hover {
    background-color: #C8942E !important;
    color: #0E1C2F !important;
}

/* Outline nav button */
.outline-btn > button {
    background-color: transparent !important;
    color: #C8942E !important;
    border: 2px solid #C8942E !important;
    border-radius: 8px !important;
}
.outline-btn > button:hover {
    background-color: #C8942E !important;
    color: #0E1C2F !important;
}

/* Chat messages */
.stChatMessage {
    font-size: 18px !important;
    border-radius: 10px !important;
    padding: 12px !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessageContent"] {
    font-size: 18px !important;
    color: #C4CDD9 !important;
}
/* User bubble */
[data-testid="stChatMessage"][data-role="user"] {
    background-color: #1E3A5F !important;
    border-left: 4px solid #C8942E !important;
}
/* Assistant bubble */
[data-testid="stChatMessage"][data-role="assistant"] {
    background-color: #162640 !important;
    border-left: 4px solid #109F35 !important;
}

/* Chat input */
.stChatInput, [data-testid="stChatInput"] {
    background-color: #0E1C2F !important;
}
.stChatInput textarea, .stChatInput input,
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input,
[data-testid="stChatInputTextArea"],
[data-baseweb="textarea"] textarea {
    background-color: #162640 !important;
    color: #C4CDD9 !important;
    border: 1.5px solid #A8B8CC !important;
    border-radius: 8px !important;
    font-size: 18px !important;
    font-family: 'DM Sans', sans-serif !important;
    caret-color: #C8942E !important;
}
.stChatInput textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInputTextArea"]::placeholder {
    color: #A8B8CC !important;
    opacity: 1 !important;
}
.stChatInput textarea:focus, .stChatInput input:focus,
[data-testid="stChatInput"] textarea:focus {
    border-color: #C8942E !important;
    outline: none !important;
    box-shadow: 0 0 0 2px rgba(200, 148, 46, 0.3) !important;
}
/* Override Streamlit's white chat input container */
[data-testid="stBottom"], [data-testid="stBottom"] > div {
    background-color: #0E1C2F !important;
}

/* Select box */
.stSelectbox > div > div {
    background-color: #162640 !important;
    color: #C4CDD9 !important;
    border: 1.5px solid #A8B8CC !important;
    border-radius: 8px !important;
    font-size: 18px !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #C8942E !important;
}

/* Radio buttons */
.stRadio > div {
    background-color: transparent !important;
}
.stRadio label {
    color: #C4CDD9 !important;
    font-size: 17px !important;
}
.stRadio [data-testid="stMarkdownContainer"] p {
    color: #C4CDD9 !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: #162640 !important;
    border-radius: 10px !important;
    padding: 16px !important;
    border: 1px solid #1E3A5F !important;
}
[data-testid="stMetricValue"] {
    color: #C8942E !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important;
}
[data-testid="stMetricLabel"] {
    color: #A8B8CC !important;
    font-size: 16px !important;
}

/* Divider */
hr {
    border-color: #1E3A5F !important;
}

/* Barb circular photo */
section[data-testid="stSidebar"] .stImage img {
    border-radius: 50% !important;
    border: 3px solid #C8942E !important;
    display: block;
    margin: 0 auto;
}

/* Sidebar text */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #C8942E !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #C4CDD9 !important;
}

/* Custom card classes */
.lmt-tip-card {
    background-color: #162640;
    border-left: 5px solid #C8942E;
    border-radius: 10px;
    padding: 20px 24px;
    margin: 12px 0;
    font-size: 18px;
    color: #C4CDD9;
    font-family: 'DM Sans', sans-serif;
}
.lmt-progress-card {
    background-color: #162640;
    border: 2px solid #C8942E;
    border-radius: 12px;
    padding: 24px;
    margin: 12px 0;
    text-align: center;
}
.lmt-progress-card h2 {
    font-family: 'Playfair Display', serif;
    color: #C8942E;
    margin: 0 0 8px 0;
    font-size: 2rem;
}
.lmt-progress-card p {
    color: #A8B8CC;
    margin: 0;
    font-size: 18px;
}
.lmt-level-badge {
    background-color: #1E3A5F;
    border: 1.5px solid #C8942E;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 8px 0;
    text-align: center;
}
.lmt-level-badge strong {
    color: #C8942E;
    font-family: 'Playfair Display', serif;
}
.lmt-section-card {
    background-color: #162640;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 12px 0;
    border: 1px solid #1E3A5F;
}
.lmt-section-card h3 {
    font-family: 'Playfair Display', serif;
    color: #C8942E;
    margin-top: 0;
}
.lmt-section-card a {
    color: #C8942E;
    text-decoration: underline;
}
.lmt-section-card a:hover {
    color: #E8B84B;
}
.lmt-section-card ul {
    padding-left: 20px;
}
.lmt-section-card li {
    color: #C4CDD9;
    margin-bottom: 8px;
}
.lmt-cat-card {
    background-color: #162640;
    border-radius: 10px;
    padding: 18px 20px;
    margin: 6px 0;
    border: 1px solid #1E3A5F;
}
.lmt-cat-card .cat-title {
    color: #C8942E;
    font-weight: 700;
    font-size: 18px;
    font-family: 'DM Sans', sans-serif;
}
.lmt-cat-card .cat-example {
    color: #A8B8CC;
    font-size: 15px;
    margin-top: 4px;
}
.lmt-hero-sub {
    color: #A8B8CC;
    font-size: 20px;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 8px;
}
.lmt-orange-msg {
    background-color: rgba(232, 115, 58, 0.15);
    border-left: 4px solid #E8733A;
    border-radius: 8px;
    padding: 16px 20px;
    color: #E8B84B;
    font-size: 18px;
    font-family: 'DM Sans', sans-serif;
    margin: 12px 0;
}
.lmt-barb-greeting {
    background-color: #162640;
    border-left: 4px solid #109F35;
    border-radius: 10px;
    padding: 20px 24px;
    margin: 12px 0;
    font-size: 18px;
    color: #C4CDD9;
    font-family: 'DM Sans', sans-serif;
}
.lmt-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'DM Sans', sans-serif;
    font-size: 17px;
}
.lmt-table th {
    background-color: #1E3A5F;
    color: #C8942E;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 2px solid #C8942E;
}
.lmt-table td {
    background-color: #162640;
    color: #C4CDD9;
    padding: 12px 16px;
    border-bottom: 1px solid #1E3A5F;
}
.lmt-table tr:hover td {
    background-color: #1E3A5F;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0
if "helpful_count" not in st.session_state:
    st.session_state.helpful_count = 0

# ── Daily tips ───────────────────────────────────────────────────────────────
daily_tips = [
    "You can ask Alexa or Siri to set medication reminders — just say 'Remind me to take my pills at 8am every day.'",
    "AI can help you write emails. Just tell ChatGPT or Claude 'Help me write a friendly email to my doctor about my upcoming appointment.'",
    "Worried about phone scams? AI can't answer your phone, but you can ask it 'What are the most common phone scams targeting adults 50+?' to learn what to watch for.",
    "You can use AI to compare Medicare plans. Ask: 'What questions should I ask when choosing a Medicare supplement plan?'",
    "Want to video call family? FaceTime (iPhone) or Google Meet (any phone) are the easiest options. Ask Barb how to set them up!",
    "AI can help you organize recipes. Take a photo of a recipe card and ask AI to type it up and adjust the serving size.",
    "Feeling isolated? Ask Barb about AI tools that help you stay connected with family and find local community events.",
]
today_tip = daily_tips[datetime.now().timetuple().tm_yday % len(daily_tips)]

# ── Pioneer levels ───────────────────────────────────────────────────────────
def get_pioneer_level(questions):
    if questions >= 50:
        return "Trailblazer", "You're leading the way!"
    elif questions >= 25:
        return "Pioneer", "You're exploring with confidence!"
    elif questions >= 10:
        return "Explorer", "You're getting comfortable with AI!"
    elif questions >= 1:
        return "Beginner", "You've taken your first step!"
    else:
        return "New", "Ask your first question to get started!"

# ── Categories ───────────────────────────────────────────────────────────────
categories = {
    "Health & Medications": [
        "How can AI help me remember my medications?",
        "Can AI help me prepare for a doctor's appointment?",
        "What apps track blood pressure or blood sugar?",
    ],
    "Money & Bills": [
        "Can AI help me manage my bills and budget?",
        "How do I spot an online scam?",
        "Can AI help me compare insurance plans?",
    ],
    "Staying Connected": [
        "What's the easiest way to video call my family?",
        "How can AI help me stay in touch with old friends?",
        "Can AI help me write letters or emails?",
    ],
    "Home & Safety": [
        "What AI tools can help me stay safe living alone?",
        "How do smart home devices work?",
        "Can AI detect if I've fallen?",
    ],
    "Creative & Fun": [
        "Can AI help me write my life story?",
        "How do I use AI to edit photos?",
        "Can AI help me learn a new hobby?",
    ],
}

CATEGORY_ICONS = {
    "Health & Medications": "💊",
    "Money & Bills": "💰",
    "Staying Connected": "📱",
    "Home & Safety": "🏠",
    "Creative & Fun": "🎨",
}

# ── Handle nav_to (Home quick-start buttons) ─────────────────────────────────
if "nav_to" in st.session_state:
    st.session_state["nav_page"] = st.session_state.pop("nav_to")

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    try:
        st.image("logo.png", width=180)
    except Exception:
        pass

    try:
        st.image("barb-avatar.png", width=100)
    except Exception:
        pass

    st.markdown("""
    <div style="margin-top: 4px; margin-bottom: 2px;">
        <span style="font-family:'Playfair Display',serif; font-size:26px; font-weight:800; color:#C8942E;">Ask Barb</span><br>
        <span style="font-family:'DM Sans',sans-serif; font-size:14px; color:#A8B8CC; letter-spacing:0.5px;">by SecureStep.ai</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F; margin:12px 0;'>", unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["Home", "Ask Barb", "My Progress", "Resources"],
        label_visibility="collapsed",
        key="nav_page"
    )

    st.markdown("<hr style='border-color:#1E3A5F; margin:12px 0;'>", unsafe_allow_html=True)

    level, level_msg = get_pioneer_level(st.session_state.questions_asked)
    st.markdown(f"""
    <div class="lmt-level-badge">
        <div style="font-size:13px; color:#A8B8CC; margin-bottom:4px;">Pioneer Level</div>
        <strong style="font-size:20px;">{level}</strong><br>
        <div style="font-size:14px; color:#A8B8CC; margin-top:4px;">{level_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; margin:10px 0; font-size:16px; color:#A8B8CC;">
        Questions Asked: <span style="color:#C8942E; font-weight:700;">{st.session_state.questions_asked}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F; margin:12px 0;'>", unsafe_allow_html=True)

    if st.button("Clear Chat History", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
if page == "Home":
    hero_col1, hero_col2 = st.columns([1, 3])
    with hero_col1:
        try:
            st.image("barb-avatar.png", use_container_width=True)
        except Exception:
            pass
    with hero_col2:
        st.markdown("""
        <h1 style="font-family:'Playfair Display',serif; font-size:3rem; color:#C8942E; margin-bottom:4px;">
            Hi, I'm Barb.
        </h1>
        <p class="lmt-hero-sub">Your AI guide for independent living.</p>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <h2 style="font-family:'Playfair Display',serif; font-size:1.3rem; color:#C8942E; margin-bottom:8px;">
        Today's AI Tip
    </h2>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="lmt-tip-card">{today_tip}</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <h2 style="font-family:'Playfair Display',serif; font-size:1.3rem; color:#C8942E; margin-bottom:8px;">
        Quick Start
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ask Barb a Question", use_container_width=True, key="home_ask"):
            st.session_state["nav_to"] = "Ask Barb"
            st.rerun()
    with col2:
        st.markdown('<div class="outline-btn">', unsafe_allow_html=True)
        if st.button("See My Progress", use_container_width=True, key="home_progress"):
            st.session_state["nav_to"] = "My Progress"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <h2 style="font-family:'Playfair Display',serif; font-size:1.3rem; color:#C8942E; margin-bottom:8px;">
        What Can Barb Help With?
    </h2>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    cats = list(categories.items())
    for i, (cat, questions) in enumerate(cats):
        icon = CATEGORY_ICONS.get(cat, "✦")
        col = col_a if i % 2 == 0 else col_b
        with col:
            st.markdown(f"""
            <div class="lmt-cat-card">
                <div class="cat-title">{icon} {cat}</div>
                <div class="cat-example">{questions[0]}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ASK BARB PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Ask Barb":
    st.markdown("""
    <h1 style="font-family:'Playfair Display',serif; font-size:2.4rem; color:#C8942E; margin-bottom:4px;">
        Ask Barb
    </h1>
    <p style="color:#A8B8CC; font-size:18px; margin-bottom:0;">No tech jargon. Just plain talk from a knowledgeable friend.</p>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)

    # Category selector
    selected_cat = st.selectbox("Choose a topic:", ["All Topics"] + list(categories.keys()))

    if selected_cat == "All Topics":
        examples = [q for cat_qs in categories.values() for q in cat_qs[:1]]
    else:
        examples = categories[selected_cat]

    st.markdown("<p style='color:#A8B8CC; font-size:16px; margin:12px 0 8px;'><strong style='color:#C4CDD9;'>Not sure what to ask? Try one of these:</strong></p>", unsafe_allow_html=True)

    for example in examples:
        if st.button(example, key=f"ex_{example}", use_container_width=True):
            st.session_state["user_input"] = example
            st.rerun()

    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)

    # Barb greeting
    if not st.session_state.messages:
        st.markdown("""
        <div class="lmt-barb-greeting">
            Hi there! I'm Barb, your AI guide. I'm here to help you learn how AI can make your daily life easier and safer.
            Ask me anything — no question is too simple, and I'll never use confusing tech talk.
            <strong style="color:#C8942E;">What would you like to know?</strong>
        </div>
        """, unsafe_allow_html=True)

    # Chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Pull from example button click or typed input
    pending = st.session_state.pop("user_input", None)
    prompt = pending or st.chat_input("Type your question here...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.questions_asked += 1

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                api_key = os.environ.get("ANTHROPIC_API_KEY")
                if not api_key:
                    api_key = st.secrets.get("ANTHROPIC_API_KEY")
                if not api_key:
                    st.error("Barb is unavailable right now — API key not configured. Please contact support.")
                    st.stop()

                client = anthropic.Anthropic(api_key=api_key)

                with client.messages.stream(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    system="""You are Barb, a warm, patient AI guide who helps adults over 50
                    learn how to use AI and technology for independent living.

                    Rules:
                    - Use simple, clear language. No tech jargon.
                    - Talk like a knowledgeable friend, not a professor.
                    - Give specific, actionable steps they can try today.
                    - When mentioning apps or tools, explain exactly how to find and use them.
                    - Be encouraging. Many of your users are trying technology for the first time.
                    - Keep answers concise — 3-5 short paragraphs max.
                    - If something is risky or could lead to scams, warn them clearly.
                    - You represent 50+TechBridge, a program that helps adults 50+ learn AI for independent living.""",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                ) as stream:
                    reply = st.write_stream(stream.text_stream)

                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                st.error(f"Barb ran into a problem: {e}")
                st.session_state.messages.pop()
                st.session_state.questions_asked -= 1

        # Feedback buttons
        col1, col2, _ = st.columns([1, 1, 4])
        with col1:
            st.markdown('<div class="pill-btn">', unsafe_allow_html=True)
            if st.button("👍 Helpful", key=f"helpful_{len(st.session_state.messages)}"):
                st.session_state.helpful_count += 1
                st.toast("Thanks for the feedback! Glad that helped.")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="pill-btn">', unsafe_allow_html=True)
            if st.button("👎 Not helpful", key=f"nothelpful_{len(st.session_state.messages)}"):
                st.toast("Thanks — I'll try to do better!")
            st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MY PROGRESS PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "My Progress":
    st.markdown("""
    <h1 style="font-family:'Playfair Display',serif; font-size:2.4rem; color:#C8942E; margin-bottom:4px;">
        My Progress
    </h1>
    <p style="color:#A8B8CC; font-size:18px; margin-bottom:0;">Track your Pioneer journey.</p>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)

    level, level_msg = get_pioneer_level(st.session_state.questions_asked)

    st.markdown(f"""
    <div class="lmt-progress-card">
        <div style="font-size:14px; color:#A8B8CC; margin-bottom:8px; text-transform:uppercase; letter-spacing:1px;">Your Pioneer Level</div>
        <h2>{level}</h2>
        <p>{level_msg}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <h2 style="font-family:'Playfair Display',serif; font-size:1.3rem; color:#C8942E; margin-bottom:8px;">
        Your Stats
    </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions Asked", st.session_state.questions_asked)
    with col2:
        st.metric("Helpful Answers", st.session_state.helpful_count)
    with col3:
        st.metric("Conversations", len([m for m in st.session_state.messages if m["role"] == "user"]))

    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <h2 style="font-family:'Playfair Display',serif; font-size:1.3rem; color:#C8942E; margin-bottom:8px;">
        Pioneer Levels
    </h2>
    <table class="lmt-table">
        <thead>
            <tr>
                <th>Level</th>
                <th>Questions</th>
                <th>What It Means</th>
            </tr>
        </thead>
        <tbody>
            <tr><td><strong>Beginner</strong></td><td>1+</td><td>You've taken your first step!</td></tr>
            <tr><td><strong>Explorer</strong></td><td>10+</td><td>You're getting comfortable with AI</td></tr>
            <tr><td><strong>Pioneer</strong></td><td>25+</td><td>You're exploring with confidence</td></tr>
            <tr><td><strong>Trailblazer</strong></td><td>50+</td><td>You're leading the way!</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="lmt-orange-msg">
        Keep going, {level}! Every question you ask is a step toward greater independence.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RESOURCES PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Resources":
    st.markdown("""
    <h1 style="font-family:'Playfair Display',serif; font-size:2.4rem; color:#C8942E; margin-bottom:4px;">
        Resources
    </h1>
    <p style="color:#A8B8CC; font-size:18px; margin-bottom:0;">Helpful links and local support for your AI learning journey.</p>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1E3A5F; margin:16px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div class="lmt-section-card">
        <h3>50+TechBridge</h3>
        <ul>
            <li>Website: <a href="https://50plustechbridge.com" target="_blank">50plustechbridge.com</a></li>
            <li>Courses: <a href="https://learnmoretechnologies.com" target="_blank">learnmoretechnologies.com</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="lmt-section-card">
        <h3>Local Austin Resources</h3>
        <ul>
            <li><strong>Austin Public Library</strong> — Free computer classes and WiFi</li>
            <li><strong>Adult learning centers</strong> — In-person Technology Assisted Trainings</li>
            <li><strong>Workforce Solutions Capital Area</strong> — Career and digital skills support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="lmt-section-card">
        <h3>Emergency Contacts</h3>
        <ul>
            <li><strong>911</strong> — Emergency</li>
            <li><strong>211</strong> — Local services and support</li>
            <li><strong>988</strong> — Mental health crisis line</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="lmt-section-card">
        <h3>AI Safety Tips</h3>
        <ul>
            <li>Never share your Social Security number, bank info, or passwords with AI</li>
            <li>AI can make mistakes — always verify important information</li>
            <li>If something feels like a scam, it probably is — ask a trusted person</li>
            <li>AI is a tool to help you, not replace your doctor, lawyer, or financial advisor</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
