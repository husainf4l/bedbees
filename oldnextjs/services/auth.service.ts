import { User, AuthState, LoginResponse, RegisterDto, Role } from '../types/auth';

class AuthService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3003/api';
  }

  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || error.message || 'Login failed');
    }
    
    const data = await response.json();
    localStorage.setItem('accessToken', data.accessToken);
    if (data.refreshToken) {
      localStorage.setItem('refreshToken', data.refreshToken);
    }
    return data;
  }

  async register(registerData: RegisterDto): Promise<LoginResponse> {
    // Set default role to TRAVELER if not provided
    const dataWithDefaults: RegisterDto = {
      ...registerData,
      role: registerData.role || Role.TRAVELER
    };

    const response = await fetch(`${this.baseUrl}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dataWithDefaults)
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || error.message || 'Registration failed');
    }
    
    const data = await response.json();
    localStorage.setItem('accessToken', data.accessToken);
    if (data.refreshToken) {
      localStorage.setItem('refreshToken', data.refreshToken);
    }
    return data;
  }

  // Deprecated - use register instead
  async signupTraveler(signupData: RegisterDto): Promise<LoginResponse> {
    return this.register({ ...signupData, role: Role.TRAVELER });
  }

  // Deprecated - use register instead  
  async signupHost(signupData: RegisterDto): Promise<LoginResponse> {
    return this.register({ ...signupData, role: Role.HOST });
  }
  
  async getCurrentUser(): Promise<User> {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${this.baseUrl}/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) {
      if (response.status === 401) {
        this.logout();
        throw new Error('Session expired. Please log in again.');
      }
      const error = await response.json();
      throw new Error(error.error || error.message || 'Failed to get user info');
    }

    return response.json();
  }

  logout(): void {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('accessToken');
  }

  getToken(): string | null {
    return localStorage.getItem('accessToken');
  }

  getAuthHeaders(): Record<string, string> {
    const token = this.getToken();
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
  }
}

export const authService = new AuthService();
export type { User, AuthState, LoginResponse, RegisterDto };