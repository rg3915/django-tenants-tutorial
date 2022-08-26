from django.urls import path

from backend.product import views as v

app_name = 'product'


urlpatterns = [
    path('', v.product_type_list, name='product_type_list'),
]
