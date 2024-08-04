from fastapi import FastAPI
import google.generativeai as genai
import os
from dotenv import load_dotenv, dotenv_values
from entities import PromptText
import requests
import json
import boto3

load_dotenv()

app = FastAPI()

@app.get("/{title}")
def generate_highlights(title: str):
    content = search_from_text_db(title)

    key_phrases = get_key_phrases(content)

    response = genai_pipeline(title, key_phrases)
    
    return { "Response": response }

def separate_term_from_key_phrase_object(key_phrase_object):
    return key_phrase_object["Text"]

def get_key_phrases(content):
    client = boto3.client(
        'comprehend',
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
        aws_session_token=os.getenv("SESSION_TOKEN"),
        region_name='us-east-1'
    )

    response = client.detect_key_phrases(
        Text=content,
        LanguageCode='en'
    )

    key_phrases_list = list(map(separate_term_from_key_phrase_object, response["KeyPhrases"]))

    return list(set(key_phrases_list))

def search_db_ref(title: str) -> str:
    search = f'https://en.wikipedia.org/w/rest.php/v1/search/title?q={title}&limit=1'
    search_response = requests.get(search)

    search_response_json = json.loads(search_response.text)

    searched_term = ""

    if len(search_response_json["pages"]) > 0:
        searched_term = search_response_json["pages"][0]["title"]
    else:
        raise Exception("Couldn't find searched term")

    return searched_term

def search_from_text_db(title: str) -> str:
    searched_term = search_db_ref(title)

    url = f'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles={searched_term}&redirects='
    response = requests.get(url)

    response_json = json.loads(response.text)

    content = ""

    sub_str = "=="

    for page in response_json["query"]["pages"].keys():
        content = response_json["query"]["pages"][page]["extract"]

    content = content[:content.index(sub_str) + len(sub_str)]

    content = content.lower()

    return content


def genai_pipeline(theme, terms):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.0-pro-latest')

    terms = ';'.join(terms)
    print(terms)
    prompt = f"With the following theme: {theme}\nClassify these terms: {terms} in order of importance from 1 (most important) to 5 (less important) and return a tuple with (term, grade) format"
    
    text = model.generate_content(prompt).text
    return text.split("\n")