"""Pydantic schemas for binary calculation data."""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class CalculationType(str, Enum):
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"


class CalculationBase(BaseModel):
    type: CalculationType = Field(..., description="Calculation operation")
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, value):
        allowed_types = {calculation_type.value for calculation_type in CalculationType}
        if not isinstance(value, str) or value.lower() not in allowed_types:
            raise ValueError(
                f"Type must be one of: {', '.join(sorted(allowed_types))}"
            )
        return value.lower()

    @model_validator(mode="after")
    def validate_division(self) -> "CalculationBase":
        if self.type == CalculationType.DIVISION and self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {"type": "addition", "a": 10.5, "b": 3},
                {"type": "division", "a": 100, "b": 2},
            ]
        },
    )


class CalculationCreate(CalculationBase):
    user_id: UUID = Field(..., description="UUID of the owning user")


class CalculationUpdate(BaseModel):
    a: Optional[float] = Field(None, description="Updated first operand")
    b: Optional[float] = Field(None, description="Updated second operand")

    model_config = ConfigDict(from_attributes=True)


class CalculationResponse(CalculationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    result: float = Field(..., description="Computed result")

    model_config = ConfigDict(from_attributes=True)
