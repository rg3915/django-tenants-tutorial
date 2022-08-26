from django.db import models


class ProductType(models.Model):
    title = models.CharField('título', max_length=100, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'tipo de produto'
        verbose_name_plural = 'tipos de produtos'

    def __str__(self):
        return f'{self.title}'
