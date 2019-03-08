from googleapiclient.discovery import build

DEVELOPER_KEY = 'AIzaSyDw2yQyKRU8a-POk2WkeCR3ROxggPpHggw'
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
