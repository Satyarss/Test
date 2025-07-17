import pytest
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.datastructures import Headers
from app.core.exception_handler import validation_exception_handler

@pytest.mark.asyncio
async def test_validation_exception_handler_missing_fields():
    mock_request = Request({
        "type": "http",
        "method": "POST",
        "path": "/",
        "headers": Headers({}),
    })

    # Simulate FastAPI validation error with missing fields
    missing_error = RequestValidationError(errors=[
        {
            "loc": ("body", "field1"),
            "msg": "field required",
            "type": "missing"
        },
        {
            "loc": ("body", "field2"),
            "msg": "field required",
            "type": "missing"
        }
    ])

    response = await validation_exception_handler(mock_request, missing_error)

    assert response.status_code == 400
    body = response.body.decode("utf-8")
    assert "Missing fields" in body
    assert "field1" in body
    assert "field2" in body


@pytest.mark.asyncio
async def test_validation_exception_handler_non_missing_field():
    mock_request = Request({
        "type": "http",
        "method": "POST",
        "path": "/",
        "headers": Headers({}),
    })

    # Simulate a non-missing field error (e.g., type error)
    error = RequestValidationError(errors=[
        {
            "loc": ("body", "age"),
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ])

    response = await validation_exception_handler(mock_request, error)

    assert response.status_code == 422 or response.status_code == 400
