from functools import lru_cache
import punq

from core.apps.budgets.services.budgets import (
    BaseCurrencyService, ORMCurrencyService, BaseBudgetService, ORMBudgetService
)
from core.apps.budgets.services.operations import (
    BaseCategoryService, ORMCategoryService, BaseOperationService, ORMOperationService
)
from core.apps.customers.services.auth import BaseAuthService, AuthService
from core.apps.customers.services.codes import BaseCodeService, DjangoCacheCodeService
from core.apps.customers.services.customers import BaseCustomerService, ORMCustomerService
from core.apps.customers.services.senders import (
    BaseSenderService, DummySenderService, SMSVonageSenderService
)


@lru_cache(maxsize=1)
def get_ioc_container() -> punq.Container:
    return _initialize_ioc_container()


def _initialize_ioc_container() -> punq.Container:
    ioc_container = punq.Container()

    ioc_container.register(BaseCurrencyService, ORMCurrencyService)
    ioc_container.register(BaseBudgetService, ORMBudgetService)

    ioc_container.register(BaseCategoryService, ORMCategoryService)
    ioc_container.register(BaseOperationService, ORMOperationService)

    ioc_container.register(BaseCustomerService, ORMCustomerService)
    ioc_container.register(BaseCodeService, DjangoCacheCodeService)
    ioc_container.register(BaseSenderService, SMSVonageSenderService)
    ioc_container.register(BaseAuthService, AuthService)

    return ioc_container
