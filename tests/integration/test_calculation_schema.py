"""Tests for calculation request and response schemas."""

from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.models.calculation import Addition
from app.schemas.calculation import (
    CalculationBase,
    CalculationCreate,
    CalculationResponse,
    CalculationType,
    CalculationUpdate,
)


def test_calculation_base_normalizes_type_and_operands():
    calculation = CalculationBase(type="AdDiTiOn", a=10, b=5)

    assert calculation.type == CalculationType.ADDITION
    assert calculation.a == 10
    assert calculation.b == 5


def test_calculation_base_rejects_unsupported_type():
    with pytest.raises(ValidationError, match="Type must be one of"):
        CalculationBase(type="modulus", a=10, b=3)


def test_calculation_base_rejects_division_by_zero():
    with pytest.raises(ValidationError, match="Cannot divide by zero"):
        CalculationBase(type="division", a=10, b=0)


def test_calculation_create_requires_a_valid_user_uuid():
    user_id = uuid4()
    calculation = CalculationCreate(
        type="addition",
        a=10,
        b=5,
        user_id=str(user_id),
    )

    assert calculation.user_id == user_id

    with pytest.raises(ValidationError):
        CalculationCreate(
            type="addition",
            a=10,
            b=5,
            user_id="not-a-valid-uuid",
        )


def test_calculation_update_allows_partial_operand_updates():
    update = CalculationUpdate(b=8)
    empty_update = CalculationUpdate()

    assert update.a is None
    assert update.b == 8
    assert empty_update.a is None
    assert empty_update.b is None


def test_calculation_response_reads_computed_result_from_model():
    now = datetime.now()
    model = Addition(
        id=uuid4(),
        user_id=uuid4(),
        type="addition",
        a=10,
        b=5,
        created_at=now,
        updated_at=now,
    )

    response = CalculationResponse.model_validate(model)

    assert response.result == 15
    assert response.a == 10
    assert response.b == 5
