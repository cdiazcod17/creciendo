from uuid import UUID
from pydantic import BaseModel

class SetActiveBabyRequest(BaseModel):
    baby_id: UUID