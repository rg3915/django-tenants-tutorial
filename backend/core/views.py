from django.shortcuts import render

from backend.crm.models import Customer, Employee
from backend.product.models import ProductType
from backend.sale.models import Sale

from django_tenants.utils import schema_context


@schema_context("public")
def product_types_all():

    return list(ProductType.objects.all().values())


def index(request):
    template_name = 'index.html'
    customers = Customer.objects.all()
    employees = Employee.objects.all()
    sales = Sale.objects.all()
    product_types = ProductType.objects.all()
    public_product_types = product_types_all()

    context = {
        'customers': customers,
        'employees': employees,
        'sales': sales,
        'product_types': product_types,
        'public_product_types': public_product_types,
    }
    return render(request, template_name, context)
