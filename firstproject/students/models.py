from django.db import models
from django.utils import timezone


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
