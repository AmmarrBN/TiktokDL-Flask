from flask import Flask, render_template, request, jsonify, send_file
import requests
import os

app = Flask(__name__)

# Helper function to fetch TikTok video data
def fetch_tiktok_data(url):
    api_url = f"https://tikwm.com/api/?url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.json.get('url')
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400
    
    data = fetch_tiktok_data(video_url)
    if not data or data.get('code') != 0:
        return jsonify({'error': 'Failed to fetch TikTok video data'}), 500

    video_data = data['data']
    return jsonify({
        'author': video_data['author']['nickname'],
        'title': video_data['title'],
        'cover': video_data['cover'],
        'music': video_data['music'],
        'play': video_data['play']
    })

@app.route('/download/<media_type>', methods=['GET'])
def download_file(media_type):
    url = request.args.get('url')
    if not url or media_type not in ['audio', 'video']:
        return "Invalid request", 400
    
    file_extension = 'mp3' if media_type == 'audio' else 'mp4'
    file_name = f"download.{file_extension}"

    # Download the file
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return send_file(file_name, as_attachment=True)
    return "Failed to download file", 500

if __name__ == '__main__':
    app.run(debug=True)
