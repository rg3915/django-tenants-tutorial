from django.shortcuts import render

from backend.crm.models import Customer, Employee
from backend.sale.models import Sale


def index(request):
    template_name = 'index.html'
    customers = Customer.objects.all()
    employees = Employee.objects.all()
    sales = Sale.objects.all()
    context = {
        'customers': customers,
        'employees': employees,
        'sales': sales,
    }
    return render(request, template_name, context)
