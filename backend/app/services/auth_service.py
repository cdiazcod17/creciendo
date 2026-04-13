from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import get_settings
from jose import jwt


class AuthService(BaseService):
    def register_user(self, payload: UserRegister) -> User:
        """Registra usuario."""
        user = User(
            full_name=payload.full_name,
            email=payload.email,
            hashed_password=get_password_hash(payload.password)
        )
        return self.add_and_refresh(user)
    
    def authenticate_user(self, email: str, password: str) -> User:
        """Valida credenciales."""
        user = self.session.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Credenciales inválidas")
        if not user.is_active:
            raise ValueError("Usuario inactivo")
        return user
    
    def generate_tokens(self, user: User) -> dict:
        """Genera tokens."""
        settings = get_settings()
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_access_token(
            data={"sub": user.email, "type": "refresh"},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    
    def refresh_token(self, refresh_token: str) -> dict:
        """Refresca access token."""
        settings = get_settings()
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise ValueError("Token inválido")
        
        user = self.get(User, payload["sub"])
        if not user:
            raise ValueError("Usuario no encontrado")
        
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}