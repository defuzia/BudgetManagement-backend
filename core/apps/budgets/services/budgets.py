from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Iterable, Optional
from uuid import UUID

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.budget_management.filters import CurrencyFilters, BudgetFilters
from core.apps.budgets.entities.budgets import Currency, Budget


from core.apps.budgets.models.budgets import (
    Currency as CurrencyModel,
    Budget as BudgetModel,
)


class BaseCurrencyService(ABC):
    @abstractmethod
    def get_currency_list(self, filters: CurrencyFilters, pagination: PaginationIn) -> Iterable[Currency]:
        ...

    @abstractmethod
    def get_currency_count(self, filters: CurrencyFilters) -> int:
        ...

    @abstractmethod
    def get_currency_by_short_name(self, short_name: str) -> Currency:
        ...


class ORMCurrencyService(BaseCurrencyService):
    def _build_currency_query(self, filters: CurrencyFilters) -> Q:
        query = Q()

        if filters.search is not None:
            query &= Q(name__icontains=filters.search) | Q(short_name__iexact=filters.search)

        return query

    def get_currency_list(self, filters: CurrencyFilters, pagination: PaginationIn) -> Iterable[Currency]:
        query = self._build_currency_query(filters)
        qs = CurrencyModel.objects.filter(query)[pagination.offset:pagination.offset + pagination.limit]

        return [currency.to_entity() for currency in qs]

    def get_currency_count(self, filters: CurrencyFilters) -> int:
        query = self._build_currency_query(filters)

        return CurrencyModel.objects.filter(query).count()

    def get_currency_by_short_name(self, short_name: str) -> Currency:
        return CurrencyModel.objects.get(short_name__iexact=short_name).to_entity()


class BaseBudgetService(ABC):
    @abstractmethod
    def get_budget_list(self, filters: BudgetFilters, pagination: PaginationIn) -> Iterable[Budget]:
        ...

    @abstractmethod
    def get_budget_count(self, filters: BudgetFilters) -> int:
        ...

    @abstractmethod
    def get_budget_by_id(self, budget_id: int) -> Budget:
        ...

    @abstractmethod
    def create_budget(
        self,
        title: str,
        initial_amount: Optional[Decimal],
        related_currency_short_name: Optional[str],
        related_user: UUID
    ) -> Budget:
        ...

    @abstractmethod
    def delete_budget(self, budget_id: int) -> None:
        ...

    @abstractmethod
    def update_budget(
        self,
        budget_id: int,
        title: Optional[str],
        initial_amount: Optional[Decimal]
    ) -> Budget:
        ...


class ORMBudgetService(BaseBudgetService):
    def _build_budget_query(self, filters: BudgetFilters) -> Q:
        query = Q()

        if filters.search is not None:
            query &= Q(title__icontains=filters.search)

        return query

    def get_budget_list(self, filters: BudgetFilters, pagination: PaginationIn) -> Iterable[Budget]:
        query = self._build_budget_query(filters)
        qs = BudgetModel.objects.filter(query)[pagination.offset:pagination.offset + pagination.limit]

        return [budget.to_entity() for budget in qs]

    def get_budget_count(self, filters: BudgetFilters) -> int:
        query = self._build_budget_query(filters)

        return BudgetModel.objects.filter(query).count()

    def get_budget_by_id(self, budget_id: int) -> Budget:
        return BudgetModel.objects.get(id=budget_id).to_entity()

    def create_budget(
            self,
            title: str,
            initial_amount: Optional[Decimal],
            related_currency_short_name: Optional[str],
            related_user: UUID
    ) -> Budget:
        if related_currency_short_name:
            related_currency = CurrencyModel.objects.get(short_name=related_currency_short_name)
        else:
            related_currency = CurrencyModel.objects.get(short_name='USD')

        budget = BudgetModel.objects.create(
            title=title,
            initial_amount=initial_amount,
            related_currency=related_currency,
            related_user=related_user
        )
        return budget.to_entity()

    def delete_budget(self, budget_id: int) -> None:
        BudgetModel.objects.get(id=budget_id).delete()

    def update_budget(
            self,
            budget_id: int,
            title: Optional[str],
            initial_amount: Optional[Decimal]
    ) -> Budget:
        budget = BudgetModel.objects.get(id=budget_id)

        if title is not None:
            budget.title = title

        if initial_amount is not None:
            budget.initial_amount = initial_amount

        budget.save()
        return budget.to_entity()
