import streamlit as st
import anthropic
import os
from datetime import datetime

# Page setup
st.set_page_config(page_title="Digital Pioneer", page_icon="🌟", layout="centered")

# Custom styling
st.markdown("""
<style>
    .stChatMessage { font-size: 18px; }
    .stMarkdown { font-size: 18px; }
    h1 { color: #2E86AB; }
    h2 { color: #2E86AB; }
    .stButton > button { font-size: 18px; padding: 10px 20px; }
    .tip-box { background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #2E86AB; margin: 10px 0; }
    .progress-box { background-color: #f5fff5; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; margin: 10px 0; }
    .category-label { font-size: 16px; font-weight: bold; color: #2E86AB; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0
if "helpful_count" not in st.session_state:
    st.session_state.helpful_count = 0

# Daily tips
daily_tips = [
    "You can ask Alexa or Siri to set medication reminders — just say 'Remind me to take my pills at 8am every day.'",
    "AI can help you write emails. Just tell ChatGPT or Claude 'Help me write a friendly email to my doctor about my upcoming appointment.'",
    "Worried about phone scams? AI can't answer your phone, but you can ask it 'What are the most common phone scams targeting seniors?' to learn what to watch for.",
    "You can use AI to compare Medicare plans. Ask: 'What questions should I ask when choosing a Medicare supplement plan?'",
    "Want to video call family? FaceTime (iPhone) or Google Meet (any phone) are the easiest options. Ask Barb how to set them up!",
    "AI can help you organize recipes. Take a photo of a recipe card and ask AI to type it up and adjust the serving size.",
    "Feeling isolated? Ask Barb about AI tools that help you stay connected with family and find local community events.",
]
today_tip = daily_tips[datetime.now().timetuple().tm_yday % len(daily_tips)]

# Pioneer levels
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

# Sidebar
with st.sidebar:
    st.image("logo.png", width=200)
    st.markdown("## Digital Pioneer")
    st.markdown("---")

    page = st.radio("Navigate", ["Home", "Ask Barb", "My Progress", "Resources"], label_visibility="collapsed")

    st.markdown("---")

    level, level_msg = get_pioneer_level(st.session_state.questions_asked)
    st.markdown(f"**Your Level:** {level}")
    st.markdown(f"**Questions Asked:** {st.session_state.questions_asked}")

    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Category examples
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

# ---------- PAGES ----------

if page == "Home":
    st.image("logo.png", width=400)
    st.title("Digital Pioneer")
    st.subheader("AI & Digital Skills for Adults 50+")
    st.markdown("Welcome! This app helps you learn how to use AI to stay independent, safe, and connected.")

    st.markdown("---")
    st.markdown("### Today's AI Tip")
    st.markdown(f'<div class="tip-box">{today_tip}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Quick Start")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ask Barb a Question", use_container_width=True):
            st.session_state["nav_to"] = "Ask Barb"
            st.rerun()
    with col2:
        if st.button("See My Progress", use_container_width=True):
            st.session_state["nav_to"] = "My Progress"
            st.rerun()

    st.markdown("---")
    st.markdown("### What Can Barb Help With?")
    for cat in categories:
        st.markdown(f"- **{cat}**")

elif page == "Ask Barb":
    st.title("Ask Barb")
    st.markdown("Your AI guide for independent living. No tech jargon, just plain talk.")
    st.markdown("---")

    # Category selector
    selected_cat = st.selectbox("Choose a topic:", ["All Topics"] + list(categories.keys()))

    if selected_cat == "All Topics":
        examples = [q for cat_qs in categories.values() for q in cat_qs[:1]]
    else:
        examples = categories[selected_cat]

    st.markdown("**Not sure what to ask? Try one of these:**")
    for example in examples:
        if st.button(example, key=example):
            st.session_state["user_input"] = example

    st.markdown("---")

    # Display chat history
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown("Hi there! I'm Barb, your AI guide. I'm here to help you learn how AI can make your daily life easier and safer. Ask me anything — no question is too simple, and I'll never use confusing tech talk. What would you like to know?")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input("Type your question here...")

    if "user_input" in st.session_state:
        prompt = st.session_state.pop("user_input")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.questions_asked += 1
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            api_key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
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

        # Feedback buttons
        col1, col2, _ = st.columns([1, 1, 4])
        with col1:
            if st.button("Helpful", key=f"helpful_{len(st.session_state.messages)}"):
                st.session_state.helpful_count += 1
                st.toast("Thanks for the feedback!")
        with col2:
            if st.button("Not helpful", key=f"nothelpful_{len(st.session_state.messages)}"):
                st.toast("Thanks — I'll try to do better!")

elif page == "My Progress":
    st.title("My Progress")
    st.markdown("Track your Digital Pioneer journey!")
    st.markdown("---")

    level, level_msg = get_pioneer_level(st.session_state.questions_asked)

    st.markdown(f'<div class="progress-box"><h3>Your Level: {level}</h3><p>{level_msg}</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Your Stats")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions Asked", st.session_state.questions_asked)
    with col2:
        st.metric("Helpful Answers", st.session_state.helpful_count)
    with col3:
        st.metric("Conversations", len([m for m in st.session_state.messages if m["role"] == "user"]))

    st.markdown("---")
    st.markdown("### Pioneer Levels")
    st.markdown("""
    | Level | Questions | What it means |
    |-------|-----------|---------------|
    | **Beginner** | 1+ | You've taken your first step! |
    | **Explorer** | 10+ | You're getting comfortable with AI |
    | **Pioneer** | 25+ | You're exploring with confidence |
    | **Trailblazer** | 50+ | You're leading the way! |
    """)

elif page == "Resources":
    st.title("Resources")
    st.markdown("Helpful links and local support for your AI learning journey.")
    st.markdown("---")

    st.markdown("### 50+TechBridge")
    st.markdown("- Website: [50plustechbridge.com](https://50plustechbridge.com)")
    st.markdown("- Courses: [learnmoretechnologies.com](https://learnmoretechnologies.com)")
    st.markdown("---")

    st.markdown("### Local Austin Resources")
    st.markdown("- **Austin Public Library** — Free computer classes and WiFi")
    st.markdown("- **Senior centers** — In-person Technology Assisted Trainings")
    st.markdown("- **Workforce Solutions Capital Area** — Career and digital skills support")
    st.markdown("---")

    st.markdown("### Emergency Contacts")
    st.markdown("- **911** — Emergency")
    st.markdown("- **211** — Local services and support")
    st.markdown("- **988** — Mental health crisis line")
    st.markdown("---")

    st.markdown("### AI Safety Tips")
    st.markdown("""
    - Never share your Social Security number, bank info, or passwords with AI
    - AI can make mistakes — always verify important information
    - If something feels like a scam, it probably is — ask a trusted person
    - AI is a tool to help you, not replace your doctor, lawyer, or financial advisor
    """)

# Handle navigation from Home buttons
if "nav_to" in st.session_state:
    del st.session_state["nav_to"]
