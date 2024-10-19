from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query, Depends
from starlette import status

from constants.permissions import GlobalPermission
from models.entities.user import User
from models.queries.pagination_query import PaginationQuery
from models.responses.error_response import AuthenticationErrorResponse, GlobalPermissionErrorResponse
from models.responses.paginated_entity_response import PaginatedEntityResponse
from models.responses.registration_code_response import RegistrationCodeResponse
from repositories.registration_code_repository import RegistrationCodeRepository, get_registration_code_repo
from security.authentication import get_current_user

router = APIRouter(prefix="/registration-code", tags=["Registration Code"])

@router.get(
    "",
    summary="Fetch available registration codes",
    response_model=PaginatedEntityResponse[RegistrationCodeResponse],
    response_description="A response including pagination information and the requested entity data.",
    status_code=status.HTTP_200_OK,
    responses={401: {"model": AuthenticationErrorResponse}, 403: {"model": GlobalPermissionErrorResponse}}
)
async def get_registration_code(
    pagination: Annotated[PaginationQuery, Query()],
    current_user: User = Depends(get_current_user),
    registration_code_repo: RegistrationCodeRepository = Depends(get_registration_code_repo)
):
    current_user.check_global_permissions([GlobalPermission.MANAGE_REGISTRATION_CODES])
    pagination.validate()
    return await registration_code_repo.find_paginated(pagination, RegistrationCodeResponse.from_registration_code)