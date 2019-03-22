import os
import json
from googleapiclient.discovery import build

is_docker = os.environ.get('DOCKER_CONTAINER', False)

if is_docker:
    DEVELOPER_KEY = os.environ.get('PROD_YOUTUBE_KEY')
else:
    with open('keys.json') as json_file:
        json_keys = json.load(json_file)
        DEVELOPER_KEY = json_keys['keys']['Dev']['youtube_key']

YOUTUBE_BASE_VIDEO_URL = 'https://www.youtube.com/watch?v='


def how_to_play(string):
    youtubeAPI = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
    response = youtubeAPI.search().list(
        q='how to play ' + string,
        part='id,snippet',
        maxResults=1,
        type='video'
    ).execute()
    for search_result in response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
    return(YOUTUBE_BASE_VIDEO_URL + video_id)


def game_ambiance(string):
    youtubeAPI = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
    response = youtubeAPI.search().list(
        q=string + ' ambiance music',
        part='id,snippet',
        maxResults=1,
        type='video'
    ).execute()
    for search_result in response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
    return(YOUTUBE_BASE_VIDEO_URL + video_id)
