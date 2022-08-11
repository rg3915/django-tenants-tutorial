from django.urls import path

from backend.sale import views as v

app_name = 'sale'


urlpatterns = [
    path('', v.sale_list, name='sale_list'),
]
