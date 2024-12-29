import streamlit as st
import pandas as pd

# Ensure this is the first Streamlit command in the script
st.set_page_config(page_title="CGPA Calculator", page_icon="🎓", layout="wide")

def grade_to_points(grade):
    """Convert grade letters to grade points."""
    grade_map = {
        "S": 10,
        "A": 9,
        "B": 8,
        "C": 7,
        "D": 6,
        "E": 5,
        "F": 0
    }
    return grade_map.get(grade.upper(), 0)

def calculate_cgpa(grades, credits):
    """Calculate CGPA given grades and credits."""
    total_points = sum(grade_to_points(grade) * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return total_points / total_credits if total_credits > 0 else 0

# Custom CSS for styling
st.markdown("""
    <style>
    .header-box {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .grade-section {
        background-color: #f7f9fc;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 2px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #1D4ED8;
        color: white;
        border-radius: 10px;
        padding: 0.5rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    .results-section {
        background: linear-gradient(135deg, #FF7EB3, #FF758C);
        padding: 2rem;
        border-radius: 1rem;
        margin: 1rem 0;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }
    .summary-box {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Page Title and Header
st.markdown("""
    <div class="header-box">
        <h1>🎓 CGPA Calculator</h1>
        <p>Calculate your CGPA and make your parents proud! 😎</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.header("🔧 Configuration")
level = st.sidebar.radio("Select your academic level:", ["Foundational", "Diploma", "Degree"], index=0)

# Course Data
courses = {
    "Foundational": [
        ("Statistics for Data Science II", 4),
        ("Mathematics for Data Science I", 4),
        ("Programming in Python", 4),
        ("English I", 4),
        ("Computational Thinking", 4),
        ("Mathematics for Data Science II", 4),
        ("English II", 4),
        ("Statistics for Data Science I", 4),
    ],
    "Diploma": [
        ("Machine Learning Techniques", 4),
        ("Machine Learning Foundations", 4),
        ("Machine Learning Practice", 4),
        ("Modern Application Development II", 4),
        ("System Commands", 3),
        ("Database Management Systems", 4),
        ("Business Data Management", 4),
        ("Programming, Data Structures and Algorithms using Python", 4),
        ("Business Analytics", 4),
        ("Tools in Data Science", 3),
        ("Programming Concepts using Java", 4),
        ("Modern Application Development I", 4),
    ],
    "Degree": [
        ("Software Engineering", 4),
        ("AI: Search Methods for Problem Solving", 4),
        ("Software Testing", 4),
        ("Large Language Models", 4),
        ("Deep Learning", 4),
        ("Strategies for Professional Growth", 4),
    ]
}

projects = {
    "Diploma": [
        ("Machine Learning Practice - Project", 2),
        ("Business Data Management - Project", 2),
        ("Modern Application Development II - Project", 2),
        ("Modern Application Development I - Project", 2)
    ]
}

# Grade Entry for Completed Levels
completed_courses = []
completed_grades = []
credits = []

if level == "Diploma":
    st.markdown("### ✅ Foundation Level Courses")
    for course, credit in courses["Foundational"]:
        grade = st.selectbox(f"Grade for {course} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"found_{course}")
        if grade != "Not Done":
            completed_courses.append(course)
            completed_grades.append(grade)
            credits.append(credit)

elif level == "Degree":
    st.markdown("### ✅ Foundation and Diploma Level Courses")
    for course, credit in courses["Foundational"] + courses["Diploma"]:
        grade = st.selectbox(f"Grade for {course} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"prev_{course}")
        if grade != "Not Done":
            completed_courses.append(course)
            completed_grades.append(grade)
            credits.append(credit)
    
    # Add Diploma Projects for Degree Students
    st.markdown("#### 🛠️ Diploma Projects")
    for project, credit in projects["Diploma"]:
        grade = st.selectbox(f"Grade for {project} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"proj_{project}")
        if grade != "Not Done":
            completed_courses.append(project)
            completed_grades.append(grade)
            credits.append(credit)

# Diploma Project Handling for Diploma Students
if level == "Diploma":
    st.markdown("#### 🛠️ Diploma Projects")
    selected_projects = st.multiselect("Select Completed Projects", [proj for proj, _ in projects["Diploma"]])
    for proj, credit in projects["Diploma"]:
        if proj in selected_projects:
            grade = st.selectbox(f"Grade for {proj} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"diploma_proj_{proj}")
            if grade != "Not Done":
                completed_courses.append(proj)
                completed_grades.append(grade)
                credits.append(credit)

# Current Level Courses
st.markdown(f"### 📝 Current {level} Level Courses")
available_courses = courses[level]
selected_courses = st.multiselect("Select Completed Courses", [course for course, _ in available_courses])
current_grades = []

if selected_courses:
    for course, credit in available_courses:
        if course in selected_courses:
            grade = st.selectbox(f"Grade for {course} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"current_{course}")
            if grade != "Not Done":
                completed_courses.append(course)
                completed_grades.append(grade)
                credits.append(credit)

# Calculate CGPA
if st.button("📈 Calculate CGPA"):
    if completed_grades:
        total_cgpa = calculate_cgpa(completed_grades, credits)
        st.markdown(f"""
            <div class="results-section">
                <h2>Your CGPA: {total_cgpa:.2f}</h2>
                <p>Keep pushing forward and make it even better! 💪</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please enter grades to calculate your CGPA!")

# Summary Table
if completed_courses:
    st.markdown("### 📋 Summary of Grades")
    summary_data = {
        "Course Name": completed_courses,
        "Grade": completed_grades,
        "Credits": credits
    }
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df.style.background_gradient(cmap="Blues"), use_container_width=True)
