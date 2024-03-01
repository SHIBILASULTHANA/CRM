from django.urls import path
from .views import (
    AdminAttendanceView,
    EmployeeAttendanceView,
    MarkAttendanceView,
    AttendanceSettingsView,
    AttendanceSettingsEditView,
)
app_name = 'attendance'
urlpatterns = [
    path('admin_attendance/',AdminAttendanceView.as_view(), name='admin_attendance'),
    path('employee_attendance/',EmployeeAttendanceView.as_view(), name='employee_attendance'),
    path('mark-attendance/', MarkAttendanceView.as_view(), name='mark_attendance'),
    path('attendance_settings/', AttendanceSettingsView.as_view(), name='attendance_settings'),
    path('attendance_settings/edit/', AttendanceSettingsEditView.as_view(), name='attendance_settings_edit'),
]

