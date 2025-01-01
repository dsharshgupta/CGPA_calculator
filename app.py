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
        "E": 4,
        "F": 0
    }
    return grade_map.get(grade.upper(), 0)

def calculate_cgpa(grades, credits):
    """Calculate CGPA given grades and credits."""
    total_points = sum(grade_to_points(grade) * credit for grade, credit in zip(grades, credits))
    total_credits = sum(credits)
    return total_points / total_credits if total_credits > 0 else 0

def update_overall_cgpa(last_cgpa, last_credits, current_cgpa, current_credits):
    """Calculate updated CGPA after the current term."""
    total_credits = last_credits + current_credits
    total_points = (last_cgpa * last_credits) + (current_cgpa * current_credits)
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
    </style>
""", unsafe_allow_html=True)

# Page Title and Header
st.markdown("""
    <div class="header-box">
        <h1>🎓 CGPA Calculator</h1>
        <p>Calculate your CGPA and make your parents proud! 😎</p>
    </div>
""", unsafe_allow_html=True)

# Option Selection
st.markdown("## Choose Calculation Method")
option = st.radio(
    "Select an option below:",
    ["Current Term CGPA","CGPA from Scratch"],
    horizontal=False
)

# Add this section just below the "Choose Calculation Method" radio button
st.markdown("## 📝 How to Use This App")

# Provide dynamic tips based on the selected option
if option == "CGPA from Scratch":
    st.markdown("""
    ### **Tips for 'CGPA from Scratch'**
    - Select your **academic level** (Foundational, Diploma, or Degree).
    - If you're in the Diploma or Degree level, the courses from previous levels will already be included.
    - Enter the grades for all completed courses and projects.
    - Use the **searchable dropdown** to select and enter grades for your current-level courses.
    - Click the **Calculate CGPA** button to view your CGPA.
    """)
else:
    st.markdown("""
    ### **Tips for 'Current Term CGPA'**
    - Enter your **last term CGPA** and the total **credits completed** in the last term.
    - Select your **current academic level** (Foundational, Diploma, or Degree).
    - Use the **searchable dropdown** to select and enter grades for your current-term courses.
    - Click the **Calculate Current Term CGPA** button to view:
      - Your **current term CGPA**.
      - Your **updated overall CGPA**.
    """)

st.markdown("---")  # Divider for better visual separation


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
        ("Software Testing", 4),
        ("AI: Search Methods for Problem Solving", 4),
        ("Deep Learning", 4),
        ("Strategies for Professional Growth", 4),
        ("Algorithmic Thinking in Bioinformatics", 4),
        ("Big Data and Biological Networks", 4),
        ("Data Visualization Design", 4),
        ("Speech Technology", 4),
        ("Design Thinking for Data-Driven App Development", 4),
        ("Industry 4.0", 4),
        ("Financial Forensics", 4),
        ("Market Research", 4),
        ("Introduction to Big Data", 4),
        ("Privacy & Security in Online Social Media", 4),
        ("Mathematical Thinking", 4),
        ("Linear Statistical Models", 4),
        ("Statistical Computing", 4),
        ("Advanced Algorithms", 4),
        ("Computer Systems Design", 4),
        ("Operating Systems", 4),
        ("Special Topics in ML (Reinforcement Learning)", 4),
        ("Programming in C", 4),
        ("Introduction to Natural Language Processing (i-NLP)", 4),
        ("Deep Learning for Computer Vision", 4),
        ("Large Language Models", 4),
        ("Game Theory and Strategy", 4),
        ("Managerial Economics", 4),
        ("Corporate Finance", 4),
        ("Deep Learning Practice", 4)
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

# Updated Code Section for CGPA from Scratch

if option == "CGPA from Scratch":
    st.markdown("### Select Academic Level")
    level = st.radio("Select your academic level:", ["Foundational", "Diploma", "Degree"], horizontal=True)
    completed_courses = []
    completed_grades = []
    credits = []

    # Handle completed levels dynamically
    with st.expander("Foundation Level Courses"):
        if level in ["Diploma", "Degree"]:
            for course, credit in courses["Foundational"]:
                grade = st.selectbox(f"Grade for {course} ({credit} credits):", ["S", "A", "B", "C", "D", "E", "F"], key=f"found_{course}")
                completed_courses.append(course)
                completed_grades.append(grade)
                credits.append(credit)

    with st.expander("Diploma Level Courses and Projects"):
        if level == "Degree":
            # Diploma Courses
            for course, credit in courses["Diploma"]:
                grade = st.selectbox(f"Grade for {course} ({credit} credits):", ["S", "A", "B", "C", "D", "E", "F"], key=f"diploma_{course}")
                completed_courses.append(course)
                completed_grades.append(grade)
                credits.append(credit)

            # Diploma Projects (Pre-Filled for Degree Students)
            st.markdown("### 🛠️ Diploma Projects (Auto-Completed for Degree Students)")
            for proj, credit in projects["Diploma"]:
                grade = st.selectbox(f"Grade for {proj} ({credit} credits):", ["S", "A", "B", "C", "D", "E", "F"], key=f"diploma_proj_{proj}")
                completed_courses.append(proj)
                completed_grades.append(grade)
                credits.append(credit)

        if level == "Diploma":
            # Allow Diploma students to select projects dynamically
            selected_projects = st.multiselect("Select completed Diploma projects", [proj for proj, _ in projects["Diploma"]])
            for proj, credit in projects["Diploma"]:
                if proj in selected_projects:
                    grade = st.selectbox(f"Grade for {proj} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"diploma_proj_{proj}")
                    if grade != "Not Done":
                        completed_courses.append(proj)
                        completed_grades.append(grade)
                        credits.append(credit)

    # Current level courses
    with st.expander("Current Level Courses"):
        selected_courses = st.multiselect("Select completed courses", [course for course, _ in courses[level]])
        for course, credit in courses[level]:
            if course in selected_courses:
                grade = st.selectbox(f"Grade for {course} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"current_{course}")
                if grade != "Not Done":
                    completed_courses.append(course)
                    completed_grades.append(grade)
                    credits.append(credit)

    # Calculate CGPA
    if st.button("📈 Calculate CGPA"):
        total_cgpa = calculate_cgpa(completed_grades, credits)
        st.markdown(f"""
            <div class="results-section">
                <h2>Your CGPA: {total_cgpa:.2f}</h2>
                <p>Keep pushing forward and make it even better! 💪</p>
            </div>
        """, unsafe_allow_html=True)

# Updated Code Section for Current Term CGPA

else:
    st.markdown("### 📋 Enter Previous Term Information")
    last_cgpa = st.number_input("Enter your last term CGPA:", min_value=0.0, max_value=10.0, step=0.01)
    last_credits = st.number_input("Enter the total credits completed in the last term:", min_value=0, step=1)

    st.markdown("### 📝 Current Term Courses and Projects")
    current_level = st.radio("Select your current academic level:", ["Foundational", "Diploma", "Degree"], horizontal=True)
    current_courses = []
    current_grades = []
    current_credits = []

    # Current Term Courses and Projects for Diploma Level
    if current_level == "Diploma":
        available_items = [(course, credit) for course, credit in courses["Diploma"]] + [
            (proj, credit) for proj, credit in projects["Diploma"]
        ]
        selected_items = st.multiselect(
            "Select completed courses and projects for the current term",
            [item[0] for item in available_items]
        )
        for item, credit in available_items:
            if item in selected_items:
                grade = st.selectbox(f"Grade for {item} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"current_diploma_{item}")
                if grade != "Not Done":
                    current_courses.append(item)
                    current_grades.append(grade)
                    current_credits.append(credit)

    # Current Term Courses for Degree Level
    elif current_level == "Degree":
        available_courses = [(course, credit) for course, credit in courses["Degree"]]
        selected_courses = st.multiselect(
            "Select completed courses for the current term",
            [course[0] for course in available_courses]
        )
        for course, credit in available_courses:
            if course in selected_courses:
                grade = st.selectbox(f"Grade for {course} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"current_degree_{course}")
                if grade != "Not Done":
                    current_courses.append(course)
                    current_grades.append(grade)
                    current_credits.append(credit)

    # Current Term Courses for Foundational Level
    elif current_level == "Foundational":
        available_courses = [(course, credit) for course, credit in courses["Foundational"]]
        selected_courses = st.multiselect(
            "Select completed courses for the current term",
            [course[0] for course in available_courses]
        )
        for course, credit in available_courses:
            if course in selected_courses:
                grade = st.selectbox(f"Grade for {course} ({credit} credits):", ["Not Done", "S", "A", "B", "C", "D", "E", "F"], key=f"current_foundation_{course}")
                if grade != "Not Done":
                    current_courses.append(course)
                    current_grades.append(grade)
                    current_credits.append(credit)

    # Calculate Current Term CGPA
    if st.button("📈 Calculate Current Term CGPA"):
        current_cgpa = calculate_cgpa(current_grades, current_credits)
        overall_cgpa = update_overall_cgpa(last_cgpa, last_credits, current_cgpa, sum(current_credits))

        st.markdown(f"""
            <div class="results-section">
                <h2>Current Term CGPA: {current_cgpa:.2f}</h2>
                <h3>Updated Overall CGPA: {overall_cgpa:.2f}</h3>
                <p>Great work! Keep it up! 🚀</p>
            </div>
        """, unsafe_allow_html=True)
