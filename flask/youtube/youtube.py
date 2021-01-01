from datetime import datetime


from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from models import Channel, Playlist, PlaylistItem

DEVELOPER_KEY = 'AIzaSyBUt2uRD7wvPWOm72P6ivTUljGfb-8F6gE'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# class Option:

#     def __init__(self, q, max_results):
#         self.q = q
#         self.max_results = max_results

# class Channel:
    
#     def __init__(self, **kwargs):
#         self.publishedAt= kwargs.get('publishedAt')
#         self.channelId= kwargs.get('channelId')
#         self.title= kwargs.get('title')
#         self.description= kwargs.get('description')
#         self.thumbnail= kwargs.get('thumbnail')


# class Playlist:
    
#     def __init__(self, **kwargs):
#         self.title = kwargs.get('title')
#         self.Id = kwargs.get('Id')
#         self.publishedAt = kwargs.get('publishedAt')
#         self.description = kwargs.get('description')
#         self.tumbnails = kwargs.get('thumbnails')


# class PlaylistItem:
    
#     def __init__(self, **kwargs):
#         self.Id = kwargs.get('id')
#         self.publishedAt = kwargs.get('publishedAt')
#         self.videoId= kwargs.get('videoId')
#         self.title= kwargs.get('title')
#         self.description= kwargs.get('description')
#         self.thumbnail= kwargs.get('thumbnail')

def searchChannel(keyword):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
            q=keyword,
            type="channel",
            part="id,snippet",
            maxResults=50
        ).execute()

    channels =[]

    for row in search_response['items']:
        
        result = row['snippet']

        channel = Channel()

        channel.youtubeId =  result['channelId']
        
        channel_reponse = youtube.channels().list(
            part="id,snippet,statistics",
            id = channel.youtubeId
        ).execute()

        stats = channel_reponse['items'][0]['statistics']
        
        channel.viewCount = int(stats['viewCount'])
        channel.commentCount = stats.get('commentCount', None)
        channel.subscriberCount = stats.get('subscriberCount', None)
        channel.hiddenSubscriberCount = stats['hiddenSubscriberCount']
        channel.videoCount = int(stats['videoCount'])


        channel.title =  result['title']
        channel.publishedAt =  result['publishedAt']
        channel.description =  result['description']
        channel.thumbnails =  result['thumbnails']['default']

        channels.append(channel)
    
    return channels

 
      
def extractPlaylist(channel_response):

    playlists =[]

    for row in channel_response['items']:
            result = row['snippet']
            playlist = Playlist(
                youtubeId = row['id'],
                title = result['title'],
                publishedAt = result['publishedAt'],
                description = result['description'],
                thumbnails = result['thumbnails']['default']
            )
            playlists.append(playlist)

    return playlists

def searchPlaylist(channelId):
    
    playlists = []
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    channel_response = youtube.playlists().list(
            channelId=channelId,
            part="id,snippet",
            maxResults=50
        ).execute()
    
    playlists.extend(extractPlaylist(channel_response))

    nextPageToken = channel_response.get('nextPageToken', None)
    
    while nextPageToken:
        channel_response = youtube.playlists().list(
            channelId=channelId,
            part="id,snippet",
            pageToken = nextPageToken,
            maxResults=50
        ).execute()

        playlists.extend(extractPlaylist(channel_response))
        nextPageToken = channel_response.get('nextPageToken', None)
    
    return playlists


def extractPlaylistItems(playlist_response):
    playlistItems =[]

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    for row in playlist_response['items']:
        result = row['snippet']

        playlistItem = PlaylistItem()
        playlistItem.youtubeId = row['id']
        playlistItem.youtubeVideoId = result['resourceId']['videoId']
        
        video_response = youtube.videos().list(
            part="id,statistics",
            id=playlistItem.youtubeVideoId,
            maxResults=50
        ).execute()

        stats = video_response['items'][0]['statistics']

        playlistItem.likeCount = stats['likeCount']
        playlistItem.dislikeCount = stats['dislikeCount']
        playlistItem.favoriteCount = stats['favoriteCount']
        playlistItem.commentCount = stats['commentCount']
        playlistItem.publishedAt = result['publishedAt']
        playlistItem.description = result['description']
        playlistItem.thumbnails = result['thumbnails']['default']
        playlistItem.title = result['title']

        playlistItems.append(playlistItem)

    return playlistItems

def searchPlaylistItems(playlistId):
    playlistItems =[]

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    playlist_response = youtube.playlistItems().list(
            playlistId=playlistId,
            part="id,snippet",
            maxResults=50
        ).execute()

    playlistItems.extend(extractPlaylistItems(playlist_response))
    nextPageToken = playlist_response.get('nextPageToken', None)

    while nextPageToken:
        playlist_response = youtube.playlistItems().list(
            playlistId=playlistId,
            part="id,snippet",
            maxResults=50,
            pageToken= nextPageToken
        ).execute()

        playlistItems.extend(extractPlaylistItems(playlist_response))
        nextPageToken = playlist_response.get('nextPageToken', None)
    
    return playlistItems

def searchVideo(videoId):

    video = []
