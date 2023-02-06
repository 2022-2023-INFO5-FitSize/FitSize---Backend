from django.urls import path

from . import views

urlpatterns = [
    path('execScript/', views.exec_script, name='exec_script'),
]
