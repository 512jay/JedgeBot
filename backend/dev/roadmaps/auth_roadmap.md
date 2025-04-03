# Auth Roadmap for JedgeBot

This file tracks upcoming features, improvements, and security enhancements related to the authentication system in the backend of JedgeBot.

---

## ✉️ Email Features

- [ ] Implement password reset via email
  - Generate and store reset tokens (JWT or UUID)
  - Create `/auth/forgot-password` and `/auth/reset-password` routes
  - Link to a frontend reset form
  - Integrate MailHog or SMTP (e.g. SendGrid)

- [ ] Email verification on signup
  - Send verification link to user email
  - Confirm token to activate account

- [ ] Resend verification link
  - Rate-limited endpoint to request resend


## 🔐 Security Enhancements

- [ ] Multi-factor authentication (MFA)
  - Email or TOTP-based 2FA

- [ ] Rate limiting for sensitive endpoints
  - Fine-tune login and password reset limits (SlowAPI in use)

- [ ] Session management
  - Revoke old sessions
  - Logout across all devices

- [ ] Secure cookie settings for production
  - Set `secure=True`, `samesite='Strict'` in prod


## 🧑‍💼 Admin Tools

- [ ] View all users and roles (admin only)
- [ ] Deactivate or ban accounts via admin panel
- [ ] Reset password manually for users


## 📜 Audit & Logging

- [ ] Log user activity (login, logout, password change)
- [ ] Add login history view to admin dashboard
- [ ] Alert on suspicious login activity


## 🔧 Dev / Maintenance

- [ ] Auto-delete deactivated or unverified accounts after X days
- [ ] Cleanup expired reset tokens
- [ ] Add `dev/routes.py` for quick manual testing


## 🔁 OAuth & Connected Accounts

- [ ] OAuth2 login support (Google, GitHub)
- [ ] View and revoke third-party app connections


## 👤 User Profile Enhancements

- [ ] Allow users to update email
- [ ] Allow users to change password
- [ ] Add settings for notification preferences, privacy, security
- [ ] Add `user_profiles` management endpoints (bio, location, etc.)


---

**Note:** This file is manually maintained and should be reviewed periodically as part of sprint planning or feature grooming.

File location: `/backend/dev/roadmap/auth_roadmap.md`
