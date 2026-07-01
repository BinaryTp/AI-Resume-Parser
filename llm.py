import json
import re

from config import GEMINI_API_KEY

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency
    genai = None

model = None
if genai is not None and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")


def _fallback_parse_resume(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    name = ""
    email = ""
    phone = ""
    skills = []
    education = []
    projects = []
    certifications = []
    achievements = []
    summary = ""

    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    if email_match:
        email = email_match.group(0)

    phone_match = re.search(r"(\+?\d[\d\s().-]{7,}\d)", text)
    if phone_match:
        phone = phone_match.group(1).strip()

    for line in lines:
        lowered = line.lower()
        if not name and not re.search(r"@|\+\d|skills:|education:|projects:|certification", lowered):
            words = re.findall(r"[A-Za-z]+", line)
            if len(words) <= 4 and any(word.isalpha() for word in words):
                name = line
                break

    for line in lines:
        if line.lower().startswith("skills") or "skills:" in line.lower():
            raw_skills = line.split(":", 1)[1] if ":" in line else line
            skills = [s.strip() for s in re.split(r",|\|", raw_skills) if s.strip()]
            break

    if not skills:
        keyword_skills = [
            "python", "java", "javascript", "typescript", "sql", "docker", "aws",
            "azure", "kubernetes", "git", "linux", "react", "node", "fastapi",
            "streamlit", "pandas", "numpy", "opencv", "pytorch", "tensorflow",
            "flask", "django", "mongodb", "postgresql", "mysql", "redis"
        ]
        found_skills = [skill for skill in keyword_skills if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)]
        skills = [skill.title() if skill.islower() else skill for skill in found_skills[:8]]

    for line in lines:
        if line.lower().startswith("education") or "education:" in line.lower():
            education_text = line.split(":", 1)[1].strip() if ":" in line else line
            education = [{
                "degree": education_text,
                "institution": "",
                "location": "",
                "start_date": "",
                "end_date": "",
                "grade": ""
            }]
            break

    for line in lines:
        if line.lower().startswith("projects") or "projects:" in line.lower():
            projects_text = line.split(":", 1)[1].strip() if ":" in line else line
            projects = [{
                "title": projects_text or "Project",
                "description": projects_text or "",
                "technologies": skills[:5]
            }]
            break

    if not summary:
        summary = " ".join(lines[:3]) if lines else ""

    score = 40
    if name:
        score += 10
    if email:
        score += 10
    if phone:
        score += 10
    if skills:
        score += 10
    if education:
        score += 10
    if projects:
        score += 10
    score = min(score, 100)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "github": "",
        "linkedin": "",
        "summary": summary,
        "skills": skills,
        "education": education,
        "projects": projects,
        "certifications": certifications,
        "achievements": achievements,
        "ats_score": score,
        "suggestions": [
            "Add measurable achievements to your experience section.",
            "Highlight your top technical skills with concrete examples.",
            "Include links to GitHub or LinkedIn for stronger credibility."
        ]
    }


def analyze_resume(text):
    if not text or not text.strip():
        return _fallback_parse_resume("")

    if model is not None:
        schema = {
            "name": "",
            "email": "",
            "phone": "",
            "github": "",
            "linkedin": "",
            "summary": "",
            "skills": [],
            "education": [{
                "degree": "",
                "institution": "",
                "location": "",
                "start_date": "",
                "end_date": "",
                "grade": ""
            }],
            "projects": [{
                "title": "",
                "description": "",
                "technologies": []
            }],
            "certifications": [{
                "name": "",
                "issuer": "",
                "year": ""
            }],
            "achievements": [],
            "ats_score": 0,
            "suggestions": []
        }

        prompt = f"""
Extract only the information defined in the JSON schema below.

Do not invent information.
Return exactly 3 suggestions.
Return ATS score between 0 and 100.
Return only technical and professional skills.
Do not include spoken languages inside skills.

Rules:
- Never return markdown.
- Never return explanations.
- Never wrap JSON inside ```json.
- If a field is missing return:
  "" for strings
  [] for lists

Return JSON exactly like this:

{json.dumps(schema, indent=2)}

ATS Score:
Give a score between 0 and 100 based on:
- Resume completeness
- Technical skills
- Education
- Projects
- Overall presentation

Suggestions:
Return exactly 3 suggestions to improve the resume.

Resume:

{text}
"""

        try:
            response = model.generate_content(prompt, generation_config={"temperature": 0.2})
            response_text = (response.text or "").strip()
            response_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(response_text)
            data.setdefault("github", "")
            data.setdefault("linkedin", "")
            data.setdefault("ats_score", 0)
            data.setdefault("suggestions", [])
            data.setdefault("certifications", [])
            data.setdefault("achievements", [])
            return data
        except Exception:
            return _fallback_parse_resume(text)

    return _fallback_parse_resume(text)
