from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    duration_years = models.PositiveSmallIntegerField(default=4)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def student_count(self):
        return self.students.count()


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Graduated', 'Graduated'),
        ('Suspended', 'Suspended'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile',
        help_text="Associated login account for student portal access"
    )
    roll_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Roll Number / ID"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    enrollment_date = models.DateField(default=timezone.now)
    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
        verbose_name="GPA / Score"
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Active')
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.roll_number} - {self.full_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def status_badge_class(self):
        badge_map = {
            'Active': 'bg-success',
            'Inactive': 'bg-secondary',
            'Graduated': 'bg-primary',
            'Suspended': 'bg-danger',
        }
        return badge_map.get(self.status, 'bg-info')

    @property
    def academic_standing(self):
        val = float(self.gpa)
        if val >= 3.7:
            return "First Class with Distinction"
        elif val >= 3.0:
            return "First Class"
        elif val >= 2.0:
            return "Second Class"
        return "Academic Warning"

    @property
    def gpa_scale_max(self):
        return 4.0 if float(self.gpa) <= 4.0 else 10.0

    @property
    def gpa_percentage(self):
        max_scale = self.gpa_scale_max
        return min(100, max(0, int((float(self.gpa) / max_scale) * 100)))

    @property
    def expected_graduation_year(self):
        duration = self.course.duration_years if self.course else 4
        return self.enrollment_date.year + duration

    @property
    def degree_progress_percentage(self):
        if self.status == 'Graduated':
            return 100
        total_years = self.course.duration_years if self.course else 4
        years_passed = max(0, timezone.now().date().year - self.enrollment_date.year)
        progress = int(((years_passed + 1) / max(1, total_years)) * 100)
        return min(95, max(25, progress))

