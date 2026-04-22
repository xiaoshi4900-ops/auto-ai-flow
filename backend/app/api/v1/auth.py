from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.api.deps import get_current_user_id
from app.schemas.auth import LoginRequest, TokenPairResponse, CurrentUserResponse, RefreshTokenRequest, RegisterRequest
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenPairResponse)
def login(req: LoginRequest, db: Session = Depends(get_db_session)):
    svc = AuthService(db)
    return svc.login(req)


@router.post("/register", response_model=CurrentUserResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db_session)):
    svc = AuthService(db)
    return svc.register(req)


@router.get("/me", response_model=CurrentUserResponse)
def get_current_user(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db_session)):
    svc = AuthService(db)
    return svc.get_current_user(user_id)


@router.post("/refresh", response_model=TokenPairResponse)
def refresh_token(req: RefreshTokenRequest, db: Session = Depends(get_db_session)):
    svc = AuthService(db)
    return svc.refresh_tokens(req.refresh_token)


@router.post("/logout")
def logout(req: RefreshTokenRequest, db: Session = Depends(get_db_session)):
    svc = AuthService(db)
    svc.logout(req.refresh_token)
    return {"message": "Logged out"}
