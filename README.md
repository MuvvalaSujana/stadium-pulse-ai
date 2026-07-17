# StadiumPulse AI - Smart Stadiums & Tournament Operations (FIFA 2026)

🚀 **Live Deployed App:** [Launch StadiumPulse AI](https://stadium-pulse-ai-rrfy6ybu5utcegw7fxxuqy.streamlit.app/)

## 🏟️ Chosen Vertical
* **Track:** [Challenge 4] Smart Stadiums & Tournament AI Assistant
* **Target Persona:** Tournament Organizers, On-site Volunteers, International Fans, and Venue Operational Staff.

## 🚀 Approach & Logic
StadiumPulse AI resolves complex logistics and communication bottlenecks at massive sporting venues by grounding Generative AI with real-time operational datasets.

* **Contextual Data Grounding:** Rather than hallucinating general stadium rules, the model analyzes a structural live metadata layer (`data/stadium_info.json`) containing transit timetables, specific entry gate queue times, and accessibility layouts.
* **Proactive Logic Routing:** When the system identifies a request targeting congested choke points (e.g., Gate B), it implements dynamic routing rules, actively advising alternatives.
* **Global Accessibility:** Built with out-of-the-box multilingual processing to support international fans effortlessly during the FIFA World Cup 2026.

## 🛠️ How It Works
1. **Context Initialization:** The application reads structural rules and status matrices from `data/stadium_info.json`.
2. **System Guardrails Configuration:** The underlying `gemini-3.1-flash-lite` model is injected with core system instructions concerning accessibility priorities, routing configurations, and language processing rules.
3. **Execution Pipeline:** A user submits a query via the accessible chat UI. The engine assesses the intent against the active dataset constraints and emits situational, localized advice.
4. **Automated Verification:** A built-in `pytest` testing suite validates file paths, JSON schemas, and core AI instruction integrity upon runtime.

## 💡 Assumptions Made
* The local stadium operational control room uploads dynamic gate metrics directly to the system's structured database storage layer.
* Users interact using mobile devices over stadium Wi-Fi infrastructure.

## 👥 Author & Contact
* **Author:** Muvvala Sujana
* **GitHub:** [@MuvvalaSujana](https://github.com/MuvvalaSujana)
* **LinkedIn:** [Sujana Muvvala](https://www.linkedin.com/in/sujana-muvvala-5491192b9/)
* **Email:** sujanamuvvala02@gmail.com
