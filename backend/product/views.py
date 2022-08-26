from django.shortcuts import render

from .models import ProductType


def product_type_list(request):
    template_name = 'product/product_type_list.html'
    object_list = ProductType.objects.all()
    context = {'object_list': object_list}
    return render(request, template_name, context)
