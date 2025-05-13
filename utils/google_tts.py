from google.cloud import texttospeech
from google.oauth2 import service_account
import streamlit as st

creds = service_account.Credentials.from_service_account_info(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])

def generate_google_tts(text, filename="customer.mp3"):
    client = texttospeech.TextToSpeechClient(credentials=creds)

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(filename, "wb") as out:
        out.write(response.audio_content)