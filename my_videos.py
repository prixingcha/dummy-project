from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery

# OAuth 2.0 credentials flow
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secrets.json',
    scopes=['https://www.googleapis.com/auth/youtube.readonly']
)
credentials = flow.run_local_server(port=8080)

# Create a YouTube API client
youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)

# Get the list of subscribed channels
channels_response = youtube.subscriptions().list(
    mine=True,
    part='snippet',
    maxResults=50  # Maximum number of results per page, change as needed
).execute()

# Iterate over the subscribed channels and print their titles
for item in channels_response['items']:
    snippet = item['snippet']
    title = snippet['title']
    print(f"Subscribed to: {title}")

# Shutdown the OAuth server gracefully
oauth_server = flow._oauth2_inst._server
oauth_server.shutdown()