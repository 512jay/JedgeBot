// /frontend/src/hooks/useAuth.js
import { useContext } from "react";
import { AuthContext } from "../context/auth-context";

export const useAuth = () => useContext(AuthContext);
