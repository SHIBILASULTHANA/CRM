from django.db import models
from web.models import Employee


class ClockRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) 
    date = models.DateField()
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    action = models.CharField(max_length=10)

    def calculate_late_attendance(self):
        late_time_threshold = AttendanceSettings.objects.first().late_time
        if self.clock_in and self.clock_in > late_time_threshold:
            return 'Late'
        else:
            return 'Punctual'

    @property
    def late_attendance(self):
        return self.calculate_late_attendance()

    def __str__(self):
        return str(self.date)
    
class AttendanceSettings(models.Model):
    # Define TimeField with default values in 12-hour format with AM/PM
    office_time = models.TimeField(default='09:30')  
    late_time = models.TimeField(default='09:40')  
    end_time = models.TimeField(default='18:00')    

    def __str__(self):
        return "Attendance Settings"

class AttendanceRecord(models.Model):
    clock_record = models.OneToOneField(ClockRecord, on_delete=models.CASCADE)
    settings = models.ForeignKey(AttendanceSettings, on_delete=models.CASCADE)
    late_attendance = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        late_time_threshold = self.settings.late_time
        if self.clock_record.action == 'clock_in' and self.clock_record.clock_in > late_time_threshold:
            self.late_attendance = 'Late'
        else:
            self.late_attendance = 'Punctual'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Attendance Record for {self.clock_record.date}"