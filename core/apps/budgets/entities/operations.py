from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from core.apps.budgets.entities.budgets import Budget


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Operation:
    id: int
    created_at: datetime
    updated_at: datetime
    operation_type: str
    amount: Decimal
    title: str
    related_budget: Budget
    related_category: Category
