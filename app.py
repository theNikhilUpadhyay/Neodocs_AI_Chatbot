import streamlit as st
import google.generativeai as genai

# Setup the web page look
st.set_page_config(page_title="Neodocs AI Health Assistant", page_icon="💧", layout="centered")

st.title("🩺 Neodocs AI Assistant")
st.markdown("Welcome! I can help you understand your health, suggest Neodocs kits, or connect you with an expert.")

# Securely pull the API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API Key missing! Please add it to the Streamlit secrets.")
    st.stop()

# The "Brain" Instructions - Edit these links before showing Pratik!
system_prompt = """You are the official AI assistant for Neodocs. 
You are empathetic, professional, and speak whatever language the user speaks.
Your goals:
1. Understand their symptoms and suggest relevant Neodocs urine or blood test kits.
2. If they need a tutorial on how to use a kit, give them this link: https://youtube.com/neodocs-tutorial
3. If they want to speak to an expert, give them this booking link: https://calendly.com/your-name/neodocs-expert
4. If they ask for blogs, provide: https://neodocs.in/blogs
Always remind users that you are an AI, not a doctor."""

# Initialize the AI Model
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

# Setup Chat Memory
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display previous chat history
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Input box for the user
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get AI response and show it
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(user_input)
        st.markdown(response.text)
