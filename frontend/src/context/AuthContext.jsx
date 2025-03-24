import React, { createContext, useContext, useState } from "react";

// Create context
export const AuthContext = createContext(null); 


// Custom hook
export const useAuth = () => useContext(AuthContext);

// Provider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Example: { name, role }

  // In real app, populate user from API or cookie
  const login = (userData) => setUser(userData);
  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
