import React, { createContext, useContext, useState, ReactNode } from 'react';
import { useLocation } from 'wouter';

interface User {
  id: string;
  name: string;
  email: string;
  age: string;
  gender: string;
  city: string;
  country: string;
}

interface AuthContextType {
  user: User | null;
  login: (userData: User) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [location, setLocation] = useLocation();

  const login = (userData: User) => {
    setUser(userData);
    setLocation('/dashboard');
  };

  const logout = () => {
    setUser(null);
    setLocation('/auth');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
