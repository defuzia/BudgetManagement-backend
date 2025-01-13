from datetime import datetime
from typing import Optional

from ninja import Schema

from core.apps.customers.entities.customers import Customer as CustomerEntity


class AuthInSchema(Schema):
    phone: str
    username: Optional[str] = None


class AuthOutSchema(Schema):
    message: str


class TokenInSchema(Schema):
    phone: str
    code: str


class TokenOutSchema(Schema):
    token: str


class CustomerSchema(Schema):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    phone: str
    username: str

    @staticmethod
    def from_entity(entity: CustomerEntity) -> 'CustomerSchema':
        return CustomerSchema(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            phone=entity.phone,
            username=entity.username,
        )


class UpdateCustomerSchema(Schema):
    username: Optional[str] = None
