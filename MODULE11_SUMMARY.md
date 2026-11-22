# Module 11: Polymorphic SQLAlchemy Models & Pydantic Schemas

## Summary

The module uses **SQLAlchemy polymorphic inheritance** for binary calculations and Pydantic schemas for validation. Calculation results are computed on demand rather than stored.

## What Was Added

### 1. SQLAlchemy Polymorphic Models (`app/models/calculation.py`)

**Polymorphic Inheritance Pattern:**
- **Base Model:** `Calculation` - uses single-table inheritance
- **Subclasses:** `Addition`, `Subtraction`, `Multiplication`, `Division`
- **Discriminator Column:** `type` - determines which subclass to instantiate
- **Factory Method:** `Calculation.create()` - returns appropriate subclass
- **Polymorphic Behavior:** Each subclass implements `get_result()` differently
- **Operands:** `a` and `b` are stored as floating-point columns
- **Ownership:** `user_id` is a foreign key to `users.id`
- **Result:** Computed on demand; it is not a database column

**Key Features:**
```python
# Factory creates correct subclass
calc = Calculation.create('add', user_id, 1, 2)
assert isinstance(calc, Addition)
assert calc.result == 3

# Polymorphic query returns mixed types
calculations = session.query(Calculation).all()
# Each maintains its specific type (Addition, Division, etc.)
```

### 2. Pydantic Schemas (`app/schemas/calculation.py`)

**Schemas Created:**
- `CalculationType` - Enum for valid calculation types
- `CalculationBase` - Base schema with common fields
- `CalculationCreate` - For creating calculations (accepts `a`, `b`, and `type`)
- `CalculationUpdate` - For updating calculations (all fields optional)
- `CalculationRead` - For reading calculations (includes computed fields)

**Validation Features:**
- Field validators for type normalization
- Model validators for cross-field validation
- Division-by-zero prevention for a zero divisor
- Validation for the two numeric operands
- Clear error messages for invalid data

### 3. Database Configuration

- `app/database.py` - SQLAlchemy engine, session management, Base class
- `app/core/config.py` - Pydantic settings for configuration
- `app/models/user.py` - User model with relationship to calculations

### 4. Comprehensive Tests

**Model and schema tests cover:**
- Each binary operation and the polymorphic factory
- Computed-on-demand results and division-by-zero handling
- The `user_id` foreign-key target
- Type validation, UUID validation, and response-schema conversion

**API Integration Tests (5 existing tests):**
- FastAPI endpoint tests still passing

## What Makes It Polymorphic

1. **Single Table, Multiple Types:** All calculations stored in one table with `type` discriminator
2. **Automatic Type Resolution:** SQLAlchemy returns correct subclass (Addition, Division, etc.)
3. **Factory Pattern:** `Calculation.create()` abstracts object creation
4. **Common Interface, Different Behavior:** All have `get_result()`, each implements differently
5. **Type Safety:** `isinstance()` checks work correctly for subclasses

## Focused Test Results

```
✓ 18 model and schema tests PASSED
```

## Key Design Patterns Demonstrated

1. **Polymorphic Inheritance** - SQLAlchemy single-table inheritance
2. **Factory Pattern** - `Calculation.create()` method
3. **Template Method** - Abstract `get_result()` implemented by subclasses
4. **Data Transfer Objects** - Pydantic schemas as DTOs
5. **Dependency Injection** - `get_db()` for database sessions

## Division-by-Zero Validation

The schema and calculation model both reject division by zero before returning a result:
```python
if self.type == CalculationType.DIVISION and self.b == 0:
    raise ValueError("Cannot divide by zero")
```

## Module Alignment

This implementation perfectly aligns with Module 11 requirements:
- ✅ Calculation model with SQLAlchemy
- ✅ Pydantic schemas for validation
- ✅ Factory pattern for calculation types
- ✅ Focused model and schema tests
- ✅ No database CRUD routes yet
- ✅ Polymorphic relationships demonstrated

## Next Steps (Module 12)

Module 12 will add:
- FastAPI routes for calculations CRUD
- Database integration with actual PostgreSQL
- Authentication/authorization
- Full API implementation

## Files Created/Modified

```
✓ requirements.txt - Added SQLAlchemy, psycopg2-binary, pydantic-settings
✓ app/core/config.py - Settings configuration
✓ app/database.py - Database configuration
✓ app/models/user.py - User model
✓ app/models/calculation.py - Polymorphic calculation models
✓ app/schemas/calculation.py - Pydantic validation schemas
✓ tests/integration/test_calculation.py - Polymorphic behavior tests
✓ tests/integration/test_calculation_schema.py - Schema validation tests
✓ .env.example - Environment configuration template
```

## Running Tests

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run polymorphic model tests
pytest tests/integration/test_calculation.py -v

# Run schema validation tests
pytest tests/integration/test_calculation_schema.py -v

# Run with coverage
pytest tests/integration/ --cov=app --cov-report=html
```
