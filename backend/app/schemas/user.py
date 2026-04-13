from pydantic import BaseModel,EmailStr, Field, field_validator,ConfigDict
import uuid
from app.core.enums import Roles

class UserRegister(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        has_upper = any(character.isupper() for character in value)
        has_lower = any(character.islower() for character in value)
        has_digit = any(character.isdigit() for character in value)
        if not (has_upper and has_lower and has_digit):
            raise ValueError("La contrasena debe incluir mayusculas, minusculas y numeros.")
        return value

class UserRead(BaseModel):
    id:  uuid.UUID
    full_name: str | None = None
    email: EmailStr
    is_active: bool
    role: Roles
    model_config = ConfigDict(from_attributes=True)