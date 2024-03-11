from django.contrib import admin
from .models import ClockRecord,AttendanceRecord
# Register your models here.
admin.site.register(ClockRecord)
admin.site.register(AttendanceRecord)