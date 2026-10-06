# StudentHub - Student Management System

A full-featured, responsive Student Management System built with **Django 6.1** and **Bootstrap 5**.

---

## 🚀 Features

- **📊 Comprehensive Analytics Dashboard:**
  - Real-time statistics: Total Students, Active Enrolled, Graduated Alumni, and Average GPA.
  - Recent enrollment activity feed.
  - Department and Course distribution overview.

- **🎓 Student Directory & Profile Management (CRUD):**
  - **Student List:** Paginated directory with dynamic search (by name, roll number, or email) and filtering by course and enrollment status.
  - **Student Details:** Clean profile view showing personal information, contact details, academic standing, and residential address.
  - **Register New Student:** Form with field validation, date pickers, GPA bounds checking, and course selection.
  - **Edit Student Profile:** Update student info with instant feedback.
  - **Delete Student:** Deletion with confirmation safeguard and alert notifications.

- **📚 Course & Degree Program Management:**
  - Create and manage degree programs and departments (Course code, name, duration, description).
  - Track active enrollment counts per course.
  - Course deletion with cascade safeguard.

- **🛡️ Django Admin Integration:**
  - Models fully registered in Django Admin with filters, search, and list displays.

- **👨‍👩‍👧‍👦 Parent Portal Module:**
  - **Parent Authentication:** Secure login/logout with parent-only access restrictions (staff and student accounts are rejected).
  - **Parent Dashboard:** Overview of all linked children with at-a-glance statistics (GPA, attendance rate, degree progress).
  - **Child Detail View:** Comprehensive report for each child including academic summary (GPA vs class average, academic standing, enrollment info), 30-day attendance history with present/absent/late breakdown, and contact information.
  - **Parent Profile Management:** Update contact phone number.
  - **Attendance Tracking:** Attendance model with present/absent/late status, remarks, and per-student-per-date uniqueness.
  - **Sample Parent Accounts:** 3 parent accounts seeded with children links and 20 days of attendance records per student.

---

## 📂 Project Structure

```text
Project/
├── .venv/                         # Virtual environment (Django 6.1, Python 3.14)
├── firstproject/
│   ├── db.sqlite3                 # SQLite database
│   ├── manage.py                  # Django management script
│   ├── firstproject/              # Project settings & URL routing
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── students/                  # Student Management App
│   │   ├── models.py              # Student and Course models
│   │   ├── forms.py               # StudentForm and CourseForm with validation
│   │   ├── views.py               # Dashboard, CRUD views, filtering
│   │   ├── urls.py                # Routing for student management
│   │   ├── admin.py               # Django Admin configuration
│   │   ├── tests.py               # Automated unit & integration tests
│   │   └── management/commands/
│   │       └── seed_data.py       # Sample data generation command
│   ├── parents/                   # Parent Portal Module
│   │   ├── models.py              # Parent (User link, children) & Attendance models
│   │   ├── forms.py               # Parent login, profile, and attendance forms
│   │   ├── views.py               # Login, logout, dashboard, child detail, profile update
│   │   ├── urls.py                # Routing for parent portal
│   │   ├── admin.py               # Django Admin configuration
│   │   ├── migrations/
│   │   │   └── 0001_initial.py
│   │   └── templates/parents/
│   │       ├── login.html          # Parent login page
│   │       ├── dashboard.html      # Children overview with statistics
│   │       ├── child_detail.html   # Detailed child statistics & attendance
│   │       └── profile_update.html # Contact info update form
│   └── templates/                 # Global templates
│       ├── base.html              # Responsive Bootstrap 5 base template
│       ├── students/
│       │   ├── dashboard.html     # Analytics & KPI overview
│       │   ├── student_list.html  # Directory with search & filters
│       │   ├── student_detail.html# Student profile view
│       │   ├── student_form.html  # Add / Edit form
│       │   ├── student_confirm_delete.html # Confirmation page
│       │   ├── course_list.html   # Course management
│       │   ├── login.html         # Student/Staff login page
│       │   └── student_portal.html# Student personal portal with GPA and profile
│       └── parents/
│           ├── login.html         # Parent login page
│           ├── dashboard.html     # Children overview with statistics
│           ├── child_detail.html  # Detailed child statistics & attendance
│           └── profile_update.html # Contact info update form
└── README.md
```

---

## 🏃 Running the Application

1. **Activate the Virtual Environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Navigate to the Django project directory:**
   ```powershell
   cd firstproject
   ```

3. **Start the Development Server:**
   ```powershell
   ..\.venv\Scripts\python.exe manage.py runserver
   ```
   Open your browser and navigate to:
    - **Student Dashboard:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    - **Student Directory:** [http://127.0.0.1:8000/students/](http://127.0.0.1:8000/students/)
    - **Courses & Programs:** [http://127.0.0.1:8000/courses/](http://127.0.0.1:8000/courses/)
    - **Parent Portal:** [http://127.0.0.1:8000/parent/](http://127.0.0.1:8000/parent/)
    - **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Default Credentials

- **Django Admin:**
  - **Username:** `admin`
  - **Password:** `admin123`

- **Parent Portal (x3 accounts):**
  - **Username:** `parent_arjun` · **Password:** `parent123` · (Child: STU2024001 - Aarav Sharma)
  - **Username:** `parent_priya` · **Password:** `parent123` · (Child: STU2024002 - Priya Nair)
  - **Username:** `parent_rohan` · **Password:** `parent123` · (Children: STU2024003, STU2024004)

- **Student Accounts:**
  - **Username / Roll No:** `STU2024001` through `STU2024008`
  - **Password:** `student123` (for all student accounts)

---

## 🧪 Running Automated Tests

To run the full suite of unit and integration tests:

```powershell
..\.venv\Scripts\python.exe manage.py test
```

---

## 🔄 Re-seeding Sample Data

To populate fresh sample courses, students, parents, and attendance records at any time:

```powershell
..\.venv\Scripts\python.exe manage.py seed_data
```

This command creates 5 sample courses, 1 admin account, 8 student accounts, 3 parent accounts (linked to their children), and 20 days of attendance records per student. It is safe to re-run — existing records are preserved and only new data is added.
