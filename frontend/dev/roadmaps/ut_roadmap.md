# Frontend UI Roadmap for JedgeBot

This document tracks current and upcoming priorities for the React + Vite frontend of the JedgeBot project. UI development uses `mdb-react-ui-kit` and all pages/components are structured for role-specific dashboards.

File location: `/frontend/dev/roadmap/ui_roadmap.md`

---

## 🚪 Authentication UI

- [x] Login page with MDB design and secure inputs
- [x] Register page with role selection and username field
- [x] Forgot Password page (basic)
- [ ] Implement Reset Password page
  - Accept reset token from URL
  - Add validation, token error states
- [ ] Show password strength indicator on register/reset
- [ ] Auto-focus + keyboard accessibility improvements


## 🧠 Role-Based Dashboards

- [x] Implement `DashboardView.jsx` with role switching logic
- [x] Create skeletons for Client, Manager, Enterprise, Free dashboards
- [ ] Connect dummy cards to real API data
- [ ] Display user email + role in header/sidebar
- [ ] Add loading state while session loads


## 🎛️ Universal Components

- [x] Sidebar with muted rose background (`#9A616D`)
- [x] Collapsible sidebar with icons
- [x] Add sidebar toggle animation
- [ ] Create universal `DashboardCard` component
- [ ] Toast / Snackbar system for alerts (e.g. login error, password reset success)


## ⚙️ Settings UI

- [ ] Add Settings page per role
- [ ] Connect settings to auth info
  - Email, role, last login, etc.
  - Allow password update
- [ ] Add tabs for: Profile | Security | Preferences


## 🔐 Cookie & Session Handling

- [x] Store JWT tokens in HTTP-only cookies
- [x] Use `/auth/check` and `/auth/me` to bootstrap session
- [ ] Add auto-refresh logic on token expiration
- [ ] Redirect to login on session expiration
- [ ] Hide dashboard routes if not authenticated


## 📬 Email Flow Integration

- [ ] Show "Email sent" alert on forgot password
- [ ] Handle reset token in URL with `useParams()`
- [ ] Graceful errors for expired/invalid tokens


## 🎨 Design Consistency

- [ ] Match all colors and fonts to brand style
- [ ] Define global design tokens / theme file
- [ ] Use consistent spacing and card layout


## 🧪 Testing / Dev

- [ ] Add `ComponentGallery.jsx` in `/dev/` to test UI elements in isolation
- [ ] Mock API responses for testing various login/role flows
- [ ] Create fake users to simulate role-based dashboards


---

**Note:** This roadmap is a living document for UI development. Check and update it regularly as features are implemented.
