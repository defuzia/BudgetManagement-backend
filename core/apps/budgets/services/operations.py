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
from core.apps.customers.entities.customers import Customer


class BaseCategoryService(ABC):
    @abstractmethod
    def get_category_list(
            self,
            filters: CategoryFilters,
            pagination: PaginationIn,
            related_customer: Customer
    ) -> Iterable[Category]:
        ...

    @abstractmethod
    def get_category_count(self, filters: CategoryFilters, related_customer: Customer) -> int:
        ...

    @abstractmethod
    def get_category_by_id(self, category_id: int, related_customer: Customer) -> Category:
        ...

    @abstractmethod
    def create_category(
            self,
            name: str,
            related_customer: Customer
    ) -> Category:
        ...

    @abstractmethod
    def delete_category(self, category_id: int, related_customer: Customer) -> None:
        ...

    @abstractmethod
    def update_category(
            self,
            category_id: int,
            name: Optional[str],
            related_customer: Customer
    ) -> Category:
        ...


class ORMCategoryService(BaseCategoryService):
    def _build_category_query(self, filters: CategoryFilters) -> Q:
        query = Q()

        if filters.search is not None:
            query &= Q(name__icontains=filters.search)

        return query

    def get_category_list(
            self,
            filters: CategoryFilters,
            pagination: PaginationIn,
            related_customer: Customer
    ) -> Iterable[Category]:
        query = self._build_category_query(filters)
        qs = CategoryModel.objects.filter(related_customer_id=related_customer.id).filter(query)[
             pagination.offset:pagination.offset + pagination.limit
        ]

        return [category.to_entity() for category in qs]

    def get_category_count(self, filters: CategoryFilters, related_customer: Customer) -> int:
        query = self._build_category_query(filters)

        return CategoryModel.objects.filter(related_customer_id=related_customer.id).filter(query).count()

    def get_category_by_id(self, category_id: int, related_customer: Customer) -> Category:
        return CategoryModel.objects.filter(related_customer_id=related_customer.id).get(id=category_id).to_entity()

    def create_category(
            self,
            name: str,
            related_customer: Customer
    ) -> Category:
        category = CategoryModel.objects.create(
            name=name,
            related_customer_id=related_customer.id
        )
        return category.to_entity()

    def delete_category(self, category_id: int, related_customer: Customer) -> None:
        CategoryModel.objects.filter(related_customer_id=related_customer.id).get(id=category_id).delete()

    def update_category(
            self,
            category_id: int,
            name: Optional[str],
            related_customer: Customer
    ) -> Category:
        category = CategoryModel.objects.filter(related_customer_id=related_customer.id).get(id=category_id)

        if name is not None:
            category.name = name

        category.save()
        return category.to_entity()


class BaseOperationService(ABC):
    @abstractmethod
    def get_operation_list(
            self,
            filters: OperationFilters,
            pagination: PaginationIn,
            related_customer: Customer
    ) -> Iterable[Operation]:
        ...

    @abstractmethod
    def get_operation_count(self, filters: OperationFilters, related_customer: Customer) -> int:
        ...

    @abstractmethod
    def get_operation_by_id(self, operation_id: int, related_customer: Customer) -> Operation:
        ...

    @abstractmethod
    def create_operation(
            self,
            title: Optional[str],
            operation_type: str,
            amount: Decimal,
            related_budget_id: int,
            related_category_id: int,
            related_customer: Customer
    ) -> Operation:
        ...

    @abstractmethod
    def delete_operation(self, operation_id: int, related_customer: Customer) -> None:
        ...

    @abstractmethod
    def update_operation(
            self,
            operation_id: int,
            title: Optional[str],
            operation_type: Optional[str],
            amount: Optional[Decimal],
            related_category_id: Optional[int],
            related_customer: Customer
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

    def get_operation_list(
            self,
            filters: OperationFilters,
            pagination: PaginationIn,
            related_customer: Customer
    ) -> Iterable[Operation]:
        query = self._build_operation_query(filters)
        qs = OperationModel.objects.filter(related_budget__related_customer_id=related_customer.id).filter(query)[
             pagination.offset:pagination.offset + pagination.limit
        ]

        return [operation.to_entity() for operation in qs]

    def get_operation_count(self, filters: OperationFilters, related_customer: Customer) -> int:
        query = self._build_operation_query(filters)

        return OperationModel.objects.filter(related_budget__related_customer_id=related_customer.id).filter(query).count()

    def get_operation_by_id(self, operation_id: int, related_customer: Customer) -> Operation:
        return OperationModel.objects.filter(related_budget__related_customer_id=related_customer.id).get(id=operation_id).to_entity()

    def create_operation(
            self,
            title: Optional[str],
            operation_type: str,
            amount: Decimal,
            related_budget_id: int,
            related_category_id: int,
            related_customer: Customer
    ) -> Operation:
        related_budget = BudgetModel.objects.filter(related_customer_id=related_customer.id).get(id=related_budget_id)
        related_category = CategoryModel.objects.filter(related_customer_id=related_customer.id).get(id=related_category_id)

        operation = OperationModel.objects.create(
            title=title,
            operation_type=operation_type,
            amount=amount,
            related_budget=related_budget,
            related_category=related_category
        )
        return operation.to_entity()

    def delete_operation(self, operation_id: int, related_customer: Customer) -> None:
        OperationModel.objects.filter(related_budget__related_customer_id=related_customer.id).get(id=operation_id).delete()

    def update_operation(
            self,
            operation_id: int,
            title: Optional[str],
            operation_type: Optional[str],
            amount: Optional[Decimal],
            related_category_id: Optional[int],
            related_customer: Customer
    ) -> Operation:
        operation = OperationModel.objects.filter(related_budget__related_customer_id=related_customer.id).get(id=operation_id)

        if title is not None:
            operation.title = title

        if operation_type is not None:
            operation.operation_type = operation_type

        if amount is not None:
            operation.amount = amount

        if related_category_id is not None:
            operation.related_category = CategoryModel.objects.filter(related_customer_id=related_customer.id).get(id=related_category_id)

        operation.save()
        return operation.to_entity()
