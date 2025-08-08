import os
from flask import Flask, render_template, request
from utils import download_youtube_audio
from audio_transcriber import transcribe_audio_with_whisper
import requests
from dotenv import load_dotenv

# Load your Groq API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    error = None

    if request.method == "POST":
        url = request.form.get("youtube_url", "").strip()
        if not url:
            error = "Please enter a valid YouTube URL."
        else:
            try:
                # 1. Download audio
                mp3_path = download_youtube_audio(url)

                # 2. Transcribe with Whisper
                transcript = transcribe_audio_with_whisper(mp3_path)
                if not transcript:
                    raise ValueError("Transcription returned empty text.")

                # 3. Summarize via Groq
                payload = {
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant that summarizes video transcripts."},
                        {"role": "user",   "content": f"Summarize this transcript:\n\n{transcript}"}
                    ],
                    "temperature": 0.7
                }
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                r = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    json=payload, headers=headers, timeout=60
                )
                r.raise_for_status()
                summary = r.json()["choices"][0]["message"]["content"]

            except Exception as e:
                error = str(e)

    return render_template("index.html", summary=summary, error=error)

if __name__ == "__main__":
    app.run(debug=True)
