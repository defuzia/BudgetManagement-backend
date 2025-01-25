from abc import ABC, abstractmethod

from core.apps.customers.entities.customers import Customer as CustomerEntity


class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        ...


class DummySenderService(BaseSenderService):
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        print(f'Code {code} sent to +{customer.phone}')


class SMSVonageSenderService(BaseSenderService):
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        from vonage_messages.models import Sms
        from vonage import Auth, Vonage

        client = Vonage(
            Auth(
                api_key="130bf108",
                api_secret="Kz0JSAHUKvlQnLqN",
            )
        )
        response = client.messages.send(
            Sms(
                to=customer.phone,
                from_='BudgetManagement team',
                text=f'Here\'s your BudgetManagement verification code: {code}',
            )
        )