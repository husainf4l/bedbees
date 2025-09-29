export interface TravelerStats {
  totalTrips: number;
  upcomingTrips: number;
  totalSpent: number;
  favoriteDestinations: number;
}

export interface TripBooking {
  id: string;
  tourId: string;
  tourTitle: string;
  guideId: string;
  guideName: string;
  guideImage?: string;
  destination: string;
  startDate: string;
  endDate: string;
  duration: number; // in minutes
  status: 'confirmed' | 'pending' | 'completed' | 'cancelled';
  totalPrice: number;
  currency: string;
  groupSize: number;
  meetingPoint?: string;
  tourImage?: string;
  category: string;
}

export interface RecentActivity {
  id: string;
  type: 'booking' | 'review' | 'favorite' | 'share';
  title: string;
  description: string;
  timestamp: string;
  tourId?: string;
  tourTitle?: string;
}

export interface FavoriteDestination {
  id: string;
  city: string;
  country: string;
  image: string;
  visitCount: number;
  lastVisited?: string;
  upcomingTrips: number;
}

export interface TravelerProfile {
  id: string;
  name: string;
  email: string;
  image?: string;
  joinedDate: string;
  totalTrips: number;
  reviewsGiven: number;
  averageRating: number;
  preferredLanguages: string[];
  travelStyles: string[];
}

export interface TravelerDashboard {
  stats: TravelerStats;
  upcomingBookings: TripBooking[];
  recentActivity: RecentActivity[];
  favoriteDestinations: FavoriteDestination[];
  profile: TravelerProfile;
}