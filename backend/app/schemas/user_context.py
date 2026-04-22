from uuid import UUID
from pydantic import BaseModel, Field

class SetActiveBabyRequest(BaseModel):
    baby_id: UUID = Field(..., alias="active_baby_id")
    
    # Esto permite que Pydantic acepte tanto baby_id como active_baby_id
    model_config = {
        "populate_by_name": True
    }
