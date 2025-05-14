# 🧠 AI Cashier Training Assistant

This is a Streamlit-based AI assistant designed to help train new retail cashiers. It provides interactive roleplay with AI-generated customer scenarios, voice-based input/output, real-time feedback, and scoring to simulate real-life customer interactions.


## ✨ Features

- 🗣️ AI-generated customer scenarios (via Gemini 2.0 Flash)
- 🎧 Customer voices generated (via Google Text-to-Speech)
- 🎙️ Upload your spoken reply (any format: mp3, wav, m4a, ogg)
- 🧠 Friendly feedback on your greeting (via Gemini 2.0 Flash)
- 🎯 Smart auto-conversion and accurate transcription (via Google Speech-to-Text)



## 🧱 Project Structure

```
.
├── app.py                       # Streamlit entry point
├── utils/
│   ├── gemini_generator.py      # Gemini 2.0 Flash prompt logic
│   ├── google_tts.py            # Google TTS voice generation
│   ├── scenario_examples.json   # Scenario prompt template
│   ├── scoring.py               # Gemini-based scoring logic
│   ├── scoring_examples.json    # Scoring examples context
│   └── transcription.py         # Whisper-based audio transcription
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── .streamlit/
    └── secrets.toml             # API credentials and secrets
```

---

## ⚙️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-cashier-trainer.git
cd ai-cashier-trainer
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Streamlit secrets

Create a `.streamlit/secrets.toml` file with the following content:

```toml
GEMINI_API_KEY = "your-google-gemini-api-key"

[GOOGLE_APPLICATION_CREDENTIALS]
"type" = "service_account"
"project_id" = "some_id"
"private_key_id" = "some_private_key_id"
"private_key" = "some_private_key"
"client_email" = "some_client_email"
"client_id" = "some_client_id"
"auth_uri" = "https://accounts.google.com/o/oauth2/auth"
"token_uri" = "https://oauth2.googleapis.com/token"
"auth_provider_x509_cert_url" = "https://www.googleapis.com/oauth2/v1/certs"
"client_x509_cert_url" = "some_client_x509_cert_url"
"universe_domain" = "googleapis.com"
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Make sure your mic permissions are granted if using the voice input.
