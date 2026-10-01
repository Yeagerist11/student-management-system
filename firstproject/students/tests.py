from django.test import TestCase
from django.urls import reverse
from datetime import date
from students.models import Course, Student


class StudentModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name="Information Technology",
            code="IT-101",
            duration_years=4,
            description="IT Degree program"
        )
        self.student = Student.objects.create(
            roll_number="STU999",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            date_of_birth=date(2002, 1, 1),
            gender="M",
            course=self.course,
            enrollment_date=date(2023, 8, 1),
            gpa=3.75,
            status="Active",
            address="123 Main St"
        )

    def test_course_str(self):
        self.assertEqual(str(self.course), "IT-101 - Information Technology")

    def test_student_str_and_properties(self):
        self.assertEqual(str(self.student), "STU999 - John Doe")
        self.assertEqual(self.student.full_name, "John Doe")
        self.assertEqual(self.student.status_badge_class, "bg-success")

    def test_course_student_count(self):
        self.assertEqual(self.course.student_count, 1)


class StudentViewTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name="Computer Science",
            code="CS-101",
            duration_years=4
        )
        self.student = Student.objects.create(
            roll_number="STU101",
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            date_of_birth=date(2003, 5, 10),
            gender="F",
            course=self.course,
            enrollment_date=date(2024, 1, 15),
            gpa=3.90,
            status="Active"
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "EduManage")
        self.assertContains(response, "Alice Smith")
        self.assertEqual(response.context['total_students'], 1)

    def test_student_list_view(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "STU101")
        self.assertContains(response, "Alice Smith")

    def test_student_list_search(self):
        response = self.client.get(reverse('student_list') + '?q=Alice')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")

        response_empty = self.client.get(reverse('student_list') + '?q=NonExistent')
        self.assertContains(response_empty, "No Students Found")

    def test_student_detail_view(self):
        response = self.client.get(reverse('student_detail', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "Academic Information")

    def test_student_create_post(self):
        data = {
            'roll_number': 'STU102',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'email': 'bob@example.com',
            'phone': '9876543210',
            'date_of_birth': '2004-06-15',
            'gender': 'M',
            'course': self.course.pk,
            'enrollment_date': '2024-08-01',
            'gpa': '3.50',
            'status': 'Active',
            'address': '456 Oak Ave'
        }
        response = self.client.post(reverse('student_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(roll_number='STU102').exists())

    def test_student_update_post(self):
        data = {
            'roll_number': self.student.roll_number,
            'first_name': 'Alicia',
            'last_name': 'Smith',
            'email': self.student.email,
            'phone': '1112223333',
            'date_of_birth': '2003-05-10',
            'gender': 'F',
            'course': self.course.pk,
            'enrollment_date': '2024-01-15',
            'gpa': '4.00',
            'status': 'Active',
            'address': 'New Address'
        }
        response = self.client.post(reverse('student_update', kwargs={'pk': self.student.pk}), data)
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Alicia')
        self.assertEqual(float(self.student.gpa), 4.00)

    def test_student_delete_post(self):
        response = self.client.post(reverse('student_delete', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())

    def test_course_create_post(self):
        data = {
            'name': 'Civil Engineering',
            'code': 'CIV-101',
            'duration_years': 4,
            'description': 'Structural engineering'
        }
        response = self.client.post(reverse('course_list'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(code='CIV-101').exists())
