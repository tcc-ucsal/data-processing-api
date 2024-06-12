from fastapi import FastAPI
import google.generativeai as genai
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

app =  FastAPI()

@app.get("/{prompt}")
def hello_world(prompt):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    
    response = model.generate_content(prompt)
    
    return { "Response": response.text }
