# 1. Build a Flask app that scrapes data from multiple websites and displays it on your site.
# You can try to scrap websites like youtube , amazon and show data on output pages and deploy it on cloud
# platform .


from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

app = Flask(__name__)

YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_youtube_data(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=5
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        video = {
            'title': search_result['snippet']['title'],
            'description': search_result['snippet']['description'],
            'thumbnail': search_result['snippet']['thumbnails']['default']['url'],
            'url': f"https://www.youtube.com/watch?v={search_result['id']['videoId']}"
        }
        videos.append(video)
    return videos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    youtube_data = get_youtube_data(query)
    return render_template('result.html', youtube_data=youtube_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

    
