from rest_framework import viewsets

from backend.crm.api.serializers import CustomerSerializer
from backend.crm.models import Customer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
