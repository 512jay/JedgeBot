// /frontend/test-utils/setupTestUser.js
// Utility for registering, logging in, and deleting a test user with saved cookies.

let cookies = '';

export const setupTestUser = async (
  testUser = {
    email: `test-${Date.now()}@example.com`,
    password: 'Test1234!',
    confirmPassword: 'Test1234!',
    first_name: 'Test',
    last_name: 'User'
  }
) => {
  const { email, password } = testUser;

  // Register the test user
  const registerRes = await fetch('http://localhost:8000/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(testUser),
  });

  if (!registerRes.ok) {
    const errorText = await registerRes.text();
    console.error('❌ Registration failed:', errorText);
    throw new Error('Registration failed');
  }

  // Log in to get the session cookie
  const loginRes = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  if (!loginRes.ok) {
    const errorText = await loginRes.text();
    console.error('❌ Login failed:', errorText);
    throw new Error('Failed to log in test user');
  }

  // Save cookies (needed for auth in tests)
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
