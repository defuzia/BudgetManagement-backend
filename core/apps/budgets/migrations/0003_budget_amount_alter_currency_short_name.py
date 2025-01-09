# Generated by Django 5.1.4 on 2025-01-08 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_category_budget_operation'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=11, verbose_name='Budget amount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currency',
            name='short_name',
            field=models.CharField(max_length=64, unique=True, verbose_name='Currency short name'),
        ),
    ]