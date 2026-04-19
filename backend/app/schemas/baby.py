from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.core.enums import BabySex
from .user import UserRead

class BabyCreate(BaseModel):
    name: str = Field(..., max_length=250)
    birth_date: date
    sex: BabySex | None = None
    notes: str | None = None
    photo_url: str | None = None


class BabyRead(BaseModel):
    id: UUID
    name: str
    birth_date: date
    sex: BabySex | None = None
    notes: str | None = None
    photo_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class BabyDetail(BabyRead):
    user: UserRead
    
class BabyUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=2, max_length=100)
    birth_date: date | None = None
    sex: BabySex | None = None
    notes: str | None = None
    photo_url: str | None = None