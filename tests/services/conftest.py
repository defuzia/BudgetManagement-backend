import pytest
from core.api.v1.budget_management.services.budgets import BaseCurrencyService, ORMCurrencyService


@pytest.fixture()
def currency_service() -> BaseCurrencyService:
    return ORMCurrencyService()
