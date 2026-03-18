import pdfplumber
import tempfile

def extract_text(file):
    text = ""

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    # Read using pdfplumber
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text.lower()


# ==========================
# Extract Skills
# ==========================

def extract_skills(text):

    skills_list = [
        "python", "java", "c++", "html", "css", "javascript",
        "react", "node", "django", "flask", "sql",
        "machine learning", "deep learning", "tensorflow",
        "pandas", "numpy", "excel", "power bi", "tableau",
        "aws", "docker", "kubernetes", "linux"
    ]

    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# ==========================
# Calculate Score
# ==========================

def calculate_score(skills, job_role):

    job_skills_map = {
        "data scientist": ["python", "machine learning", "pandas", "numpy", "sql"],
        "data analyst": ["excel", "sql", "python", "power bi", "tableau"],
        "machine learning engineer": ["python", "machine learning", "tensorflow"],
        "ai engineer": ["python", "deep learning", "tensorflow"],
        "web developer": ["html", "css", "javascript"],
        "frontend developer": ["html", "css", "javascript", "react"],
        "backend developer": ["python", "django", "flask", "sql"],
        "full stack developer": ["html", "css", "javascript", "react", "python", "sql"],
        "software engineer": ["python", "java", "c++"],
        "devops engineer": ["docker", "kubernetes", "aws", "linux"]
    }

    job_role = job_role.lower()

    if job_role not in job_skills_map:
        return 0, []

    required_skills = job_skills_map[job_role]

    matched_skills = list(set(skills) & set(required_skills))

    score = int((len(matched_skills) / len(required_skills)) * 100)

    return score, matched_skills


# ==========================
# Missing Skills
# ==========================

def get_missing_skills(skills, job_role):

    job_skills_map = {
        "data scientist": ["python", "machine learning", "pandas", "numpy", "sql"],
        "data analyst": ["excel", "sql", "python", "power bi", "tableau"],
        "machine learning engineer": ["python", "machine learning", "tensorflow"],
        "ai engineer": ["python", "deep learning", "tensorflow"],
        "web developer": ["html", "css", "javascript"],
        "frontend developer": ["html", "css", "javascript", "react"],
        "backend developer": ["python", "django", "flask", "sql"],
        "full stack developer": ["html", "css", "javascript", "react", "python", "sql"],
        "software engineer": ["python", "java", "c++"],
        "devops engineer": ["docker", "kubernetes", "aws", "linux"]
    }

    job_role = job_role.lower()

    required = job_skills_map.get(job_role, [])
    missing = list(set(required) - set(skills))

    return missing

def recruiter_insights(score, matched_skills, missing_skills):
    
    # Ranking
    if score >= 80:
        level = "⭐⭐⭐⭐ Strong Candidate"
    elif score >= 60:
        level = "⭐⭐⭐ Job Ready"
    elif score >= 40:
        level = "⭐⭐ Intermediate"
    else:
        level = "⭐ Beginner"

    # Strengths
    strengths = matched_skills[:5]

    # Weakness
    weaknesses = missing_skills[:5]

    # Suggestions
    suggestions = []
    for skill in missing_skills[:5]:
        suggestions.append(f"Learn {skill}")

    return level, strengths, weaknesses, suggestions