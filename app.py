import streamlit as st
from parser import extract_text, extract_skills, calculate_score, get_missing_skills, recruiter_insights
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Smart Resume Parser",
    page_icon="📄",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📌 Project Info")

st.sidebar.markdown("""
**Smart Resume Parser & Job Matcher**

This tool helps:
- Extract skills from resumes
- Match with job roles
- Provide recruiter insights
- Rank candidates automatically
""")

theme = st.sidebar.selectbox(
    "🎨 Select Theme",
    ["Light", "Dark"]
)

# =========================
# 🎨 THEME STYLES
# =========================

if theme == "Light":
    st.markdown("""
    <style>

    /* =========================
       BACKGROUND
    ========================== */
    .stApp { 
        background-color: #FFFFFF;
    }

    /* =========================
       TITLE & HEADINGS
    ========================== */
    h1 { 
        color: #1D4ED8 !important;
        font-weight: 700;
    }

    h3 { 
        color: #6B7280 !important;
        font-weight: 600;
    }

    /* =========================
       TEXT
    ========================== */
    p, span, label, div {
        color: #111827 !important;
    }

    /* Label text (Select Job Role) */
    label {
        color: #4B5563 !important;
        font-weight: 500;
    }

    /* =========================
       SELECT BOX
    ========================== */
    div[data-baseweb="select"] > div {
        background: #E6EEF6 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] span {
        color: #4B5563 !important;
    }

    /* =========================
       FILE UPLOADER
    ========================== */
    div[data-testid="stFileUploader"] {
        background: #E6EEF6 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 10px !important;
        padding: 10px;
    }

    /* Inner drag area */
    div[data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #D1D5DB !important;
    }

    /* Drag text */
    div[data-testid="stFileUploader"] section span,
    div[data-testid="stFileUploader"] section p {
        color: #4B5563 !important;
    }

    /* Browse button */
    div[data-testid="stFileUploader"] button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
    }

    div[data-testid="stFileUploader"] button:hover {
        background-color: #F3F4F6 !important;
    }

    /* =========================
       SIDEBAR (LIGHT THEME)
    ========================== */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* Sidebar dropdown */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #000000 !important;
    }

    /* =========================
       🔥 DROPDOWN POPUP FIX (IMPORTANT)
    ========================== */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    div[role="listbox"] {
        background-color: #FFFFFF !important;
    }

    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }

    li[role="option"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    li[role="option"]:hover {
        background-color: #F3F4F6 !important;
        color: #000000 !important;
    }

    li[aria-selected="true"] {
        background-color: #E6EEF6 !important;
        color: #000000 !important;
    }

    /* =========================
       BUTTONS
    ========================== */
    button {
        background-color: #1D4ED8;
        color: white !important;
        border-radius: 6px;
    }

    /* =========================
       METRIC + PROGRESS
    ========================== */
    [data-testid="stMetricValue"] {
        color: #1D4ED8 !important;
    }

    .stProgress > div > div > div > div {
        background-color: #1D4ED8;
    }

    </style>
    """, unsafe_allow_html=True)

elif theme == "Dark":
    st.markdown("""
    <style>

    /* Background */
    .stApp { 
        background-color: #000000;
    }

    /* ✅ MAIN TITLE ONLY (Smart Resume Parser...) */
    h1 { 
        color: #ADD8E6!important;  /* powder blue */
        font-weight: 700;
    }

    /* Subheadings */
    h3 { 
        color: #ADD8E6;
    }

    /* Normal Text */
    p, span, label, div {
        color: #D1D5DB !important;
    }

    /* Selectbox */
    [data-baseweb="select"] {
        background-color: #111111 !important;
        color: #D1D5DB !important;
        border: 1px solid #333333;
    }

    /* File uploader */
    section[data-testid="stFileUploader"] {
        background-color: #111111;
        border: 1px solid #333333;
    }

    /* Buttons */
    button {
        background-color: #1F2937;
        color: #ADD8E6 !important;
    }

    /* Metric value */
    [data-testid="stMetricValue"] {
        color: #ADD8E6 !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #ADD8E6;
    }

    </style>
    """, unsafe_allow_html=True)


# =========================
# TITLE
# =========================
st.title("📄 Smart Resume Parser & Job Matcher")

# =========================
# JOB ROLE
# =========================
job_roles = [
    "Select Job Role",
    "Data Scientist",
    "Data Analyst",
    "Machine Learning Engineer",
    "AI Engineer",
    "Web Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Software Engineer",
    "DevOps Engineer"
]

job_role = st.selectbox("🎯 Select Job Role", job_roles)

# =========================
# FILE UPLOAD
# =========================
uploaded_files = st.file_uploader(
    "📂 Upload Resume (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

# ===============================
# MAIN LOGIC
# ===============================
if uploaded_files:

    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]

    results = []

    for file in uploaded_files:
        resume_text = extract_text(file)
        skills = extract_skills(resume_text)

        if job_role != "Select Job Role":
            score, matched_skills = calculate_score(skills, job_role)
            missing_skills = get_missing_skills(skills, job_role)

            results.append({
                "name": file.name,
                "score": score,
                "skills": skills,
                "matched": matched_skills,
                "missing": missing_skills
            })

    if job_role == "Select Job Role":
        st.warning("Please select a job role.")
        st.stop()

    if not results:
        st.warning("No valid resumes processed.")
        st.stop()

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    top = results[0]

    skills = top["skills"]
    matched_skills = top["matched"]
    missing_skills = top["missing"]
    score = top["score"]

    # ===============================
    # SKILLS
    # ===============================
    st.markdown("---")
    st.subheader("🛠 Skills Found")

    if skills:
        col1, col2 = st.columns(2)
        mid = len(skills) // 2

        with col1:
            for s in skills[:mid]:
                st.write(f"✔ {s}")

        with col2:
            for s in skills[mid:]:
                st.write(f"✔ {s}")
    else:
        st.warning("No skills found.")

    # ===============================
    # SCORE
    # ===============================
    st.markdown("---")
    st.metric("Match Score", f"{score}%")
    st.progress(score)

    # ===============================
    # INSIGHTS
    # ===============================
    st.markdown("---")
    level, strengths, weaknesses, suggestions = recruiter_insights(
        score, matched_skills, missing_skills
    )

    st.subheader("🧠 Recruiter Insights")
    st.write(f"**{level}**")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Strengths**")
        for s in strengths:
            st.write(f"✔ {s}")

    with col2:
        st.write("**Weaknesses**")
        for w in weaknesses:
            st.write(f"✘ {w}")

    st.write("**Suggestions**")
    for sug in suggestions:
        st.write(f"👉 {sug}")

    # ===============================
    # RANKING
    # ===============================
    st.markdown("---")
    st.subheader("🏆 Candidate Ranking")

    for i, res in enumerate(results):
        st.write(f"{i+1}. {res['name']} — {res['score']}%")

    # ===============================
    # TOP CANDIDATE
    # ===============================
    st.markdown("---")
    st.subheader("🥇 Top Candidate")
    st.success(f"{top['name']} ({top['score']}%)")

    # ===============================
    # DONUT CHART
    # ===============================
    st.markdown("---")
    st.subheader("📊 Skill Matching Overview")

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        fig, ax = plt.subplots(figsize=(2.2, 2.2))

        ax.pie(
            [len(matched_skills), len(missing_skills)],
            labels=["Matched", "Missing"],
            autopct='%1.0f%%',
            pctdistance=0.75,
            wedgeprops=dict(width=0.3)
        )

        ax.set_title("Skills", fontsize=10)

        st.pyplot(fig)

else:
    st.info("Upload resume(s) to start.")