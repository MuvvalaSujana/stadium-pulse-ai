import streamlit as st
import google.generativeai as genai
import json
import os

# Configure the Gemini API Key securely
if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
elif "gemini" in st.secrets:
    genai.configure(api_key=st.secrets["gemini"]["api_key"])

# 1. Load the operational database context matrix
def load_stadium_data():
    data_path = os.path.join("data", "stadium_info.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"gates": {}, "transit": {}, "accessibility": {}}

stadium_context = load_stadium_data()

# 2. Configure core AI Guardrails and Instructions
SYSTEM_INSTRUCTION = (
    "You are StadiumPulse AI, an executive operational assistant for the FIFA World Cup 2026. "
    "Your responses must be strictly grounded in the provided stadium operational data JSON matrix. "
    "If a query targets congested choke points (e.g., Gate B showing heavy delays), you must "
    "implement dynamic routing logic to actively advise alternative transit configurations. "
    "Maintain complete professional multilingual support for international venue operational staff and fans."
)

# 3. Build the User Interface
st.set_page_config(page_title="StadiumPulse AI", page_icon="🏟️", layout="wide")
st.title("Smart Stadiums & Tournament Operations Assistant")
st.caption("Powered by Gemini 3.1 Flash-Lite | Contextually Grounded Live Operational Engine")

# Maintain session state for conversation streams
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am StadiumPulse AI. How can I assist you with tournament logistics today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Handle Execution Pipeline & Prompt Augmentation
user_query = st.chat_input("Ask about gates, transit, or accessibility layouts...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        model = genai.GenerativeModel(
            model_name="gemini-3.1-flash-lite",
            system_instruction=SYSTEM_INSTRUCTION
        )
        
        # Grounding Payload Injection
        augmented_prompt = f"Operational Context:\n{stadium_context}\n\nUser Question: {user_query}"
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing operational matrices..."):
                response = model.generate_content(augmented_prompt)
                assistant_response = response.text
                st.markdown(assistant_response)
                
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
    except Exception as e:
        st.error("System connection delayed. Please ensure production environment keys are mapped.")