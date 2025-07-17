import pytest
from app.core.exceptions import BadRequestException


def test_bad_request_exception():
    with pytest.raises(BadRequestException):
        raise BadRequestException("Bad request error occurred")
