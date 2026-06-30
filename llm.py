from urllib import response

import google.generativeai as genai
import json

from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_resume(text):

    prompt = f"""
You are an expert HR Resume Analyzer.

Analyze the following resume and return ONLY valid JSON.

The JSON must contain these fields:

{{
    "name": "",
    "email": "",
    "phone": "",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "summary": ""
}}

Resume:

{text}
"""

    response = model.generate_content(prompt)

    response_text = response.text 

    response_text = response_text.replace("```json", "")

    response_text = response_text.replace("```", "")

    data = json.loads(response_text)

    return data