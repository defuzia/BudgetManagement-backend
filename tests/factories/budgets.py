from factory.django import DjangoModelFactory
import factory

from core.apps.budgets.models import Currency


class CurrencyModelFactory(DjangoModelFactory):
    name = factory.Faker('currency_name')
    short_name = factory.Faker('currency_code')
    symbol = factory.Faker('currency_symbol')

    class Meta:
        model = Currency

