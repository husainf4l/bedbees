// API Service for direct backend communication
import { Role } from '../types/auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3003/api';

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  private async request(endpoint: string, options: RequestInit = {}, isRetry = false): Promise<unknown> {
    const url = `${this.baseURL}${endpoint}`;

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add authorization header if token exists (only on client-side)
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('accessToken');
      if (token) {
        (config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
        console.log('API Request with token:', url);
      } else {
        console.log('API Request without token:', url);
      }
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        // Handle token expiration - try to refresh token once (only on client-side)
        if (response.status === 401 && !isRetry && typeof window !== 'undefined') {
          const refreshToken = localStorage.getItem('refreshToken');
          if (refreshToken) {
            try {
              const refreshResponse = await this.refreshAccessToken() as { accessToken?: string };
              if (refreshResponse.accessToken) {
                // Retry the original request with new token
                localStorage.setItem('accessToken', refreshResponse.accessToken);
                return this.request(endpoint, options, true);
              }
            } catch (refreshError) {
              console.error('Token refresh failed:', refreshError);
              // Refresh failed, clear tokens
              localStorage.removeItem('accessToken');
              localStorage.removeItem('refreshToken');
            }
          }
        }

        // Provide more specific error messages for common HTTP status codes
        let errorMessage = data.message || `HTTP error! status: ${response.status}`;

        if (response.status === 401) {
          errorMessage = data.message || "Token has expired. Please log in again.";
          // Clear tokens on 401 if we're on client-side
          if (typeof window !== 'undefined') {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
          }
        } else if (response.status === 403) {
          errorMessage = data.message || "Forbidden - You don't have permission";
        } else if (response.status === 404) {
          // For tour and accommodation endpoints, don't throw errors as they have demo fallbacks
          if (url.includes('/tours') || url.includes('/accommodations')) {
            console.warn(`API 404 for ${url.includes('/tours') ? 'tour' : 'accommodation'} endpoint ${url}, will use demo data`);
            return null; // Return null instead of throwing
          }
          errorMessage = data.message || "Resource not found - The requested endpoint may not be available";
        } else if (response.status >= 500) {
          errorMessage = data.message || "Server error - Please try again later";
        }

        // Log the error details for debugging but don't expose internal details to users
        console.warn(`API Error ${response.status} for ${url}:`, data);

        throw new Error(errorMessage);
      }

      return data;
    } catch (error) {
      // Handle network errors and other fetch failures
      if (error instanceof TypeError && error.message.includes('fetch')) {
        // Network error - backend might be down
        console.warn('Network error - backend server may be unavailable:', url);
        // Don't throw for API services that have fallbacks - let them handle it
        throw new Error('Unable to connect to server. Please check your internet connection and try again.');
      }

      // Log and re-throw other errors (like HTTP errors from above)
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Authentication methods
  async login(credentials: { email: string; password: string }) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async signup(userData: { name: string; email: string; password: string; role?: Role | string; travelStyle?: string }) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({
        ...userData,
        role: userData.role || 'TRAVELER'
      }),
    });
  }

  async getCurrentUser() {
    const response = await this.request('/auth/me', {
      method: 'GET',
    });

    // The backend now returns the user object directly
    return response;
  }

  async refreshAccessToken() {
    // Only run on client-side
    if (typeof window === 'undefined') {
      throw new Error('Refresh token not available on server-side');
    }

    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    return this.request('/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refreshToken }),
    });
  }

  async requestPasswordReset(email: string) {
    return this.request('/auth/password/request', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }

  async resetPassword(token: string, password: string) {
    return this.request('/auth/password/reset', {
      method: 'POST',
      body: JSON.stringify({ token, password }),
    });
  }

  async resendVerification(email: string) {
    return this.request('/auth/resend-verify', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }

  // GetYourGuide integration
  async searchGetYourGuideTours(query: { location?: string; activity?: string; date?: string }) {
    return this.request('/getyourguide/search', {
      method: 'POST',
      body: JSON.stringify(query),
    });
  }

  async getGetYourGuideTourDetails(tourId: string) {
    return this.request(`/getyourguide/tour/${tourId}`, {
      method: 'GET',
    });
  }

  async createBookingWithGetYourGuide(data: { 
    tourId: string; 
    headcount: number; 
    specialRequests?: string;
    getYourGuideData?: Record<string, unknown>;
  }) {
    return this.request(`/bookings/${data.tourId}`, {
      method: 'POST',
      body: JSON.stringify({
        headcount: data.headcount,
        specialRequests: data.specialRequests,
        getYourGuideData: data.getYourGuideData
      }),
    });
  }

  async sendPhoneOtp(data: { userId: string; phone: string }) {
    return this.request('/onboarding/send-phone-otp', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async verifyPhoneOtp(data: { userId: string; phone: string; code: string }) {
    return this.request('/onboarding/verify-phone-otp', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async submitKyc(data: { userId: string; documents: Record<string, unknown>[] }) {
    return this.request('/onboarding/submit-kyc', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async setupPayout(data: { userId: string; stripeToken: string }) {
    return this.request('/onboarding/setup-payout', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async saveStep(data: { userId: string; stepNumber: number; data: Record<string, unknown> }) {
    return this.request('/onboarding/save-step', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Generic GET method for fetching data
  async get(endpoint: string) {
    return this.request(endpoint, {
      method: 'GET',
    });
  }

  // Generic POST method for creating data
  async post(endpoint: string, data: Record<string, unknown>) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Generic PUT method for updating data
  async put(endpoint: string, data: Record<string, unknown>) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Generic DELETE method for deleting data
  async delete(endpoint: string) {
    return this.request(endpoint, {
      method: 'DELETE',
    });
  }

  // Health check to verify backend connectivity
  async checkBackendHealth() {
    try {
      const response = await fetch(`${this.baseURL}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        return { status: 'healthy', message: 'Backend is running' };
      } else {
        return { status: 'unhealthy', message: `Backend responded with status ${response.status}` };
      }
    } catch (error: unknown) {
      console.error('Health check failed:', error);
      return { status: 'unavailable', message: 'Unable to connect to backend server' };
    }
  }
}

// Export a singleton instance
export const apiService = new ApiService();
export default apiService;
