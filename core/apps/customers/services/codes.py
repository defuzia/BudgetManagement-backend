from random import randint
from abc import ABC, abstractmethod

from django.core.cache import cache

from core.apps.customers.entities.customers import Customer as CustomerEntity
from core.apps.customers.exceptions.codes import CodeNotFoundException, CodesNotEqualException


class BaseCodeService(ABC):
    @abstractmethod
    def generate_code(self, customer: CustomerEntity) -> str:
        ...

    @abstractmethod
    def validate_code(self, code: str, customer: CustomerEntity) -> None:
        ...


class DjangoCacheCodeService(BaseCodeService):
    def generate_code(self, customer: CustomerEntity) -> str:
        code_length = 6
        code = ''.join([f'{randint(0, 9)}' for _ in range(code_length)])
        cache.set(customer.phone, code)

        return code

    def validate_code(self, code: str, customer: CustomerEntity) -> None:
        cached_code = cache.get(customer.phone)

        if cached_code is None:
            raise CodeNotFoundException(code=code)

        if cached_code != code:
            raise CodesNotEqualException(code=code, cached_code=cached_code)

        cache.delete(customer.phone)
