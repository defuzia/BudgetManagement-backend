from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CustomerException(ServiceException):
    @property
    def message(self):
        return 'Customer exception occurred.'


@dataclass(eq=False)
class CustomerNotFoundException(CustomerException):
    code: str

    @property
    def message(self):
        return 'Code not found.'
