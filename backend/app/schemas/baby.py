from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict
from app.core.enums import BabySex
from .user import UserRead

class BabyCreate(BaseModel):
    name: str = Field(..., max_length=250)
    birth_date: date
    sex: BabySex | None = None
    notes: str | None = None


class BabyRead(BaseModel):
    id: str
    name: str
    birth_date: date
    sex: BabySex | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class BabyDetail(BabyRead):
    user: UserRead