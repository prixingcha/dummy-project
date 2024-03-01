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

class YouTubeChannelMonitor:
    def __init__(self, api_key, channel_ids_file):
        self.api_key = api_key
        self.channel_ids = self.load_channel_ids(channel_ids_file)
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.current_datetime = datetime.utcnow()
        self.previous_datetime = self.current_datetime - timedelta(hours=24)
        self.results = []

    def load_channel_ids(self, file_path):
        with open(file_path) as f:
            return json.load(f)['first_names']

    def get_channel_info(self, channel_id):
        try:
            channel_response = self.youtube.channels().list(
                part="brandingSettings,contentDetails,contentOwnerDetails,id,localizations,snippet,statistics,status,topicDetails",
                id=channel_id
            ).execute()
            return channel_response['items'][0] if 'items' in channel_response else None
        except HttpError as e:
            print("An HTTP error occurred:", str(e))
            return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None

    def get_latest_video(self, channel_id):
        try:
            response = self.youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=1,
                order="date",
                type="video",
            ).execute()
            return response['items'][0] if 'items' in response else None
        except HttpError as e:
            print("An HTTP error occurred:", str(e))
            return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None

    def get_video_stats(self, video_id):
        try:
            stats_response = self.youtube.videos().list(
                part='statistics,contentDetails',
                id=video_id
            ).execute()
            return stats_response['items'][0] if 'items' in stats_response else None
        except HttpError as e:
            print("An HTTP error occurred:", str(e))
            return None
        except Exception as e:
            print("An error occurred:", str(e))
            return None

    def format_video_duration(self, duration):
        time_components = [int(match.group(1)) if match else 0
                            for match in [re.search(r'(\d+)H', duration),
                                          re.search(r'(\d+)M', duration),
                                          re.search(r'(\d+)S', duration)]]
        return f"{time_components[0]:02d}:{time_components[1]:02d}:{time_components[2]:02d}"

    def process_channel(self, channel_id):
        result = {}
        channel_info = self.get_channel_info(channel_id)
        if channel_info:
            snippet = channel_info['snippet']
            channel_name = snippet['title']
            creation_year = int(snippet['publishedAt'][:4])
            country = snippet.get('country', 'Unknown')
            
            latest_video = self.get_latest_video(channel_id)
            if latest_video:
                video_date = datetime.strptime(latest_video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=None)
                if self.previous_datetime <= video_date <= self.current_datetime:
                    video_id = latest_video['id']['videoId']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    video_stats = self.get_video_stats(video_id)
                    if video_stats:
                        stats = video_stats['statistics']
                        total_likes = int(stats.get('likeCount', 0))
                        total_dislikes = int(stats.get('dislikeCount', 0))
                        total_views = int(stats.get('viewCount', 0))
                        
                        result["thumbnail"] = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                        result[emojis.title] = channel_info['snippet']['title'] + " >>> " + latest_video['snippet']['title']
                        result[emojis.url] = video_url
                        result["status"] = emojis.like + " "+ '{:,}'.format(int(total_likes)) \
                            + "  " + emojis.dislike + " " + '{:,}'.format(int(total_dislikes)) + emojis.views \
                            + "  " + '{:,}'.format(int(total_views))
                        result["others"] = emojis.duration \
                            + "  " + self.format_video_duration(video_stats['contentDetails']['duration']) \
                            + "  " + emojis.subscribers \
                            + '{:,}'.format(int(channel_info['statistics'].get('subscriberCount', 0))) \
                            + emojis.country +  country + " " + emojis.created +  " " + str(creation_year)
                        
        return result

    def monitor_channels(self):
        for channel_id in self.channel_ids:
            result = self.process_channel(channel_id)
            if result:
                self.results.append(result)
        
        filtered_data = [obj for obj in self.results if obj]
        results_json = json.dumps(filtered_data, indent=4, ensure_ascii=False)
        print(results_json)

# Example usage
monitor = YouTubeChannelMonitor(API, 'youtube-channel-id.json')
monitor.monitor_channels()
