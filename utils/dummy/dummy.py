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

with open('mcqs.json', 'r') as file:
    mcqs = json.load(file)

# Create the form structure
form = {
    "info": {
        "title": mcqs["title"],
    }
}

# Create the form
result = service.forms().create(body=form).execute()
form_id = result['formId']

requests = []

# Add quiz settings to enable showing scores after submission
requests.append({
    "updateSettings": {
        "settings": {
            "quizSettings": {
                "isQuiz": True  # Enable quiz mode
            }
        },
        "updateMask": "quizSettings.isQuiz"
    }
})

# Add questions with correct answers
for question in mcqs['questions']:
    # Identify the correct answer's index
    correct_index = question["options"].index(question["correct_option"])

    requests.append({
        "createItem": {
            "item": {
                "title": question["question"],
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [{"value": opt} for opt in question["options"]],
                            "shuffle": False
                        }
                    }
                },
                "grading": {  # Add grading information
                    "correctAnswers": {
                        "answers": [{
                            "value": question["options"][correct_index]
                        }]
                    },
                    "pointValue": 1  # Assign 1 point for the correct answer
                }
            },
            "location": {
                "index": 0  # Insert each question at the beginning (reverse order)
            }
        }
    })

# Batch update to add questions
batch_update = {"requests": requests}
service.forms().batchUpdate(formId=form_id, body=batch_update).execute()

print(f"Form created: https://docs.google.com/forms/d/{form_id}/edit")

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
