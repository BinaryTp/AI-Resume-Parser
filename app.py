import streamlit as st
import pdfplumber

st.title("AI Resume Parser")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
      for page in pdf.pages:
          extracted_text = page.extract_text()

          if extracted_text:
              text += extracted_text + "\n"

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        text,
        height=300
    )