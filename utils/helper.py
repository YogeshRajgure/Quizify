import os
import docx
import PyPDF2


llm_prompt_for_interview_quiz = """
You are an assistant that generates interview quiz questions from resume or job description provided by the user to test their knowledge on those skills.
Based on the text provided by user, create a JSON object with 10 multiple-choice questions to test the user for their skills,
each having 4 options and one correct answer.
Output format:
{
    "title": "Quiz Title",
    "questions": [
        {
            "question": "What is the capital of France?",
            "choices": [
                "Paris",
                "London",
                "Berlin",
                "Madrid"
            ],
            "answer": "Paris"
        },
    ]
}
do not format as ```json\n{ }```
"""

llm_prompt_for_docs_quiz = """
You are an assistant that generates quiz questions from text provided by user.
Based on the text provided by user, create a JSON object with 10 multiple-choice questions,
each having 4 options and one correct answer.
Output format:
{
    "title": "Quiz Title",
    "questions": [
        {
            "question": "What is the capital of France?",
            "choices": [
                "Paris",
                "London",
                "Berlin",
                "Madrid"
            ],
            "answer": "Paris"
        },
    ]
}
do not format as ```json\n{ }```
"""

dummy_output = """
{
  "questions": [
    {
      "question": "What is Yogesh Rajgure's email address?",
      "choices": [
        "yogeshrajgure@gmail.com",
        "yogeshrajgure.vraj@gmail.com",
        "rajgureyogesh@gmail.com",
        "vraj.yogeshrajgure@gmail.com"
      ],
      "answer": "yogeshrajgure.vraj@gmail.com"
    },
    {
      "question": "In which city does Yogesh Rajgure currently work?",
      "choices": [
        "Bengaluru",
        "Mumbai",
        "Pune",
        "Delhi"
      ],
      "answer": "Pune"
    },
  ]
}"""
    # {
    #   "question": "What was the percentage increase in model accuracy for predicting CLTV achieved by Yogesh?",
    #   "choices": [
    #     "5%",
    #     "10%",
    #     "15%",
    #     "20%"
    #   ],
    #   "answer": "10%"
    # },
    # {
    #   "question": "What model did Yogesh use to predict upcoming defects in a system at Intelliswift, achieving ~93% accuracy?",
    #   "choices": [
    #     "XGBoost",
    #     "Random Forest",
    #     "Logistic Regression",
    #     "Support Vector Machine"
    #   ],
    #   "answer": "Random Forest"
    # },
    # {
    #   "question": "By how much did Yogesh improve cost efficiency at Intelliswift by leveraging dbt code optimization and AWS Lambda function code optimization?",
    #   "choices": [
    #     "5%",
    #     "10%",
    #     "15%",
    #     "20%"
    #   ],
    #   "answer": "15%"
    # },
    # {
    #   "question": "Which university did Yogesh Rajgure attend for his Bachelor of Engineering?",
    #   "choices": [
    #     "IIT Bombay",
    #     "BITS Pilani",
    #     "D. Y. Patil Institute of Engineering and Technology",
    #     "College of Engineering, Pune"
    #   ],
    #   "answer": "D. Y. Patil Institute of Engineering and Technology"
    # },
    # {
    #   "question": "What programming language did Yogesh use to automate model creation at ResoluteAI.in, reducing development time by 50%?",
    #   "choices": [
    #     "Java",
    #     "C++",
    #     "Python",
    #     "R"
    #   ],
    #   "answer": "Python"
    # },
    # {
    #   "question": "Which cloud platform did Yogesh use for the Real-Time Sales Data Dashboard project?",
    #   "choices": [
    #     "AWS",
    #     "Azure",
    #     "GCP",
    #     "Snowflake"
    #   ],
    #   "answer": "Snowflake"
    # },
    # {
    #   "question": "Which machine learning model did Yogesh use in his Covid-19 Health Risk Prediction project?",
    #   "choices": [
    #     "Logistic Regression",
    #     "Support Vector Machine",
    #     "Random Forest Classifier",
    #     "Naive Bayes"
    #   ],
    #   "answer": "Random Forest Classifier"
    # },
    # {
    #   "question": "Which framework did Yogesh use for building the web application in his Covid-19 Health Risk Prediction project?",
    #   "choices": [
    #     "React",
    #     "Angular",
    #     "Django",
    #     "Flask"
    #   ],
    #   "answer": "Flask"
    # }
#   ]
# }"""
dummy_output = eval(dummy_output)


def allowed_file(filename, ALLOWED_EXTENSIONS):
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
