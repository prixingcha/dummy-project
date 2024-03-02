from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
import json

# OAuth 2.0 credentials flow
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secrets.json',
    scopes=['https://www.googleapis.com/auth/youtube.readonly']
)
credentials = flow.run_local_server(port=8080)

# Create a YouTube API client
youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)


string_list = []

all_json_obj = {}


next_page_token = None
i  = 0
while True:
    # Get the list of subscribed channels
    channels_response = youtube.subscriptions().list(
        mine=True,
        part='snippet',
        maxResults=50,  # Maximum number of results per page, change as needed
        pageToken=next_page_token,  # Use the next page token
    ).execute()
    # Iterate over the subscribed channels and print their titles
    for item in channels_response['items']:
        i = i  + 1
        
        # channel_name = item['snippet']['title']
        channel_id = item['snippet']['resourceId']["channelId"]
        
        # title = item['snippet']['title']
        # str = f"{channel_id} : {channel_name}"
        
        
        string_list.append(channel_id)
        
        # all_json_obj.update(data_dict)

        # print(data_dict)
        
        # print(json.dumps(channels_response, indent=4, ensure_ascii=True))
        # break
        # print(f"{title} :  https://www.youtube.com/{title}")
    # break
    # Check if there are more pages
    next_page_token = channels_response.get('nextPageToken')
    if not next_page_token:
        break
print('testing')
# full_subscribe_list = json.dumps(string_list, indent=None)
# print(string_list)

print(string_list)
# # Write the merged dictionary to a JSON file
with open('subscribe_list.json', 'w') as file:
    file.write(str(string_list))


# Shutdown the OAuth server gracefully
# oauth_server = flow._oauth2_inst._server
# oauth_server.shutdown()
