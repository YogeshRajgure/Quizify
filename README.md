# Flask Web Application for Document Upload and Question Generation

This project is a Flask web application that allows users to upload documents and generate multiple-choice questions based on the content of those documents using a language model.

You will need to have credentials.json file as shown below

## Download Ollama models for running offline
```powershell
ollama run deepseek-r1:1.5b
ollama run deepseek-r1:7b
```

## Project Structure

```
flask-web-app
├── templates
│   ├── index.html        # Main landing page with upload form
│   ├── upload.html       # Page for entering prompts after document upload
│   └── result.html       # Displays generated multiple-choice questions
├── static
│   ├── css
│   │   └── styles.css    # Styles for the web application
│   └── js
│       └── scripts.js     # JavaScript for client-side functionality
├── uploads               # Directory for temporarily storing uploaded documents
├── utils
│   ├── notebooks
│   ├── google_forms
│   │   └── g_forms_api_connectivity.py
│   └── result.html
├── app.py                # Main application file with Flask routes and logic
├── requirements.txt      # Lists project dependencies
├── credentials.json
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/YogeshRajgure/Quizify.git
   cd flask-web-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python app.py
   ```

5. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage Guidelines

- On the main page, users can upload a document and provide a prompt for generating questions.
- After uploading, users will be redirected to a page where they can enter their prompt.
- Once the prompt is submitted, the application will process the document and display the generated multiple-choice questions.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
