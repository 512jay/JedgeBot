# ✅ How to Add a New Database Table in JedgeBot

This guide outlines a clean, consistent, and scalable process for adding new tables to the JedgeBot backend using SQLAlchemy and Alembic. This includes setting up the model, migration, and API endpoint, using a clean modular structure.

---

## 🧱 General Principles
- **One major responsibility per table/module** (e.g. `user_profiles`, `portfolios`, `transactions`).
- Each module lives in its own folder (e.g. `backend/users/`, `backend/profiles/`).
- Each module contains files for: models, schemas, services, queries, routes, and db setup.
- Start small and iterate, designing for future extensibility.

---

## 📁 Folder and File Structure

```
backend/
  user_profiles/
    ├── __init__.py
    ├── models.py                # SQLAlchemy model
    ├── schemas.py               # Pydantic schemas
    ├── queries.py               # SQL queries
    ├── services.py              # Business logic
    ├── routes.py                # FastAPI endpoints
    └── profiles_db.py           # Optional: separate DB session config
```

---

## 🔁 Step-by-Step: Creating a New Table with Alembic

### ✅ Step 1: Define the Model
Create your SQLAlchemy model in `models.py`. Example:

```python
# /backend/user_profiles/models.py
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    username = mapped_column(String, unique=True, nullable=True)
    display_name = mapped_column(String, nullable=True)
    avatar_url = mapped_column(String, nullable=True)
    timezone = mapped_column(String, default="UTC")
    created_at = mapped_column(DateTime, default=datetime.utcnow)
```

Ensure it's imported in your metadata scope (e.g., via `models/__init__.py`).

---

### ✅ Step 2: Generate the Alembic Migration

```bash
alembic revision --autogenerate -m "create user_profiles table"
```

Check the generated migration file under `alembic/versions/` to confirm it contains the new table.

---

### ✅ Step 3: Apply the Migration

```bash
alembic upgrade head
```

---

### ✅ Step 4: Add Schemas
Create your Pydantic schemas in `schemas.py`:

```python
class UserProfileCreate(BaseModel):
    username: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    timezone: Optional[str] = "UTC"

class UserProfileRead(UserProfileCreate):
    id: UUID
    user_id: UUID
    created_at: datetime
```

---

### ✅ Step 5: Add Routes
Define basic FastAPI routes in `routes.py`:

```python
@router.post("/profile", response_model=UserProfileRead)
def create_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    ...
```

Then mount in `main.py`:
```python
from backend.user_profiles.routes import router as profile_router
app.include_router(profile_router, prefix="/users")
```

---

### ✅ Step 6: Add Tests and Docs
Use `tests/unit/user_profiles/test_routes.py` to verify profile creation.
Add a docstring to `models.py` and route methods for clarity.

---

### ✅ Summary Checklist

- [x] Create SQLAlchemy model
- [x] Ensure it's imported by Alembic metadata
- [x] Generate Alembic migration
- [x] Apply migration
- [x] Create Pydantic schemas
- [x] Implement API routes
- [x] Mount routes into app
- [x] Write basic test cases
- [ ] Document decisions and optional future fields

---

Following this refactored guide ensures a clean, scalable workflow for database tables in JedgeBot while minimizing unnecessary migrations or features. Start lean, then grow.
