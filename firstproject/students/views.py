from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator

from .models import Student, Course
from .forms import StudentForm, CourseForm


def dashboard(request):
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


def student_detail(request, pk):
    student = get_object_or_404(Student.objects.select_related('course'), pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student "{student.full_name}" registered successfully!')
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


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f'Student "{name}" has been deleted.')
        return redirect('student_list')

    return render(request, 'students/student_confirm_delete.html', {'student': student})


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


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        name = course.name
        course.delete()
        messages.success(request, f'Course "{name}" deleted successfully.')
    return redirect('course_list')
