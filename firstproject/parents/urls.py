from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.parent_login, name='parent_login'),
    path('logout/', views.parent_logout, name='parent_logout'),
    path('profile/update/', views.parent_profile_update, name='parent_profile_update'),
    path('', views.parent_dashboard, name='parent_dashboard'),
    path('child/<int:pk>/', views.parent_child_detail, name='parent_child_detail'),
]
