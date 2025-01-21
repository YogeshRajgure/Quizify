from googleapiclient.discovery import build
from google.oauth2 import service_account

# Path to your service account credentials
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/forms.body',
          'https://www.googleapis.com/auth/drive']

# Authenticate with Google Forms API
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('forms', 'v1', credentials=credentials)

# Load the JSON file
import json


form_id = "1rNYglTGp3pa4diTKive5IGgnxyuUu9PDy4Ax0PQRk70"

# Add permissions to the form
permission = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': 'yogeshrajgure.vraj@gmail.com'
}

drive_service = build('drive', 'v3', credentials=credentials)

drive_service.permissions().create(
    fileId=form_id,
    body=permission,
    fields='id'
).execute()

print("Permission granted successfully.")
