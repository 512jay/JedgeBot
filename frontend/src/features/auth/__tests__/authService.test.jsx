// /frontend/src/features/auth/__tests__/authService.test.jsx

import { describe, it, vi, expect } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { AuthContext } from "@/context/auth-context";
import { useAuthService } from "../authService";

// ✅ Full mock of both login and logout
vi.mock("@auth/auth_api", async () => {
  return {
    login: vi.fn().mockResolvedValue({ user: { id: "123", email: "test@example.com" } }),
    logoutApi: vi.fn().mockResolvedValue({ message: "Mock logout complete" }),
  };
});

describe("authService", () => {
  it("calls loadUserSession after login", async () => {
    const loadUserSession = vi.fn();
    const wrapper = ({ children }) => (
      <AuthContext.Provider value={{ setUser: vi.fn(), loadUserSession }}>
        {children}
      </AuthContext.Provider>
    );

    const { result } = renderHook(() => useAuthService(), { wrapper });

    await act(() => result.current.login("test@example.com", "secret"));
    expect(loadUserSession).toHaveBeenCalled();
  });

  it("calls logoutApi and clears user", async () => {
    const setUser = vi.fn();
    const wrapper = ({ children }) => (
      <AuthContext.Provider value={{ setUser, loadUserSession: vi.fn() }}>
        {children}
      </AuthContext.Provider>
    );

    const { result } = renderHook(() => useAuthService(), { wrapper });
    await act(() => result.current.logout());
    expect(setUser).toHaveBeenCalledWith(null);
  });
});
