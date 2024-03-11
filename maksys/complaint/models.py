from django.db import models
from web.models import Client,Employee

# Create your models here.
class Complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    complaint_name = models.CharField(max_length=100)
    start_date = models.DateField()
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=100)
    summary = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.complaint_name