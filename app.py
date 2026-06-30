import streamlit as st
from utils import extract_text_from_pdf
from parser import (
    extract_email,
    extract_phone,
    extract_name,
    extract_skills
)
from llm import analyze_resume


st.title("AI Resume Parser")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    text = extract_text_from_pdf(uploaded_file)
    ai_response = analyze_resume(text)

    st.write("Length of extracted text:", len(text))

    st.text_area(
        "Debug OCR Text",
        text,
        height=200
    )

    email = extract_email(text)

    phone = extract_phone(text)

    name = extract_name(text)

    skills = extract_skills(text)


    st.subheader("Extracted Information")

    st.subheader("👤 Candidate Information")

    st.write(f"**Name:** {ai_response['name']}")
    st.write(f"**Email:** {ai_response['email']}")
    st.write(f"**Phone:** {ai_response['phone']}")

    st.subheader("💻 Skills")

    for skill in ai_response["skills"]:
        st.write(f"✅ {skill}")
    
    st.subheader("🎓 Education")

    for edu in ai_response["education"]:

        st.markdown(f"### {edu['degree']}")

        st.write(f"🏫 Institution: {edu['institution']}")

        st.write(f"📅 Years: {edu['years']}")

        st.write(f"📖 Details: {edu['details']}")

        st.divider()


    st.subheader("📂 Projects")

    for project in ai_response["projects"]:

        with st.expander(project["title"]):

            st.write(project["description"])
    
    st.subheader("📝 Professional Summary")

    st.info(ai_response["summary"])
    st.code(ai_response, language="json")


    