// /frontend/src/test-utils/setupTestUser.js
// Sets up a test user by registering, logging in, and preparing for cleanup.

let cookies = '';

export const setupTestUser = async (
  testUser = { email: 'testuser@example.com', password: 'Test1234!' }
) => {
  const { email, password } = testUser;

  // Register the test user
  await fetch('http://localhost:8000/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  // Log in to get the session cookie
  const loginRes = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!loginRes.ok) {
    throw new Error('Failed to log in test user');
  }

  cookies = loginRes.headers.get('set-cookie');

  return {
    email,
    password,
    getCookies: () => cookies,
    cleanup: async () => {
      await fetch('http://localhost:8000/auth/delete', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Cookie': cookies,
        },
        body: JSON.stringify({ email }),
      });
    },
  };
};
