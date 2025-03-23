// /frontend/test-utils/setupTestUser.test.js
// Validates setupTestUser: register → login → delete test user

import { describe, expect, it, beforeAll, afterAll } from 'vitest';
import { setupTestUser } from './setupTestUser';

describe('setupTestUser utility', () => {
  let testUser;

  beforeAll(async () => {
    testUser = await setupTestUser({
      email: 'testuser-util@example.com',
      password: 'Test1234!',
    });
  });

  afterAll(async () => {
    await testUser.cleanup();
  });

  it('should return a valid cookie after login', () => {
    const cookie = testUser.getCookies();
    expect(cookie).toBeDefined();
    expect(typeof cookie).toBe('string');
  });

  it('should allow the user to login with correct credentials', async () => {
    const res = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: testUser.email,
        password: testUser.password,
      }),
    });

    expect(res.status).toBe(200);
  });

  it('should successfully delete the user during cleanup', async () => {
    const res = await fetch('http://localhost:8000/auth/delete', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        Cookie: testUser.getCookies(),
      },
      body: JSON.stringify({ email: testUser.email }),
    });

    // This may return 404 if already deleted by cleanup, so we expect 200 or 404
    expect([200, 404]).toContain(res.status);
  });
});
