from django.urls import path
from .views import ActivityView,CreateBoardView, CreateCardView,CreateListView
app_name = 'activity'
urlpatterns = [
    path('activity-view/', ActivityView.as_view(), name='activity_view'),
    path('create-board/' , CreateBoardView.as_view(), name='create_board'),
    path('create-card/', CreateCardView.as_view(), name='create_card'),
    path('create-list/', CreateListView.as_view(), name='create_list'),
]
