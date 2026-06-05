import streamlit as st
import pdfplumber
import base64

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

skills_db = [
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "git",
    "tensorflow",
    "pandas",
    "numpy"
]

recommended = ["python", "sql", "git", "docker", "aws"]

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    # ---------------- SKILL DETECTION ----------------
    found_skills = []
    text_lower = text.lower()

    for skill in skills_db:
        if skill in text_lower:
            found_skills.append(skill)

    # ---------------- SCORE ----------------
    score = len(found_skills) * 10
    if score > 100:
        score = 100

    missing = [s for s in recommended if s not in found_skills]

    questions = []

    if "python" in found_skills:
        questions.append("What is OOP in Python?")
    if "sql" in found_skills:
        questions.append("What is a JOIN in SQL?")
    if "machine learning" in found_skills:
        questions.append("What is overfitting?")

    summary = "Candidate has skills in: " + ", ".join(found_skills) if found_skills else "No strong skills detected"

    # ---------------- UI LAYOUT ----------------
    col1, col2 = st.columns([2, 1])

    # LEFT SIDE
    with col1:
        st.subheader("📄 Resume Text")

        with st.container():
            st.write(text)

        st.subheader("📌 Resume Sections")

        name = text.split("\n")[0] if text else "Not found"
        email = "Found" if "@" in text else "Not found"
        phone = "Found" if any(char.isdigit() for char in text) else "Not found"

        st.write("Name:", name)
        st.write("Email:", email)
        st.write("Phone:", phone)

    # RIGHT SIDE (DASHBOARD)
    with col2:

        st.markdown("### 🧠 Skills Detected")
        st.success(", ".join(found_skills) if found_skills else "No skills detected")

        st.markdown("### 📊 ATS Score")
        st.progress(int(score))
        st.metric("Score", int(score))

        st.markdown("### ⚠️ Missing Skills")
        if missing:
            for m in missing:
                st.error(m)
        else:
            st.success("No missing skills")

        st.markdown("### ❓ Interview Questions")
        if questions:
            for q in questions:
                st.info(q)
        else:
            st.write("No questions generated")

        st.markdown("### 📝 Summary")
        st.write(summary)

    # ---------------- DOWNLOAD ----------------
    st.markdown("---")
    st.subheader("📥 Download Report")

    job_role = st.selectbox(
        "Select Job Role",
        ["Data Analyst", "ML Engineer", "Software Developer"]
    )

    report_text = f"""
Resume Analysis Report

Name: {name}
Email: {email}
Phone: {phone}

Skills: {found_skills}
Score: {score}
Job Role: {job_role}
Summary: {summary}
"""

    b64 = base64.b64encode(report_text.encode()).decode()

    href = f'<a href="data:file/txt;base64,{b64}" download="resume_report.txt">📥 Download Report</a>'

    st.markdown(href, unsafe_allow_html=True)
