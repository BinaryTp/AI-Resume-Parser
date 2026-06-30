from urllib import response

import google.generativeai as genai
import json

from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_resume(text):

    prompt = f"""
You are an expert AI Resume Parser and HR Assistant.

Analyze the following resume carefully and extract ALL available information.

Return ONLY valid JSON.

Rules:
- Never add explanations.
- Never add markdown.
- Never wrap JSON inside ```json.
- If a field is missing, return "" for strings and [] for lists.
- Never invent information.

Return the following JSON format:

{{
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "github": "",
    "portfolio": "",

    "summary": "",

    "skills": [],
    "tools": [],
    "languages": [],

    "education": [],

    "experience": [],

    "internships": [],

    "projects": [],

    "certifications": [],

    "achievements": [],

    "ats_score": 0,

    "strengths": [],

    "suggestions": []
}}

Resume:

{text}
"""

    response = model.generate_content(prompt)

    response_text = response.text.strip()

    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "")
    response_text = response_text.strip()

    data = json.loads(response_text)

    return data