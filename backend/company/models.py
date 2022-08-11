from django.db import models

from backend.tenant.models import Client


class Company(models.Model):
    name = models.CharField('nome', max_length=100, unique=True)
    cnpj = models.CharField('CNPJ', max_length=14, unique=True, null=True, blank=True)
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        verbose_name='cliente',
        related_name='companies',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'

    def __str__(self):
        return f'{self.name}'
