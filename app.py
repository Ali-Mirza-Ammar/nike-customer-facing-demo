import streamlit as st
import os
from utils.gemini_generator import generate_customer_scenario
from utils.google_tts import generate_google_tts
from utils.transcription import transcribe_audio
from utils.scoring import analyze_tone_with_gemini

st.set_page_config(page_title="Nike Retail Trainer", page_icon="🛍️")
st.title("👟 Nike Store - Customer Greeting Trainer")

st.write("""
Welcome to the **Nike Store Customer Interaction Trainer!** 🏃‍♂️

Here, you'll practice your greeting skills as a cashier in a Nike retail environment:

1. 🎧 **Listen** to a realistic Nike customer.
2. 🎙️ **Record and upload** your natural reply.
3. 🧠 **Get instant AI feedback** on the friendliness and warmth of your greeting!

This tool helps you sound more welcoming, natural, and professional when assisting customers in a dynamic Nike store.
Let's get started!
""")

# Always normal difficulty
scenario_text = st.session_state.get("scenario_text")
if not scenario_text:
    scenario_text = generate_customer_scenario()
    st.session_state["scenario_text"] = scenario_text

st.subheader("🎭 Customer Says:")
st.write(f"_{scenario_text}_")

# Generate and play customer voice
generate_google_tts(scenario_text, "customer.mp3")
st.audio("customer.mp3")

# Upload user's reply
st.markdown("### 🎙️ Upload your voice reply")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a", "ogg"])

if uploaded_file:
    with open("uploaded_audio", "wb") as f:
        f.write(uploaded_file.read())
    st.session_state["uploaded_audio"] = True  # Mark that an upload happened

    user_text = transcribe_audio("uploaded_audio")

    if user_text:
        st.success(f"🗨️ You said: {user_text}")
        feedback = analyze_tone_with_gemini(user_text)
        st.info(f"🧠 {feedback}")
    else:
        st.error("⚠️ Could not understand your voice.")

# Button to regenerate scenario
st.markdown("---")
if st.button("🔄 New Customer"):
    # Clear the customer scenario
    st.session_state.pop("scenario_text", None)

    # Delete customer.mp3 if exists
    if os.path.exists("customer.mp3"):
        os.remove("customer.mp3")

    # Delete uploaded audio if exists
    if os.path.exists("uploaded_audio"):
        os.remove("uploaded_audio")
    st.session_state.pop("uploaded_audio", None)

    # Rerun the app fresh
    st.rerun()
