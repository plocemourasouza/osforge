---
name: python-fastapi
description: FastAPI REST API template principles. SQLAlchemy, Pydantic, Alembic.
---

# FastAPI API Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Language | Python 3.11+ |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Migrations | Alembic |
| Auth | JWT + passlib |

---

## Directory Structure

```
project-name/
├── alembic/             # Migrations
├── app/
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings
│   ├── database.py      # DB connection
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routers/         # API routes
│   ├── services/        # Business logic
│   ├── dependencies/    # DI
│   └── utils/
├── tests/
├── .env.example
└── requirements.txt
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Async | async/await throughout |
| Dependency Injection | FastAPI Depends |
| Pydantic v2 | Validation + serialization |
| SQLAlchemy 2.0 | Async sessions |

---

## Best Practices

- Use async everywhere
- Pydantic v2 for validation
- SQLAlchemy 2.0 async sessions
- Alembic for migrations
- pytest-asyncio for tests
