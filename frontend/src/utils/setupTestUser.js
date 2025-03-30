// /frontend/src/utils/setupTestUser.js
// /frontend/test-utils/setupTestUser.js

let cookies = '';

export const setupTestUser = async (
  testUser = {
    email: `test-${Date.now()}@example.com`,
    password: 'Test1234!',
    confirmPassword: 'Test1234!',
    first_name: 'Test',
    last_name: 'User',
    role: 'client',
  }
) => {
  const { email, password } = testUser;

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

// ✅ Define helpers AFTER the main function
export const setupTestManagerUser = () =>
  setupTestUser({
    email: `manager-${Date.now()}@example.com`,
    password: 'Test1234!',
    confirmPassword: 'Test1234!',
    first_name: 'Manager',
    last_name: 'User',
    role: 'manager',
  });

export const setupTestClientUser = () =>
  setupTestUser({
    email: `client-${Date.now()}@example.com`,
    password: 'Test1234!',
    confirmPassword: 'Test1234!',
    first_name: 'Client',
    last_name: 'User',
    role: 'client',
  });
