from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class Currency:
    id: int
    name: str
    short_name: str
    symbol: str


@dataclass
class Budget:
    id: int
    created_at: datetime
    updated_at: datetime
    title: str
    amount: Decimal
    related_currency: Currency
    related_user: UUID

