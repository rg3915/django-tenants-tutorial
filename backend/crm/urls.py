from django.urls import include, path
from rest_framework import routers

from backend.crm import views as v
from backend.crm.api.viewsets import CustomerViewSet

app_name = 'crm'

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('customer/', v.customer_list, name='customer_list'),
    path('employee/', v.employee_list, name='employee_list'),
    path('employee/create/', v.employee_create, name='employee_create'),
    path('api/', include(router.urls)),
]
