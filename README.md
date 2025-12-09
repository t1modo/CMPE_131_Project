# Scanva

Scanva is a lightweight Flask-based learning management system that combines Canvas-style assignment distribution with Gradescope-style submission, grading, and feedback workflows.
This Milestone 2 release implements a complete end-to-end prototype where:

- Instructors create assignments, upload prompt PDFs, review student submissions, and provide grades and feedback.
- Students view course assignments, upload their own PDFs, and receive graded feedback.

---

## Quick start

### 1) Create & activate a virtual environment (recommended)

`python3 -m venv .venv`
On mac: `source .venv/bin/activate` 
On Windows: `.venv\Scripts\activate`

### 2) Install dependencies

`pip install -r requirements.txt`

### 3) Run

`python run.py`

### 4) Test Instructions (Optional)

`pytest`

---

# 👥 User Roles
## 🟦 Instructor Role

### Instructors can:

- Create assignments

- Upload assignment prompt files

- View all student submissions

- Grade, comment, and upload graded feedback PDFs

- Navigate via the Instructor Dashboard

## 🟩 Student Role

- Students can:

- View enrolled courses

- View assignments per course

- Download assignment prompt file

- Upload submission PDF

- View instructor feedback and grades

- Navigate via the Student Dashboard

---

### Rendered Screenshots

![](/app/images/Home_Page.png)

![](/app/images/Login_Page.png)

![](/app/images/SignUp_Page.png)

![](/app/images/Dashboard_Instructor_Page.png)

![](/app/images/Dashboard_Student_Page.png)

![](/app/images/Create_Assignment_Page.png)