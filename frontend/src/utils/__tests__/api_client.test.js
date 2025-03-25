/// <reference types="vitest" />
import {
  fetchWithCredentials,
  fetchMessage,
  fetchUserProfile,
} from "../../api/api_client";

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
  const BASE = "http://localhost:8000";

  beforeEach(() => {
    vi.stubEnv("VITE_API_URL", BASE);
    fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve("Welcome!"),
    });
  });

  test("calls fetchWithCredentials with full API_URL", async () => {
    const result = await fetchMessage();
    expect(fetch).toHaveBeenCalledWith(`${BASE}/`, expect.any(Object));
    expect(result).toBe("Welcome!");
  });
});

describe("fetchUserProfile", () => {
  const BASE = "http://localhost:8000";

  beforeEach(() => {
    vi.stubEnv("VITE_API_URL", BASE);
    fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ name: "Jane" }),
    });
  });

  test("calls fetchWithCredentials with full API_URL", async () => {
    const result = await fetchUserProfile();
    expect(fetch).toHaveBeenCalledWith(`${BASE}/profile`, expect.any(Object));
    expect(result).toEqual({ name: "Jane" });
  });
});
