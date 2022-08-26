from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('backend.core.urls')),
    path('crm/', include('backend.crm.urls')),
    path('sale/', include('backend.sale.urls')),
    path('admin/', admin.site.urls),
]
