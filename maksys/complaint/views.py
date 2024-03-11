from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView,FormView
from django.urls import reverse_lazy
from .models import Complaint
from .forms import ComplaintForm,AssignComplaintForm
from web.models import Employee

# Create your views here.
class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    context_object_name = 'complaints'

    def get_template_names(self):
        if self.request.user.is_superuser:
            # Use the admin template for staff users
            return ['web/admin/complaint.html']
        else:
            # Use the client template for non-staff users
            return ['web/client/complaint_list.html']
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            # Add employees to the context for superuser
            context['employees'] = Employee.objects.all()
        return context

class ComplaintCreateView(CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'web/client/complaint_register.html'
    success_url = reverse_lazy('complaint:complaint_list')

class AssignComplaintView(FormView):
    template_name = 'web/admin/complaint.html'
    form_class = AssignComplaintForm
    success_url = reverse_lazy('complaint:complaint_list')

    def form_valid(self, form):
        complaint_id = self.kwargs['complaint_id']
        employee = form.cleaned_data['employee']
        remarks = form.cleaned_data['remarks']
        
        # Update the complaint with assigned employee and remarks
        complaint = Complaint.objects.get(complaint_id=complaint_id)
        complaint.employee = employee
        complaint.remarks = remarks
        complaint.save()
        
        return super().form_valid(form)