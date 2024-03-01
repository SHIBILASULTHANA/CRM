from django.shortcuts import  render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import DepartmentForm,EmployeeForm,ClientForm
from .models import Department,Employee,Client
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,TemplateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
User = get_user_model() 

# Create your views here.

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.is_superuser:
            return redirect('web:admin_dashboard')
        elif user.usertype == 'Employee':
            return redirect('web:employee_dashboard')
        elif user.usertype == 'Client':
            return redirect('web:client_dashboard')
        # Handle case if user is not authenticated or doesn't have appropriate usertype
        return super().form_valid(form)
    
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'web/admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve necessary data
        total_clients = Client.objects.count()
        total_employees = Employee.objects.count()
        departments = Department.objects.all()

        context.update({
            'total_clients': total_clients,
            'total_employees': total_employees,
            'departments': departments,
        })

        return context

class EmployeeDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'web/employee/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.request.user.employee
        return context
    
class ClientDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'web/client/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.request.user.client 
        return context

class DepartmentListView(View):
    model = Department
    template_name = 'web/admin/department.html'  # Using the same template for listing and adding departments

    def get(self, request):
        form = DepartmentForm()  # Creating an instance of the DepartmentForm
        departments = self.model.objects.all()
        return render(request, self.template_name, {'departments': departments, 'form': form})  # Passing form to the template

    def post(self, request):
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('web:department_list')  # Redirect to the same page after successful form submission
        departments = self.model.objects.all()
        return render(request, self.template_name, {'departments': departments, 'form': form})  # Passing form to the template

class EmployeeListView(ListView):
    model = Employee
    template_name = 'web/admin/employee_list.html'
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_employees'] = self.model.objects.count()
        return context

class AddEmployeeView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'web/admin/add_employee.html'
    success_url = reverse_lazy('web:employee_list')

    def form_valid(self, form):
        employee = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user = User.objects.create_user(username=employee.email, email=employee.email, password=password, is_staff=True, usertype="Employee")
        employee.user = user
        employee.save()
        messages.success(self.request, f"Employee '{employee.name}' added successfully.")
        return super().form_valid(form)
    
class EditEmployeeView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'web/admin/add_employee.html'
    success_url = reverse_lazy('employee_list')

class DeleteEmployeeView(DeleteView):
    model = Employee
    success_url = reverse_lazy('web:employee_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class ClientListView(ListView):
    model = Client
    template_name = 'web/admin/client_list.html'
    context_object_name = 'clients'

class AddClientView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'web/admin/add_client.html'
    success_url = reverse_lazy('web:client_list')

    def form_valid(self, form):
        client = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user = User.objects.create_user(username=client.email, email=client.email, password=password, usertype="Client")
        client.user = user
        client.save()
        messages.success(self.request, f"Client '{client.client_name}' added successfully. Password: {password}")
        return super().form_valid(form)

class EditClientView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'web/admin/add_client.html'
    success_url = reverse_lazy('web:client_list')

class DeleteClientView(DeleteView):
    model = Client
    success_url = reverse_lazy('web:client_list')

