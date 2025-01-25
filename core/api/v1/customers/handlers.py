from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from core.api.auth import TokenAuth
from core.api.schemas import ApiResponse, DetailResponse
from core.api.v1.customers.schemas.customers import AuthInSchema, AuthOutSchema, TokenOutSchema, TokenInSchema, \
    CustomerSchema, UpdateCustomerSchema
from core.apps.common.exceptions import ServiceException
from core.apps.customers.services.auth import BaseAuthService
from core.apps.customers.services.customers import BaseCustomerService
from core.project.ioc_containers import get_ioc_container

router = Router(tags=['Customers'])


@router.post('auth', response=ApiResponse[AuthOutSchema], operation_id='authorize')
def auth_handler(
        request: HttpRequest,
        schema: AuthInSchema
) -> ApiResponse[AuthOutSchema]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseAuthService)

    service.authorize(phone=schema.phone, username=schema.username)

    return ApiResponse(data=AuthOutSchema(
        message=f'Code is sent to {schema.phone}.'
    ))


@router.post('confirm', response=ApiResponse[TokenOutSchema], operation_id='confirm_code')
def get_token_handler(
        request: HttpRequest,
        schema: TokenInSchema
) -> ApiResponse[TokenOutSchema]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseAuthService)

    try:
        token = service.confirm(code=schema.code, phone=schema.phone)
    except ServiceException as exception:
        raise HttpError(
            status_code=400,
            message=exception.message
        )

    return ApiResponse(data=TokenOutSchema(token=token))


@router.get('profile', response=ApiResponse[DetailResponse[CustomerSchema]], auth=TokenAuth())
def get_customer_handler(
        request: HttpRequest,
) -> ApiResponse[DetailResponse[CustomerSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseCustomerService)

    customer = service.get(phone=request.auth.phone)
    item = CustomerSchema.from_entity(customer)

    return ApiResponse(data=DetailResponse(item=item))


@router.put('profile', response=ApiResponse[DetailResponse[CustomerSchema]], auth=TokenAuth())
def update_budget_handler(
        request: HttpRequest,
        schema: UpdateCustomerSchema
) -> ApiResponse[DetailResponse[CustomerSchema]]:

    ioc_container = get_ioc_container()
    service = ioc_container.resolve(BaseCustomerService)

    updated_customer = service.update_username(
        username=schema.username,
        customer=request.auth
    )
    item = CustomerSchema.from_entity(updated_customer)

    return ApiResponse(data=DetailResponse(item=item))
