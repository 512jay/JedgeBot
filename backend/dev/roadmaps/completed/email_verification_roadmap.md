# Email Verification Roadmap for JedgeBot

**Purpose:** Implement secure email verification and password reset flows using MailHog in development and SES in production. This document outlines the technical steps and files involved.

---

## ✅ Goals

1. Send email upon registration (with verification link)
2. Track whether an email is verified in the database
3. Allow users to verify via a secure token link
4. Send email for password reset requests
5. Redirect user to login or dashboard after verification

---

## 🧩 Plan Breakdown

### 1. Add `is_email_verified` to `User` model

```python
is_email_verified = Column(Boolean, default=False)
```

**Steps:**
- Modify the SQLAlchemy model (`User`)
- Generate migration:
  ```bash
  alembic revision --autogenerate -m "add email verified"
  ```
- Apply migration:
  ```bash
  alembic upgrade head
  ```

---

### 2. Generate Email Verification Token

**Function (e.g., in `auth_services.py` or new `email_tokens.py`)**

```python
from datetime import datetime, timedelta
from jose import jwt

def create_email_verification_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {"sub": email, "exp": expire, "type": "verify"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

---

### 3. Send Verification Email

**Modify `/register` route:**

```python
from backend.notifications.email_service import send_email

token = create_email_verification_token(request.email)
verify_link = f"http://localhost:3000/verify-email?token={token}"
send_email(
    to=request.email,
    subject="Verify your email",
    body=f"Click to verify: {verify_link}"
)
```

---

### 4. Create `/auth/verify-email` Route

```python
@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "verify":
            raise ValueError("Invalid token type")
        user = get_user_by_email(db, payload["sub"])
        if not user:
            raise HTTPException(404, "User not found")
        user.is_email_verified = True
        db.commit()
        return {"message": "Email verified successfully"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
```

---

### 5. Password Reset Email

- Use existing `create_password_reset_token()`
- Send a reset link using `send_email()` to user

---

### Optional: Prevent Unverified Login

Inside `/login`, check:

```python
if not user.is_email_verified:
    raise HTTPException(status_code=403, detail="Email not verified")
```

---

## 🔁 Flexible Environment Support

- Local: MailHog (`localhost:1025`, Web UI `localhost:8025`)
- Production: SES/SendGrid/Mailgun via `.env` switching

---

## 📂 Suggested File Locations

- `email_service.py` → `backend/notifications/`
- `create_email_verification_token()` → `auth_services.py` or `email_tokens.py`
- `/auth/verify-email` → in `auth_routes.py`
- Token validation → `auth_services.py`

---

Let this serve as the step-by-step blueprint to build and test a secure and professional email verification system for JedgeBot.

