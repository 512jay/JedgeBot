// /frontend/src/__tests__/setupTestUser.test.js

import { describe, expect, it, beforeAll, afterAll } from 'vitest';
import { setupTestUser } from '@/../test-utils/setupTestUser';

describe('setupTestUser utility', () => {
  let testUser;

  beforeAll(async () => {
    try {
      testUser = await setupTestUser();
    } catch (error) {
      console.error('🚨 setupTestUser failed in beforeAll:', error);
    }
  });

  afterAll(async () => {
    if (testUser?.cleanup) {
      await testUser.cleanup();
    }
  });

  it('should return a valid cookie after login', () => {
    expect(testUser).toBeDefined();
    const cookie = testUser.getCookies?.();
    expect(cookie).toBeDefined();
    expect(typeof cookie).toBe('string');
  });

  it('should allow the user to login with correct credentials', async () => {
    const res = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
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
        Cookie: testUser.getCookies?.(),
      },
      body: JSON.stringify({ email: testUser.email }),
    });

    expect([200, 404]).toContain(res.status); // 404 is okay if already deleted
  });
});
