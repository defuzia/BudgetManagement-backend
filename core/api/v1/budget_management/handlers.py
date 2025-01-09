from django.http import HttpRequest
from ninja import Router, Query, Body

from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse, DetailResponse, PaginationOut
from core.api.v1.budget_management.filters import CurrencyFilters, BudgetFilters, CategoryFilters, OperationFilters

from core.api.v1.budget_management.schemas.budgets import (
    CurrencySchema, BudgetSchema, CreateBudgetSchema, UpdateBudgetSchema
)
from core.api.v1.budget_management.schemas.operations import CategorySchema, OperationSchema, CreateOperationSchema, \
    UpdateOperationSchema
from core.api.v1.budget_management.services.budgets import (
    BaseCurrencyService, ORMCurrencyService, BaseBudgetService, ORMBudgetService
)
from core.api.v1.budget_management.services.operations import BaseCategoryService, ORMCategoryService, \
    BaseOperationService, ORMOperationService

router = Router(tags=['Budget managing'])


@router.get('currencies', response=ApiResponse[ListPaginatedResponse[CurrencySchema]])
def get_currency_list_handler(
        request: HttpRequest,
        filters: Query[CurrencyFilters],
        pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[CurrencySchema]]:
    service: BaseCurrencyService = ORMCurrencyService()
    currency_list = service.get_currency_list(filters=filters, pagination=pagination_in)
    currency_count = service.get_currency_count(filters=filters)
    items = [CurrencySchema.from_entity(entity=obj) for obj in currency_list]
    pagination_out = PaginationOut(offset=pagination_in.limit, limit=pagination_in.limit, total=currency_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('currencies/{short_name}', response=ApiResponse[DetailResponse[CurrencySchema]])
def get_currency_handler(
        request: HttpRequest,
        short_name: str
) -> ApiResponse[DetailResponse[CurrencySchema]]:
    service: BaseCurrencyService = ORMCurrencyService()
    item = CurrencySchema.from_entity(service.get_currency_by_short_name(short_name=short_name))

    return ApiResponse(data=DetailResponse(item=item))


@router.get('budgets', response=ApiResponse[ListPaginatedResponse[BudgetSchema]])
def get_budget_list_handler(
        request: HttpRequest,
        filters: Query[BudgetFilters],
        pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[BudgetSchema]]:
    service: BaseBudgetService = ORMBudgetService()
    budget_list = service.get_budget_list(filters=filters, pagination=pagination_in)
    budget_count = service.get_budget_count(filters=filters)
    items = [BudgetSchema.from_entity(entity=obj) for obj in budget_list]
    pagination_out = PaginationOut(offset=pagination_in.limit, limit=pagination_in.limit, total=budget_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('budgets/{budget_id}', response=ApiResponse[DetailResponse[BudgetSchema]])
def get_budget_handler(
        request: HttpRequest,
        budget_id: int
) -> ApiResponse[DetailResponse[BudgetSchema]]:
    service: BaseBudgetService = ORMBudgetService()
    item = BudgetSchema.from_entity(service.get_budget_by_id(budget_id=budget_id))

    return ApiResponse(data=DetailResponse(item=item))


@router.post('budgets', response=ApiResponse[DetailResponse[BudgetSchema]])
def create_budget_handler(
        request: HttpRequest,
        payload: Body[CreateBudgetSchema]
) -> ApiResponse[DetailResponse[BudgetSchema]]:
    service: BaseBudgetService = ORMBudgetService()
    budget = service.create_budget(
        title=payload.title,
        amount=payload.amount,
        related_currency_short_name=payload.related_currency_short_name,
        related_user=payload.related_user
    )
    item = BudgetSchema.from_entity(budget)
    return ApiResponse(data=DetailResponse(item=item))


@router.delete('budgets/{budget_id}', response=ApiResponse[DetailResponse[BudgetSchema]])
def delete_budget_handler(
        request: HttpRequest,
        budget_id: int
) -> ApiResponse[DetailResponse[BudgetSchema]]:
    service: BaseBudgetService = ORMBudgetService()
    budget = service.get_budget_by_id(budget_id=budget_id)
    service.delete_budget(budget_id=budget_id)
    item = BudgetSchema.from_entity(budget)
    return ApiResponse(data=DetailResponse(item=item))


@router.put('budgets/{budget_id}', response=ApiResponse[DetailResponse[BudgetSchema]])
def update_budget_handler(
        request: HttpRequest,
        budget_id: int,
        payload: Body[UpdateBudgetSchema]
) -> ApiResponse[DetailResponse[BudgetSchema]]:
    service: BaseBudgetService = ORMBudgetService()
    updated_budget = service.update_budget(
        budget_id=budget_id,
        title=payload.title,
        related_currency_short_name=payload.related_currency_short_name,
        amount=payload.amount
    )
    item = BudgetSchema.from_entity(updated_budget)
    return ApiResponse(data=DetailResponse(item=item))


@router.get('category', response=ApiResponse[ListPaginatedResponse[CategorySchema]])
def get_category_list_handler(
        request: HttpRequest,
        filters: Query[CategoryFilters],
        pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[CategorySchema]]:
    service: BaseCategoryService = ORMCategoryService()
    category_list = service.get_category_list(filters=filters, pagination=pagination_in)
    category_count = service.get_category_count(filters=filters)
    items = [CategorySchema.from_entity(entity=obj) for obj in category_list]
    pagination_out = PaginationOut(offset=pagination_in.limit, limit=pagination_in.limit, total=category_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('category/{category_id}', response=ApiResponse[DetailResponse[CategorySchema]])
def get_category_handler(
        request: HttpRequest,
        category_id: int
) -> ApiResponse[DetailResponse[CategorySchema]]:
    service: BaseCategoryService = ORMCategoryService()
    item = CategorySchema.from_entity(service.get_category_by_id(category_id=category_id))

    return ApiResponse(data=DetailResponse(item=item))


@router.get('operations', response=ApiResponse[ListPaginatedResponse[OperationSchema]])
def get_operation_list_handler(
        request: HttpRequest,
        filters: Query[OperationFilters],
        pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[OperationSchema]]:
    service: BaseOperationService = ORMOperationService()
    operation_list = service.get_operation_list(filters=filters, pagination=pagination_in)
    operation_count = service.get_operation_count(filters=filters)
    items = [OperationSchema.from_entity(entity=obj) for obj in operation_list]
    pagination_out = PaginationOut(offset=pagination_in.limit, limit=pagination_in.limit, total=operation_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('operations/{operation_id}', response=ApiResponse[DetailResponse[OperationSchema]])
def get_operation_handler(
        request: HttpRequest,
        operation_id: int
) -> ApiResponse[DetailResponse[OperationSchema]]:
    service: BaseOperationService = ORMOperationService()
    item = OperationSchema.from_entity(service.get_operation_by_id(operation_id=operation_id))

    return ApiResponse(data=DetailResponse(item=item))


@router.post('operations', response=ApiResponse[DetailResponse[OperationSchema]])
def create_operation_handler(
        request: HttpRequest,
        payload: Body[CreateOperationSchema]
) -> ApiResponse[DetailResponse[OperationSchema]]:
    service: BaseOperationService = ORMOperationService()
    operation = service.create_operation(
        title=payload.title,
        operation_type=payload.operation_type,
        amount=payload.amount,
        related_budget_id=payload.related_budget_id,
        related_category_id=payload.related_category_id
    )
    item = OperationSchema.from_entity(operation)

    return ApiResponse(data=DetailResponse(item=item))


@router.delete('operations/{operation_id}', response=ApiResponse[DetailResponse[OperationSchema]])
def delete_operation_handler(
        request: HttpRequest,
        operation_id: int
) -> ApiResponse[DetailResponse[OperationSchema]]:
    service: BaseOperationService = ORMOperationService()
    operation = service.get_operation_by_id(operation_id=operation_id)
    service.delete_operation(operation_id=operation_id)
    item = OperationSchema.from_entity(operation)

    return ApiResponse(data=DetailResponse(item=item))


@router.put('operations/{operation_id}', response=ApiResponse[DetailResponse[OperationSchema]])
def update_operation_handler(
        request: HttpRequest,
        operation_id: int,
        payload: Body[UpdateOperationSchema]
) -> ApiResponse[DetailResponse[OperationSchema]]:
    service: BaseOperationService = ORMOperationService()
    updated_operation = service.update_operation(
        operation_id=operation_id,
        title=payload.title,
        operation_type=payload.operation_type,
        amount=payload.amount,
        related_budget_id=payload.related_budget_id,
        related_category_id=payload.related_category_id
    )
    item = OperationSchema.from_entity(updated_operation)
    return ApiResponse(data=DetailResponse(item=item))
