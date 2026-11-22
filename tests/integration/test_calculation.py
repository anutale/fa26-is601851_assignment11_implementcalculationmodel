"""Tests for SQLAlchemy calculation models."""

import uuid

import pytest

from app.models.calculation import (
    Addition,
    Calculation,
    Division,
    Multiplication,
    Subtraction,
)


def test_calculation_model_columns_and_user_foreign_key():
    columns = Calculation.__table__.c

    assert {"id", "a", "b", "type", "user_id"} <= set(columns.keys())
    assert "result" not in columns
    assert next(iter(columns.user_id.foreign_keys)).target_fullname == "users.id"


@pytest.mark.parametrize(
    ("calculation_class", "a", "b", "expected"),
    [
        (Addition, 10, 5, 15),
        (Subtraction, 10, 5, 5),
        (Multiplication, 10, 5, 50),
        (Division, 10, 5, 2),
    ],
)
def test_calculation_result_is_computed_on_demand(
    calculation_class, a, b, expected
):
    calculation = calculation_class(user_id=uuid.uuid4(), a=a, b=b)

    assert calculation.get_result() == expected
    assert calculation.result == expected


def test_division_by_zero_raises_value_error():
    division = Division(user_id=uuid.uuid4(), a=10, b=0)

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        division.get_result()


@pytest.mark.parametrize(
    ("calculation_type", "calculation_class", "expected"),
    [
        ("addition", Addition, 7),
        ("subtraction", Subtraction, 3),
        ("multiplication", Multiplication, 10),
        ("division", Division, 2.5),
        ("AdDiTiOn", Addition, 7),
    ],
)
def test_calculation_factory(calculation_type, calculation_class, expected):
    calculation = Calculation.create(calculation_type, uuid.uuid4(), 5, 2)

    assert isinstance(calculation, calculation_class)
    assert calculation.result == expected


def test_calculation_factory_rejects_unsupported_type():
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        Calculation.create("modulus", uuid.uuid4(), 10, 3)
