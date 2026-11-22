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


_TYPE_ALIASES = {
    "add": CalculationType.ADDITION.value,
    "sub": CalculationType.SUBTRACTION.value,
    "multiply": CalculationType.MULTIPLICATION.value,
    "divide": CalculationType.DIVISION.value,
}


class CalculationBase(BaseModel):
    type: CalculationType = Field(
        ...,
        description="Operation: add, sub, multiply, or divide",
    )
    a: float = Field(..., description="First operand")
    b: float = Field(..., description="Second operand")

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, value):
        allowed_types = {calculation_type.value for calculation_type in CalculationType}
        if not isinstance(value, str):
            raise ValueError(
                "Type must be one of: add, sub, multiply, divide"
            )
        normalized = value.strip().lower()
        normalized = _TYPE_ALIASES.get(normalized, normalized)
        if normalized not in allowed_types:
            raise ValueError(
                "Type must be one of: add, sub, multiply, divide"
            )
        return normalized

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
    """Request schema for creating a calculation."""


class CalculationUpdate(BaseModel):
    a: Optional[float] = Field(None, description="Updated first operand")
    b: Optional[float] = Field(None, description="Updated second operand")

    model_config = ConfigDict(from_attributes=True)


class CalculationRead(CalculationBase):
    """Response schema for a calculation, including its computed result."""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    result: float = Field(..., description="Computed result")

    model_config = ConfigDict(from_attributes=True)


CalculationResponse = CalculationRead
