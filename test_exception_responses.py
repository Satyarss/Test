from app.core.exception_responses import responses


def test_response_200_structure():
    response_200 = responses.get(200)
    assert response_200 is not None
    assert "description" in response_200
    assert "headers" in response_200
    assert "x-clientrefid" in response_200["headers"]
    assert "x-correlation-id" in response_200["headers"]


def test_response_400_structure():
    response_400 = responses.get(400)
    assert response_400 is not None
    assert response_400["status"] == 400
    assert response_400["title"] == "One or more validation errors occurred"
    assert response_400["type"] == "https://www.rfc-editor.org/rfc/rfc7231#section-6.5.1"
    assert "correlationId" in response_400
    assert "detail" in response_400
    assert "errors" in response_400
    assert "message" in response_400
