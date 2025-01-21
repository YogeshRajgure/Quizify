from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive'
    ]

# Authenticate with Google Forms API
def authenticate_google_api():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
        )
    service = build('forms', 'v1', credentials=credentials)
    print("authentication complete")
    return service

def create_google_form(service, title):
    form = {
        "info": {
            "title": title,
        }
    }
    result = service.forms().create(body=form).execute()
    form_id = result['formId']
    print("create google form complete")
    return form_id

def add_quiz_settings(requests):
    # requests = []
    requests.append({
        "updateSettings": {
            "settings": {
                "quizSettings": {
                    "isQuiz": True
                }
            },
            "updateMask": "quizSettings.isQuiz"
        }
    })
    print("add quiz settings complete")
    return requests

def add_questions(requests, questions):
    # requests = []
    # Add questions with correct answers
    for question in questions:
        # Identify the correct answer's index
        correct_index = question["choices"].index(question["answer"])
        requests.append({
            "createItem": {
                "item": {
                    "title": question["question"],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [{"value": opt} for opt in question["choices"]],
                                "shuffle": False
                            },
                            "grading": {  # Add grading information
                                "correctAnswers": {
                                    "answers": [{
                                        "value": question["choices"][correct_index]
                                    }]
                                },
                                "pointValue": 1  # Assign 1 point for the correct answer
                            }
                        }
                    },
                },
                "location": {
                    "index": 0  # Insert each question at the beginning (reverse order)
                }
            }
        })
    print("add questions complete")
    return requests

def update_google_form(service, form_id, requests):
    try:
        service.forms().batchUpdate(
            formId=form_id,
            body={"requests": requests}
        ).execute()
        print(f"Form created: https://docs.google.com/forms/d/{form_id}/edit")
        return True
    except Exception as e:
        print(e)
        raise Exception("Error updating Google Form")

def grant_permissions(service, form_id, email):
    try:
        credentials = service_account.Credentials.from_service_account_file(
                        SERVICE_ACCOUNT_FILE,
                        scopes=SCOPES
                    )
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': email
        }
        drive_service = build('drive', 'v3', credentials=credentials)
        drive_service.permissions().create(
            fileId=form_id,
            body=permission,
            fields='id'
        ).execute()
        print("Permission granted successfully.")
        return True
    except Exception as e:
        print(e)
        raise Exception("Error granting permission to Google Form")
