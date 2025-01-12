from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.customers.schemas.customers import AuthInSchema, AuthOutSchema, TokenOutSchema, TokenInSchema
from core.apps.common.exceptions import ServiceException
from core.apps.customers.services.auth import BaseAuthService
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
