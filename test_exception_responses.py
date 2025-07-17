from app.core.exception_responses import ErrorResponseModel

def test_error_response_model():
    model = ErrorResponseModel(
        code="ERR001",
        message="Invalid input format",
        status=400,
        field="username"
    )

    assert model.code == "ERR001"
    assert model.message == "Invalid input format"
    assert model.status == 400
    assert model.field == "username"