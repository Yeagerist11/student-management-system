# EduManage - Student Management System

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
│   └── templates/                 # Global templates
│       ├── base.html              # Responsive Bootstrap 5 base template
│       └── students/
│           ├── dashboard.html     # Analytics & KPI overview
│           ├── student_list.html  # Directory with search & filters
│           ├── student_detail.html# Student profile view
│           ├── student_form.html  # Add / Edit form
│           ├── student_confirm_delete.html # Confirmation page
│           └── course_list.html   # Course management
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
   - **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🔑 Default Credentials

- **Django Admin:**
  - **Username:** `admin`
  - **Password:** `admin123`

---

## 🧪 Running Automated Tests

To run the full suite of unit and integration tests:

```powershell
..\.venv\Scripts\python.exe manage.py test
```

---

## 🔄 Re-seeding Sample Data

To populate fresh sample courses and students at any time:

```powershell
..\.venv\Scripts\python.exe manage.py seed_data
```
