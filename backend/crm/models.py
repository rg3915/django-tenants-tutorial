from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    occupation = models.CharField('cargo', max_length=100, unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='usuário',
        related_name='employees',
    )

    class Meta:
        ordering = ('user__first_name',)
        verbose_name = 'funcionário'
        verbose_name_plural = 'funcionários'

    def __str__(self):
        return f'{self.user.get_full_name()}'