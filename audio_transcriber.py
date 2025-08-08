import whisper

def transcribe_audio_with_whisper(audio_path):
    """Loads Whisper, transcribes the MP3 (or WAV) at audio_path, returns the text."""
    model = whisper.load_model("base")  # switch to "small", "medium", etc., for speed/accuracy
    result = model.transcribe(audio_path)
    return result.get("text", "")
