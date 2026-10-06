from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from functools import wraps

from .models import Student, Course
from .forms import StudentForm, CourseForm, StudentProfileUpdateForm


def staff_required(view_func):
    """
    Decorator to restrict administrative pages to staff/superusers.
    Students attempting to access these views are safely redirected
    to their personal dashboard so they cannot see other students' data.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to continue.")
            return redirect('login')
        if not (request.user.is_staff or request.user.is_superuser):
            if hasattr(request.user, 'student_profile'):
                messages.warning(request, "Access restricted. You can only view your own student dashboard.")
                return redirect('student_dashboard')
            messages.error(request, "Administrator privileges are required to access that page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def dashboard_router(request):
    """
    Directs authenticated users to their corresponding dashboard:
    - Students -> Personal Student Dashboard (only their own statistics)
    - Staff / Administrators -> Global Institution Dashboard
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if hasattr(request.user, 'student_profile') and not request.user.is_staff:
        return redirect('student_dashboard')
    return redirect('dashboard')


@login_required
def student_dashboard(request):
    """
    Dedicated Student Dashboard:
    Displays only the statistics, academic records, and peers
    pertaining to the logged-in student.
    """
    try:
        student = request.user.student_profile
    except (AttributeError, Student.DoesNotExist):
        if request.user.is_staff or request.user.is_superuser:
            messages.info(request, "You are logged in as Staff/Admin. Redirected to the institution dashboard.")
            return redirect('dashboard')
        messages.error(request, "No student profile is associated with your account. Please contact the administrator.")
        return redirect('login')

    # Handle profile contact info update
    if request.method == 'POST' and request.POST.get('action') == 'update_profile':
        profile_form = StudentProfileUpdateForm(request.POST, instance=student)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your contact details have been updated successfully.")
            return redirect('student_dashboard')
        else:
            messages.error(request, "Please correct the errors in the update form.")
    else:
        profile_form = StudentProfileUpdateForm(instance=student)

    # Compute personal and anonymized comparative statistics
    course = student.course
    if course:
        course_student_count = course.students.count()
        avg_val = course.students.aggregate(avg=Avg('gpa'))['avg']
        course_avg_gpa = round(avg_val, 2) if avg_val else 0.0
        gpa_difference = round(float(student.gpa) - float(course_avg_gpa), 2)
        # Classmates in same program (privacy-preserved: name, roll number, status)
        course_peers = course.students.exclude(pk=student.pk).order_by('roll_number')[:6]
    else:
        course_student_count = 0
        course_avg_gpa = 0.0
        gpa_difference = 0.0
        course_peers = []

    context = {
        'student': student,
        'course': course,
        'course_student_count': course_student_count,
        'course_avg_gpa': course_avg_gpa,
        'gpa_difference': gpa_difference,
        'course_peers': course_peers,
        'profile_form': profile_form,
    }
    return render(request, 'students/student_portal.html', context)


@staff_required
def dashboard(request):
    """
    Administrative Institution Dashboard (Staff/Admin only).
    """
    total_students = Student.objects.count()
    active_students = Student.objects.filter(status='Active').count()
    graduated_students = Student.objects.filter(status='Graduated').count()
    total_courses = Course.objects.count()

    avg_gpa_val = Student.objects.aggregate(avg=Avg('gpa'))['avg']
    avg_gpa = round(avg_gpa_val, 2) if avg_gpa_val else 0.0

    recent_students = Student.objects.select_related('course').order_by('-created_at')[:6]
    courses_with_counts = Course.objects.annotate(total=Count('students')).order_by('-total')[:5]

    context = {
        'total_students': total_students,
        'active_students': active_students,
        'graduated_students': graduated_students,
        'total_courses': total_courses,
        'avg_gpa': avg_gpa,
        'recent_students': recent_students,
        'courses_with_counts': courses_with_counts,
    }
    return render(request, 'students/dashboard.html', context)


@staff_required
def student_list(request):
    query = request.GET.get('q', '').strip()
    course_id = request.GET.get('course', '')
    status = request.GET.get('status', '')

    students = Student.objects.select_related('course').all()

    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(email__icontains=query)
        )

    if course_id:
        students = students.filter(course_id=course_id)

    if status:
        students = students.filter(status=status)

    paginator = Paginator(students, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    courses = Course.objects.all()
    status_choices = Student.STATUS_CHOICES

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_course': course_id,
        'selected_status': status,
        'courses': courses,
        'status_choices': status_choices,
        'total_count': students.count(),
    }
    return render(request, 'students/student_list.html', context)


@staff_required
def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related('course'), pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


@staff_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            # Auto-create user login for student if roll number username is available
            username = student.roll_number.lower().replace("-", "")
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=student.email,
                    password="student123",
                    first_name=student.first_name,
                    last_name=student.last_name
                )
                student.user = user
                student.save()
            messages.success(
                request,
                f'Student "{student.full_name}" registered! Portal login username: "{username}", password: "student123"'
            )
            return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {
        'form': form,
        'action_title': 'Register New Student',
        'submit_btn_text': 'Add Student'
    })


@staff_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student "{student.full_name}" updated successfully!')
            return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student,
        'action_title': f'Edit Student: {student.full_name}',
        'submit_btn_text': 'Update Student'
    })


@staff_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.full_name
        # Also clean up linked user account if exists and not staff
        if student.user and not (student.user.is_staff or student.user.is_superuser):
            student.user.delete()
        student.delete()
        messages.success(request, f'Student "{name}" has been deleted.')
        return redirect('student_list')

    return render(request, 'students/student_confirm_delete.html', {'student': student})


@staff_required
def course_list(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course "{course.name}" created successfully!')
            return redirect('course_list')
        else:
            messages.error(request, 'Please correct the errors in the course form.')
    else:
        form = CourseForm()

    courses = Course.objects.annotate(total_students=Count('students')).order_by('name')
    return render(request, 'students/course_list.html', {'courses': courses, 'form': form})


@staff_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        name = course.name
        course.delete()
        messages.success(request, f'Course "{name}" deleted successfully.')
    return redirect('course_list')


def user_login(request):
    """
    Login view supporting both username and roll_number.
    Provides quick demo accounts for rapid testing.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_router')

    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Check if identifier corresponds to a student's roll number
        target_username = identifier
        student_match = Student.objects.filter(roll_number__iexact=identifier).first()
        if student_match and student_match.user:
            target_username = student_match.user.username

        user = authenticate(request, username=target_username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard_router')
        else:
            messages.error(request, 'Invalid username / roll number or password.')

    # Provide demo accounts for quick one-click review
    demo_students = Student.objects.filter(user__isnull=False).select_related('course', 'user')[:4]

    return render(request, 'students/login.html', {
        'demo_students': demo_students
    })


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
