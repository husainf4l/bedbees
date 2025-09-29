import {
  TravelerDashboard,
  TravelerStats,
  TripBooking,
  RecentActivity,
  FavoriteDestination,
  TravelerProfile
} from '@/types/traveler';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3003/api';

class TravelerService {
  private async request(endpoint: string, options: RequestInit = {}): Promise<unknown> {
    const url = `${API_BASE_URL}${endpoint}`;

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add authorization header if token exists
    const token = localStorage.getItem('accessToken');
    if (token) {
      (config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Get dashboard stats
  async getStats(): Promise<TravelerStats> {
    return this.request('/traveler/dashboard') as Promise<TravelerStats>;
  }

  // Get upcoming bookings
  async getUpcomingBookings(): Promise<TripBooking[]> {
    return this.request('/traveler/bookings/upcoming') as Promise<TripBooking[]>;
  }

  // Get recent activity
  async getRecentActivity(): Promise<RecentActivity[]> {
    return this.request('/traveler/activity/recent') as Promise<RecentActivity[]>;
  }

  // Get favorite destinations
  async getFavoriteDestinations(): Promise<FavoriteDestination[]> {
    return this.request('/traveler/destinations/favorites') as Promise<FavoriteDestination[]>;
  }

  // Get traveler profile
  async getProfile(): Promise<TravelerProfile> {
    return this.request('/traveler/profile') as Promise<TravelerProfile>;
  }

  // Get complete dashboard data
  async getDashboardData(): Promise<TravelerDashboard> {
    try {
      const [stats, upcomingBookings, recentActivity, favoriteDestinations, profile] = await Promise.all([
        this.getStats(),
        this.getUpcomingBookings(),
        this.getRecentActivity(),
        this.getFavoriteDestinations(),
        this.getProfile()
      ]);

      return {
        stats,
        upcomingBookings: upcomingBookings || [],
        recentActivity: recentActivity || [],
        favoriteDestinations: favoriteDestinations || [],
        profile
      };
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      throw error;
    }
  }

  // Safe methods that return empty arrays if API fails
  async getUpcomingBookingsSafe(): Promise<TripBooking[]> {
    try {
      const bookings = await this.getUpcomingBookings();
      return Array.isArray(bookings) ? bookings : [];
    } catch (error) {
      console.warn('Failed to fetch upcoming bookings:', error);
      return [];
    }
  }

  async getRecentActivitySafe(): Promise<RecentActivity[]> {
    try {
      const activity = await this.getRecentActivity();
      return Array.isArray(activity) ? activity : [];
    } catch (error) {
      console.warn('Failed to fetch recent activity:', error);
      return [];
    }
  }

  async getFavoriteDestinationsSafe(): Promise<FavoriteDestination[]> {
    try {
      const destinations = await this.getFavoriteDestinations();
      return Array.isArray(destinations) ? destinations : [];
    } catch (error) {
      console.warn('Failed to fetch favorite destinations:', error);
      return [];
    }
  }

  async getDashboardDataSafe(): Promise<TravelerDashboard> {
    try {
      const [stats, upcomingBookings, recentActivity, favoriteDestinations, profile] = await Promise.all([
        this.getStats().catch(() => ({ totalTrips: 0, upcomingTrips: 0, totalSpent: 0, favoriteDestinations: 0 })),
        this.getUpcomingBookingsSafe(),
        this.getRecentActivitySafe(),
        this.getFavoriteDestinationsSafe(),
        this.getProfile().catch(() => ({ 
          id: '', 
          name: 'User', 
          email: '', 
          image: undefined, 
          joinedDate: new Date().toISOString(),
          totalTrips: 0,
          reviewsGiven: 0,
          averageRating: 0,
          preferredLanguages: [],
          travelStyles: []
        }))
      ]);

      return {
        stats,
        upcomingBookings,
        recentActivity,
        favoriteDestinations,
        profile
      };
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Return minimal safe data structure
      return {
        stats: { totalTrips: 0, upcomingTrips: 0, totalSpent: 0, favoriteDestinations: 0 },
        upcomingBookings: [],
        recentActivity: [],
        favoriteDestinations: [],
        profile: { 
          id: '', 
          name: 'User', 
          email: '', 
          image: undefined, 
          joinedDate: new Date().toISOString(),
          totalTrips: 0,
          reviewsGiven: 0,
          averageRating: 0,
          preferredLanguages: [],
          travelStyles: []
        }
      };
    }
  }

  // Fallback methods with demo data for development/testing
  private getDemoStats(): TravelerStats {
    return {
      totalTrips: 12,
      upcomingTrips: 3,
      totalSpent: 2847,
      favoriteDestinations: 8
    };
  }

  private getDemoUpcomingBookings(): TripBooking[] {
    return [
      {
        id: '1',
        tourId: 'tour-1',
        tourTitle: 'Historic Paris Walking Tour',
        guideId: 'guide-1',
        guideName: 'Marie Dubois',
        guideImage: '/images/guides/marie.jpg',
        destination: 'Paris, France',
        startDate: '2025-09-25T10:00:00Z',
        endDate: '2025-09-25T13:00:00Z',
        duration: 180,
        status: 'confirmed',
        totalPrice: 45,
        currency: 'EUR',
        groupSize: 8,
        meetingPoint: 'Notre Dame Cathedral',
        tourImage: '/images/tours/paris-historic.jpg',
        category: 'SHARE_TRIP'
      },
      {
        id: '2',
        tourId: 'tour-2',
        tourTitle: 'Tokyo Street Food Adventure',
        guideId: 'guide-2',
        guideName: 'Hiroshi Tanaka',
        guideImage: '/images/guides/hiroshi.jpg',
        destination: 'Tokyo, Japan',
        startDate: '2025-10-02T18:00:00Z',
        endDate: '2025-10-02T21:00:00Z',
        duration: 180,
        status: 'pending',
        totalPrice: 75,
        currency: 'USD',
        groupSize: 6,
        meetingPoint: 'Shibuya Crossing',
        tourImage: '/images/tours/tokyo-food.jpg',
        category: 'GROUP'
      }
    ];
  }

  private getDemoRecentActivity(): RecentActivity[] {
    return [
      {
        id: '1',
        type: 'booking',
        title: 'Booked Barcelona Art Tour',
        description: 'Successfully booked Barcelona Art & Architecture tour with Carlos Martinez',
        timestamp: '2025-09-15T14:30:00Z',
        tourId: 'tour-3',
        tourTitle: 'Barcelona Art & Architecture'
      },
      {
        id: '2',
        type: 'review',
        title: 'Left review for London Tour',
        description: 'Rated 5 stars for the amazing London Historic Pubs tour',
        timestamp: '2025-09-12T09:15:00Z',
        tourId: 'tour-4',
        tourTitle: 'London Historic Pubs'
      }
    ];
  }

  private getDemoFavoriteDestinations(): FavoriteDestination[] {
    return [
      {
        id: '1',
        city: 'Paris',
        country: 'France',
        image: '/images/destinations/paris.jpg',
        visitCount: 3,
        lastVisited: '2025-06-15T00:00:00Z',
        upcomingTrips: 1
      },
      {
        id: '2',
        city: 'Tokyo',
        country: 'Japan',
        image: '/images/destinations/tokyo.jpg',
        visitCount: 2,
        lastVisited: '2025-03-22T00:00:00Z',
        upcomingTrips: 1
      }
    ];
  }

  private getDemoProfile(): TravelerProfile {
    return {
      id: 'traveler-1',
      name: 'Alex Johnson',
      email: 'alex.johnson@email.com',
      image: '/images/travelers/alex.jpg',
      joinedDate: '2024-03-15T00:00:00Z',
      totalTrips: 12,
      reviewsGiven: 8,
      averageRating: 4.8,
      preferredLanguages: ['English', 'Spanish', 'French'],
      travelStyles: ['Cultural', 'Food & Drink', 'History', 'Art']
    };
  }

  // Development methods that can fallback to demo data
  async getStatsWithFallback(): Promise<TravelerStats> {
    try {
      return await this.getStats();
    } catch (error) {
      console.warn('API call failed, using demo data:', error);
      return this.getDemoStats();
    }
  }

  async getDashboardDataWithFallback(): Promise<TravelerDashboard> {
    try {
      return await this.getDashboardData();
    } catch (error) {
      console.warn('API call failed, using demo data:', error);
      return {
        stats: this.getDemoStats(),
        upcomingBookings: this.getDemoUpcomingBookings(),
        recentActivity: this.getDemoRecentActivity(),
        favoriteDestinations: this.getDemoFavoriteDestinations(),
        profile: this.getDemoProfile()
      };
    }
  }
}

export const travelerService = new TravelerService();
export default travelerService;