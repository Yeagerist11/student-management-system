from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Router & Portals
    path('', views.dashboard_router, name='dashboard_router'),
    path('portal/', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', views.dashboard, name='dashboard'),

    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Administrative Student Management
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),

    # Course Management
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
]
