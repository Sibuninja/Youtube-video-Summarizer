import groq
from dotenv import load_dotenv
load_dotenv()
def summarize_with_groq(text):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
    client = groq.Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "Summarize the following transcript in a concise paragraph."},
            {"role": "user", "content": text}
        ],
        max_tokens=256,
        temperature=0.7
    )
    return response.choices[0].message.content
import os
import shutil
import whisper
from pytube import YouTube
from moviepy.editor import AudioFileClip
import tempfile
from transformers import pipeline
def summarize_text(text):
    import logging
    logging.getLogger("transformers.pipeline").setLevel(logging.ERROR)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # HuggingFace models have a max input length, so chunk if needed
    if len(text) > 1000:
        text = text[:1000]
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def download_audio_from_youtube(url):
    try:
        print("📥 Downloading YouTube video with yt-dlp...")
        output_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(output_dir, exist_ok=True)
        audio_path = os.path.join(output_dir, "audio.mp3")
        import subprocess
        yt_dlp_exe = "yt-dlp.exe" if os.name == "nt" else "yt-dlp"
        # Try to find yt-dlp in PATH, else use Scripts folder in venv
        yt_dlp_path = yt_dlp_exe
        scripts_dir = os.path.join(os.path.dirname(os.sys.executable), "Scripts")
        possible_path = os.path.join(scripts_dir, yt_dlp_exe)
        if not shutil.which(yt_dlp_exe) and os.path.exists(possible_path):
            yt_dlp_path = possible_path
        result = subprocess.run([
            yt_dlp_path, "-f", "bestaudio", "-o", audio_path, url
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ yt-dlp error: {result.stderr}")
            return None
        print(f"✅ Audio downloaded to {audio_path}")
        return audio_path
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        return None

def transcribe_audio_with_whisper(audio_path):
    try:
        print("🧠 Loading Whisper model...")
        model = whisper.load_model("tiny")  # much faster, less accurate
        print("📜 Transcribing...")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None

def main():
    import torch
    print("CUDA available:", torch.cuda.is_available())
    print("Device count:", torch.cuda.device_count())
    print("Device name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU found")

    url = input("📥 Enter YouTube video URL: ").strip()
    audio_path = download_audio_from_youtube(url)

    if audio_path:
        transcript = transcribe_audio_with_whisper(audio_path)
        if transcript:
            print("\n📝 Transcription:\n")
            print(transcript)
            print("\n📝 Summary (HuggingFace):\n")
            print(summarize_text(transcript))
            print("\n📝 Summary (Groq):\n")
            try:
                print(summarize_with_groq(transcript))
            except Exception as e:
                print(f"❌ Groq summarization error: {e}")
        else:
            print("❌ Failed to transcribe audio.")
    else:
        print("❌ Could not download audio.")

if __name__ == "__main__":
    main()
