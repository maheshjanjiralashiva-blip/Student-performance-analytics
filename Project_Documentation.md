
Project_Documentation.md
# Student Performance Analytics System - Assessment Documentation

**1. Project Title**
Student Performance Analytics System
**Student Details:** Janjirala Mahesh 

**2. Objective**
The objective of this project is to automate the evaluation of student academic records using Python. It solves the problem of manual grading and performance tracking by processing raw marks and attendance data to generate class summaries, identify top performers, and flag low attendance or failed subjects.

**3. Technologies Used**
* Python 3
* NumPy (for vectorized numerical calculations and condition checking)
* Pandas (for dataset loading, tabular data manipulation, and aggregation)

**4. Dataset Description**
The dataset (`students.csv`) contains 20 records of simulated student data. Key columns include `Student_ID`, `Name`, `Department`, `Attendance`, and marks for five subjects (Maths, Physics, Chemistry, English, Computer_Science). 

**5. Implementation**
* **Data Loading:** Pandas `read_csv()` is used to load the dataset, followed by column validation to ensure all required fields are present.
* **Processing:** NumPy arrays are extracted from the DataFrame. `np.sum()` and `np.mean()` calculate total and average marks across the subject axes.
* **Conditionals:** NumPy's `np.where()` and `np.all()` evaluate if a student scored above the passing threshold (40) in every individual subject. Standard Python loops iterate through the DataFrame to assign letter grades based on the calculated averages.
* **Analysis:** Pandas aggregation functions extract the highest and lowest scores, while boolean masking is used to filter students with low attendance (<75%).

**6. Key Features**
* Automated grading system (A+ to F).
* Strict Pass/Fail verification across all subjects simultaneously.
* Subject-wise performance breakdown (Average, Highest, Lowest, Pass/Fail counts).
* Automatic extraction of the Top 3 performers.
* Low attendance identification module.

**7. Output/Screenshots**
![Class summary](Screenshot_2026_1014_082228.png)

![Subject-wise table](Screenshot_2026_1014_082510.png)

![Top 3 performers](Screenshot_2026_1014_082605.jpg)


**8. Final Outcome**
The project successfully processes the raw CSV file and outputs a clean, readable command-line report. It provides actionable insights, such as identifying the weakest subject across the class, listing students who require attendance warnings, and ranking the top students by total marks.

**9. Challenges & Learning**
A key challenge was applying the rule that a student failing a single subject must receive an overall "F" grade, regardless of their average. This was solved by separating the Pass/Fail check using NumPy vectorization before passing the boolean result into the grade assignment loop. The project reinforced the value of modular programming by separating calculations (`functions.py`) from the execution script (`main.py`).

**10. GitHub Repository**
*https://github.com/maheshjanjiralashiva-blip/Student-performance-analytics.*

