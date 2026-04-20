from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_active_user
from app.api.deps.services import get_auth_service
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserRead
from app.schemas.user_context import SetActiveBabyRequest
from app.services.auth_service import AuthService
from app.services.baby_context_service import BabyContextService

router = APIRouter()


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    payload: UserRegister,
    service: AuthService = Depends(get_auth_service),
):
    try:
        return service.register_user(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    try:
        user = service.authenticate_user(form_data.username, form_data.password)
        return service.generate_tokens(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh")
def refresh(
    payload: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        return service.refresh_token(payload.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/logout")
def logout():
    return {"msg": "Logout exitoso"}


@router.get("/me", response_model=UserRead)
def read_users_me(
    current_user: User = Depends(get_current_active_user),
):
    return current_user


@router.patch("/me/active-baby")
def set_active_baby(
    payload: SetActiveBabyRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    service = BabyContextService(db)
    user = service.set_active_baby(
        user=current_user,
        baby_id=payload.baby_id,
    )
    return {"active_baby_id": str(user.active_baby_id)}