from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Parent(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='parent_profile',
        help_text="Associated login account for parent portal access"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    children = models.ManyToManyField(
        'students.Student',
        related_name='parents',
        blank=True,
        help_text="Students linked to this parent (their children)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} (Parent)"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    def get_children(self):
        return self.children.all().select_related('course')


class Attendance(models.Model):
    STATUS_PRESENT = 'present'
    STATUS_ABSENT = 'absent'
    STATUS_LATE = 'late'

    STATUS_CHOICES = [
        (STATUS_PRESENT, 'Present'),
        (STATUS_ABSENT, 'Absent'),
        (STATUS_LATE, 'Late'),
    ]

    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PRESENT
    )
    remarks = models.TextField(blank=True, verbose_name="Remarks")
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']
        get_latest_by = 'date'

    def __str__(self):
        return f"{self.student.full_name} - {self.get_status_display()} on {self.date}"

    @property
    def status_badge_class(self):
        badge_map = {
            'present': 'bg-success',
            'absent': 'bg-danger',
            'late': 'bg-warning',
        }
        return badge_map.get(self.status, 'bg-info')
