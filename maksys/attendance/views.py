import pytz
from calendar import monthrange
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View,FormView,UpdateView
from web.models import Department, Employee
from .models import ClockRecord,AttendanceSettings,AttendanceRecord
import calendar,datetime
from django.utils import timezone 
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import AttendanceSettingsForm
import calendar

class AdminAttendanceView(TemplateView):
    template_name = 'web/admin/attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve selected department, employee, month, and year from the request
        selected_department_id = self.request.GET.get('department')
        selected_employee_id = self.request.GET.get('employee')
        selected_month = self.request.GET.get('month')
        selected_year = self.request.GET.get('year')
        
        # Default to current month and year if not provided
        current_date = datetime.now()
        selected_month = int(selected_month) if selected_month else current_date.month
        selected_year = int(selected_year) if selected_year else current_date.year

        # Filter employees based on the selected department
        if selected_department_id:
            selected_department = Department.objects.filter(id=selected_department_id).first()
            if selected_department:
                employees = selected_department.employee_set.all()
            else:
                employees = []
        else:
            # If no department is selected, show all employees
            employees = Employee.objects.all()

        # Fetch attendance data based on selected month and year
        attendance_data = self.get_attendance_data(employees, selected_month, selected_year)

        # Calculate days of the selected month
        days_in_month = monthrange(selected_year, selected_month)[1]

        # Populate context with necessary data
        context['departments'] = Department.objects.all()
        context['employees'] = employees
        context['attendance_data'] = attendance_data
        context['months'] = [(str(month), calendar.month_name[month]) for month in range(1, 13)]
        indian_tz = pytz.timezone('Asia/Kolkata')
        current_year = current_date.year
        context['years'] = range(2010, current_year + 1)
        context['selected_department_id'] = selected_department_id
        context['selected_employee_id'] = selected_employee_id
        context['selected_month'] = selected_month
        context['selected_year'] = selected_year
        context['days_of_month'] = range(1, days_in_month + 1)

        return context

    def get_attendance_data(self, employees, selected_month, selected_year):
        # Dictionary to store attendance records for each employee
        attendance_data = {}
        for employee in employees:
            # Fetch past and future attendance for each employee
            past_attendance, future_attendance, late_attendance = self.get_employee_attendance(employee, selected_month, selected_year)
            
            # Store attendance data in the dictionary using employee ID as key
            attendance_data[employee.id] = {
                'name': employee.name,
                'past_attendance': past_attendance,
                'future_attendance': future_attendance,
                'late_attendance': late_attendance
            }

        return attendance_data

    def get_employee_attendance(self, employee, selected_month, selected_year):
        # Get the number of days in the selected month and year
        days_in_month = calendar.monthrange(selected_year, selected_month)[1]

        past_attendance = []
        future_attendance = []
        late_attendance = []  # Initialize list for late attendance status

        for i in range(1, days_in_month + 1):
            day = datetime(selected_year, selected_month, i).date()
            if day <= timezone.now().date():
                if ClockRecord.objects.filter(employee=employee, date=day).exists():
                    past_attendance.append('✅')
                    if ClockRecord.objects.filter(employee=employee, date=day, action='clock_in').exists():
                        late_time_threshold = AttendanceSettings.objects.first().late_time
                        clock_in_time = ClockRecord.objects.get(employee=employee, date=day, action='clock_in').clock_in
                        if clock_in_time > late_time_threshold:
                            late_attendance.append('Late')
                        else:
                            late_attendance.append('')
                else:
                    past_attendance.append('❌')
                    
            else:
                future_attendance.append('0')

        return past_attendance, future_attendance, late_attendance  # Return three values




    
class EmployeeAttendanceView(TemplateView):
    template_name = 'web/employee/attendance.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_in_employee = self.request.user.employee
        context['logged_in_employee_name'] = logged_in_employee.name
        context['logged_in_employee_department'] = logged_in_employee.department.name
        
        indian_tz = pytz.timezone('Asia/Kolkata')       
        current_time = datetime.now(indian_tz)
        
        context['current_date'] = current_time.strftime("%Y-%m-%d")
        context['current_time'] = current_time.strftime("%H:%M:%S")
        context['departments'] = Department.objects.all()
        
        selected_department_id = self.request.GET.get('department')
        if selected_department_id:
            selected_department = Department.objects.get(pk=selected_department_id)
            employees = Employee.objects.filter(department=selected_department)
        else:
            employees = Employee.objects.all()
        
        context['employees'] = employees 
        context['months'] = [(str(month), calendar.month_name[month]) for month in range(1, 13)]
        
        current_year = current_time.year
        context['years'] = range(2010, current_year + 1)

        # Get the number of days for each month
        days_in_month = [31, 29 if calendar.isleap(current_year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # Get the selected month and year
        month = int(self.request.GET.get('month', current_time.month))
        year = int(self.request.GET.get('year', current_time.year))
        
        days_of_month = days_in_month[month - 1]
        
        days_list = [str(day) if day <= days_of_month else '0' for day in range(1, days_of_month + 1)]
        
        # Calculate past and future attendance based on the current date
        past_attendance = []
        future_attendance = []
        for i in range(1, days_of_month + 1):
            day = datetime(year, month, i).date()
            if day <= current_time.date():
                # Check if there's an attendance record for this day
                # If yes, mark as present, else mark as absent
                if ClockRecord.objects.filter(employee=logged_in_employee, date=day).exists():
                    past_attendance.append('✅')
                else:
                    past_attendance.append('❌')
            else:
                # For future days, mark as '0'
                future_attendance.append('0')
        
        context['days_of_month'] = days_list
        context['past_attendance'] = past_attendance
        context['future_attendance'] = future_attendance

        return context
    
class MarkAttendanceView(LoginRequiredMixin, View):
    template_name = 'web/employee/mark_attendance.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if request.user.usertype == 'Employee':
            today = timezone.localdate()
            try:
                latest_record = ClockRecord.objects.filter(employee=request.user.employee, date=today).latest('id')
                clocked_in = not latest_record.clock_out
            except ClockRecord.DoesNotExist:
                latest_record = None
                clocked_in = False
            all_records = ClockRecord.objects.filter(employee=request.user.employee).order_by('-date', '-id')
            return render(request, self.template_name, {'latest_record': latest_record, 'all_records': all_records, 'clocked_in': clocked_in})
        else:
            return redirect('some_other_page')

    def post(self, request, *args, **kwargs):
        indian_tz = pytz.timezone('Asia/Kolkata')
        current_time = timezone.now().astimezone(indian_tz)
        
        if request.user.usertype == 'Employee':
            action = request.POST.get('action')

            attendance_settings = AttendanceSettings.objects.first()
            if attendance_settings:
                office_time = attendance_settings.office_time
                late_time = attendance_settings.late_time
                end_time = attendance_settings.end_time
                
                if office_time <= current_time.time() <= end_time:
                    if action == 'clock_in':
                        is_late = current_time.time() > late_time
                    else:
                        is_late = False
                    
                    clock_record, created = ClockRecord.objects.get_or_create(
                        employee=request.user.employee,
                        date=current_time.date(),
                        defaults={'clock_in': current_time} if action == 'clock_in' else {'clock_out': current_time}
                    )
                    
                    if not created and action == 'clock_out' and not clock_record.clock_out:
                        clock_record.clock_out = current_time
                        clock_record.save()
                    
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        # Fetch updated records
                        updated_records = ClockRecord.objects.filter(employee=request.user.employee).order_by('-date', '-id')
                        # Serialize records with late attendance status
                        serialized_records = []
                        for record in updated_records:
                            late_attendance = 'Punctual'
                            if action == 'clock_in' and record.clock_in and record.clock_in > attendance_settings.late_time:
                                late_attendance = 'Late'
                            
                            serialized_record = {
                                'date': record.date,
                                'clock_in': record.clock_in,
                                'clock_out': record.clock_out,
                                'late_attendance': late_attendance
                            }
                            serialized_records.append(serialized_record)
                        
                        return JsonResponse({'success': True, 'records': serialized_records})

                else:
                    # Handle case where current time is outside office hours
                    pass
            else:
                # Handle case where attendance settings are not available
                pass
        
        # Redirect to some other page if not an Employee or if attendance settings are not available
        return redirect('some_other_page')


        
class AttendanceSettingsView(View):
    template_name = 'web/admin/settings/attendance.html'
    success_url = reverse_lazy('web:admin_dashboard')

    def get(self, request, *args, **kwargs):
        try:
            attendance_settings = AttendanceSettings.objects.first()  # Get the first object
            form = AttendanceSettingsForm(instance=attendance_settings)
        except AttendanceSettings.DoesNotExist:
            form = AttendanceSettingsForm()
        
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AttendanceSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        
        return render(request, self.template_name, {'form': form})
    
class AttendanceSettingsEditView(UpdateView):
    model = AttendanceSettings
    form_class = AttendanceSettingsForm
    template_name = 'web/admin/settings/attendance.html'
    success_url = reverse_lazy('web:admin_dashboard')

    def get_object(self):
        # Assuming there's only one AttendanceSettings object
        return AttendanceSettings.objects.first()
    
class GetAttendanceDataView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve attendance data from the database
        attendance_records = AttendanceRecord.objects.all()
        
        # Serialize the data into a format suitable for JSON response
        serialized_data = []
        for record in attendance_records:
            serialized_record = {
                'date': record.date,
                'clock_in': record.clock_in,
                'clock_out': record.clock_out,
                'late_attendance': record.late_attendance,
            }
            serialized_data.append(serialized_record)
        
        # Return the serialized data as JSON response
        return JsonResponse({'success': True, 'records': serialized_data})