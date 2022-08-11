from django.urls import path

from backend.crm import views as v

app_name = 'crm'


urlpatterns = [
    path('employee/create/', v.employee_create, name='employee_create'),
]
