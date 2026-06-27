import streamlit as st
from utils import extract_text_from_pdf
from parser import (
    extract_email,
    extract_phone,
    extract_name
)

st.title("AI Resume Parser")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    text = extract_text_from_pdf(uploaded_file)

    st.write("Length of extracted text:", len(text))

    st.text_area(
        "Debug OCR Text",
        text,
        height=200
    )

    email = extract_email(text)

    phone = extract_phone(text)

    name = extract_name(text)

    st.subheader("Extracted Resume Text")

    st.subheader("Extracted Information")


    st.write("📧 Email :", email)

    st.write("📱 Phone :", phone)

    st.write("👤 Name :", name)
    st.text_area("OCR Output", text, height=300)