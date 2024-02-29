import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


flow = InstalledAppFlow.from_client_secrets_file(
    "new-token2.json",  scopes=scopes 
)
flow.run_local_server(port=8080, prompt="consent")

credentails = flow.credentails
print(credentails.to_json())