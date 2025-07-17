from app.core.exceptions import (
    BusinessValidationException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException
)

def test_business_validation_exception():
    exc = BusinessValidationException(message="Validation error", status_code=400)
    assert exc.message == "Validation error"
    assert exc.status_code == 400

def test_unauthorized_exception():
    exc = UnauthorizedException(message="Unauthorized access", status_code=401)
    assert exc.message == "Unauthorized access"
    assert exc.status_code == 401

def test_forbidden_exception():
    exc = ForbiddenException(message="Forbidden action", status_code=403)
    assert exc.message == "Forbidden action"
    assert exc.status_code == 403

def test_not_found_exception():
    exc = NotFoundException(message="Resource not found", status_code=404)
    assert exc.message == "Resource not found"
    assert exc.status_code == 404