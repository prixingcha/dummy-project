from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'AIzaSyChsz0qAvBVhe0wSk-x3nLtvyE71ZAl5nU'

youtube = build('youtube', 'v3', developerKey=api_key)

# Specify the part parameter to retrieve the snippet
request = youtube.channels().list(part='snippet', forUsername='RJPRAVEEN')
response = request.execute()

print(response)

# # Extract the channel ID and browse ID
# channel_id = response['items'][0]['id']
# browse_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# print(f"Channel ID: {channel_id}")
# print(f"Browse ID: {browse_id}")
