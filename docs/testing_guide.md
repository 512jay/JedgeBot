# 🧪 JedgeBot Testing Guide

This guide documents how testing is structured and implemented in the JedgeBot project. It includes the types of tests, current coverage, best practices, and a roadmap for future testing.

---

## ✅ Test Types Used

| Type | Purpose | Tools |
|------|---------|-------|
| **Unit Test** | Test a single function or component in isolation | Vitest |
| **Integration Test** | Test how components/services work together (e.g. context + routing) | Vitest + React Testing Library |
| **End-to-End (E2E)** | Simulate full user flows in a real browser | (Planned) Playwright |
| **Regression Test** | Prevent recurrence of previously fixed bugs | Vitest |
| **Smoke Test** | Ensure app starts and key paths don’t crash | Vitest |

---

## 🧩 Feature-Based Test Matrix

| Feature | Unit | Integration | Notes |
|---------|------|-------------|-------|
| Sidebar | ✅ Renders, icons, layout | ✅ Logout calls and redirect | `Sidebar.test.jsx` |
| AuthContext | ✅ Handles logout, fetch failures | ✅ With sidebar + router | Wrapped in `AuthProvider` |
| Login | 🔜 Form validation | 🔜 Full login flow | To be implemented |
| Dashboard | ✅ Renders cards | ✅ Role-based routing | Covers client/manager views |
| Profile Page | 🔜 | 🔜 | Add after route is live |

---

## 🔍 Testing Utilities

- `renderWithProviders.jsx` wraps components with `AuthProvider` and `MemoryRouter`
- `authHelpers.js` includes `fetchWithRefresh`, now patched to use `VITE_API_BASE_URL`
- `LocationDisplay` is used in routing tests to confirm URL changes

---

## 🔄 Testing Setup

- All fetches route through `VITE_API_BASE_URL` — no hardcoded URLs
- No `.env.test` is used; real environment values apply during tests
- Tests run with:
  ```bash
  pnpm test
  ```

---

## 🧠 Best Practices

- Always wrap router-dependent components in `MemoryRouter` during tests
- Clear mocks after each test with `vi.restoreAllMocks()`
- Use `screen.getByRole` or `getByTestId` for accessible queries
- Add regression tests for every bug fixed (especially auth, routing, etc.)

---

## 🧪 Example Test: Logout Integration

```jsx
it("logs out and navigates to /login", async () => {
  renderWithProviders(...);
  fireEvent.click(screen.getByRole("button", { name: /logout/i }));

  await waitFor(() => {
    expect(authApi.logout).toHaveBeenCalled();
    expect(screen.getByTestId("location-display").textContent).toBe("/login");
  });
});
```

---

## 🔭 Testing Roadmap

- [ ] Add integration test for login + token handling
- [ ] Add tests for manager > client dashboard access
- [ ] Add account creation/removal tests
- [ ] Add Playwright setup for full E2E testing
- [ ] Add regression tests for known bugs (like token expiration)

---

## 📂 File Locations

| Purpose | Folder |
|---------|--------|
| Unit/Integration Tests | `/frontend/src/__tests__` |
| Test Utilities | `/frontend/src/test-utils` |
| Future E2E Tests | `/frontend/e2e` |

---

Happy testing! 🚀