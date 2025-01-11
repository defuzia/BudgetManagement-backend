from ninja import Router
from core.api.v1.budget_management.handlers import router as budget_management_router
from core.api.v1.customers.handlers import router as customers_router

router = Router(tags=['v1'])

router.add_router('management/', budget_management_router)
router.add_router('customers/', customers_router)
