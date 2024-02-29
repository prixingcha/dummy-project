import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

# Set your API key here
API_KEY = "AIzaSyChsz0qAvBVhe0wSk-x3nLtvyE71ZAl5nU"

# Set the YouTube channel ID here
CHANNEL_ID = "UChz9LmLfA1Q2SCx32fYw-Og" #"UCwHcAD2W-VitvrmzLT3xE0Q"

# Set the path to the token file
TOKEN_FILE = 'token.json'

# Set the scopes required for the YouTube Data API
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

# Load the token file or request authorization if not available
creds = None
if TOKEN_FILE:
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

# Create a YouTube API client
youtube = build('youtube', 'v3', credentials=creds)

# Get the current date and time
current_datetime = datetime.utcnow()

result = {}

try:
    # Get the latest video uploaded by the channel
    response = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        maxResults=1,
        order="date",
        type="video"
    ).execute()

    if 'items' in response and len(response['items']) > 0:
        video = response['items'][0]
        video_date = datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=None)
        
        # Calculate the time elapsed since the video was uploaded
        time_elapsed = current_datetime - video_date
        days = time_elapsed.days
        years = days // 365
        days %= 365
        hours, remainder = divmod(time_elapsed.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Check if the video was uploaded today
        if video_date.date() == current_datetime.date():
            video_id = video['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # Get video statistics
            stats_response = youtube.videos().list(
                part="statistics",
                id=video_id
            ).execute()
            
            stats = stats_response['items'][0]['statistics']
            total_likes = int(stats.get('likeCount', 0))
            total_dislikes = int(stats.get('dislikeCount', 0))
            total_views = int(stats.get('viewCount', 0))
            
            result['title'] = video['snippet']['title']
            result['url'] = video_url
            result['total_likes'] = total_likes
            result['total_dislikes'] = total_dislikes
            result['total_views'] = total_views
            result['time_elapsed'] = {
                'years': years,
                'days': days,
                'hours': hours,
                'minutes': minutes
            }

            # Check if the authenticated user is subscribed to the channel
            subscription_response = youtube.subscriptions().list(
                part="snippet",
                mine=True,
                forChannelId=CHANNEL_ID
            ).execute()
            
            result['is_subscribed'] = len(subscription_response['items']) > 0
            
        else:
            result['message'] = "No video uploaded today."
    else:
        result['message'] = "No videos found for the channel."
        
except HttpError as e:
    result['error'] = "An HTTP error occurred: " + str(e)
except Exception as e:
    result['error'] = "An error occurred: " + str(e)

# Convert result to JSON format
result_json = json.dumps(result, indent=4)
print(result_json)
