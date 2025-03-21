# ✅ Password Reset Test Coverage

Integration tests located at:
`tests/integration/auth/test_password_reset.py`

## ✔️ Covered Scenarios

| Test # | Description |
|--------|-------------|
| 1 | Generate token for valid email |
| 2 | Request reset for invalid email |
| 3 | Use valid token to reset password |
| 4 | Reject reset with invalid token |
| 5 | Reject reused token |
| 6 | Reject expired token |

## 🧪 Notes

- Tests run against the real Postgres database
- Test tokens are created, used, and deleted cleanly
- All foreign key constraints are respected
