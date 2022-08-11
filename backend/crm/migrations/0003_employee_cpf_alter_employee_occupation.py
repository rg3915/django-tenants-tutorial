# Generated by Django 4.0.7 on 2022-08-11 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='cpf',
            field=models.CharField(
                blank=True, max_length=11, null=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='occupation',
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name='cargo'),
        ),
    ]
