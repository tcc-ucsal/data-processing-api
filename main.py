from fastapi import FastAPI
import google.generativeai as genai
import os
from dotenv import load_dotenv, dotenv_values
from entities import PromptText
import requests
import json

load_dotenv()

app = FastAPI()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.0-pro-latest')

@app.get("/{title}")
def generate_highlights(title: str):
    content = search_from_text_db(title)

    response = genai_pipeline(content)
    
    return { "Response": response.text }

def search_from_text_db(title: str) -> str:
    url = f'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles={title}&redirects='
    response = requests.get(url)

    response_json = json.loads(response.text)

    content = ""

    sub_str = "=="

    for page in response_json["query"]["pages"].keys():
        content = response_json["query"]["pages"][page]["extract"]

    content = content[:content.index(sub_str) + len(sub_str)]

    return content


def genai_pipeline(text):
    prompt = """With the following text: \n""" + text + """\nHighlight the 20 most important words to understand the subject and classify these words in
    order from 1-5 where 1 is the most important and 5 is the less important"""
    
    return model.generate_content(prompt + text)