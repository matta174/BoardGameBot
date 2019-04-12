import os
import json

from googleapiclient.discovery import build
from util.config import DEVELOPER_KEY


YOUTUBE_BASE_VIDEO_URL = 'https://www.youtube.com/watch?v='

#variables to keep track of the last video search for next_video()
last_video = ''
request_type = 0
vidNum = 2


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

    global last_video 
    global request_type
    global vidNum

    last_video = string
    request_type = 1
    vidNum = 2

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

    global last_video 
    global request_type
    global vidNum

    last_video = string
    request_type = 2
    vidNum = 2

    return(YOUTUBE_BASE_VIDEO_URL + video_id)

def search_next_video():
    global last_video 
    global request_type
    global vidNum
    qType = ''

    #determines which type of video to return the next result for based on last search term and type
    if request_type == 1:
        qType = 'how to play ' + last_video      
    elif request_type == 2:
        qType = last_video + ' ambiance music'
    else:
        return "No recently played video found."

    youtubeAPI = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
    response = youtubeAPI.search().list(
        q=qType,
        part = 'id, snippet',
        maxResults = vidNum,
        type = 'video'
    ).execute()
    for search_result in response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']

    #returns the video id of the last result based on maxResult
    vidNum+=1
    if vidNum > 10:
        vidNum = 2
    return(YOUTUBE_BASE_VIDEO_URL + video_id)
    