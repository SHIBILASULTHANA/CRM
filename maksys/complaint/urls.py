from django.urls import path
from .views import ComplaintListView, ComplaintCreateView,AssignComplaintView

app_name = 'complaint'

urlpatterns = [
    path('register/', ComplaintCreateView.as_view(), name='complaint_register'),
    path('assign/<int:complaint_id>/', AssignComplaintView.as_view(), name='assign_complaint'),
    path('complaints/', ComplaintListView.as_view(), name='complaint_list'),

]