from flask import Flask, render_template, request, send_file
from youtube_dl import YoutubeDL

import os

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'tmp\%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        url = request.form['link']
        yt = YoutubeDL(ydl_opts)
        get_url = yt.extract_info(url, download=True)
        return render_template('index.html', get_url=get_url)

    return render_template('index.html')

@app.route('/tmp/<path:url>/')
def download(url):
    return send_file(f'../tmp/{url}')

if __name__ == "__main__":
    app.run()
