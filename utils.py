import os
from pytube import YouTube
from moviepy.editor import AudioFileClip

def download_youtube_audio(url, output_path="downloads"):
    os.makedirs(output_path, exist_ok=True)
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    if stream is None:
        raise ValueError("No audio stream found for this video.")
    audio_path = stream.download(output_path=output_path, filename="audio.mp4")
    return audio_path

def extract_audio_to_wav(mp4_path, output_path="downloads"):
    output_wav = os.path.join(output_path, "audio.wav")
    audio_clip = AudioFileClip(mp4_path)
    audio_clip.write_audiofile(output_wav, codec='pcm_s16le')
    audio_clip.close()
    return output_wav
