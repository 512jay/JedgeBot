# 📘 Email Verification Flow – Frontend Roadmap

This document outlines the steps needed to implement frontend support for user registration, email verification, and login restriction until email is confirmed.

> 📁 Location: `frontend/dev/roadmaps/email_verification_frontend.md`

---

## ✅ Overview

The backend now supports:
- Sending a verification email with a token after registration
- A `/verify-email?token=...` route that marks the user as verified
- Blocking login for unverified users
- Resending verification tokens via `/auth/resend-verification`

Your job on the frontend is to:
- Handle registration feedback
- Process token links
- Display user-friendly messages
- Guide unverified users to verify

---

## 1. 📝 **Registration Flow**

- [ ] POST form to `/auth/register`
- [ ] On success: show message like:
  > "🎉 Registration successful! Please check your email to verify your account."
- [ ] Redirect to `/login`

---

## 2. 🔐 **Login Page Behavior**

- [ ] POST form to `/auth/login`
- [ ] If `403 Email not verified`, show:
  > "Your account hasn’t been verified yet. [Resend Verification Email]"

- [ ] If redirected from `/login?verified=true`, show:
  > "✅ Your email was successfully verified. Please log in."

- [ ] Disable login until verified (visually or via alert)

---

## 3. 📩 **Resend Verification Email**

- [ ] Add a button below login form:
  > "Didn’t get the email? [Resend it]"

- [ ] POST `{ email }` to `/auth/resend-verification`
- [ ] Show confirmation:
  > "If your account exists, we’ve sent a new verification link."

---

## 4. 🔗 **Verify Email Redirect**

- [ ] Create page: `/verify-email`
- [ ] On page load, read `token` from query string:
  ```js
  const token = new URLSearchParams(location.search).get("token")
# 📘 Email Verification Flow – Frontend Roadmap

This document outlines the steps needed to implement frontend support for user registration, email verification, and login restriction until email is confirmed.

> 📁 Location: `frontend/dev/roadmaps/email_verification_frontend.md`

---

## ✅ Overview

The backend now supports:
- Sending a verification email with a token after registration
- A `/verify-email?token=...` route that marks the user as verified
- Blocking login for unverified users
- Resending verification tokens via `/auth/resend-verification`

Your job on the frontend is to:
- Handle registration feedback
- Process token links
- Display user-friendly messages
- Guide unverified users to verify

---

## 1. 📝 **Registration Flow**

- [ ] POST form to `/auth/register`
- [ ] On success: show message like:
  > "🎉 Registration successful! Please check your email to verify your account."
- [ ] Redirect to `/login`

---

## 2. 🔐 **Login Page Behavior**

- [ ] POST form to `/auth/login`
- [ ] If `403 Email not verified`, show:
  > "Your account hasn’t been verified yet. [Resend Verification Email]"

- [ ] If redirected from `/login?verified=true`, show:
  > "✅ Your email was successfully verified. Please log in."

- [ ] Disable login until verified (visually or via alert)

---

## 3. 📩 **Resend Verification Email**

- [ ] Add a button below login form:
  > "Didn’t get the email? [Resend it]"

- [ ] POST `{ email }` to `/auth/resend-verification`
- [ ] Show confirmation:
  > "If your account exists, we’ve sent a new verification link."

---

## 4. 🔗 **Verify Email Redirect**

- [ ] Create page: `/verify-email`
- [ ] On page load, read `token` from query string:
  ```js
  const token = new URLSearchParams(location.search).get("token")

## 5.  💡 UX Enhancements (Optional)
 Use toast notifications or alerts

 Auto-focus on email field if unverified

 Add spinner/loading state for network calls

 Animate successful redirects