import io
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import which
from google.cloud import speech
from google.oauth2 import service_account
import streamlit as st

# Set ffmpeg path
AudioSegment.converter = which("ffmpeg")

creds = service_account.Credentials.from_service_account_info(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])
client = speech.SpeechClient(credentials=creds)

def transcribe_audio(file_path, language_code="en-US", max_alternatives=1):
    """Convert audio to 16kHz WAV, clean it, and transcribe using Google Cloud Speech-to-Text."""

    # Load and normalize audio
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio = audio.normalize()

    # Trim long silences
    audio_chunks = split_on_silence(
        audio,
        min_silence_len=500,      # Consider as silence if >500ms
        silence_thresh=audio.dBFS-14,  # dB threshold
        keep_silence=250           # Keep small padding
    )

    if not audio_chunks:
        audio_chunks = [audio]

    cleaned_audio = AudioSegment.silent(duration=250)
    for chunk in audio_chunks:
        cleaned_audio += chunk + AudioSegment.silent(duration=250)

    # Export to WAV
    converted_path = "converted_audio.wav"
    cleaned_audio.export(converted_path, format="wav")

    # Prepare audio for Google API
    with io.open(converted_path, "rb") as f:
        content = f.read()

    recognition_audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        model="video",  # Best model for cashier/customer speech
        use_enhanced=True,
        audio_channel_count=1,
        enable_automatic_punctuation=True,
        max_alternatives=max_alternatives
    )

    try:
        response = client.recognize(config=config, audio=recognition_audio)
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

    if not response.results:
        return None

    # Return best transcript
    transcript = response.results[0].alternatives[0].transcript.strip()
    return transcript