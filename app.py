import html
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


# ==========================================================
# UI COMPONENTS
# ==========================================================

# ==========================================================
# UI HELPERS
# ==========================================================

def section_title(title, icon):
    st.markdown(
        f"""
        <h3 style="
        color:#F8FAFC;
        margin-bottom:18px;
        font-weight:700;">
        {icon} {title}
        </h3>
        """,
        unsafe_allow_html=True
    )


def is_non_empty(value):
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(is_non_empty(item) for item in value)
    return bool(value)


def sanitize_text(value):
    if value is None:
        return ""
    return html.escape(str(value)).replace("\n", "<br>")


def skill_badges(skills):
    filtered_skills = [skill for skill in skills if is_non_empty(skill)] if skills else []

    if not filtered_skills:
        st.info("No skills found.")
        return

    html = ""

    for skill in filtered_skills:
        html += f"""
        <span class="badge">
            {sanitize_text(skill)}
        </span>
        """

    st.markdown(html, unsafe_allow_html=True)

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
<div class="hero">

<h1 class="hero-title">
🤖 AI Resume Parser
</h1>

<p class="hero-subtitle">
AI-Powered Resume Parsing with Google Gemini
</p>

<p class="hero-description">
Extract structured information from resumes in seconds using Artificial Intelligence.
</p>

</div>
""", unsafe_allow_html=True)

st.divider()


# -------------------- FILE UPLOADER -------------------- #
st.markdown("### 📄 Upload Resume")

uploaded_file = st.file_uploader(
    "",
    type=["pdf"],
    help="Upload a PDF resume to begin AI parsing."
)


# ===========================================================
#                      MAIN APPLICATION
# ===========================================================

if uploaded_file:

    st.success("✅ Resume uploaded successfully.")

    # Extract text
    resume_text = extract_text_from_pdf(uploaded_file)

    # Gemini Analysis
    with st.spinner("🤖 Gemini AI is analyzing your resume..."):
        ai_response = analyze_resume(resume_text)

   
   
    # ==========================================================
    # PROFILE + SKILLS
    # ==========================================================

    left, right = st.columns(2, gap="large")

    # ---------------- Candidate ---------------- #

    with left:

        st.markdown(f"""
        <div class="card">

        <h3>👤 Candidate Information</h3>

        <p><b>Name</b><br>{ai_response.get("name","Not Available")}</p>

        <p><b>Email</b><br>{ai_response.get("email","Not Available")}</p>

        <p><b>Phone</b><br>{ai_response.get("phone","Not Available")}</p>

        </div>
        """, unsafe_allow_html=True)


    # ---------------- Skills ---------------- #

    with right:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        section_title("Skills", "💻")

        skill_badges(ai_response.get("skills", []))

        st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================================
    # ATS SCORE
    # ==========================================================

    ats_score = ai_response.get("ats_score", 0)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    section_title("ATS Resume Score", "⭐")

    st.progress(ats_score / 100)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        st.metric(
            label="Overall Score",
            value=f"{ats_score}/100"
        )

    if ats_score >= 90:
        st.success("🌟 Excellent Resume")

    elif ats_score >= 75:
        st.success("✅ Good Resume")

    elif ats_score >= 60:
        st.warning("⚠️ Average Resume")

    else:
        st.error("❌ Resume Needs Improvement")

    st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================================
    # EDUCATION
    # ==========================================================

    education = ai_response.get("education", [])
    if isinstance(education, dict):
        education = [education]

    valid_education = [
        edu for edu in education
        if any(is_non_empty(edu.get(key, "")) for key in ("degree", "institution", "location", "start_date", "end_date", "grade"))
    ]

    if valid_education:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        section_title("Education", "🎓")

        for edu in valid_education:
            degree = sanitize_text(edu.get("degree", ""))
            institution = sanitize_text(edu.get("institution", ""))
            location = sanitize_text(edu.get("location", ""))
            start_date = sanitize_text(edu.get("start_date", ""))
            end_date = sanitize_text(edu.get("end_date", ""))
            grade = sanitize_text(edu.get("grade", ""))

            st.markdown(f"""
            <div class="edu-card">

                <div class="edu-degree">
                    {degree}
                </div>

                <div class="edu-inst">
                    🏫 {institution}
                </div>

                <div class="edu-info">

                    📍 {location}

                </div>

                <div class="edu-info">

                    📅 {start_date} - {end_date}

                </div>

                <div class="edu-grade">

                    🎖 {grade}

                </div>

            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================================
    # PROJECTS
    # ==========================================================

    projects = ai_response.get("projects", [])
    if isinstance(projects, dict):
        projects = [projects]

    valid_projects = [
        project for project in projects
        if any(is_non_empty(project.get(key, "")) for key in ("title", "description", "technologies"))
    ]

    if valid_projects:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        section_title("Projects", "📂")

        for project in valid_projects:
            title = sanitize_text(project.get("title", "Untitled Project"))
            desc = sanitize_text(project.get("description", "No description available."))
            tech = project.get("technologies", []) or []

            with st.expander(f"🚀 {title}", expanded=False):
                st.markdown(f"""
                <div class="project-description">
                {desc}
                </div>
                """, unsafe_allow_html=True)

                if tech:
                    st.markdown("#### 🛠 Technologies")
                    skill_badges(tech)

        st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================================
    # CERTIFICATIONS
    # ==========================================================

    certifications = ai_response.get("certifications", [])
    if isinstance(certifications, dict):
        certifications = [certifications]

    valid_certifications = [
        cert for cert in certifications
        if any(is_non_empty(cert.get(key, "")) for key in ("name", "issuer", "year"))
    ]

    if valid_certifications:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        section_title("Certifications", "📜")

        for cert in valid_certifications:
            st.markdown(f"""
            <div class="simple-card">
                <b>{sanitize_text(cert.get("name", ""))}</b><br>
                <span>{sanitize_text(cert.get("issuer", ""))}</span><br>
                <small>{sanitize_text(cert.get("year", ""))}</small>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================================
    # ACHIEVEMENTS
    # ==========================================================

    achievements = ai_response.get("achievements", []) or []
    valid_achievements = [achievement for achievement in achievements if is_non_empty(achievement)]

    if valid_achievements:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        section_title("Achievements", "🏆")

        for achievement in valid_achievements:
            st.markdown(f"✅ {sanitize_text(achievement)}")

        st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================================
    # PROFESSIONAL LINKS
    # ==========================================================

    github = ai_response.get("github","")
    linkedin = ai_response.get("linkedin","")

    if github or linkedin:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        section_title("Professional Links", "🔗")

        if github:
            st.markdown(f"**GitHub:** {github}")

        if linkedin:
            st.markdown(f"**LinkedIn:** {linkedin}")

        st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================================
    # PROFESSIONAL SUMMARY
    # ==========================================================

    summary = ai_response.get("summary", "")

    if is_non_empty(summary):

        st.markdown('<div class="card">', unsafe_allow_html=True)

        section_title("Professional Summary", "📝")

        st.markdown(f"""
        <div class="summary-box">
        {sanitize_text(summary)}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================================
    # AI SUGGESTIONS
    # ==========================================================

    suggestions = ai_response.get("suggestions", []) or []
    valid_suggestions = [suggestion for suggestion in suggestions if is_non_empty(suggestion)]

    if valid_suggestions:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        section_title("AI Suggestions", "💡")

        for suggestion in valid_suggestions:
            st.markdown(f"""
            <div class="suggestion-card">
                ✅ {sanitize_text(suggestion)}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)



    st.markdown("---")

    st.markdown("""
    <div class="footer">

    <h3>🤖 AI Resume Parser</h3>

    <p>
    Powered by Google Gemini AI
    </p>

    <p>
    Designed & Developed by <b>Tushar Patel</b>
    </p>

    <p style="font-size:13px;">
    AI-Powered Resume Parsing System • Version 1.0
    </p>

    </div>
    """, unsafe_allow_html=True)