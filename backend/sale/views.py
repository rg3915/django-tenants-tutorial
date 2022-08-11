from django.shortcuts import render

from .models import Sale


def sale_list(request):
    template_name = 'sale/sale_list.html'
    object_list = Sale.objects.all()
    context = {'object_list': object_list}
    return render(request, template_name, context)
