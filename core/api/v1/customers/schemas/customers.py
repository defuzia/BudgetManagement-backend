from typing import Optional

from ninja import Schema


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
