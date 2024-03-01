from django.urls import path
from .views import (
    CustomLoginView,
    DepartmentListView,
    AdminDashboardView,
    ClientDashboardView,
    EmployeeDashboardView,
    EmployeeListView,
    AddEmployeeView,
    EditEmployeeView,
    DeleteEmployeeView,
    ClientListView,
    AddClientView,
    EditClientView,
    DeleteClientView,
)
app_name = 'web'
urlpatterns = [
    path('', CustomLoginView.as_view(), name='custom_login'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('employee/dashboard/', EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('client/dashboard/', ClientDashboardView.as_view(), name='client_dashboard'),
    path('admin/department/', DepartmentListView.as_view(), name='department_list'),
    path('admin/employee/', EmployeeListView.as_view(), name='employee_list'),
    path('admin/add/employee/', AddEmployeeView.as_view(), name='add_employee'),
    path('admin/edit/employee/<int:pk>/', EditEmployeeView.as_view(), name='edit_employee'),
    path('admin/delete/employee/<int:pk>/', DeleteEmployeeView.as_view(), name='delete_employee'),
    path('admin/client/', ClientListView.as_view(), name='client_list'),
    path('admin/add/client/', AddClientView.as_view(), name='add_client'),
    path('admin/edit/client/<int:pk>/', EditClientView.as_view(), name='edit_client'),
    path('admin/delete/client/<int:pk>/', DeleteClientView.as_view(), name='delete_client'),
    
]

