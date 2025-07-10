import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, register as apiRegister, getProfile, setToken, logout as apiLogout } from './api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setToken(token);
      getProfile().then(setUser).catch(() => setUser(null)).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (data) => {
    const res = await apiLogin(data);
    setToken(res.access_token);
    const profile = await getProfile();
    setUser(profile);
    return profile;
  };

  const register = async (data) => {
    await apiRegister(data);
    return login({ email: data.email, password: data.password });
  };

  const logout = async () => {
    await apiLogout();
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
} 