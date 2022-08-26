from django.shortcuts import render

from backend.crm.models import Customer, Employee
from backend.product.models import ProductType
from backend.sale.models import Sale


def index(request):
    template_name = 'index.html'
    customers = Customer.objects.all()
    employees = Employee.objects.all()
    sales = Sale.objects.all()
    product_types = ProductType.objects.all()
    context = {
        'customers': customers,
        'employees': employees,
        'sales': sales,
        'product_types': product_types,
    }
    return render(request, template_name, context)
