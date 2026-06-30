import streamlit as st

# -------------------- PAGE CONFIG -------------------- #
st.set_page_config(
    page_title="AI Resume Parser",
    page_icon="📄",
    layout="wide"
)

# -------------------- IMPORTS -------------------- #
from utils import extract_text_from_pdf
from llm import analyze_resume


# -------------------- LOAD CSS -------------------- #
def load_css():
    with open("css/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# -------------------- HEADER -------------------- #
st.markdown("""
<div style="text-align:center; padding:20px;">

<h1 style="color:#4F8BF9; font-size:55px;">
🤖 AI Resume Parser
</h1>

<h4 style="color:gray;">
Powered by Google Gemini AI
</h4>

<p style="color:#A0A0A0;">
Upload your resume and let AI automatically extract structured information
such as personal details, skills, education, projects and professional summary.
</p>

</div>
""", unsafe_allow_html=True)

st.divider()


# -------------------- FILE UPLOADER -------------------- #
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)


# ===========================================================
#                      MAIN APPLICATION
# ===========================================================

if uploaded_file:

    st.success("Resume uploaded successfully!")

    # Extract text
    resume_text = extract_text_from_pdf(uploaded_file)

    # Gemini Analysis
    ai_response = analyze_resume(resume_text)

   
    # ===================================================
    # Candidate Information + Skills
    # ===================================================

    left, right = st.columns([1, 1])

    with left:

        st.markdown("""
        <div class="card">
        <div class="section-title">
        👤 Candidate Information
        </div>
        """, unsafe_allow_html=True)

        st.write(f"**👤 Name:** {ai_response.get('name', 'Not Available')}")
        st.write(f"**📧 Email:** {ai_response.get('email', 'Not Available')}")
        st.write(f"**📱 Phone:** {ai_response.get('phone', 'Not Available')}")

        st.markdown("</div>", unsafe_allow_html=True)

    with right:

        st.subheader("💻 Skills")

        skills = ai_response.get("skills", [])

        if skills:
            for skill in skills:
                st.success(skill)
        else:
            st.info("No skills found.")

    # ===================================================
    # EDUCATION
    # ===================================================

    education = ai_response.get("education", [])

    if education:

        st.subheader("🎓 Education")

        for edu in education:

            st.markdown(f"### {edu.get('degree', '')}")

            st.write(f"🏫 Institution: {edu.get('institution', '')}")

            st.write(f"📍 Location: {edu.get('location', '')}")

            start = edu.get("start_date", "")
            end = edu.get("end_date", "")

            if start or end:
                st.write(f"📅 Duration: {start} - {end}")

            st.write(f"🎖 Grade: {edu.get('grade', '')}")

            st.divider()

    # ===================================================
    # EXPERIENCE
    # ===================================================

    experience = ai_response.get("experience", [])

    if experience:

        st.subheader("💼 Experience")

        for exp in experience:

            with st.expander(exp.get("company", "Experience")):

                st.write(f"**Role:** {exp.get('role', '')}")
                st.write(f"**Duration:** {exp.get('duration', '')}")
                st.write(exp.get("description", ""))

    # ===================================================
    # INTERNSHIPS
    # ===================================================

    internships = ai_response.get("internships", [])

    if internships:

        st.subheader("🏢 Internships")

        for intern in internships:

            with st.expander(intern.get("organization", "Internship")):

                st.write(f"**Role:** {intern.get('role', '')}")
                st.write(f"**Duration:** {intern.get('duration', '')}")
                st.write(intern.get("description", ""))

    # ===================================================
    # PROJECTS
    # ===================================================

    projects = ai_response.get("projects", [])

    if projects:

        st.subheader("📂 Projects")

        for project in projects:

            with st.expander(project.get("title", "Project")):

                st.write(project.get("description", ""))

    # ===================================================
    # CERTIFICATIONS
    # ===================================================

    certifications = ai_response.get("certifications", [])

    if certifications:

        st.subheader("📜 Certifications")

        for cert in certifications:
            st.success(cert)

    # ===================================================
    # ACHIEVEMENTS
    # ===================================================

    achievements = ai_response.get("achievements", [])

    if achievements:

        st.subheader("🏆 Achievements")

        for achievement in achievements:
            st.success(achievement)

    # ===================================================
    # TOOLS
    # ===================================================

    tools = ai_response.get("tools", [])

    if tools:

        st.subheader("🛠 Tools")

        for tool in tools:
            st.success(tool)

    # ===================================================
    # LANGUAGES
    # ===================================================

    languages = ai_response.get("languages", [])

    if languages:

        st.subheader("🌍 Languages")

        for language in languages:
            st.success(language)

    # ===================================================
    # SUMMARY
    # ===================================================

    summary = ai_response.get("summary", "")

    if summary:

        st.subheader("📝 Professional Summary")

        st.info(summary)