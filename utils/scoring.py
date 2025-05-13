import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load scoring examples
examples_path = os.path.join(os.path.dirname(__file__), "scoring_examples.json")
with open(examples_path, "r", encoding="utf-8") as f:
    examples = json.load(f)

def analyze_tone_with_gemini(user_text):
    """Analyze cashier greeting tone and return short feedback."""

    model = genai.GenerativeModel('gemini-2.0-flash')

    system_prompt = (
        "You are a friendly retail coach helping Nike store cashiers improve their greetings.\n\n"
        "Evaluate the greeting based on warmth, friendliness, and professional helpfulness.\n\n"
        "If the greeting sounds warm, helpful, and professional, ONLY give a positive compliment. DO NOT suggest any improvements.\n\n"
        "If the greeting is missing warmth, friendliness, or sounds rushed, THEN suggest one small improvement after first highlighting a positive.\n\n"
        "Feedback must be brief (one or two short sentences maximum), positive in tone, and forgiving — they are still learning.\n\n"
        "Never give numerical scores."
    )

    content = [{"role": "user", "parts": [system_prompt]}]

    for ex in examples:
        content.append({"role": "user", "parts": [ex["user"]]})
        content.append({"role": "model", "parts": [ex["model"]]})

    content.append({"role": "user", "parts": [f"Cashier says: '{user_text}'"]})

    response = model.generate_content(content)
    return response.text.strip()
