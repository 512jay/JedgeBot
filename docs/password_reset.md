# 🔐 Password Reset System (JedgeBot)

This document explains the purpose, flow, and backend implementation of the password reset system for the JedgeBot platform.

## ✨ Features

- Secure password reset tokens generated and stored per user
- Tokens expire after 30 minutes
- Used tokens cannot be reused
- Fully tested integration with user authentication system
- Token lookup avoids email enumeration attacks

## 🔄 Password Reset Flow

1. User submits their email via `/auth/forgot-password`
2. System:
   - Validates the email exists (quietly)
   - Generates and stores a secure token
   - Sends (or prints) the token for the user
3. User visits frontend form and submits:
   - The reset token
   - A new password
4. Backend:
   - Verifies token is valid and not expired or used
   - Updates user's password hash
   - Marks token as used
5. User can now log in with their new password

## 🔒 Security

- All `/forgot-password` requests return 200 to prevent email enumeration.
- Expired and used tokens are rejected with proper error messaging.
- Password hashes use `bcrypt` (via `passlib`).

## 🛠 Tech Notes

- Password reset tokens are stored in `password_reset_tokens` table
- Linked to `users.id` with `ondelete="CASCADE"`
- Created with `secrets.token_urlsafe(48)`
- ORM: SQLAlchemy
