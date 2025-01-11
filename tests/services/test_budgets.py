import pytest

from core.api.filters import PaginationIn
from core.api.v1.budget_management.filters import CurrencyFilters
from core.api.v1.budget_management.services.budgets import BaseCurrencyService
from tests.factories.budgets import CurrencyModelFactory


@pytest.mark.django_db
def test_get_currencies_count_zero(currency_service: BaseCurrencyService):
    """
    Test currency count zero with no currencies in DB.
    :param currency_service:
    :return:
    """

    currency_count = currency_service.get_currency_count(CurrencyFilters())
    assert currency_count == 0, f'{currency_count=}'


@pytest.mark.django_db
def test_get_currencies_count_exist(currency_service: BaseCurrencyService):
    """
    Test currency count with expected currencies in DB.
    :param currency_service:
    :return:
    """

    expected_count = 5
    CurrencyModelFactory.create_batch(size=expected_count)

    currency_count = currency_service.get_currency_count(CurrencyFilters())
    assert currency_count == expected_count, f'{currency_count=}'


@pytest.mark.django_db
def test_get_currencies_all(currency_service: BaseCurrencyService):
    """
    Test all currency attributes with expected count and all currency attributes with generated currency attributes.
    :param currency_service:
    :return:
    """
    expected_count = 5
    currencies = CurrencyModelFactory.create_batch(size=expected_count)
    currency_names = {currency.name for currency in currencies}
    currency_short_names = {currency.short_name for currency in currencies}
    currency_symbols = {currency.symbol for currency in currencies}

    fetched_currencies = currency_service.get_currency_list(CurrencyFilters(), PaginationIn())
    fetched_names = {currency.name for currency in fetched_currencies}
    fetched_short_names = {currency.short_name for currency in fetched_currencies}
    fetched_symbols = {currency.symbol for currency in fetched_currencies}

    assert len(fetched_names) == expected_count, f'Fetched names: {fetched_names=}'
    assert len(fetched_short_names) == expected_count, f'Fetched short_names: {fetched_short_names=}'
    assert len(fetched_symbols) == expected_count, f'Fetched symbols: {fetched_symbols=}'

    assert currency_names == fetched_names, f'Generated names: {currency_names=}\nFetched names: {fetched_names=}'
    assert currency_short_names == fetched_short_names, f'Generated short_names: {currency_short_names=}\nFetched short_names: {fetched_short_names=}'
    assert currency_symbols == fetched_symbols, f'Generated symbols: {currency_symbols=}\nFetched symbols: {fetched_symbols=}'
