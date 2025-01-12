from django.contrib import admin

from core.apps.budgets.models import Currency, Budget, Category, Operation


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'symbol', 'name',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'initial_amount', 'related_currency', 'related_customer',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'related_customer',)


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'operation_type', 'amount', 'title', 'related_budget', 'related_category',)
