from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class GrowthCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    measured_at: datetime
    weight_kg: float | None = Field(default=None, gt=0, le=50)
    height_cm: float | None = Field(default=None, gt=0, le=150)
    head_circumference_cm: float | None = Field(default=None, gt=0, le=100)
    notes: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validate_at_least_one_measurement(self):
        if (
            self.weight_kg is None
            and self.height_cm is None
            and self.head_circumference_cm is None
        ):
            raise ValueError("Debes informar al menos una medición")
        return self


class GrowthUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    measured_at: datetime | None = None
    weight_kg: float | None = Field(default=None, gt=0, le=50)
    height_cm: float | None = Field(default=None, gt=0, le=150)
    head_circumference_cm: float | None = Field(default=None, gt=0, le=100)
    notes: str | None = Field(default=None, max_length=500)


class GrowthRead(BaseModel):
    id: UUID
    baby_id: UUID
    measured_at: datetime
    weight_kg: float | None = None
    height_cm: float | None = None
    head_circumference_cm: float | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)