import streamlit as st
import google.generativeai as genai
import json
import os

# --- 1. MUST BE THE ABSOLUTE FIRST STREAMLIT COMMAND ---
st.set_page_config(
    page_title="StadiumPulse AI | FIFA World Cup 2026",
    page_icon="⚽",
    layout="centered"
)

# --- 2. SECURE API INITIALIZATION ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    st.error("🔒 Security Alert: GEMINI_API_KEY is missing. Configure it in your deployment environment variables.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# --- 3. DATA LAYER LOADER ---
@st.cache_data
def load_stadium_intelligence():
    try:
        with open("data/stadium_info.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading system operational data: {e}")
        return {}

stadium_context = load_stadium_intelligence()

# --- 4. SYSTEM INSTRUCTION ARCHITECTURE ---
SYSTEM_INSTRUCTION = f"""
You are "StadiumPulse AI", the official real-time operation and experience assistant for the FIFA World Cup 2026.
Your focus is to provide instant, precise help to fans, venue volunteers, and operational staff.

Operational Stadium Data Blueprint:
{json.dumps(stadium_context, indent=2)}

Core Operational Logic Rules:
1. Multilingual Capability: Detect the input language automatically and respond fluently in that exact language (e.g., English, Spanish, French, Arabic, German).
2. Crowd Mitigation: If a user asks about entry or leaving via Gate B, warn them about the {stadium_context.get('gates', {}).get('Gate B (East)', {}).get('wait_time_minutes', 45)} minute delay and clearly suggest routing through Gate A or Gate C depending on their target sections.
3. Accessibility First: Proactively suggest accessible pathways (like Gate C's ramps and elevators) if the user mentions strollers, wheelchairs, or limited mobility.
4. Sustainability Promotion: Encourage green habits by highlighting eco-bins and public transit alternatives (Secaucus Junction train loops) whenever transportation or waste disposal is brought up.
5. Keep descriptions direct, clear, and professional. Avoid lengthy commentary.
"""

# --- 5. STREAMLIT INTERFACE SETUP ---
# Header Section
st.markdown("<h1 style='text-align: center;'>⚽ StadiumPulse AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Smart Stadium Operations & Fan Guidance System</p>", unsafe_allow_html=True)
st.hr()

# Informational Live Dashboard Pills
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🏟️ Live Venue", value="MetLife Stadium")
with col2:
    st.metric(label="🚦 Gate B Status", value="Heavy Delay", delta="-45 min", delta_color="inverse")
with col3:
    st.metric(label="🌱 Eco Action Tracker", value="Active")

st.markdown("---")

# --- 6. CHAT ENGINE & MEMORY STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display current chat stream
for conversation in st.session_state.chat_history:
    with st.chat_message(conversation["role"]):
        st.markdown(conversation["content"])

# User prompt ingestion
if prompt := st.chat_input("Ask about gate access, transportation, or stadium accessibility..."):
    # Render user query
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process AI context response stream
    with st.chat_message("assistant"):
        try:
            # Using the fast, robust gemini-1.5-flash model optimized for multi-turn chat tasks
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_INSTRUCTION
            )
            
            response = model.generate_content(prompt)
            output_text = response.text
            
            st.markdown(output_text)
            st.session_state.chat_history.append({"role": "assistant", "content": output_text})
            
        except Exception as err:
            st.error(f"Backend processing failure: {err}") # Fixed JS comment to Python comment