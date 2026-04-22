import pytest
from app.schemas.auth import LoginRequest, TokenPairResponse, CurrentUserResponse, RegisterRequest


def test_login_request_required_fields():
    with pytest.raises(Exception):
        LoginRequest()
    req = LoginRequest(username="user", password="pass")
    assert req.username == "user"
    assert req.password == "pass"


def test_token_pair_fields():
    resp = TokenPairResponse(access_token="at", refresh_token="rt")
    assert resp.access_token == "at"
    assert resp.refresh_token == "rt"
    assert resp.token_type == "bearer"


def test_current_user_no_password_hash():
    resp = CurrentUserResponse(id=1, username="u", email="e@e.com")
    dumped = resp.model_dump()
    assert "hashed_password" not in dumped
    assert "password" not in dumped


def test_register_request_fields():
    req = RegisterRequest(username="new", email="new@e.com", password="123456")
    assert req.username == "new"
    assert req.display_name is None


def test_login_request_missing_email():
    with pytest.raises(Exception):
        LoginRequest(username="user")
