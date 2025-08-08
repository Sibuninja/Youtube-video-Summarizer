import os
import whisper
from pytube import YouTube
from moviepy.editor import AudioFileClip
import tempfile

def download_audio_from_youtube(url):
    try:
        print("📥 Downloading YouTube video...")
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, "audio.mp4")
        video.download(output_path=temp_dir, filename="audio.mp4")
        print(f"✅ Audio downloaded to {audio_path}")
        return audio_path
    except Exception as e:
        print(f"❌ Error downloading video: {e}")
        return None

def transcribe_audio_with_whisper(audio_path):
    try:
        print("🧠 Loading Whisper model...")
        model = whisper.load_model("base")  # or "small", "medium", "large" depending on speed/accuracy tradeoff
        print("📜 Transcribing...")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None

def main():
    url = input("📥 Enter YouTube video URL: ").strip()
    audio_path = download_audio_from_youtube(url)
    
    if audio_path:
        transcript = transcribe_audio_with_whisper(audio_path)
        if transcript:
            print("\n📝 Transcription:\n")
            print(transcript)
        else:
            print("❌ Failed to transcribe audio.")
    else:
        print("❌ Could not download audio.")

if __name__ == "__main__":
    main()
