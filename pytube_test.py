from pytube import YouTube

url = "https://www.youtube.com/watch?v=uAJkvA_IE-Y"
yt = YouTube(url)
stream = yt.streams.filter(only_audio=True).first()
if stream is None:
    print("No audio stream found.")
else:
    stream.download(filename="test_audio.mp4")
    print("Download successful.")
