from typing import Annotated, List

from fastapi import APIRouter
from fastapi.params import Query, Depends
from starlette import status
from starlette.responses import JSONResponse

from config import settings
from constants.permissions import GlobalPermission
from models.entities.registration_code import RegistrationCode
from models.entities.user import User
from models.queries.registration_code_query import RegistrationCodeQuery
from models.responses.error_responses import AuthenticationErrorResponse, GlobalPermissionErrorResponse
from models.responses.generated_registration_codes_response import GeneratedRegistrationCodesResponse
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
    query: Annotated[RegistrationCodeQuery, Query()],
    current_user: User = Depends(get_current_user),
    registration_code_repo: RegistrationCodeRepository = Depends(get_registration_code_repo)
):
    current_user.check_global_permissions([GlobalPermission.MANAGE_REGISTRATION_CODES])
    query.validate()
    return await registration_code_repo.find_paginated(
        query=query,
        data_transform=RegistrationCodeResponse.from_registration_code,
        used=not query.unused,
    )

@router.post(
    "",
    summary="Create new registration codes",
    response_model=GeneratedRegistrationCodesResponse,
    response_description="A list of all generated registration codes.",
    status_code=status.HTTP_201_CREATED,
    responses={401: {"model": AuthenticationErrorResponse}, 403: {"model": GlobalPermissionErrorResponse}},
)
async def post_registration_code(
    count: int = 1,
    current_user: User = Depends(get_current_user),
    registration_code_repo: RegistrationCodeRepository = Depends(get_registration_code_repo)
):
    current_user.check_global_permissions([GlobalPermission.MANAGE_REGISTRATION_CODES])
    count = min(count, settings.REGISTRATION_CODE_GENERATION_MAX_COUNT)

    registration_codes = [RegistrationCode.generate(creator=current_user) for _ in range(count)]
    await registration_code_repo.save_many(registration_codes)
    codes = [registration_code.code for registration_code in registration_codes]

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=GeneratedRegistrationCodesResponse(codes=codes).model_dump()
    )