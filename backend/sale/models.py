from django.db import models

from backend.crm.models import Customer, Employee


class Sale(models.Model):
    title = models.CharField('título', max_length=30)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        verbose_name='cliente',
        related_name='customer_sales',
        null=True,
        blank=True
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        verbose_name='vendedor',
        related_name='employees_sales',
        null=True,
        blank=True
    )
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now_add=False,
        auto_now=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'

    def __str__(self):
        return f'{self.title}'
