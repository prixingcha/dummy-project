import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import re
from emoji import emojis

load_dotenv()
API = os.getenv('GOOGLE-API-KEY')

current_datetime = datetime.utcnow()
previous_datetime = current_datetime - timedelta(hours=24)

# Load channel IDs from JSON file
with open('youtube-channel-id.json') as f:
    channel_ids = json.load(f)['first_names']

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=API)

results = []


# channel_response = youtube.channels().list(
#             part="brandingSettings,contentDetails,contentOwnerDetails,id,localizations,snippet,statistics,status,topicDetails",
#             id= ",".join(channel_ids)
#         ).execute()

# res = json.dumps(channel_response, indent=4, ensure_ascii=False)


# print(res)

# exit()

for CHANNEL_ID in channel_ids:
    result = {}
    
    try:
        channel_response = youtube.channels().list(
            part="brandingSettings,contentDetails,contentOwnerDetails,id,localizations,snippet,statistics,status,topicDetails",
            id=CHANNEL_ID
        ).execute()
    
        
        print(json.dumps(channel_response, indent=4, ensure_ascii=False))
        
        
        continue

        if 'items' in channel_response and len(channel_response['items']) > 0:
            channel = channel_response['items'][0]
            snippet = channel['snippet']
            statistics = channel['statistics']

            # Get the channel name, creation year, and country of origin
            channel_name = snippet['title']
            creation_year = int(snippet['publishedAt'][:4])
            country = snippet.get('country', 'Unknown')

            # Get the current date
            current_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

            # Get the latest video uploaded by the channel
            response = youtube.search().list(
                part="snippet",
                channelId=CHANNEL_ID,
                maxResults=1,
                order="date",
                type="video",
            ).execute()
            
            if 'items' in response and len(response['items']) > 0:
                video = response['items'][0]
                video_date = datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=None)
                if previous_datetime <= video_date <= current_datetime:
                    video_id = video['id']['videoId']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"

                    # Get video statistics
                    stats_response = youtube.videos().list(
                        part='statistics,contentDetails',
                        id=video_id
                    ).execute()
                    
                    duration =  stats_response['items'][0]['contentDetails']['duration']
                    
                    time_components = [int(match.group(1)) if match else 0
                                    for match in [re.search(r'(\d+)H', duration),
                                                    re.search(r'(\d+)M', duration),
                                                    re.search(r'(\d+)S', duration)]]
                    stats = stats_response['items'][0]['statistics']
                    total_likes = int(stats.get('likeCount', 0))
                    total_dislikes = int(stats.get('dislikeCount', 0))
                    total_views = int(stats.get('viewCount', 0))
                    result["thumbnail"] =f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                    result[emojis.title] = channel_response['items'][0]['snippet']['title'] + " >>> " + video['snippet']['title']
                    result[emojis.url] = video_url
                    result["status"] = emojis.like + " "+ '{:,}'.format(int(total_likes)) \
                        + "  " + emojis.dislike + " " + '{:,}'.format(int(total_dislikes)) + emojis.views \
                        + "  " + '{:,}'.format(int(total_views))
                    result["others"] = emojis.duration \
                        + "  " + f"{time_components[0]:02d}:{time_components[1]:02d}:{time_components[2]:02d}" \
                        + "  " + emojis.subscribers \
                        + '{:,}'.format(int(channel_response['items'][0]['statistics'].get('subscriberCount', 0))) \
                        + emojis.country +  country + " " + emojis.created +  " " + str(creation_year)
                    
                    
                    
                    # result[emojis.channel] = channel_name
                    # result[emojis.created] creation_year
                    # result[emojis.country] = country
                    
                    # result[emojis.url] = video_url
                    # result[emojis.like] = '{:,}'.format(int(total_likes)) 
                    # result[emojis.dislike]  = total_dislikes
                    # result[emojis.views]  = '{:,}'.format(int(total_views))
                    # result[emojis.duration]= f"{time_components[0]:02d}:{time_components[1]:02d}:{time_components[2]:02d}"     
                    # result[emojis.channel]= '{:,}'.format(int(channel_response['items'][0]['statistics'].get('subscriberCount', 0)))
                # else:
                    # result['message'] = "No video uploaded today."
            # else:
            #     result['message'] = "No videos found for the channel."
        else:
            result['message'] = "Channel not found."

    except HttpError as e:
        result['error'] = "An HTTP error occurred: " + str(e)
    except Exception as e:
        result['error'] = "An error occurred: " + str(e)

    # Append result to results list
    results.append(result)

# Convert results to JSON format

filtered_data = [obj for obj in results if obj]

results_json = json.dumps(filtered_data, indent=4, ensure_ascii=False)

print(results_json)
