# Step1: Setup Streamlit
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step2: User is able to ask question
# Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # AI Agent exists here
    fixed_dummy_response = "I'm here to listen. Can you tell me more about how you're feeling?"
    st.session_state.chat_history.append({"role": "assistant", "content": fixed_dummy_response})

# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])