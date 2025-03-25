# ✅ How to Add a New Database Table in JedgeBot

This guide outlines a clean, consistent, and scalable process for adding new tables to the JedgeBot backend using SQLAlchemy and Alembic, modeled on the structure used in the `auth` system. This process also supports future migration to a dedicated database if needed.

---

## 🧱 General Principles
- **One major responsibility per table/module** (e.g. `users`, `portfolios`, `transactions`).
- Each module lives in its own folder (e.g. `backend/users/`).
- Each module contains files for: models, schemas, services, queries, routes, and db setup.
- Start small and iterate, designing for future extensibility.

---

## 📁 Folder and File Structure

```
backend/
  users/
    ├── __init__.py
    ├── models.py                # SQLAlchemy models
    ├── schemas.py               # Pydantic schemas
    ├── queries.py               # SQL queries and helpers
    ├── services.py              # Business logic and orchestration
    ├── routes.py                # FastAPI route handlers
    └── users_db.py              # DB engine and session config (optional)
```

> 📌 If this table might later move to its own database, isolate DB setup in `users_db.py` like `auth_db.py` does.

---

## ⚙️ Checklist for Adding a New Table

### 1. **Design Your Table**
- Choose a clear single responsibility.
- Identify required vs. optional fields.

### 2. **Create Alembic Migration**
- Write or auto-generate the Alembic migration:
  ```bash
  alembic revision -m "add users table"
  ```
- Edit the generated script in `alembic/versions/` to define the new table.
- Apply the migration:
  ```bash
  alembic upgrade head
  ```

### 3. **Implement Models** (`models.py`)
- Define SQLAlchemy ORM models.
- Use `Base = declarative_base()` if needed.
- Set `nullable=False` for required fields.

### 4. **Implement Schemas** (`schemas.py`)
- Create `Base`, `Create`, `Update`, and `Read` Pydantic schemas.
- Use field aliases if necessary to match frontend naming.

### 5. **Write Queries** (`queries.py`)
- Add reusable query logic here.
- Example: get user by ID, get users by manager ID, etc.

### 6. **Write Services** (`services.py`)
- Use this layer to house your business logic.
- Coordinate data validation, DB access, and cross-table logic.

### 7. **Define Routes** (`routes.py`)
- Add FastAPI route handlers here.
- Mount your routes in `main.py` or `dev_routes.py`.

### 8. **Hook Up to the App**
- Import and include your router:
  ```python
  from backend.users.routes import router as users_router
  app.include_router(users_router, prefix="/users")
  ```

### 9. **Create Tests**
- Add unit tests and integration tests:
  - `tests/unit/users/test_routes.py`
  - `tests/integration/users/test_services.py`

---

## 🔄 Updating Existing Tables With Required Fields

### If you're adding a **new required field** to a table with existing rows:

1. **Make it nullable in the DB at first** in Alembic:
   ```python
   op.add_column("users", sa.Column("username", sa.String(), nullable=True))
   ```

2. **Backfill a default value** for all rows:
   ```python
   op.execute("UPDATE users SET username = 'placeholder' WHERE username IS NULL")
   ```

3. **Then make it non-nullable** in a follow-up migration:
   ```python
   op.alter_column("users", "username", nullable=False)
   ```

4. **Update model and schema validation.**

---

## 🔄 Optional: Move Table to Its Own DB

1. Create a new database URI and engine in `users_db.py`:
   ```python
   # /backend/users/users_db.py
   engine = create_engine(USERS_DB_URI)
   SessionLocal = sessionmaker(bind=engine)
   Base = declarative_base()
   ```

2. Update `models.py` to use this `Base`.
3. Update Alembic or write raw migrations if needed.
4. Update services and queries to use the new `SessionLocal`.

> 🔐 Consider security and data access isolation if moving to its own DB.

---

## 🧪 Testing Tips
- Always test:
  - Creation, retrieval, update, and deletion.
  - Validation errors.
  - Unique constraints.
  - Relationships (e.g. foreign keys).

---

## ✅ Summary Checklist

- [ ] Design table structure (fields, types, relationships)
- [ ] Generate Alembic migration
- [ ] Define SQLAlchemy model
- [ ] Create Pydantic schemas
- [ ] Add queries
- [ ] Implement services
- [ ] Define FastAPI routes
- [ ] Mount routes into the app
- [ ] Write unit & integration tests
- [ ] (Optional) Setup dedicated DB file if needed
- [ ] Document decisions and defaults

---

This workflow keeps the code modular, testable, and extensible, and allows you to migrate parts of your system to separate databases as your platform grows.

