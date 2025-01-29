from langchain_google_genai import ChatGoogleGenerativeAI
from ollama import chat
from ollama import ChatResponse
import time


def get_response_from_llm(which_model, which_prompt, extracted_text, api_secret_key=None):

    # use switch statement
    match which_model.lower():
        case 'gemini-1.5-flash' | 'gemini-1.5':
            response = get_response_from_google_llm(which_model, which_prompt, extracted_text, api_secret_key)
        case 'deepseek-r1:7b' | 'deepseek-r1:1.5b':
            response = get_response_from_deepseek_llm(which_model, which_prompt, extracted_text)
        case _:  # default
            response = get_response_from_deepseek_llm(which_model, which_prompt, extracted_text)

    return response

def get_response_from_deepseek_llm(which_model, which_prompt, extracted_text):
    print("running deepseek model", which_model)
    start_time = time.time()
    response: ChatResponse = chat(model= which_model, #'deepseek-r1:1.5b',
                                  messages=[
                                        {
                                            'role': 'user',
                                            'content': which_prompt + '\n' + extracted_text ,
                                        },
                                    ])
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    response = response['message']['content']
    print(response)
    response_json = response.split("</think>")[1]
    d = response_json
    response_json = response_json.replace("\n", "")
    if response_json.startswith("```json"):
        response_json = response_json[7:-3]
    print(response_json)
    response_json = eval(response_json)
    print(response_json)
    return response_json

def get_response_from_google_llm(which_model, which_prompt, extracted_text, api_secret_key):
    print("running gemini model", which_model)
    start_time = time.time()

    llm = ChatGoogleGenerativeAI(
            model=which_model, #"gemini-1.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_secret_key
        )
    print(which_prompt)

    messages = [
            (
                "system",
                which_prompt,
            ),
            ("human", extracted_text),
        ]
    # Initialize LangChain with the prompt and LLM
    ai_msg = llm.invoke(messages)

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

    # Run the chain with the document text
    quiz_json = eval(ai_msg.content)
    # quiz_json = helper.dummy_output
    print(quiz_json)
    return quiz_json
