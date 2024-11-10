from fastapi import FastAPI
import os
from dotenv import load_dotenv, dotenv_values
from text_db import TextDB
from key_phrase_finder import KeyPhraseFinder
from ranking import Ranking

load_dotenv()

app = FastAPI()

app.text_db = TextDB()
app.ranking = Ranking()
app.key_phrase_finder = KeyPhraseFinder(os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY"), os.getenv("AWS_SESSION_TOKEN"))

@app.get("/highlight/{title}")
def generate_highlights(title: str):
    content, full_text, source, searched_term = app.text_db.search_from_text_db(title)

    key_phrases = app.key_phrase_finder.get_key_phrases(title, content)

    response = app.ranking.get_ranks(title, key_phrases)
    
    return { "nodes": response, "article": full_text, "source": source, "searched_term": searched_term }

@app.get("/get_search_options/{title}/{limit}")
def show_search_options(title: str, limit: int):
    results = app.text_db.get_search_options(title, limit)

    return { "results": results }

@app.get("/free_highlight/{title}")
def generate_free_highlights(title: str):
    content, full_text, source, searched_term = app.text_db.get_content(title)

    key_phrases = app.key_phrase_finder.get_key_phrases(content)

    response = app.ranking.get_ranks(title, key_phrases)

    return { "nodes": response, "article": full_text, "source": source, "searched_term": searched_term }

@app.get("/full_text/{title}")
def show_full_text(title: str):
    _content, full_text, source, searched_term = app.text_db.search_from_text_db(title)

    return { "article": full_text, "source": source, "searched_term": searched_term }

@app.get("/key_phrases/{title}")
def show_key_phrases(title: str):
    content, _full_text, _url, _title = app.text_db.get_content(title)

    response = app.key_phrase_finder.get_key_phrases(content)

    return response
