import streamlit as st
import anthropic
import os

# Page setup
st.set_page_config(page_title="Digital Pioneer", page_icon="🌟", layout="centered")

# Custom styling
st.markdown("""
<style>
    .stChatMessage { font-size: 18px; }
    .stMarkdown { font-size: 18px; }
    h1 { color: #2E86AB; }
    .stButton > button { font-size: 18px; padding: 10px 20px; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("Digital Pioneer")
st.subheader("Ask Barb — Your AI Guide for Independent Living")
st.markdown("Ask me anything about using AI to make your daily life easier. No tech jargon, just plain talk.")
st.markdown("---")

# Example questions they can click
st.markdown("**Not sure what to ask? Try one of these:**")
examples = [
    "How can AI help me remember my medications?",
    "What's the easiest way to video call my family?",
    "Can AI help me manage my bills and budget?",
    "How do I use voice assistants like Alexa or Siri?",
    "What AI tools can help me stay safe living alone?",
]

# Handle example button clicks
for example in examples:
    if st.button(example, key=example):
        st.session_state["user_input"] = example

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type your question here...")

# Check if an example button was clicked
if "user_input" in st.session_state:
    prompt = st.session_state.pop("user_input")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Barb's response
    with st.chat_message("assistant"):
        with st.spinner("Barb is thinking..."):
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
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
            )
            reply = response.content[0].text
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
