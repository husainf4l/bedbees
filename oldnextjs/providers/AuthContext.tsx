"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import apiService from "@/services/api";
import { User, RegisterDto } from "@/types/auth";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<User>;
  signup: (signupData: RegisterDto) => Promise<User>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const checkAuth = useCallback(async () => {
    // Only run on client-side
    if (typeof window === 'undefined') {
      setLoading(false);
      return;
    }

    const token = localStorage.getItem("accessToken");
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      // Add a timeout to prevent hanging
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

      const response = await fetch(
        `${
          process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:3003/api"
        }/auth/me`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          signal: controller.signal,
        }
      );

      clearTimeout(timeoutId);

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else if (response.status === 401) {
        // Token is invalid, clear it
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        setUser(null);
      }
    } catch (err: unknown) {
      // Handle network errors, timeouts, etc.
      if (err instanceof Error && err.name === "AbortError") {
        console.warn("Auth check timed out - backend may be unavailable");
      } else {
        console.warn("Auth check failed - backend may be unavailable:", err);
      }
      // Don't clear user data on network errors to avoid unnecessary logouts
    } finally {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const data = (await apiService.login({ email, password })) as {
      accessToken: string;
      refreshToken: string;
      user: User;
    };

    // Only access localStorage on client-side
    if (typeof window !== 'undefined') {
      localStorage.setItem("accessToken", data.accessToken);
      localStorage.setItem("refreshToken", data.refreshToken);

      // Also set cookies for middleware
      document.cookie = `accessToken=${data.accessToken}; path=/; max-age=86400; samesite=strict`;
      document.cookie = `refreshToken=${data.refreshToken}; path=/; max-age=604800; samesite=strict`;
    }

    // Set user data immediately from login response
    setUser(data.user);

    // Return the user data for immediate use
    return data.user;
  };

  const signup = async (signupData: RegisterDto) => {
    const data = (await apiService.signup(signupData)) as {
      accessToken: string;
      refreshToken: string;
      user: User;
    };

    // Only access localStorage on client-side
    if (typeof window !== 'undefined') {
      localStorage.setItem("accessToken", data.accessToken);
      localStorage.setItem("refreshToken", data.refreshToken);

      // Also set cookies for middleware
      document.cookie = `accessToken=${data.accessToken}; path=/; max-age=86400; samesite=strict`;
      document.cookie = `refreshToken=${data.refreshToken}; path=/; max-age=604800; samesite=strict`;
    }

    // Set user data immediately from signup response
    setUser(data.user);

    // Return the user data for immediate use
    return data.user;
  };

  const logout = () => {
    // Only access localStorage on client-side
    if (typeof window !== 'undefined') {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");

      // Clear cookies
      document.cookie =
        "accessToken=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
      document.cookie =
        "refreshToken=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }

    setUser(null);
    router.push("/login");
  };

  const initializeCookies = () => {
    // Only run on client-side
    if (typeof window === 'undefined') return;

    const accessToken = localStorage.getItem("accessToken");
    const refreshToken = localStorage.getItem("refreshToken");

    if (accessToken) {
      document.cookie = `accessToken=${accessToken}; path=/; max-age=86400; samesite=strict`;
    }
    if (refreshToken) {
      document.cookie = `refreshToken=${refreshToken}; path=/; max-age=604800; samesite=strict`;
    }
  };

  useEffect(() => {
    initializeCookies();
    checkAuth();

    // Fallback: ensure loading is set to false after 10 seconds max
    const timeout = setTimeout(() => {
      setLoading(false);
    }, 10000);

    return () => clearTimeout(timeout);
  }, []);

  const value = {
    user,
    loading,
    login,
    signup,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
