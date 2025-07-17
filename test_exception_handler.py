import pytest
from fastapi import Request
from app.core.exceptions import BusinessValidationException
from app.core.exception_handler import handle_business_validation_exception

@pytest.mark.asyncio
async def test_business_validation_exception_handler():
    mock_request = Request(scope={"type": "http", "path": "/"})
    exc = BusinessValidationException(message="Invalid input", status_code=422)
    response = await handle_business_validation_exception(mock_request, exc)

    assert response.status_code == 422
    assert b"Invalid input" in await response.body()