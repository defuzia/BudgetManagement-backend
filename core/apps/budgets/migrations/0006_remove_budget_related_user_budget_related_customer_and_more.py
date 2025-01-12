# Generated by Django 5.1.4 on 2025-01-11 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0005_rename_amount_budget_initial_amount_and_more'),
        ('customers', '0002_customer_username_alter_customer_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='related_user',
        ),
        migrations.AddField(
            model_name='budget',
            name='related_customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='customers.customer', verbose_name='Related customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='related_customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='customers.customer', verbose_name='Related user id'),
            preserve_default=False,
        ),
    ]