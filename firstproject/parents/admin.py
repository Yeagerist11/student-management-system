from django.contrib import admin
from .models import Parent, Attendance


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_username', 'phone', 'children_count', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    filter_horizontal = ('children',)

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'

    def children_count(self, obj):
        return obj.children.count()
    children_count.short_description = 'Children'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'recorded_at')
    list_filter = ('status', 'date', 'student__course')
    search_fields = ('student__roll_number', 'student__first_name', 'student__last_name')
    date_hierarchy = 'date'
