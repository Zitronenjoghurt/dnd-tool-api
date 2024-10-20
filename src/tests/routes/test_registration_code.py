import pytest
from httpx import AsyncClient

from models.queries.registration_code_query import RegistrationCodeQuery
from models.responses.paginated_entity_response import PaginatedEntityResponse
from models.responses.registration_code_response import RegistrationCodeResponse


@pytest.mark.asyncio
async def test_get_registration_code(
        client: AsyncClient,
        token_headers: dict,
        test_user_registration_code: str,
        super_user_token_headers: dict
):
    query = RegistrationCodeQuery(unused=False).model_dump()
    json_response = await client.get("/registration-code", params=query, headers=super_user_token_headers)
    response = PaginatedEntityResponse[RegistrationCodeResponse].model_validate(json_response.json())
    assert json_response.status_code == 200
    assert response.page == 1
    assert response.limit == 10
    assert response.count == 1
    assert response.total == 1
    assert response.max_pages == 1
    assert len(response.entities) == 1

    entity = response.entities[0]
    assert test_user_registration_code == entity.code
    assert entity.used