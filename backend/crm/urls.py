from django.urls import path

from backend.crm import views as v

app_name = 'crm'


urlpatterns = [
    path('customer/', v.customer_list, name='customer_list'),
    path('employee/', v.employee_list, name='employee_list'),
    path('employee/create/', v.employee_create, name='employee_create'),
]
