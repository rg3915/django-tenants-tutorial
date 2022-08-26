from django.conf import settings
from django.contrib import admin
from django.urls import include, path

public_urlpatterns = [
    path('', include('backend.core.urls')),
    path('crm/', include('backend.crm.urls')),
    path('sale/', include('backend.sale.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEV:
    # Não mostra em produção, se DEV = False.
    urlpatterns += public_urlpatterns
