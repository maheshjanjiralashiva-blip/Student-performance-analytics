"""
main.py
Student Performance Analytics System

Run with:  python main.py
Reads students.csv, processes the marks and prints the final analysis.
"""

import pandas as pd

import functions as fn

DATA_FILE = "students.csv"

# Make the printed tables easy to read in the terminal
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)


def print_heading(title):
    """Print a clear section heading."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    # ---- Step 1: Read the data -------------------------------------------
    df = fn.load_data(DATA_FILE)

    print_heading("1. DATASET OVERVIEW")
    print(f"Records : {df.shape[0]}")
    print(f"Columns : {df.shape[1]} -> {list(df.columns)}")
    print("\nFirst 5 records:")
    print(df.head().to_string(index=False))

    # ---- Step 2: Process the data ----------------------------------------
    df = fn.process_students(df)

    print_heading("2. STUDENT RESULTS (Total, Average, Grade, Result)")
    result_columns = ["Student_ID", "Name", "Total", "Average", "Grade", "Result"]
    print(df[result_columns].to_string(index=False))

    # ---- Step 3: Class summary -------------------------------------------
    summary = fn.class_summary(df)

    print_heading("3. CLASS SUMMARY")
    print(f"Total students      : {summary['total_students']}")
    print(f"Class average       : {summary['class_average']}")
    print(f"Highest average     : {summary['highest_average']} ({summary['highest_student']})")
    print(f"Lowest average      : {summary['lowest_average']} ({summary['lowest_student']})")
    print(f"Students passed     : {summary['passed']}")
    print(f"Students failed     : {summary['failed']}")
    print(f"Pass percentage     : {summary['pass_percentage']}%")

    # ---- Step 4: Pass / fail details and grade distribution --------------
    print_heading("4. FAILED STUDENTS")
    failed = df[df["Result"] == "Fail"]
    # Loop through the failed students and show which subjects they failed
    for _, student in failed.iterrows():
        failed_subjects = [s for s in fn.SUBJECTS if student[s] < fn.PASS_MARK]
        print(f"{student['Student_ID']}  {student['Name']:<16} failed in: {', '.join(failed_subjects)}")

    print_heading("5. GRADE DISTRIBUTION")
    distribution = fn.grade_distribution(df)
    for grade, count in distribution.items():
        print(f"Grade {grade:<2}: {'#' * int(count)} ({count})")

    # ---- Step 5: Subject-wise analysis -----------------------------------
    subjects = fn.subject_analysis(df)

    print_heading("6. SUBJECT-WISE ANALYSIS")
    print(subjects.to_string(index=False))

    best = subjects.loc[subjects["Average"].idxmax()]
    weakest = subjects.loc[subjects["Average"].idxmin()]
    print(f"\nBest subject (highest average)    : {best['Subject']} ({best['Average']})")
    print(f"Weakest subject (lowest average)  : {weakest['Subject']} ({weakest['Average']})")

    # ---- Step 6: Top performers ------------------------------------------
    print_heading("7. TOP 3 PERFORMERS")
    top = fn.get_top_performers(df, n=3)
    rank = 1
    for _, student in top.iterrows():
        print(f"Rank {rank}: {student['Name']:<14} | {student['Department']:<17} | "
              f"Total {student['Total']} | Average {student['Average']} | Grade {student['Grade']}")
        rank += 1

    # ---- Step 7: Attendance check ----------------------------------------
    print_heading(f"8. LOW ATTENDANCE (below {fn.MIN_ATTENDANCE}%)")
    low = fn.low_attendance_students(df)
    if low.empty:
        print("No students below the attendance limit.")
    else:
        print(low.to_string(index=False))

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
