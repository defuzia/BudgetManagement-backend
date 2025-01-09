from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Iterable, Optional

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.budget_management.filters import CategoryFilters, OperationFilters
from core.apps.budgets.entities.operations import Category, Operation

from core.apps.budgets.models.operations import (
    Category as CategoryModel,
    Operation as OperationModel,
    Budget as BudgetModel,
)


class BaseCategoryService(ABC):
    @abstractmethod
    def get_category_list(self, filters: CategoryFilters, pagination: PaginationIn) -> Iterable[Category]:
        ...

    @abstractmethod
    def get_category_count(self, filters: CategoryFilters) -> int:
        ...

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> Category:
        ...


class ORMCategoryService(BaseCategoryService):
    def _build_category_query(self, filters: CategoryFilters) -> Q:
        query = Q()

        if filters.search is not None:
            query &= Q(name__icontains=filters.search)

        return query

    def get_category_list(self, filters: CategoryFilters, pagination: PaginationIn) -> Iterable[Category]:
        query = self._build_category_query(filters)
        qs = CategoryModel.objects.filter(query)[pagination.offset:pagination.offset + pagination.limit]

        return [category.to_entity() for category in qs]

    def get_category_count(self, filters: CategoryFilters) -> int:
        query = self._build_category_query(filters)

        return CategoryModel.objects.filter(query).count()

    def get_category_by_id(self, category_id: int) -> Category:
        return CategoryModel.objects.get(id=category_id).to_entity()


class BaseOperationService(ABC):
    @abstractmethod
    def get_operation_list(self, filters: OperationFilters, pagination: PaginationIn) -> Iterable[Operation]:
        ...

    @abstractmethod
    def get_operation_count(self, filters: OperationFilters) -> int:
        ...

    @abstractmethod
    def get_operation_by_id(self, operation_id: int) -> Operation:
        ...

    @abstractmethod
    def create_operation(
        self,
        title: Optional[str],
        operation_type: str,
        amount: Decimal,
        related_budget_id: int,
        related_category_id: int
    ) -> Operation:
        ...

    @abstractmethod
    def delete_operation(self, operation_id: int) -> None:
        ...

    @abstractmethod
    def update_operation(
        self,
        operation_id: int,
        title: Optional[str],
        operation_type: Optional[str],
        amount: Optional[Decimal],
        related_budget_id: Optional[int],
        related_category_id: Optional[int]
    ) -> Operation:
        ...


class ORMOperationService(BaseOperationService):
    def _build_operation_query(self, filters: OperationFilters) -> Q:
        query = Q()

        if filters.search is not None:
            query &= (
                Q(title__icontains=filters.search) | Q(operation_type__iexact=filters.search) |
                Q(related_budget__title__icontains=filters.search) | Q(related_category__name__icontains=filters.search)
            )

        return query

    def get_operation_list(self, filters: OperationFilters, pagination: PaginationIn) -> Iterable[Operation]:
        query = self._build_operation_query(filters)
        qs = OperationModel.objects.filter(query)[pagination.offset:pagination.offset + pagination.limit]

        return [operation.to_entity() for operation in qs]

    def get_operation_count(self, filters: OperationFilters) -> int:
        query = self._build_operation_query(filters)

        return OperationModel.objects.filter(query).count()

    def get_operation_by_id(self, operation_id: int) -> Operation:
        return OperationModel.objects.get(id=operation_id).to_entity()

    def create_operation(
        self,
        title: Optional[str],
        operation_type: str,
        amount: Decimal,
        related_budget_id: int,
        related_category_id: int
    ) -> Operation:
        related_budget = BudgetModel.objects.get(id=related_budget_id)
        related_category = CategoryModel.objects.get(id=related_category_id)

        operation = OperationModel.objects.create(
            title=title,
            operation_type=operation_type,
            amount=amount,
            related_budget=related_budget,
            related_category=related_category
        )
        return operation.to_entity()

    def delete_operation(self, operation_id: int) -> None:
        OperationModel.objects.get(id=operation_id).delete()

    def update_operation(
        self,
        operation_id: int,
        title: Optional[str],
        operation_type: Optional[str],
        amount: Optional[Decimal],
        related_budget_id: Optional[int],
        related_category_id: Optional[int]
    ) -> Operation:
        operation = OperationModel.objects.get(id=operation_id)

        if title is not None:
            operation.title = title

        if operation_type is not None:
            operation.operation_type = operation_type

        if amount is not None:
            operation.amount = amount

        if related_budget_id is not None:
            operation.related_budget = BudgetModel.objects.get(id=related_budget_id)

        if related_category_id is not None:
            operation.related_category = CategoryModel.objects.get(id=related_category_id)

        operation.save()
        return operation.to_entity()
