from django.contrib import admin
from .models import Course, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'duration_years', 'created_at')
    search_fields = ('code', 'name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'first_name', 'last_name', 'email', 'course', 'gpa', 'status', 'enrollment_date')
    list_filter = ('status', 'course', 'gender')
    search_fields = ('roll_number', 'first_name', 'last_name', 'email')
    ordering = ('-created_at',)
