

llm_prompt = """
You are an assistant that generates quiz questions from text provided by user.
Based on the text provided by user, create a JSON object with 10 multiple-choice questions,
each having 4 options and one correct answer.
Output format:
{
    "questions": [
        {
            "question": "What is the capital of France?",
            "choices": {
                "a": "Paris",
                "b": "London",
                "c": "Berlin",
                "d": "Madrid"
            },
            "answer": "a"
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
      "choices": {
        "a": "yogeshrajgure@gmail.com",
        "b": "yogeshrajgure.vraj@gmail.com",
        "c": "rajgureyogesh@gmail.com",
        "d": "vraj.yogeshrajgure@gmail.com"
      },
      "answer": "b"
    },
    {
      "question": "In which city does Yogesh Rajgure currently work?",
      "choices": {
        "a": "Bengaluru",
        "b": "Mumbai",
        "c": "Pune",
        "d": "Delhi"
      },
      "answer": "c"
    },
    {
      "question": "What was the percentage increase in model accuracy for predicting CLTV achieved by Yogesh?",
      "choices": {
        "a": "5%",
        "b": "10%",
        "c": "15%",
        "d": "20%"
      },
      "answer": "b"
    },
    {
      "question": "What model did Yogesh use to predict upcoming defects in a system at Intelliswift, achieving ~93% accuracy?",
      "choices": {
        "a": "XGBoost",
        "b": "Random Forest",
        "c": "Logistic Regression",
        "d": "Support Vector Machine"
      },
      "answer": "b"
    },
    {
      "question": "By how much did Yogesh improve cost efficiency at Intelliswift by leveraging dbt code optimization and AWS Lambda function code optimization?",
      "choices": {
        "a": "5%",
        "b": "10%",
        "c": "15%",
        "d": "20%"
      },
      "answer": "c"
    },
    {
      "question": "Which university did Yogesh Rajgure attend for his Bachelor of Engineering?",
      "choices": {
        "a": "IIT Bombay",
        "b": "BITS Pilani",
        "c": "D. Y. Patil Institute of Engineering and Technology",
        "d": "College of Engineering, Pune"
      },
      "answer": "c"
    },
    {
      "question": "What programming language did Yogesh use to automate model creation at ResoluteAI.in, reducing development time by 50%?",
      "choices": {
        "a": "Java",
        "b": "C++",
        "c": "Python",
        "d": "R"
      },
      "answer": "c"
    },
    {
      "question": "Which cloud platform did Yogesh use for the Real-Time Sales Data Dashboard project?",
      "choices": {
        "a": "AWS",
        "b": "Azure",
        "c": "GCP",
        "d": "Snowflake"
      },
      "answer": "d"
    },
    {
      "question": "Which machine learning model did Yogesh use in his Covid-19 Health Risk Prediction project?",
      "choices": {
        "a": "Logistic Regression",
        "b": "Support Vector Machine",
        "c": "Random Forest Classifier",
        "d": "Naive Bayes"
      },
      "answer": "c"
    },
    {
      "question": "Which framework did Yogesh use for building the web application in his Covid-19 Health Risk Prediction project?",
      "choices": {
        "a": "React",
        "b": "Angular",
        "c": "Django",
        "d": "Flask"
      },
      "answer": "d"
    }
  ]
}"""
dummy_output = eval(dummy_output)
