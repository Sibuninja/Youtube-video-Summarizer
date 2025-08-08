import os, time
import yt_dlp

def download_youtube_audio(url, output_path="downloads"):
    """Downloads the best audio stream from the given YouTube URL and returns the MP3 path."""
    os.makedirs(output_path, exist_ok=True)
    timestamp = int(time.time())
    template = os.path.join(output_path, f"audio_{timestamp}.%(ext)s")
    opts = {
        "format": "bestaudio/best",
        "outtmpl": template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    return template.replace("%(ext)s", "mp3")
