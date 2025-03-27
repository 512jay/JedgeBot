// /frontend/src/features/auth/__tests__/auth_api.test.js
// Unit tests for authentication API functions using Vitest

import { describe, it, expect, vi, beforeEach } from "vitest";
import * as authApi from "@/api/auth_api";
import { fetchWithCredentials } from "@/api/api_client";

// Mock fetchWithCredentials so we can control API responses
vi.mock("@/api/api_client", () => ({
  fetchWithCredentials: vi.fn(),
}));

// Simulate global fetch for login, which does not use fetchWithCredentials
global.fetch = vi.fn();

describe("auth_api.js", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("register()", () => {
    it("calls the correct URL with user data", async () => {
      const mockUserData = { email: "test@example.com", password: "password" };
      fetchWithCredentials.mockResolvedValueOnce({ ok: true });

      await authApi.register(mockUserData);

      expect(fetchWithCredentials).toHaveBeenCalledWith(
        expect.stringContaining("/auth/register"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify(mockUserData),
        })
      );
    });
  });

  describe("login()", () => {
    it("returns data on successful login", async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ access_token: "abc123" }),
      };

      fetch.mockResolvedValueOnce(mockResponse);

      const data = await authApi.login("user@example.com", "pass123");

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/auth/login"),
        expect.objectContaining({
          method: "POST",
          credentials: "include",
        })
      );

      expect(data).toEqual({ access_token: "abc123" });
    });

    it("throws an error on failed login", async () => {
      const mockError = {
        ok: false,
        status: 401,
        json: async () => ({ detail: "Invalid credentials" }),
      };

      fetch.mockResolvedValueOnce(mockError);

      await expect(authApi.login("bad@example.com", "wrongpass")).rejects.toMatchObject({
        message: "Invalid credentials",
        status: 401,
        detail: "Invalid credentials",
      });
    });
  });

  describe("logout()", () => {
    it("calls the correct endpoint with POST", async () => {
      fetchWithCredentials.mockResolvedValueOnce({ ok: true });

      await authApi.logout();

      expect(fetchWithCredentials).toHaveBeenCalledWith(
        expect.stringContaining("/auth/logout"),
        { method: "POST" }
      );
    });
  });

  describe("checkAuthentication()", () => {
    it("calls the /auth/check endpoint", async () => {
      fetchWithCredentials.mockResolvedValueOnce({ user: { id: 1 } });

      await authApi.checkAuthentication();

      expect(fetchWithCredentials).toHaveBeenCalledWith(
        expect.stringContaining("/auth/check")
      );
    });
  });

  describe("refreshToken()", () => {
    it("calls the /auth/refresh endpoint with POST", async () => {
      fetchWithCredentials.mockResolvedValueOnce({ token: "newToken" });

      await authApi.refreshToken();

      expect(fetchWithCredentials).toHaveBeenCalledWith(
        expect.stringContaining("/auth/refresh"),
        { method: "POST" }
      );
    });
  });
});
