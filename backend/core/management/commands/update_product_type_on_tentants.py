from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, tenant_context

from backend.product.models import ProductType


def update_product_type_all_tenants():
    # Transforma os dados num JSON.
    items = list(ProductType.objects.values())

    # Percorre todos os tenants.
    for tenant in get_tenant_model().objects.all():
        with tenant_context(tenant):
            # Percorre todos os itens do JSON.
            for item in items:
                # Atualiza os dados.
                ProductType.objects.get_or_create(title=item['title'])


class Command(BaseCommand):
    help = "Atualiza os dados de Tipos de Produtos em todos os tenants."

    def handle(self, *args, **options):
        update_product_type_all_tenants()
