from abc import ABC, abstractmethod

from core.apps.customers.entities.customers import Customer as CustomerEntity


class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        ...


class DummySenderService(BaseSenderService):
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        print(f'Code {code} sent to +{customer.phone}')
