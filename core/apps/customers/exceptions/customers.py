from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CustomerException(ServiceException):
    @property
    def message(self):
        return 'Customer exception occurred.'


@dataclass(eq=False)
class CustomerNotFoundException(CustomerException):

    @property
    def message(self):
        return 'Customer not found.'
