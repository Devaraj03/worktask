from django.urls import path
from .views import *

urlpatterns = [
    path('', KanbanView.as_view(), name='kanban'),
    path('create/', WorkCreateView.as_view(), name='work_create'),
    path('update/<int:pk>/', WorkUpdateView.as_view(), name='work_update'),
    path('delete/<int:pk>/', WorkDeleteView.as_view(), name='work_delete'),

    path("update-status/", update_status, name="update_status"),

]
