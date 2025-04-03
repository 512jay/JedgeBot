# 📘 API: Password Reset Endpoints

## `POST /auth/forgot-password`

Request a reset token for a known email.

### Request Body
```json
{
  "email": "user@example.com"
}
```

### Response (Always 200 OK)
```json
{
  "message": "If that email exists, a reset link has been sent."
}
```

## `POST /auth/reset-password`

Reset password using a valid token.

### Request Body
```json
{
  "token": "long-reset-token",
  "new_password": "NewSecurePass123"
}
```

### Successful Response
```json
{
  "message": "Password reset successfully."
}
```

### Error Responses
- 400: Token is invalid, expired, or already used
