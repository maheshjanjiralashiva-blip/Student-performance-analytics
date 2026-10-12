"""
functions.py
Reusable functions for the Student Performance Analytics System.

Every calculation lives here so that main.py only has to call the functions
and print the results.
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Settings (change these to change the rules for the whole project)
# ---------------------------------------------------------------------------
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer_Science"]
MAX_MARKS_PER_SUBJECT = 100
PASS_MARK = 40            # a student must score at least this in EVERY subject
MIN_ATTENDANCE = 75       # attendance (%) below this is flagged as low
GRADE_ORDER = ["A+", "A", "B", "C", "D", "E", "F"]


# ---------------------------------------------------------------------------
# 1. Loading and checking the data
# ---------------------------------------------------------------------------
def load_data(file_path):
    """Read the student CSV file into a Pandas DataFrame."""
    df = pd.read_csv(file_path)

    # Make sure every column we need is present
    required = ["Student_ID", "Name", "Department", "Attendance"] + SUBJECTS
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"CSV file is missing columns: {missing}")

    return df


# ---------------------------------------------------------------------------
# 2. Per-student calculations
# ---------------------------------------------------------------------------
def calculate_totals_and_averages(df):
    """Add Total and Average columns using NumPy on the subject marks."""
    marks = df[SUBJECTS].to_numpy()                  # 2D NumPy array (students x subjects)

    df["Total"] = np.sum(marks, axis=1)              # row-wise total
    df["Average"] = np.round(np.mean(marks, axis=1), 2)   # row-wise average
    return df


def assign_grade(average, has_failed):
    """
    Grading rule (based on the average marks):
        90 and above -> A+      60 - 69 -> C      40 - 49 -> E
        80 - 89      -> A       50 - 59 -> D      below 40 -> F
        70 - 79      -> B
    A student who fails any subject always gets grade F.
    """
    if has_failed:
        return "F"
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    elif average >= 40:
        return "E"
    else:
        return "F"


def check_pass_fail(df):
    """
    Add a Result column.
    Condition: a student is 'Pass' only if marks >= PASS_MARK in ALL subjects.
    """
    marks = df[SUBJECTS].to_numpy()
    passed_all = np.all(marks >= PASS_MARK, axis=1)        # True/False per student
    df["Result"] = np.where(passed_all, "Pass", "Fail")

    # Count how many subjects each student failed (useful for the report)
    df["Subjects_Failed"] = np.sum(marks < PASS_MARK, axis=1)
    return df


def add_grades(df):
    """Add a Grade column by looping over every student."""
    grades = []
    for average, result in zip(df["Average"], df["Result"]):
        grades.append(assign_grade(average, has_failed=(result == "Fail")))
    df["Grade"] = grades
    return df


def process_students(df):
    """Run all per-student calculations in the correct order."""
    df = calculate_totals_and_averages(df)
    df = check_pass_fail(df)
    df = add_grades(df)
    return df


# ---------------------------------------------------------------------------
# 3. Class-level analysis
# ---------------------------------------------------------------------------
def class_summary(df):
    """Return overall class statistics as a dictionary."""
    best = df.loc[df["Average"].idxmax()]
    worst = df.loc[df["Average"].idxmin()]
    passed = int((df["Result"] == "Pass").sum())
    total_students = len(df)

    return {
        "total_students": total_students,
        "class_average": round(float(np.mean(df["Average"])), 2),
        "highest_average": float(best["Average"]),
        "highest_student": best["Name"],
        "lowest_average": float(worst["Average"]),
        "lowest_student": worst["Name"],
        "passed": passed,
        "failed": total_students - passed,
        "pass_percentage": round(passed / total_students * 100, 1),
    }


def subject_analysis(df):
    """Build a subject-wise table: average, highest, lowest, passes, topper."""
    rows = []
    for subject in SUBJECTS:                              # loop through each subject
        scores = df[subject].to_numpy()
        passed = int(np.sum(scores >= PASS_MARK))
        topper = df.loc[df[subject].idxmax(), "Name"]

        rows.append({
            "Subject": subject,
            "Average": round(float(np.mean(scores)), 2),
            "Highest": int(np.max(scores)),
            "Lowest": int(np.min(scores)),
            "Passed": passed,
            "Failed": len(scores) - passed,
            "Topper": topper,
        })
    return pd.DataFrame(rows)


def get_top_performers(df, n=3):
    """Return the top n students ranked by average (total marks break ties)."""
    ranked = df.sort_values(by=["Average", "Total"], ascending=False)
    return ranked.head(n)[["Student_ID", "Name", "Department", "Total", "Average", "Grade"]]


def grade_distribution(df):
    """Count how many students received each grade (in A+ to F order)."""
    counts = df["Grade"].value_counts()
    return counts.reindex(GRADE_ORDER, fill_value=0)


def low_attendance_students(df):
    """Return students whose attendance is below MIN_ATTENDANCE."""
    low = df[df["Attendance"] < MIN_ATTENDANCE]
    return low[["Student_ID", "Name", "Attendance", "Result"]]
