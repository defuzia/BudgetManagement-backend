from ninja import Router
from core.api.v1.budget_management.handlers import router as budget_management_router

router = Router(tags=['v1'])
router.add_router('', budget_management_router)
