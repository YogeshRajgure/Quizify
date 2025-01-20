from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
import PyPDF2
import docx
from utils import helper
from langchain_google_genai import ChatGoogleGenerativeAI



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB


load_dotenv()

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.api_secret_key = os.getenv('GEMINI_KEY')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

extracted_text = ""

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath):
            ext = os.path.splitext(filepath)[1].lower()
            text = ""
            if ext == '.txt':
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
            elif ext == '.pdf':
                with open(filepath, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(reader.pages)):
                        page = reader.pages[page_num]
                        text += page.extract_text()
            elif ext in ['.doc', '.docx']:
                doc = docx.Document(filepath)
                for para in doc.paragraphs:
                    text += para.text + '\n'
            return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs2Quiz', methods=['POST', 'GET'])
def docs2Quiz():
    return render_template('docs2Quiz.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract text from the uploaded document
        global extracted_text
        extracted_text = extract_text_from_file(filepath)

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


        messages = [
            (
                "system",
                helper.llm_prompt,
            ),
            ("human", extracted_text),
        ]

        # Initialize LangChain with the prompt and LLM
        # ai_msg = llm.invoke(messages)

        # # Run the chain with the document text
        # quiz_json = eval(ai_msg.content)
        quiz_json = helper.dummy_output
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

@app.route('/export-google-form')
def export_google_form():
    global quiz_json
    # Logic to export quiz_json to Google Forms API can be added here
    return "Export to Google Forms feature is under construction."

@app.route('/submit-quiz', methods=['POST', 'GET'])
def submit_quiz():

    return render_template('index.html')


def generate_questions_from_document(filename, prompt):
    # Simulated question generation logic
    return [f"Question {i+1} based on {filename}" for i in range(10)]

if __name__ == '__main__':
    app.run(debug=True)