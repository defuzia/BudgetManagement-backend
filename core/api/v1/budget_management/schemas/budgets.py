from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from ninja import Schema

from core.apps.budgets.entities.budgets import Currency as CurrencyEntity, Budget as BudgetEntity


class CurrencySchema(Schema):
    id: int
    name: str
    short_name: str
    symbol: str

    @staticmethod
    def from_entity(entity: CurrencyEntity) -> 'CurrencySchema':
        return CurrencySchema(
            id=entity.id,
            name=entity.name,
            short_name=entity.short_name,
            symbol=entity.symbol
        )


class CreateBudgetSchema(Schema):
    title: str
    initial_amount: Optional[Decimal]
    related_currency_short_name: Optional[str]
    related_user: UUID


class BudgetSchema(Schema):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    title: str
    initial_amount: Decimal
    related_currency: CurrencyEntity
    related_user: UUID

    @staticmethod
    def from_entity(entity: BudgetEntity) -> 'BudgetSchema':
        return BudgetSchema(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            title=entity.title,
            initial_amount=entity.initial_amount,
            related_currency=entity.related_currency,
            related_user=entity.related_user
        )


class UpdateBudgetSchema(Schema):
    title: Optional[str] = None
    initial_amount: Optional[Decimal] = None


class DeleteBudgetSchema(Schema):
    message: str
