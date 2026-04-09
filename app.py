import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIGURATION (Must be the first Streamlit command)
st.set_page_config(page_title="Neodocs Health Assistant", page_icon="🩸", layout="wide")

# 2. SIDEBAR BRANDING
with st.sidebar:
    st.title("🩸 Neodocs")
    st.markdown("### Your Pocket Health Expert")
    st.markdown("Track your wellness instantly with our smart smartphone-based test kits.")
    st.divider()
    st.markdown("**Popular Kits:**")
    st.markdown("- 💧 Hydration & Kidney")
    st.markdown("- 🍎 Wellness & Nutrition")
    st.markdown("- 🤰 Pregnancy Care")
    st.divider()
    st.info("⚠️ **Disclaimer:** This AI prototype is for informational purposes only and does not replace professional medical advice.")

# 3. MAIN CHAT HEADER
st.title("🩺 NeoBot: AI Health Assistant")
st.markdown("Describe how you are feeling, or ask about our test kits!")

# 4. SECURE API CONNECTION
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API Key missing! Please add it to the Streamlit secrets.")
    st.stop()

# 5. UPGRADED SYSTEM PROMPT (The "Smarter" Brain)
system_prompt = """You are NeoBot, the official, highly professional AI health assistant for Neodocs. 
Always reply in the exact language the user speaks.

CORE RULES:
1. Empathy & Speed: Be extremely warm, concise, and get straight to the point.
2. Formatting: ALWAYS use bullet points and bold text to make your answers highly readable. Do not write long walls of text.
3. The Pivot: After addressing the user's symptom, ALWAYS recommend a relevant Neodocs urine test kit to help them track their biomarkers. 
4. Call to Action: Provide these exact links when relevant:
   - To buy a kit: https://neodocs.in/shop
   - To book an expert: https://calendly.com/neodocs-expert
   - Tutorial video: https://youtube.com/neodocs-tutorial
5. Boundaries: You are an AI. If a user describes a severe emergency, tell them to visit a hospital immediately."""

# 6. INITIALIZE AI MODEL
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)

# 7. CHAT MEMORY SETUP
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 8. DISPLAY CHAT HISTORY WITH CUSTOM AVATARS
for message in st.session_state.chat_session.history:
    if message.role == "model":
        with st.chat_message("assistant", avatar="🩺"):
            st.markdown(message.parts[0].text)
    else:
        with st.chat_message("user", avatar="👤"):
            st.markdown(message.parts[0].text)

# 9. CHAT INPUT
user_input = st.chat_input("E.g., My back hurts, what test should I take?")

if user_input:
    # Display user prompt
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Generate and display AI response
    with st.chat_message("assistant", avatar="🩺"):
        response = st.session_state.chat_session.send_message(user_input)
        st.markdown(response.text)
