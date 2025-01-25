from ninja.security import HttpBearer

from core.apps.customers.models import Customer


class TokenAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            customer = Customer.objects.get(token=token)
            return customer.to_entity()
        except Customer.DoesNotExist:
            return None
