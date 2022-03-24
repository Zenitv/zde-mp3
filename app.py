from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL

import os

ydl_opts = {
    'format': 'bestaudio',
    'outtmpl': '/tmp/%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        url = request.form['url']
        yt = YoutubeDL(ydl_opts)
        data = yt.extract_info(url, download=True)
        return render_template('index.html', data=data)

    return render_template('index.html')

@app.route('/tmp/<path:url>', methods=['GET'])
def download(url):
    if request.method == 'GET':
        return send_file(f"{os.getenv('DIR_TMP')}/{url}")

@app.errorhandler(500)
def base(e):
    return render_template('index.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
