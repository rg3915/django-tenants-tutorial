# Generated by Django 4.0.7 on 2022-08-11 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='cnpj',
            field=models.CharField(
                blank=True, max_length=14, null=True, unique=True, verbose_name='CNPJ'),
        ),
    ]
