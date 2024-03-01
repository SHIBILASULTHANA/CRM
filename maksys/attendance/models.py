from django.db import models
from web.models import Employee,Department
 

# Create your models here.
class ClockRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) 
    date = models.DateField()
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    action = models.CharField(max_length=10)

class AttendanceSettings(models.Model):
    # Define TimeField with default values in 12-hour format with AM/PM
    office_time = models.TimeField(default='09:30')  
    late_time = models.TimeField(default='09:40')  
    end_time = models.TimeField(default='18:00')    

    def __str__(self):
        return "Attendance Settings"