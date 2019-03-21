from googleapiclient.discovery import build
from keys import DEVELOPER_KEY

DEVELOPER_KEY = DEVELOPER_KEY
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