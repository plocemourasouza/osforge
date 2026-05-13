# Python Patterns

**Trigger:** Python, FastAPI, Django, Flask, pip, poetry

---

## Project Structure

```
my_project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       └── services/
│           ├── __init__.py
│           └── user_service.py
├── tests/
│   ├── __init__.py
│   └── test_user.py
├── pyproject.toml
└── README.md
```

---

## FastAPI

### Basic API
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI()

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class User(BaseModel):
    id: int
    email: EmailStr
    name: str

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    # Create user logic
    return User(id=1, **user.dict())

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = await find_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Dependencies
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user

@app.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### Database (SQLAlchemy)
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

---

## Type Hints

```python
from typing import Optional, List, Dict, Union, TypeVar, Generic
from dataclasses import dataclass

# Basic types
def greet(name: str) -> str:
    return f"Hello, {name}"

# Optional (can be None)
def find_user(id: int) -> Optional[User]:
    ...

# Lists and dicts
def process_items(items: List[str]) -> Dict[str, int]:
    ...

# Union types (Python 3.10+: use |)
def parse(value: Union[str, int]) -> str:
    ...
# Or: def parse(value: str | int) -> str:

# Generics
T = TypeVar('T')

class Repository(Generic[T]):
    def get(self, id: int) -> Optional[T]:
        ...

    def save(self, item: T) -> T:
        ...

# Dataclasses
@dataclass
class Point:
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5
```

---

## Async Patterns

```python
import asyncio
from typing import List

# Basic async
async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Concurrent execution
async def fetch_all(urls: List[str]) -> List[dict]:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)

# With timeout
async def fetch_with_timeout(url: str, timeout: float = 5.0):
    try:
        return await asyncio.wait_for(fetch_data(url), timeout=timeout)
    except asyncio.TimeoutError:
        return None

# Semaphore for rate limiting
semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

async def rate_limited_fetch(url: str):
    async with semaphore:
        return await fetch_data(url)
```

---

## Testing (pytest)

```python
import pytest
from httpx import AsyncClient
from main import app

# Basic test
def test_add():
    assert add(2, 3) == 5

# Async test
@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/users",
            json={"email": "test@example.com", "name": "Test"}
        )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

# Fixtures
@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
def user_data():
    return {"email": "test@example.com", "name": "Test User"}

async def test_with_fixtures(db_session, user_data):
    user = User(**user_data)
    db_session.add(user)
    await db_session.commit()
    assert user.id is not None

# Parametrized tests
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("test", 4),
])
def test_length(input, expected):
    assert len(input) == expected

# Mocking
from unittest.mock import AsyncMock, patch

async def test_with_mock():
    with patch("services.fetch_data", new_callable=AsyncMock) as mock:
        mock.return_value = {"data": "test"}
        result = await some_function()
        assert result == {"data": "test"}
```

---

## Dependency Management

### Poetry
```bash
# Create project
poetry new my-project
poetry init

# Add dependencies
poetry add fastapi uvicorn
poetry add --group dev pytest pytest-asyncio

# Install
poetry install

# Run
poetry run python -m my_project.main
poetry run pytest

# Export requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

### pyproject.toml
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.0"
uvicorn = "^0.24.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
ruff = "^0.1.0"

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

## Best Practices

1. **Use type hints everywhere**
2. **Prefer `async def` for I/O operations**
3. **Use Pydantic for data validation**
4. **Write tests with pytest**
5. **Use `ruff` for linting (faster than flake8)**
6. **Use `black` for formatting**
7. **Handle errors explicitly, avoid bare `except`**
8. **Use virtual environments**
