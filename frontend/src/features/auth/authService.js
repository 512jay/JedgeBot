// /frontend/src/features/auth/authService.js
// Provides high-level auth workflows using auth API + AuthContext
// Purpose: Centralize login/logout workflows, so Login.jsx and others stay clean.

import { login as apiLogin, logoutApi } from "@auth/auth_api";
import { useAuth } from "@/hooks/useAuth"; // /frontend/src/hooks/useAuth.js


/**
 * High-level authentication service that combines raw API
 * calls with user state management from the AuthContext.
 */
export const useAuthService = () => {
  const { setUser, loadUserSession } = useAuth();

  /**
   * Performs login and loads user into context.
   * @param {string} email
   * @param {string} password
   */
  const login = async (email, password) => {
    await apiLogin(email, password);
    await loadUserSession();
  };

  /**
   * Logs out user and clears local context.
   */
  const logout = async () => {
    await logoutApi();
    setUser(null);
  };

  return { login, logout };
};
