from flask import Flask, render_template_string, request
import summarizer
import audio_transcriber
import pytube
import os
import utils
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    error = None
    if request.method == 'POST':
        url = request.form.get('youtube_url')
        if not url:
            error = "Please enter a YouTube video URL."
        else:
            try:
                # Download audio from YouTube (store in project folder)
                audio_path = utils.download_youtube_audio(url, output_path=os.path.dirname(__file__))
                # Transcribe audio
                transcript = audio_transcriber.transcribe(audio_path)
                # Summarize transcript
                summary = summarizer.summarize(transcript)
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                print(tb)
                error = f"Error type: {type(e).__name__}<br>Message: {str(e)}<br><br>Traceback:<br><pre>{tb}</pre>"
                error += "<br><b>Possible reasons:</b> Invalid/unsupported YouTube URL, video is private, age-restricted, region-blocked, or pytube is outdated. Try a different public video or update pytube."
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>YouTube Video Summarizer</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f7f7f7; }
                .container { max-width: 600px; margin: auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }
                input[type=text] { width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 4px; border: 1px solid #ccc; }
                button { padding: 10px 20px; border: none; background: #007bff; color: #fff; border-radius: 4px; cursor: pointer; }
                button:hover { background: #0056b3; }
                .summary { margin-top: 20px; background: #e9ecef; padding: 15px; border-radius: 4px; }
                .error { color: red; margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>YouTube Video Summarizer</h2>
                <form method="post">
                    <input type="text" name="youtube_url" placeholder="Enter YouTube video URL" required />
                    <button type="submit">Summarize</button>
                </form>
                {% if summary %}
                    <div class="summary">
                        <h4>Summary:</h4>
                        <p>{{ summary }}</p>
                    </div>
                {% endif %}
                {% if error %}
                    <div class="error">{{ error }}</div>
                {% endif %}
            </div>
        </body>
        </html>
    ''', summary=summary, error=error)

if __name__ == "__main__":
    app.run(debug=True)
