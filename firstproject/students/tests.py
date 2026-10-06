from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
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
            gpa=3.85,
            status="Active",
            address="123 Main St"
        )

    def test_course_str(self):
        self.assertEqual(str(self.course), "IT-101 - Information Technology")

    def test_student_str_and_properties(self):
        self.assertEqual(str(self.student), "STU999 - John Doe")
        self.assertEqual(self.student.full_name, "John Doe")
        self.assertEqual(self.student.status_badge_class, "bg-success")
        self.assertEqual(self.student.academic_standing, "First Class with Distinction")
        self.assertEqual(self.student.expected_graduation_year, 2027)

    def test_course_student_count(self):
        self.assertEqual(self.course.student_count, 1)


class StudentPortalViewTests(TestCase):
    """
    Tests ensuring each logged-in student sees ONLY their own statistics
    and cannot access administrative student management pages.
    """
    def setUp(self):
        self.course_cse = Course.objects.create(
            name="Computer Science",
            code="CSE-101",
            duration_years=4
        )
        self.course_ds = Course.objects.create(
            name="Data Science",
            code="DS-201",
            duration_years=4
        )

        # Student 1: Aarav
        self.user_aarav = User.objects.create_user(
            username="stu2024001",
            email="aarav@campus.edu",
            password="student123",
            first_name="Aarav",
            last_name="Sharma"
        )
        self.student_aarav = Student.objects.create(
            user=self.user_aarav,
            roll_number="STU2024001",
            first_name="Aarav",
            last_name="Sharma",
            email="aarav@campus.edu",
            phone="9876543210",
            date_of_birth=date(2003, 5, 14),
            gender="M",
            course=self.course_cse,
            enrollment_date=date(2023, 8, 1),
            gpa=3.92,
            status="Active",
            address="42 MG Road, Bengaluru"
        )

        # Student 2: Priya
        self.user_priya = User.objects.create_user(
            username="stu2024002",
            email="priya@campus.edu",
            password="student123",
            first_name="Priya",
            last_name="Nair"
        )
        self.student_priya = Student.objects.create(
            user=self.user_priya,
            roll_number="STU2024002",
            first_name="Priya",
            last_name="Nair",
            email="priya@campus.edu",
            phone="9123456780",
            date_of_birth=date(2004, 3, 22),
            gender="F",
            course=self.course_ds,
            enrollment_date=date(2023, 8, 1),
            gpa=3.40,
            status="Active",
            address="15 Marine Drive, Kochi"
        )

        # Admin / Staff User
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@campus.edu",
            password="admin123"
        )

    def test_unauthenticated_user_redirected_to_login(self):
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_logged_in_student_sees_only_own_statistics(self):
        # Log in as Aarav
        self.client.login(username="stu2024001", password="student123")
        response = self.client.get(reverse('student_dashboard'))

        self.assertEqual(response.status_code, 200)
        # Should see Aarav's own statistics
        self.assertContains(response, "Aarav Sharma")
        self.assertContains(response, "STU2024001")
        self.assertContains(response, "3.92")
        self.assertContains(response, "42 MG Road, Bengaluru")
        self.assertContains(response, "CSE-101")

        # Must NOT display Priya's private address or details
        self.assertNotContains(response, "15 Marine Drive, Kochi")
        self.assertNotContains(response, "9123456780")

    def test_student_cannot_access_admin_dashboard(self):
        # Log in as student
        self.client.login(username="stu2024001", password="student123")
        response = self.client.get(reverse('dashboard'))
        # Should be redirected to student_dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_student_cannot_access_student_list(self):
        # Log in as student
        self.client.login(username="stu2024001", password="student123")
        response = self.client.get(reverse('student_list'))
        # Should be intercepted and redirected to student_dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_student_can_update_own_contact_info(self):
        self.client.login(username="stu2024001", password="student123")
        post_data = {
            'action': 'update_profile',
            'email': 'aarav.new@campus.edu',
            'phone': '9999988888',
            'address': 'New Residence, Bengaluru'
        }
        response = self.client.post(reverse('student_dashboard'), post_data)
        self.assertEqual(response.status_code, 302)
        self.student_aarav.refresh_from_db()
        self.assertEqual(self.student_aarav.phone, '9999988888')
        self.assertEqual(self.student_aarav.address, 'New Residence, Bengaluru')

    def test_login_with_roll_number(self):
        response = self.client.post(reverse('login'), {
            'username': 'STU2024001',
            'password': 'student123'
        })
        self.assertEqual(response.status_code, 302)
        # Should route to student dashboard
        self.assertRedirects(response, reverse('dashboard_router'))


class AdminStaffViewTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@campus.edu",
            password="admin123"
        )
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
        self.client.login(username="admin", password="admin123")

    def test_admin_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "StudentHub")
        self.assertContains(response, "Alice Smith")
        self.assertEqual(response.context['total_students'], 1)

    def test_admin_student_list_view(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "STU101")
        self.assertContains(response, "Alice Smith")

    def test_admin_student_create_post(self):
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

    def test_admin_student_delete_post(self):
        response = self.client.post(reverse('student_delete', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())
