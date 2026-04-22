import pytest
from unittest.mock import MagicMock, patch
from app.services.auth_service import AuthService
from app.core.exceptions import UnauthorizedException, ConflictException
from app.schemas.auth import LoginRequest, RegisterRequest
from app.db.models.user import User, RefreshToken


def _make_user(id=1, username="testuser", email="test@example.com", is_active=True):
    user = User(username=username, email=email, hashed_password="hashed", is_active=is_active)
    user.id = id
    return user


def test_login_success(db):
    service = AuthService(db)
    user = _make_user()
    with patch.object(service.user_repo, "authenticate", return_value=user):
        with patch("app.services.auth_service.create_access_token", return_value="at"):
            with patch("app.services.auth_service.create_refresh_token", return_value="rt"):
                req = LoginRequest(username="testuser", password="pass")
                result = service.login(req)
    assert result.access_token == "at"
    assert result.refresh_token == "rt"


def test_login_wrong_password(db):
    service = AuthService(db)
    with patch.object(service.user_repo, "authenticate", return_value=None):
        with pytest.raises(UnauthorizedException):
            req = LoginRequest(username="testuser", password="wrong")
            service.login(req)


def test_login_inactive_user(db):
    service = AuthService(db)
    with patch.object(service.user_repo, "authenticate", return_value=None):
        with pytest.raises(UnauthorizedException):
            req = LoginRequest(username="testuser", password="pass")
            service.login(req)


def test_logout_revokes_token(db):
    service = AuthService(db)
    user = _make_user()
    db.add(user)
    db.commit()
    token = RefreshToken(token="rt_logout", user_id=user.id)
    db.add(token)
    db.commit()
    service.logout("rt_logout")
    db.refresh(token)
    assert token.is_revoked is True


def test_register_duplicate_username(db):
    service = AuthService(db)
    with patch.object(service.user_repo, "get_by_username", return_value=_make_user()):
        with pytest.raises(ConflictException):
            req = RegisterRequest(username="testuser", email="new@e.com", password="123")
            service.register(req)


def test_register_duplicate_email(db):
    service = AuthService(db)
    with patch.object(service.user_repo, "get_by_username", return_value=None):
        with patch.object(service.user_repo, "get_by_email", return_value=_make_user()):
            with pytest.raises(ConflictException):
                req = RegisterRequest(username="new", email="test@example.com", password="123")
                service.register(req)
