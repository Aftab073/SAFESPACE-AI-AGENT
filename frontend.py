import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def make_authenticated_request(endpoint, method="GET", data=None):
    """Make authenticated API request"""
    headers = {
        "Authorization": f"Bearer {st.session_state.token}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "POST":
            response = requests.post(f"{BACKEND_URL}{endpoint}", 
                                   json=data, headers=headers, timeout=30)
        else:
            response = requests.get(f"{BACKEND_URL}{endpoint}", 
                                  headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def login_page():
    """Login/Register page"""
    st.title("🧠 SafeSpace – AI Mental Health Therapist")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn:
                if email and password:
                    try:
                        response = requests.post(f"{BACKEND_URL}/auth/login", 
                                               json={"email": email, "password": password})
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.token = data["access_token"]
                            st.session_state.user = data["user"]
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    except requests.exceptions.RequestException:
                        st.error("Connection failed. Is the backend running?")
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("Create Account")
        with st.form("register_form"):
            reg_email = st.text_input("Email", key="reg_email")
            reg_name = st.text_input("Full Name (Optional)", key="reg_name")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            register_btn = st.form_submit_button("Register")
            
            if register_btn:
                if reg_email and reg_password:
                    try:
                        payload = {"email": reg_email, "password": reg_password}
                        if reg_name:
                            payload["full_name"] = reg_name
                            
                        response = requests.post(f"{BACKEND_URL}/auth/register", json=payload)
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.token = data["access_token"]
                            st.session_state.user = data["user"]
                            st.success("Account created successfully!")
                            st.rerun()
                        else:
                            error_detail = response.json().get("detail", "Registration failed")
                            st.error(f"Registration failed: {error_detail}")
                    except requests.exceptions.RequestException:
                        st.error("Connection failed. Is the backend running?")
                else:
                    st.error("Email and password are required")

def chat_page():
    """Main chat interface"""
    # Header with user info and logout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🧠 SafeSpace – AI Mental Health Therapist")
        if st.session_state.user:
            st.caption(f"Welcome, {st.session_state.user.get('full_name', st.session_state.user['email'])}!")
    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.chat_history = []
            st.rerun()
    
    # Load chat history from backend
    if st.button("📚 Load Previous Conversations"):
        history_data = make_authenticated_request("/chat/history")
        if history_data:
            st.session_state.chat_history = []
            for msg in history_data["history"]:
                st.session_state.chat_history.append({"role": "user", "content": msg["message"]})
                st.session_state.chat_history.append({"role": "assistant", "content": f'{msg["response"]} WITH TOOL: [{msg.get("tool_used", "None")}]'})
    
    # Chat input
    user_input = st.chat_input("What's on your mind today?")
    
    if user_input:
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        response_data = make_authenticated_request("/ask", "POST", {"message": user_input})
        if response_data:
            ai_response = f'{response_data["response"]} WITH TOOL: [{response_data.get("tool_used", "None")}]'
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        else:
            st.session_state.chat_history.append({"role": "assistant", "content": "Sorry, I'm having technical difficulties. Please try again."})
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Main app logic
if st.session_state.token is None:
    login_page()
else:
    chat_page()
