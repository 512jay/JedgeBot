/// <reference types="vitest" />
import {
  fetchWithCredentials,
  fetchMessage,
  fetchUserProfile,
} from "../api/api_client";

// Mock fetch globally
global.fetch = vi.fn();

describe("fetchWithCredentials", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("sends fetch with credentials and JSON header", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ message: "Success" }),
    });

    await fetchWithCredentials("/api/test");

    expect(fetch).toHaveBeenCalledWith("/api/test", {
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });
  });

  test("merges custom headers", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({}),
    });

    await fetchWithCredentials("/api/with-headers", {
      headers: {
        Authorization: "Bearer 123",
      },
    });

    expect(fetch).toHaveBeenCalledWith("/api/with-headers", expect.objectContaining({
      headers: expect.objectContaining({
        Authorization: "Bearer 123",
        "Content-Type": "application/json",
      }),
    }));
  });

  test("throws error if response is not ok", async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 403,
    });

    await expect(fetchWithCredentials("/fail")).rejects.toThrow("HTTP Error: 403");
  });
});

describe("fetchMessage", () => {
  test("calls fetchWithCredentials with /", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve("Welcome!"),
    });

    const result = await fetchMessage();
    expect(fetch).toHaveBeenCalledWith("/", expect.any(Object));
    expect(result).toBe("Welcome!");
  });
});

describe("fetchUserProfile", () => {
  test("calls fetchWithCredentials with /profile", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ name: "Jane" }),
    });

    const result = await fetchUserProfile();
    expect(fetch).toHaveBeenCalledWith("/profile", expect.any(Object));
    expect(result).toEqual({ name: "Jane" });
  });
});
