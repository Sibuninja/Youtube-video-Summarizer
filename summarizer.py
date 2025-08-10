# summarizer.py
import whisper

model = whisper.load_model("base")


# Simple text summarizer: returns first 3 sentences
def summarize(text, num_sentences=3):
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary = ' '.join(sentences[:num_sentences])
    return summary
