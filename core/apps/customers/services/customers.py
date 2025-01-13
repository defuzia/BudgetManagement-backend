from abc import ABC, abstractmethod
from uuid import uuid4

from core.apps.customers.entities.customers import Customer as CustomerEntity
from core.apps.customers.models import Customer as CustomerModel


class BaseCustomerService(ABC):
    @abstractmethod
    def get(self, phone: str) -> CustomerEntity:
        ...

    @abstractmethod
    def get_or_create(self, phone: str, username: str) -> CustomerEntity:
        ...

    @abstractmethod
    def generate_token(self, customer: CustomerEntity) -> str:
        ...


class ORMCustomerService(BaseCustomerService):
    def get(self, phone: str) -> CustomerEntity:
        try:
            customer_dto = CustomerModel.objects.get(phone=phone)
        except CustomerModel.DoesNotExist:
            raise

        return customer_dto.to_entity()

    def get_or_create(self, phone: str, username: str) -> CustomerEntity:
        customer_dto, _ = CustomerModel.objects.get_or_create(phone=phone, defaults={'username': username})

        return customer_dto.to_entity()

    def generate_token(self, customer: CustomerEntity) -> str:
        generated_token = str(uuid4())
        CustomerModel.objects.filter(phone=customer.phone).update(
            token=generated_token
        )
        return generated_token

    def update_username(self, username: str, customer: CustomerEntity) -> CustomerEntity:
        customer = CustomerModel.objects.get(id=customer.id)

        customer.username = username
        customer.save()

        return customer.to_entity()

