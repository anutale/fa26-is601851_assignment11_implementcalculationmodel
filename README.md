# IS601 Calculator API

A small FastAPI calculator project with a browser-based interface, arithmetic API endpoints, and SQLAlchemy/Pydantic examples for calculation models and schemas.

## Features

- Browser calculator served at `/`
- JSON endpoints for addition, subtraction, multiplication, and division
- Input validation and JSON error responses
- SQLAlchemy models demonstrating polymorphic calculation types
- Pydantic schemas for calculation data
- Unit, integration, and Playwright end-to-end tests

The database models and schemas are not currently connected to the arithmetic API routes; calculations submitted to `/add`, `/subtract`, `/multiply`, and `/divide` are not stored.

The SQLAlchemy `Calculation` model stores `id`, the owning user's foreign-key `user_id`, operands `a` and `b`, and the operation `type`. Its `result` property computes the answer on demand rather than storing it in the database.

The Pydantic `CalculationCreate` schema accepts `a`, `b`, and `type` (`add`, `sub`, `multiply`, or `divide`). `CalculationRead` returns the calculation fields along with its computed result.

`Calculation.create()` is a factory method that accepts those short names (or the full operation names) and creates the matching polymorphic SQLAlchemy model.

## Requirements

- Python 3.10 or later
- For end-to-end tests: Chromium, installed through Playwright
- Optional for the Docker Compose setup: Docker with the Compose plugin

## Run locally

Create and activate a virtual environment, then install the pinned dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the application:

```bash
uvicorn main:app --reload
```

Open the calculator at <http://127.0.0.1:8000>. Interactive API documentation is available at <http://127.0.0.1:8000/docs>.

## API

Each operation accepts two numbers in a JSON request body and returns the result:

```bash
curl -X POST http://127.0.0.1:8000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5}'
```

Successful response:

```json
{"result": 15}
```

Available endpoints:

| Method | Path | Operation |
| --- | --- | --- |
| `POST` | `/add` | Add `b` to `a` |
| `POST` | `/subtract` | Subtract `b` from `a` |
| `POST` | `/multiply` | Multiply `a` by `b` |
| `POST` | `/divide` | Divide `a` by `b` |

Division by zero returns HTTP `400` with an `error` field:

```json
{"error": "Cannot divide by zero!"}
```

## Tests

Run the unit and integration tests:

```bash
pytest tests/unit tests/integration
```

The end-to-end tests launch the app and use Playwright Chromium:

```bash
python -m playwright install chromium
pytest tests/e2e
```

To run all tests, including end-to-end tests, use `pytest` after installing Chromium.

## Docker Compose

Start the web app, PostgreSQL, and pgAdmin services:

```bash
docker compose up --build
```

- Calculator: <http://localhost:8000>
- pgAdmin: <http://localhost:5050> (local development credentials are defined in `docker-compose.yml`)
- PostgreSQL: `localhost:5432`

The Compose file supplies `DATABASE_URL` to the application container. The database services support the SQLAlchemy model work; the calculator routes themselves do not currently use the database.

## Project layout

```text
.
├── .env.example                    Example database configuration
├── .gitignore
├── .github/
│   └── workflows/
│       └── test.yml                CI workflow
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py               Environment-based settings
│   ├── database.py                 SQLAlchemy engine and session setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── calculation.py          Polymorphic calculation models
│   │   └── user.py                 User model
│   ├── operations/
│   │   └── __init__.py             Arithmetic functions
│   └── schemas/
│       ├── __init__.py
│       └── calculation.py          Pydantic calculation schemas
├── templates/
│   └── index.html                  Browser calculator UI
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 Playwright and server fixtures
│   ├── e2e/
│   │   ├── __init__.py
│   │   └── test_e2e.py             Browser tests
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_calculation.py     Calculation model tests
│   │   ├── test_calculation_schema.py
│   │   └── test_fastapi_calculator.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_calculator.py      Arithmetic function tests
├── Dockerfile
├── LICENSE
├── MODULE11_SUMMARY.md
├── README.md
├── docker-compose.yml
├── main.py                         FastAPI app and arithmetic endpoints
├── pytest.ini                      Pytest configuration
└── requirements.txt                Pinned Python dependencies
```
