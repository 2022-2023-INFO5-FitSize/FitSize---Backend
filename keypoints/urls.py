from django.urls import path

from . import views

urlpatterns = [
    path('execScript/', views.exec_script, name='exec_script'),
    path('taskStatus/<str:task_id>/', views.task_status, name='task_status'),
]
