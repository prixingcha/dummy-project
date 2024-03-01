import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY =  os.getenv('GOOGLE-API-KEY')

# Set the YouTube channel ID here
CHANNEL_ID = "UCwHcAD2W-VitvrmzLT3xE0Q"

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

result = {}

try:
    # Get channel information
    channel_response = youtube.channels().list(
        part="snippet,statistics",
        id=CHANNEL_ID
    ).execute()

    if 'items' in channel_response and len(channel_response['items']) > 0:
        channel = channel_response['items'][0]
        snippet = channel['snippet']
        statistics = channel['statistics']
        
        # Get the channel name, creation year, and country of origin
        channel_name = snippet['title']
        creation_year = int(snippet['publishedAt'][:4])
        country = snippet['country']
        
        # Get the current date
        current_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        
        
        # Get the latest video uploaded by the channel
        response = youtube.search().list(
            part="snippet",
            channelId=CHANNEL_ID,
            maxResults=1,
            order="date",
            type="video"
        ).execute()

        video_id = response['items'][0]['id']['videoId']
        
        
        stats_response = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()
        
        print(json.dumps(response['items'], indent=4))

        print(stats_response)
        print('===================')
        print(f"https://www.youtube.com/watch?v={video_id}")
        print('===================')
        
        exit()

        if 'items' in response and len(response['items']) > 0:
            video = response['items'][0]
            video_date = datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=None)
            
            stats_response = youtube.videos().list(
                part="statistics",
                id=video_id
            ).execute()
            
            print(stats_response)
            
            video_id = video['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            
            
            
            
            # # Check if the video was uploaded today
            # if video_date.date() == current_date.date():
            #     video_id = video['id']['videoId']
            #     video_url = f"https://www.youtube.com/watch?v={video_id}"
                
            #     # Get video statistics
            #     stats_response = youtube.videos().list(
            #         part="statistics",
            #         id=video_id
            #     ).execute()
                
            #     stats = stats_response['items'][0]['statistics']
            #     total_likes = int(stats.get('likeCount', 0))
            #     total_dislikes = int(stats.get('dislikeCount', 0))
            #     total_views = int(stats.get('viewCount', 0))
                
            #     result['channel_name'] = channel_name
            #     result['creation_year'] = creation_year
            #     result['country'] = country
            #     result['title'] = video['snippet']['title']
            #     result['url'] = video_url
            #     result['total_likes'] = total_likes
            #     result['total_dislikes'] = total_dislikes
            #     result['total_views'] = total_views
            # else:
            #     result['message'] = "No video uploaded today."
        else:
            result['message'] = "No videos found for the channel."
    else:
        result['message'] = "Channel not found."
        
except HttpError as e:
    result['error'] = "An HTTP error occurred: " + str(e)
except Exception as e:
    result['error'] = "An error occurred: " + str(e)

# Convert result to JSON format
result_json = json.dumps(result, indent=4)
print(result_json)