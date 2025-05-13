import os
import json
import google.generativeai as genai
import streamlit as st

# Load environment variables
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load examples from JSON
examples_path = os.path.join(os.path.dirname(__file__), "scenario_examples.json")
with open(examples_path, "r", encoding="utf-8") as f:
    examples = json.load(f)

def generate_customer_scenario():
    """Generate a short, natural customer utterance for a Nike store using Gemini 2.0 Flash."""

    system_prompt = (
        "You are a customer who just entered a Nike store or approached the cashier for the first time. Generate a short, natural utterance (1-2 sentences, max 25 words) for this first interaction. Do not mention specific products with names, be general"
    )

    task_prompt = "Generate a new natural customer utterance for the first interaction in a Nike store."

    model = genai.GenerativeModel('gemini-2.0-flash')

    content = [{"role": "user", "parts": [system_prompt]}]
    for ex in examples:
        content.append({"role": "user", "parts": [ex["user"]]})
        content.append({"role": "model", "parts": [ex["model"]]})
    content.append({"role": "user", "parts": [task_prompt]})

    response = model.generate_content(content)
    return response.text.strip()
