import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from langchain_google_genai import ChatGoogleGenerativeAI
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

from utils import helper
from utils.google_forms.g_forms_api_connection import authenticate_google_api, \
    create_google_form, add_quiz_settings, add_questions, \
    update_google_form, grant_permissions


load_dotenv()

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.api_secret_key = os.getenv('GEMINI_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SHARE_GMAIL'] = 'yogeshrajgure.vraj@gmail.com'

extracted_text = ""

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs2Quiz', methods=['POST', 'GET'])
def docs2Quiz():
    session['which_prompt'] = helper.llm_prompt_for_docs_quiz
    return render_template('docs2Quiz.html')

@app.route('/interQuiz', methods=['POST', 'GET'])
def interQuiz():
    session['which_prompt'] = helper.llm_prompt_for_interview_quiz
    return render_template('docs2Quiz.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and helper.allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract text from the uploaded document
        global extracted_text
        extracted_text = helper.extract_text_from_file(filepath)

        # Delete the file from the saved path
        os.remove(filepath)
        # print(extracted_text)

        return jsonify({"message": "File uploaded successfully"}), 200

    return jsonify({"error": "File type not allowed"}), 400

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    try:
        # Get extracted text from the client
        if not extracted_text:
            return jsonify({"error": "No document text provided"}), 400

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=app.api_secret_key
        )
        print(session['which_prompt'])

        messages = [
            (
                "system",
                session['which_prompt'],
            ),
            ("human", extracted_text),
        ]

        # Initialize LangChain with the prompt and LLM
        ai_msg = llm.invoke(messages)

        # Run the chain with the document text
        quiz_json = eval(ai_msg.content)
        # quiz_json = helper.dummy_output
        print(quiz_json)

        # Store quiz_json in session
        session['quiz_json'] = quiz_json

        return redirect(url_for('quiz_options'))

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/quiz-options')
def quiz_options():
    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == 'take-quiz':
            return redirect(url_for('take_quiz'))
        elif choice == 'export-google-form':
            return redirect(url_for('export_google_form'))

    return render_template('quiz_options.html')

@app.route('/take-quiz', methods=['POST', 'GET'])
def take_quiz():
    return render_template('take_quiz.html', quiz=session['quiz_json'])

@app.route('/review_questions')
def review_questions():
    return render_template('review_questions.html', quiz=session['quiz_json'])

@app.route('/export-google-form', methods=['GET', 'POST'])
def export_google_form():
    try:
        # call function to export quiz_json to Google Forms API
        service = authenticate_google_api()
        if not service:
            raise Exception("Failed to authenticate Google API")

        form_id = create_google_form(service, session['quiz_json']["title"])
        if not form_id:
            raise Exception("Failed to create Google Form")
        requests = []
        requests = add_quiz_settings(requests)
        if 'quiz_json' in session and 'questions' in session['quiz_json'] and isinstance(session['quiz_json']['questions'], list):
            requests = add_questions(requests, session['quiz_json']['questions'])
        else:
            return jsonify({"error": "Invalid quiz data"}), 400

        if update_google_form(service, form_id, requests):
            if grant_permissions(service, form_id, app.config['SHARE_GMAIL']):
                session['google_form_link'] = f"https://docs.google.com/forms/d/{form_id}"

        # Logic to export quiz_json to Google Forms API can be added here
        return render_template('export_google_form.html', form_link=session['google_form_link'])
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/submit-quiz', methods=['POST', 'GET'])
def submit_quiz():
    return render_template('index.html')


def generate_questions_from_document(filename, prompt):
    # Simulated question generation logic
    return [f"Question {i+1} based on {filename}" for i in range(10)]



if __name__ == '__main__':
    app.run(debug=True)
