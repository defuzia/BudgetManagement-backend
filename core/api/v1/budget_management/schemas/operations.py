from datetime import datetime
from decimal import Decimal
from typing import Optional

from ninja import Schema

from core.apps.budgets.entities.budgets import Budget as BudgetEntity
from core.apps.budgets.entities.operations import Category as CategoryEntity, Operation as OperationEntity
from core.apps.customers.entities.customers import Customer as CustomerEntity


class CreateCategorySchema(Schema):
    name: str


class CategorySchema(Schema):
    id: int
    name: str
    related_customer: CustomerEntity

    @staticmethod
    def from_entity(entity: CategoryEntity) -> 'CategorySchema':
        return CategorySchema(
            id=entity.id,
            name=entity.name,
            related_customer=entity.related_customer,
        )


class UpdateCategorySchema(Schema):
    name: Optional[str] = None


class DeleteCategorySchema(Schema):
    message: str


class CreateOperationSchema(Schema):
    title: Optional[str]
    operation_type: str
    amount: Decimal
    related_category_id: Optional[int] = None
    related_budget_id: int


class OperationSchema(Schema):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    title: Optional[str]
    operation_type: str
    amount: Decimal
    related_budget: BudgetEntity
    related_category: Optional[CategoryEntity] = None

    @staticmethod
    def from_entity(entity: OperationEntity) -> 'OperationSchema':
        return OperationSchema(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            operation_type=entity.operation_type,
            amount=entity.amount,
            title=entity.title,
            related_budget=entity.related_budget,
            related_category=entity.related_category,
        )


class UpdateOperationSchema(Schema):
    title: Optional[str] = None
    operation_type: Optional[str] = None
    amount: Optional[Decimal] = None
    related_category_id: Optional[int] = None


class DeleteOperationSchema(Schema):
    message: str
