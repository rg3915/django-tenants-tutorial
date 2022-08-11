from django.contrib import admin

from backend.sale.models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'customer', 'employee', 'created')
    search_fields = ('title',)
