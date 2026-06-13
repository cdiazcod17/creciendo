import secrets
from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session
from app.services.base import BaseService
from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.schemas.user import UserRegister
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import get_settings
from jose import jwt
from app.core.enums import Roles
from app.repositories.user_repository import UserRepository
from app.repositories.password_reset_repository import PasswordResetRepository
from app.services.email_service import EmailService
from app.core.logger import setup_logger

logger = setup_logger(__name__)

class AuthService(BaseService):
    def __init__(self, session: Session, user_repo: UserRepository, password_reset_repo: PasswordResetRepository, email_service: EmailService):
        super().__init__(session)
        self.user_repo = user_repo
        self.password_reset_repo = password_reset_repo
        self.email_service = email_service

    def register_user(self, payload: UserRegister) -> User:
        existing_user = self.user_repo.get_by_email(payload.email)
        if existing_user:
            logger.warning(f"Registration failed: Email {payload.email} already registered")
            raise ValueError("Email already registered")
        
        user = User(
            full_name=payload.full_name,
            email=payload.email,
            hashed_password=get_password_hash(payload.password),
            role=Roles.user
        )
        logger.info(f"User registered successfully: {payload.email}")
        return self.user_repo.add(user)
    
    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Failed authentication attempt for email: {email}")
            raise ValueError("Invalid credentials")
        if not user.is_active:
            logger.warning(f"Authentication failed: User {email} is inactive")
            raise ValueError("Inactive user")
        return user
    
    def generate_tokens(self, user: User) -> dict:
        settings = get_settings()
        token_data = {"sub": user.email, "token_version": user.token_version}
        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_access_token(
            data={**token_data, "type": "refresh"},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    def logout_user(self, user: User) -> None:
        user.token_version += 1
        self.user_repo.update()
        logger.info(f"User {user.id} logged out, token_version={user.token_version}")

    def refresh_token(self, refresh_token: str) -> dict:
        settings = get_settings()
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "refresh":
            logger.warning("Token refresh failed: Invalid token type")
            raise ValueError("Token inválido")

        user = self.user_repo.get_by_email(payload["sub"])
        if not user:
            logger.warning(f"Token refresh failed: User {payload['sub']} not found")
            raise ValueError("Usuario no encontrado")

        if payload.get("token_version") != user.token_version:
            logger.warning(f"Token refresh failed: token_version mismatch for user {user.id}")
            raise ValueError("Token inválido o revocado")

        access_token = create_access_token(
            data={"sub": user.email, "token_version": user.token_version},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def request_password_reset(self, email: str) -> None:
        user = self.user_repo.get_by_email(email)
        if not user:
            logger.warning(f"Password reset requested for unknown email: {email}")
            return None
        
        # Delete any existing tokens for this user
        self.password_reset_repo.delete_by_user_id(user.id)
        
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        
        reset_token = PasswordResetToken(
            token=token,
            expires_at=expires_at,
            user_id=user.id
        )
        self.password_reset_repo.add(reset_token)
        logger.info(f"Generated password reset token for {email}")
        
        # Send the email via Resend
        self.email_service.send_password_reset_email(user.email, token)

    def reset_password(self, token: str, new_password: str) -> None:
        reset_token = self.password_reset_repo.get_by_token(token)
        if not reset_token:
            logger.warning("Password reset failed: Invalid token")
            raise ValueError("Token inválido")
        
        expires_at = reset_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        if expires_at < datetime.now(timezone.utc):
            self.password_reset_repo.delete(reset_token)
            logger.warning(f"Password reset failed: Expired token for user {reset_token.user_id}")
            raise ValueError("Token expirado")
        
        user = self.user_repo.get(reset_token.user_id)
        if not user:
            logger.error(f"Password reset failed: User {reset_token.user_id} not found for valid token")
            raise ValueError("Usuario no encontrado")
        
        user.hashed_password = get_password_hash(new_password)
        self.user_repo.update()
        logger.info(f"Password reset successful for user {user.id}")
        
        # Delete the token after successful reset
        self.password_reset_repo.delete(reset_token)
