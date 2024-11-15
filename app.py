from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# API URL for fetching video data
API_URL = "https://tikwm.com/api/"

@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend HTML page

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('videoUrl')

    if not video_url:
        return jsonify({'error': 'Please provide a TikTok video URL.'}), 400
    
    # Call the TikTok API to fetch video data
    response = requests.get(f'{API_URL}?url={video_url}')
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch video details.'}), 500
    
    data = response.json()

    if data['code'] != 0:
        return jsonify({'error': data['msg']}), 500

    video_data = {
        'title': data['data']['title'],
        'cover': data['data']['cover'],
        'video_url': data['data']['play'],
        'music_url': data['data']['music'],
        'music_title': data['data']['music_info']['title']
    }
    
    return jsonify(video_data)

if __name__ == '__main__':
    app.run(debug=True)
