from email.mime import text
import re
def extract_email(text):

    pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_phone(text):

    pattern = r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b'

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"



def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) > 2 and line.isupper():

            return line.title()

    return "Not Found"



def extract_skills(text):

    skills_database = [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "React",
        "Node.js",
        "MongoDB",
        "MySQL",
        "SQL",
        "Git",
        "GitHub",
        "Machine Learning",
        "TensorFlow",
        "PyTorch",
        "Streamlit",
        "Flask",
        "Django"
    ]

    found_skills = []

    for skill in skills_database:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    return found_skills