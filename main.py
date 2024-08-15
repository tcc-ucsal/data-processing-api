from fastapi import FastAPI
import os
from dotenv import load_dotenv, dotenv_values
from text_db import TextDB
from key_phrase_finder import KeyPhraseFinder
from ranking import Ranking

load_dotenv()

app = FastAPI()

app.text_db = TextDB()
app.ranking = Ranking(os.getenv("GOOGLE_API_KEY"))
app.key_phrase_finder = KeyPhraseFinder(os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY"), os.getenv("AWS_SESSION_TOKEN"))

@app.get("/highlight/{title}")
def generate_highlights(title: str):
    content, full_text = app.text_db.search_from_text_db(title)

    key_phrases = app.key_phrase_finder.get_key_phrases(content)

    response = app.ranking.get_ranks(title, key_phrases)
    
    return { "nodes": response, "article": full_text }