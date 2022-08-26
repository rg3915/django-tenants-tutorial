from django.contrib import admin

from .models import ProductType


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('title',)
