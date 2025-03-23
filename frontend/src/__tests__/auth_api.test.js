/// <reference types="vitest" />
import {
  register,
  login,
  logout,
  checkAuthentication,
  refreshToken,
} from "../api/auth_api";

import * as client from "../api/api_client";

// Mock environment variable
const API_URL = "http://localhost:8000";

vi.mock("../api/api_client", () => ({
  fetchWithCredentials: vi.fn(),
}));

describe("auth_api", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("register() calls correct endpoint and payload", async () => {
    const userData = { email: "test@example.com", password: "1234" };
    await register(userData);

    expect(client.fetchWithCredentials).toHaveBeenCalledWith(
      `${API_URL}/auth/register`,
      {
        method: "POST",
        body: JSON.stringify(userData),
      }
    );
  });

  test("login() calls correct endpoint and payload", async () => {
    await login("user@test.com", "secret");
    expect(client.fetchWithCredentials).toHaveBeenCalledWith(
      `${API_URL}/auth/login`,
      {
        method: "POST",
        body: JSON.stringify({ email: "user@test.com", password: "secret" }),
      }
    );
  });

  test("logout() posts to /auth/logout", async () => {
    await logout();
    expect(client.fetchWithCredentials).toHaveBeenCalledWith(
      `${API_URL}/auth/logout`,
      { method: "POST" }
    );
  });

  test("checkAuthentication() hits /auth/check", async () => {
    await checkAuthentication();
    expect(client.fetchWithCredentials).toHaveBeenCalledWith(
      `${API_URL}/auth/check`
    );
  });

  test("refreshToken() posts to /auth/refresh", async () => {
    await refreshToken();
    expect(client.fetchWithCredentials).toHaveBeenCalledWith(
      `${API_URL}/auth/refresh`,
      { method: "POST" }
    );
  });
});
