from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from students.models import Course, Student


class Command(BaseCommand):
    help = "Seed database with initial courses and students for demonstration"

    def handle(self, *args, **options):
        self.stdout.write("Seeding sample courses and students...")

        courses_data = [
            {
                "code": "CSE-101",
                "name": "Computer Science & Engineering",
                "duration_years": 4,
                "description": "Comprehensive program covering software engineering, algorithms, AI, and systems architecture."
            },
            {
                "code": "DS-201",
                "name": "Data Science & Artificial Intelligence",
                "duration_years": 4,
                "description": "Specialized curriculum focusing on machine learning, big data analysis, and predictive modeling."
            },
            {
                "code": "ECE-102",
                "name": "Electronics & Communication",
                "duration_years": 4,
                "description": "Study of embedded systems, telecommunications, signal processing, and IoT hardware."
            },
            {
                "code": "BBA-301",
                "name": "Business Administration",
                "duration_years": 3,
                "description": "Focuses on strategic management, marketing, corporate finance, and entrepreneurship."
            },
            {
                "code": "ME-105",
                "name": "Mechanical Engineering",
                "duration_years": 4,
                "description": "Principles of thermodynamics, robotics, automotive engineering, and mechanics."
            },
        ]

        course_objs = {}
        for c in courses_data:
            course, created = Course.objects.get_or_create(
                code=c["code"],
                defaults={
                    "name": c["name"],
                    "duration_years": c["duration_years"],
                    "description": c["description"]
                }
            )
            course_objs[c["code"]] = course
            if created:
                self.stdout.write(f"Created Course: {course.code} - {course.name}")

        students_data = [
            {
                "roll_number": "STU2024001",
                "first_name": "Aarav",
                "last_name": "Sharma",
                "email": "aarav.sharma@campus.edu",
                "phone": "+91 98765 43210",
                "date_of_birth": date(2003, 5, 14),
                "gender": "M",
                "course": course_objs["CSE-101"],
                "enrollment_date": date(2023, 8, 1),
                "gpa": 3.92,
                "status": "Active",
                "address": "42 MG Road, Bengaluru, Karnataka"
            },
            {
                "roll_number": "STU2024002",
                "first_name": "Priya",
                "last_name": "Nair",
                "email": "priya.nair@campus.edu",
                "phone": "+91 98111 22334",
                "date_of_birth": date(2004, 3, 22),
                "gender": "F",
                "course": course_objs["DS-201"],
                "enrollment_date": date(2023, 8, 1),
                "gpa": 3.88,
                "status": "Active",
                "address": "15 Marine Drive, Kochi, Kerala"
            },
            {
                "roll_number": "STU2024003",
                "first_name": "Rohan",
                "last_name": "Verma",
                "email": "rohan.verma@campus.edu",
                "phone": "+91 99222 33445",
                "date_of_birth": date(2002, 11, 9),
                "gender": "M",
                "course": course_objs["ECE-102"],
                "enrollment_date": date(2022, 8, 15),
                "gpa": 3.45,
                "status": "Active",
                "address": "78 Park Street, Kolkata, West Bengal"
            },
            {
                "roll_number": "STU2024004",
                "first_name": "Ananya",
                "last_name": "Deshmukh",
                "email": "ananya.d@campus.edu",
                "phone": "+91 97333 44556",
                "date_of_birth": date(2003, 7, 30),
                "gender": "F",
                "course": course_objs["BBA-301"],
                "enrollment_date": date(2023, 7, 20),
                "gpa": 3.75,
                "status": "Active",
                "address": "12 FC Road, Pune, Maharashtra"
            },
            {
                "roll_number": "STU2024005",
                "first_name": "Vikram",
                "last_name": "Singh",
                "email": "vikram.singh@campus.edu",
                "phone": "+91 96444 55667",
                "date_of_birth": date(2001, 9, 18),
                "gender": "M",
                "course": course_objs["ME-105"],
                "enrollment_date": date(2021, 8, 10),
                "gpa": 3.60,
                "status": "Graduated",
                "address": "88 Civil Lines, Jaipur, Rajasthan"
            },
            {
                "roll_number": "STU2024006",
                "first_name": "Sneha",
                "last_name": "Patel",
                "email": "sneha.patel@campus.edu",
                "phone": "+91 95555 66778",
                "date_of_birth": date(2004, 1, 15),
                "gender": "F",
                "course": course_objs["CSE-101"],
                "enrollment_date": date(2024, 8, 5),
                "gpa": 3.95,
                "status": "Active",
                "address": "25 SG Highway, Ahmedabad, Gujarat"
            },
            {
                "roll_number": "STU2024007",
                "first_name": "Karthik",
                "last_name": "Rao",
                "email": "karthik.rao@campus.edu",
                "phone": "+91 94666 77889",
                "date_of_birth": date(2002, 4, 12),
                "gender": "M",
                "course": course_objs["DS-201"],
                "enrollment_date": date(2022, 8, 12),
                "gpa": 3.30,
                "status": "Inactive",
                "address": "10 Banjara Hills, Hyderabad, Telangana"
            },
            {
                "roll_number": "STU2024008",
                "first_name": "Meera",
                "last_name": "Kapoor",
                "email": "meera.kapoor@campus.edu",
                "phone": "+91 93777 88990",
                "date_of_birth": date(2003, 10, 5),
                "gender": "F",
                "course": course_objs["CSE-101"],
                "enrollment_date": date(2023, 8, 1),
                "gpa": 3.82,
                "status": "Active",
                "address": "104 Defence Colony, New Delhi"
            },
        ]

        for s in students_data:
            student, created = Student.objects.get_or_create(
                roll_number=s["roll_number"],
                defaults=s
            )
            if created:
                self.stdout.write(f"Created Student: {student.roll_number} - {student.full_name}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded sample data!"))
