from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta, datetime
from functools import wraps

from students.models import Student, Course
from .models import Parent, Attendance
from .forms import ParentUserCreationForm, ParentProfileForm, ParentLoginForm, AttendanceForm


def parent_required(view_func):
    """
    Decorator to restrict views to authenticated parents only.
    Staff/admins are redirected to the admin dashboard.
    Unauthenticated users are redirected to the login page.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('parent_login')
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard')
        if not hasattr(request.user, 'parent_profile'):
            messages.info(request, "Parent profile not found. Please contact the administrator.")
            return redirect('parent_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def parent_login(request):
    if request.user.is_authenticated and hasattr(request.user, 'parent_profile') and not request.user.is_staff:
        return redirect('parent_dashboard')

    if request.method == 'POST':
        form = ParentLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and hasattr(user, 'parent_profile') and not user.is_staff:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('parent_dashboard')
            else:
                messages.error(request, 'Invalid credentials or account is not a parent account.')
    else:
        form = ParentLoginForm()

    return render(request, 'parents/login.html', {'form': form})


def parent_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('parent_login')


@parent_required
def parent_dashboard(request):
    """
    Parent Dashboard: Lists all children linked to the parent with
    quick statistics (GPA, attendance summary, status).
    """
    parent = request.user.parent_profile
    children = parent.get_children()

    child_stats = []
    for child in children:
        recent_attendance = child.attendances.filter(
            date__gte=timezone.now().date() - timedelta(days=30)
        )
        present_count = recent_attendance.filter(status=Attendance.STATUS_PRESENT).count()
        absent_count = recent_attendance.filter(status=Attendance.STATUS_ABSENT).count()
        late_count = recent_attendance.filter(status=Attendance.STATUS_LATE).count()
        total_days = recent_attendance.count()

        attendance_rate = round((present_count / total_days) * 100, 1) if total_days > 0 else 0

        child_stats.append({
            'student': child,
            'present_count': present_count,
            'absent_count': absent_count,
            'late_count': late_count,
            'total_days': total_days,
            'attendance_rate': attendance_rate,
        })

    context = {
        'parent': parent,
        'child_stats': child_stats,
    }
    return render(request, 'parents/dashboard.html', context)


@parent_required
def parent_child_detail(request, pk):
    """
    Detailed view of a child's statistics, attendance history, and performance.
    Only children linked to the logged-in parent are accessible.
    """
    parent = request.user.parent_profile
    student = get_object_or_404(
        parent.children.select_related('course').all(),
        pk=pk
    )

    # Attendance filtering
    attendance_qs = student.attendances.all()
    month_filter = request.GET.get('month')
    if month_filter:
        try:
            year, month = month_filter.split('-')
            attendance_qs = attendance_qs.filter(date__year=year, date__month=month)
        except (ValueError, AttributeError):
            pass

    # Recent attendance (last 30 days)
    cutoff_date = timezone.now().date() - timedelta(days=30)
    recent_attendance = attendance_qs.filter(date__gte=cutoff_date).order_by('-date')
    all_attendance = attendance_qs.order_by('-date')[:50]

    present_count = attendance_qs.filter(status=Attendance.STATUS_PRESENT).count()
    absent_count = attendance_qs.filter(status=Attendance.STATUS_ABSENT).count()
    late_count = attendance_qs.filter(status=Attendance.STATUS_LATE).count()
    total_attendance = present_count + absent_count + late_count
    attendance_rate = round((present_count / total_attendance) * 100, 1) if total_attendance > 0 else 0

    # Performance stats
    course = student.course
    course_avg_gpa = 0.0
    gpa_difference = 0.0
    course_student_count = 0
    if course:
        course_student_count = course.students.count()
        avg_val = course.students.aggregate(avg=Avg('gpa'))['avg']
        course_avg_gpa = round(avg_val, 2) if avg_val else 0.0
        gpa_difference = round(float(student.gpa) - float(course_avg_gpa), 2)

    context = {
        'parent': parent,
        'student': student,
        'course': course,
        'course_avg_gpa': course_avg_gpa,
        'gpa_difference': gpa_difference,
        'course_student_count': course_student_count,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'total_attendance': total_attendance,
        'attendance_rate': attendance_rate,
        'recent_attendance': recent_attendance,
        'all_attendance': all_attendance,
    }
    return render(request, 'parents/child_detail.html', context)


@parent_required
def parent_profile_update(request):
    """Update parent's own contact information."""
    parent = request.user.parent_profile
    if request.method == 'POST':
        form = ParentProfileForm(request.POST, instance=parent)
        if form.is_valid():
            form.save()
            messages.success(request, "Your contact details have been updated.")
            return redirect('parent_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ParentProfileForm(instance=parent)

    return render(request, 'parents/profile_update.html', {'form': form})
