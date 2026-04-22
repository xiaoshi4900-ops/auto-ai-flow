from sqlalchemy.orm import Session

from app.db.repositories.user_repo import UserRepository
from app.db.models.user import RefreshToken
from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password
from app.schemas.auth import LoginRequest, TokenPairResponse, CurrentUserResponse, RegisterRequest
from app.core.exceptions import UnauthorizedException, BadRequestException, ConflictException


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def login(self, req: LoginRequest) -> TokenPairResponse:
        user = self.user_repo.authenticate(req.username, req.password)
        if not user:
            raise UnauthorizedException("Invalid username or password")
        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        token_record = RefreshToken(token=refresh_token, user_id=user.id)
        self.db.add(token_record)
        self.db.commit()
        return TokenPairResponse(access_token=access_token, refresh_token=refresh_token)

    def register(self, req: RegisterRequest) -> CurrentUserResponse:
        if self.user_repo.get_by_username(req.username):
            raise ConflictException("Username already exists")
        if self.user_repo.get_by_email(req.email):
            raise ConflictException("Email already exists")
        user = self.user_repo.create(username=req.username, email=req.email, password=req.password, display_name=req.display_name)
        return CurrentUserResponse(id=user.id, username=user.username, email=user.email, display_name=user.display_name, is_active=user.is_active)

    def get_current_user(self, user_id: int) -> CurrentUserResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("User not found")
        return CurrentUserResponse(id=user.id, username=user.username, email=user.email, display_name=user.display_name, is_active=user.is_active)

    def refresh_tokens(self, refresh_token: str) -> TokenPairResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedException("Invalid refresh token")
        token_record = self.db.query(RefreshToken).filter(RefreshToken.token == refresh_token, RefreshToken.is_revoked == False).first()
        if not token_record:
            raise UnauthorizedException("Refresh token not found or revoked")
        token_record.is_revoked = True
        self.db.commit()
        user_id = int(payload["sub"])
        new_access = create_access_token(str(user_id))
        new_refresh = create_refresh_token(str(user_id))
        new_record = RefreshToken(token=new_refresh, user_id=user_id)
        self.db.add(new_record)
        self.db.commit()
        return TokenPairResponse(access_token=new_access, refresh_token=new_refresh)

    def logout(self, refresh_token: str) -> None:
        token_record = self.db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        if token_record:
            token_record.is_revoked = True
            self.db.commit()
