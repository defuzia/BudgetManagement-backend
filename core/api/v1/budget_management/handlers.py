from django.http import HttpRequest
from ninja import Router, Query
from ninja.security import HttpBearer

from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse, DetailResponse, PaginationOut
from core.api.v1.budget_management.filters import CurrencyFilters, BudgetFilters, CategoryFilters, OperationFilters

from core.api.v1.budget_management.schemas.budgets import (
    CurrencySchema, BudgetSchema, CreateBudgetSchema, UpdateBudgetSchema, DeleteBudgetSchema
)
from core.api.v1.budget_management.schemas.operations import (
    CategorySchema, OperationSchema, CreateOperationSchema, UpdateOperationSchema, DeleteOperationSchema,
    CreateCategorySchema, DeleteCategorySchema, UpdateCategorySchema
)
from core.project.ioc_containers import get_ioc_container

from core.apps.budgets.services.budgets import BaseCurrencyService, BaseBudgetService
from core.apps.budgets.services.operations import BaseCategoryService, BaseOperationService
from core.apps.customers.models import Customer


class TokenAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            customer = Customer.objects.get(token=token)
            return customer.to_entity()
        except Customer.DoesNotExist:
            return None


router = Router(tags=['Budget managing'])


@router.get('currencies', response=ApiResponse[ListPaginatedResponse[CurrencySchema]], auth=TokenAuth())
def get_currency_list_handler(
        request: HttpRequest,
        filters: Query[CurrencyFilters],
        pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[CurrencySchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseCurrencyService)

    currency_list = service.get_currency_list(filters=filters, pagination=pagination_in)
    currency_count = service.get_currency_count(filters=filters)
    items = [CurrencySchema.from_entity(entity=obj) for obj in currency_list]
    pagination_out = PaginationOut(offset=pagination_in.limit, limit=pagination_in.limit, total=currency_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('currencies/{short_name}', response=ApiResponse[DetailResponse[CurrencySchema]], auth=TokenAuth())
def get_currency_handler(
        request: HttpRequest,
        short_name: str
) -> ApiResponse[DetailResponse[CurrencySchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseCurrencyService)

    currency = service.get_currency_by_short_name(short_name=short_name)
    item = CurrencySchema.from_entity(currency)

    return ApiResponse(data=DetailResponse(item=item))


@router.post('budgets', response=ApiResponse[DetailResponse[BudgetSchema]], auth=TokenAuth())
def create_budget_handler(
        request: HttpRequest,
        schema: CreateBudgetSchema
) -> ApiResponse[DetailResponse[BudgetSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseBudgetService)

    budget = service.create_budget(
        title=schema.title,
        initial_amount=schema.initial_amount,
        related_currency_short_name=schema.related_currency_short_name,
        related_customer=request.auth
    )
    item = BudgetSchema.from_entity(entity=budget)

    return ApiResponse(data=DetailResponse(item=item))


@router.get('budgets', response=ApiResponse[ListPaginatedResponse[BudgetSchema]], auth=TokenAuth())
def get_budget_list_handler(
        request: HttpRequest,
        filters: Query[BudgetFilters],
        pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[BudgetSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseBudgetService)

    budget_list = service.get_budget_list(filters=filters, pagination=pagination_in, related_customer=request.auth)
    budget_count = service.get_budget_count(filters=filters, related_customer=request.auth)
    items = [BudgetSchema.from_entity(entity=obj) for obj in budget_list]
    pagination_out = PaginationOut(offset=pagination_in.limit, limit=pagination_in.limit, total=budget_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('budgets/{budget_id}', response=ApiResponse[DetailResponse[BudgetSchema]], auth=TokenAuth())
def get_budget_handler(
        request: HttpRequest,
        budget_id: int
) -> ApiResponse[DetailResponse[BudgetSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseBudgetService)

    budget = service.get_budget_by_id(budget_id=budget_id, related_customer=request.auth)
    item = BudgetSchema.from_entity(budget)

    return ApiResponse(data=DetailResponse(item=item))


@router.put('budgets/{budget_id}', response=ApiResponse[DetailResponse[BudgetSchema]], auth=TokenAuth())
def update_budget_handler(
        request: HttpRequest,
        budget_id: int,
        schema: UpdateBudgetSchema
) -> ApiResponse[DetailResponse[BudgetSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseBudgetService)

    updated_budget = service.update_budget(
        budget_id=budget_id,
        title=schema.title,
        initial_amount=schema.initial_amount,
        related_customer=request.auth
    )
    item = BudgetSchema.from_entity(updated_budget)

    return ApiResponse(data=DetailResponse(item=item))


@router.delete('budgets/{budget_id}', response=ApiResponse[DeleteBudgetSchema], auth=TokenAuth())
def delete_budget_handler(
        request: HttpRequest,
        budget_id: int
) -> ApiResponse[DeleteBudgetSchema]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseBudgetService)

    service.delete_budget(budget_id=budget_id, related_customer=request.auth)

    return ApiResponse(data=DeleteBudgetSchema(message='Budget deleted successfully.'))


@router.post('categories', response=ApiResponse[DetailResponse[CategorySchema]], auth=TokenAuth())
def create_category_handler(
        request: HttpRequest,
        schema: CreateCategorySchema
) -> ApiResponse[DetailResponse[CategorySchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseCategoryService)

    category = service.create_category(
        name=schema.name,
        related_customer=request.auth
    )
    item = CategorySchema.from_entity(category)

    return ApiResponse(data=DetailResponse(item=item))


@router.get('categories', response=ApiResponse[ListPaginatedResponse[CategorySchema]], auth=TokenAuth())
def get_category_list_handler(
        request: HttpRequest,
        filters: Query[CategoryFilters],
        pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[CategorySchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseCategoryService)

    category_list = service.get_category_list(filters=filters, pagination=pagination_in, related_customer=request.auth)
    category_count = service.get_category_count(filters=filters, related_customer=request.auth)
    items = [CategorySchema.from_entity(entity=obj) for obj in category_list]
    pagination_out = PaginationOut(offset=pagination_in.limit, limit=pagination_in.limit, total=category_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('categories/{category_id}', response=ApiResponse[DetailResponse[CategorySchema]], auth=TokenAuth())
def get_category_handler(
        request: HttpRequest,
        category_id: int
) -> ApiResponse[DetailResponse[CategorySchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseCategoryService)

    category = service.get_category_by_id(category_id=category_id, related_customer=request.auth)
    item = CategorySchema.from_entity(category)

    return ApiResponse(data=DetailResponse(item=item))


@router.put('categories/{category_id}', response=ApiResponse[DetailResponse[CategorySchema]], auth=TokenAuth())
def update_category_handler(
        request: HttpRequest,
        category_id: int,
        schema: UpdateCategorySchema
) -> ApiResponse[DetailResponse[CategorySchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseCategoryService)

    updated_category = service.update_category(
        category_id=category_id,
        name=schema.name,
        related_customer=request.auth
    )
    item = CategorySchema.from_entity(updated_category)

    return ApiResponse(data=DetailResponse(item=item))


@router.delete('categories/{category_id}', response=ApiResponse[DeleteCategorySchema], auth=TokenAuth())
def delete_category_handler(
        request: HttpRequest,
        category_id: int
) -> ApiResponse[DeleteCategorySchema]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseCategoryService)

    service.delete_category(category_id=category_id, related_customer=request.auth)

    return ApiResponse(data=DeleteCategorySchema(message='Category deleted successfully.'))


@router.post('operations', response=ApiResponse[DetailResponse[OperationSchema]], auth=TokenAuth())
def create_operation_handler(
        request: HttpRequest,
        schema: CreateOperationSchema
) -> ApiResponse[DetailResponse[OperationSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseOperationService)

    operation = service.create_operation(
        title=schema.title,
        operation_type=schema.operation_type,
        amount=schema.amount,
        related_budget_id=schema.related_budget_id,
        related_category_id=schema.related_category_id,
        related_customer=request.auth
    )
    item = OperationSchema.from_entity(operation)

    return ApiResponse(data=DetailResponse(item=item))


@router.get('operations', response=ApiResponse[ListPaginatedResponse[OperationSchema]], auth=TokenAuth())
def get_operation_list_handler(
        request: HttpRequest,
        filters: Query[OperationFilters],
        pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[OperationSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseOperationService)

    operation_list = service.get_operation_list(filters=filters, pagination=pagination_in, related_customer=request.auth)
    operation_count = service.get_operation_count(filters=filters, related_customer=request.auth)
    items = [OperationSchema.from_entity(entity=obj) for obj in operation_list]
    pagination_out = PaginationOut(offset=pagination_in.limit, limit=pagination_in.limit, total=operation_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('operations/{operation_id}', response=ApiResponse[DetailResponse[OperationSchema]], auth=TokenAuth())
def get_operation_handler(
        request: HttpRequest,
        operation_id: int
) -> ApiResponse[DetailResponse[OperationSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseOperationService)

    operation = service.get_operation_by_id(operation_id=operation_id, related_customer=request.auth)
    item = OperationSchema.from_entity(operation)

    return ApiResponse(data=DetailResponse(item=item))


@router.put('operations/{operation_id}', response=ApiResponse[DetailResponse[OperationSchema]], auth=TokenAuth())
def update_operation_handler(
        request: HttpRequest,
        operation_id: int,
        schema: UpdateOperationSchema
) -> ApiResponse[DetailResponse[OperationSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseOperationService)

    updated_operation = service.update_operation(
        operation_id=operation_id,
        title=schema.title,
        operation_type=schema.operation_type,
        amount=schema.amount,
        related_category_id=schema.related_category_id,
        related_customer=request.auth
    )
    item = OperationSchema.from_entity(updated_operation)

    return ApiResponse(data=DetailResponse(item=item))


@router.delete('operations/{operation_id}', response=ApiResponse[DeleteOperationSchema], auth=TokenAuth())
def delete_operation_handler(
        request: HttpRequest,
        operation_id: int
) -> ApiResponse[DeleteOperationSchema]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseOperationService)

    service.delete_operation(operation_id=operation_id, related_customer=request.auth)

    return ApiResponse(data=DeleteOperationSchema(message='Operation deleted successfully.'))
