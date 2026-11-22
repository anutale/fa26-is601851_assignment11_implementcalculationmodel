"""SQLAlchemy models for binary calculations."""

from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr, relationship

from app.database import Base


class AbstractCalculation:
    """Shared fields and behavior for calculation types."""

    @declared_attr
    def __tablename__(cls):
        return "calculations"

    @declared_attr
    def id(cls):
        return Column(
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False,
        )

    @declared_attr
    def user_id(cls):
        return Column(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )

    @declared_attr
    def a(cls):
        return Column(Float, nullable=False)

    @declared_attr
    def b(cls):
        return Column(Float, nullable=False)

    @declared_attr
    def type(cls):
        return Column(String(50), nullable=False, index=True)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
        )

    @declared_attr
    def user(cls):
        return relationship("User", back_populates="calculations")

    @property
    def result(self) -> float:
        """Calculate the result on demand instead of storing it in the table."""
        return self.get_result()

    @classmethod
    def create(
        cls,
        calculation_type: str,
        user_id: uuid.UUID,
        a: float,
        b: float,
    ) -> "Calculation":
        calculation_classes = {
            "add": Addition,
            "addition": Addition,
            "sub": Subtraction,
            "subtraction": Subtraction,
            "multiply": Multiplication,
            "multiplication": Multiplication,
            "divide": Division,
            "division": Division,
        }
        normalized_type = calculation_type.strip().lower()
        calculation_class = calculation_classes.get(normalized_type)
        if calculation_class is None:
            raise ValueError(f"Unsupported calculation type: {calculation_type}")
        return calculation_class(user_id=user_id, a=a, b=b)

    def get_result(self) -> float:
        raise NotImplementedError("Subclasses must implement get_result().")

    def __repr__(self):
        return f"<Calculation(type={self.type}, a={self.a}, b={self.b})>"


class Calculation(Base, AbstractCalculation):
    """Base model using single-table polymorphic inheritance."""

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "calculation",
    }


class Addition(Calculation):
    __mapper_args__ = {"polymorphic_identity": "addition"}

    def get_result(self) -> float:
        return self.a + self.b


class Subtraction(Calculation):
    __mapper_args__ = {"polymorphic_identity": "subtraction"}

    def get_result(self) -> float:
        return self.a - self.b


class Multiplication(Calculation):
    __mapper_args__ = {"polymorphic_identity": "multiplication"}

    def get_result(self) -> float:
        return self.a * self.b


class Division(Calculation):
    __mapper_args__ = {"polymorphic_identity": "division"}

    def get_result(self) -> float:
        if self.b == 0:
            raise ValueError("Cannot divide by zero.")
        return self.a / self.b
