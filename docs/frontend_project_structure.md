# JedgeBot Frontend Structure Strategy

## ✅ Recommended Structure Overview (Post-Migration)

```
frontend/
├── public/                        # Static files
│   ├── images/
│   ├── logo.webp

├── src/
│   ├── assets/                    # Logos, icons, fonts
│   │   └── react.svg

│   ├── components/                # Reusable shared building blocks
│   │   ├── ui/                    # mdb-react-ui-kit based components
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── PieChart.jsx
│   │   │   ├── Table.jsx
│   │   │   ├── __tests__/
│   │   │       ├── Button.test.jsx
│   │   │       ├── Card.test.jsx
│   │   │       ├── PieChart.test.jsx
│   │   │       ├── Table.test.jsx
│   │   ├── layout/                # Layout elements
│   │   │   ├── Sidebar.jsx
│   │   │   ├── LoadingScreen.jsx
│   │   │   ├── __tests__/
│   │   │       ├── Sidebar.test.jsx

│   ├── context/                   # React contexts
│   │   └── AuthContext.jsx

│   ├── features/                  # Feature-based domain folders
│   │   ├── auth/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── ForgotPassword.jsx
│   │   │   ├── ResetPassword.jsx
│   │   │   ├── auth_api.js
│   │   │   ├── PrivateRoute.jsx
│   │   │   ├── __tests__/
│   │   │       ├── Login.test.jsx
│   │   │       ├── Register.test.jsx
│   │   │       ├── ForgotPassword.test.jsx
│   │   │       ├── ResetPassword.test.jsx
│   │   │       ├── auth_api.test.js
│   │   ├── dashboard/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DashboardCards.jsx
│   │   │   ├── views/
│   │   │   │   ├── FreeDashboard.jsx
│   │   │   │   ├── ClientDashboard.jsx
│   │   │   │   ├── ManagerDashboard.jsx
│   │   │   │   ├── EnterpriseDashboard.jsx
│   │   │   ├── __tests__/
│   │   │       ├── Dashboard.test.jsx
│   │   │       ├── DashboardCards.test.jsx
│   │   ├── landing/               # Public-facing pages (marketing)
│   │   │   ├── Landing.jsx
│   │   │   ├── Pricing.jsx        # (future)
│   │   │   ├── About.jsx          # (future)
│   │   │   ├── Contact.jsx        # (future)
│   │   │   ├── components/
│   │   │   │   ├── HeroSection.jsx
│   │   │   │   ├── PricingTable.jsx
│   │   │   │   ├── FAQSection.jsx
│   │   │   ├── __tests__/
│   │   │       ├── Landing.test.jsx
│   │   ├── enterprise/            # (future)
│   │   ├── clients/               # (future)
│   │   ├── settings/              # (future)
│   │   ├── app/
│   │   │   ├── App.jsx            # App shell / layout
│   │   │   ├── __tests__/
│   │   │   │   ├── AppLayout.test.jsx

│   ├── routes/                    # App-wide route definitions
│   │   └── AppRoutes.jsx

│   ├── utils/                     # Generic helpers
│   │   ├── apiClient.js
│   │   ├── authHelpers.js
│   │   ├── setupTestUser.js
│   │   ├── __tests__/
│   │       ├── api_client.test.js

│   ├── test-utils/                # Testing tools
│   │   ├── renderWithProviders.jsx
│   │   ├── setup.js

│   ├── styles/                    # Tailwind / global CSS
│   │   ├── global.css
│   │   ├── Landing.css
│   │   ├── Sidebar.css

│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
```

---

## 🚀 Strategy Benefits

### ✅ Feature-First Modularity
- Logical grouping by domain (`auth`, `dashboard`, `landing`, etc.)
- Easy to test, extend, and isolate features
- Encourages decoupled, scalable architecture

### ✅ Clear Reusables Layer
- `components/` is only for cross-feature UI pieces
- `layout/` and `ui/` layers support fast iteration with consistent design

### ✅ Alignment with Backend
- Mirrors `backend/auth`, `backend/users`, etc.
- Improves navigation and cross-team handoff

### ✅ DevX & Collaboration Friendly
- Predictable and easy to onboard new devs
- Well-suited for future scale, testing, and build optimizations

---

## ✅ Next Steps

- Move existing files into the structure above manually or using Git-aware tooling
- Clean up any broken imports (VS Code should catch most)
- Remove deprecated folders like `views/landing/` or `pages/` if migrated
- Place tests under `__tests__` folders within their respective features

---

## 🔄 Long-Term Evolution Ideas

- Expand `features/` to include `users/`, `subscriptions/`, `analytics/`, etc.
- Add `services/` and `hooks/` per feature for logic co-location
- Add Storybook for isolated UI development
- Support theming via global Tailwind config

---

This structure sets up JedgeBot’s frontend for maintainability, testability, and seamless collaboration as you scale into multi-role dashboards, landing pages, and broker management.

