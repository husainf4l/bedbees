export enum TourCategory {
  SHARE_TRIP = 'SHARE_TRIP',
  PRIVATE = 'PRIVATE',
  GROUP = 'GROUP',
}

export enum CancellationPolicy {
  FLEXIBLE = 'flexible',
  STANDARD = 'standard',
  STRICT = 'strict',
}

export interface CreateTourDto {
  title: string;
  city: string;
  country: string;
  category: TourCategory;
  description?: string;
  startTimes: string[]; // ISO date strings
  basePrice: number; // Price in cents
  currency?: string;
  minGroup: number;
  maxGroup: number;
  durationMins: number;
  language: string;
  languages?: string[];
  isPayWhatYouWant?: boolean;
  status?: string;
  
  // Enhanced filtering fields
  travelStyles?: string[];
  accessibility?: string[];
  startWindow?: string; // 'morning', 'afternoon', 'evening'
  instantBook?: boolean;
  cancellationPolicy?: CancellationPolicy;
  
  // Location details
  latitude?: number;
  longitude?: number;
  meetingPoint?: string;
  
  // SEO and searchability
  tags?: string[];
  searchKeywords?: string[];
}

export interface Guide {
  id: string;
  userId: string;
  bio?: string | null;
  kycStatus: string;
  payoutMethod?: string | null;
  stripeAccountId?: string | null;
  ratingAvg: number;
  toursCount: number;
  user: {
    id: string;
    name: string;
    email: string;
    image?: string | null;
  };
}

export interface TourMedia {
  id: string;
  url: string;
  type: string;
  // Add other media fields as needed
}

export interface Tour {
  id: string;
  guideId: string;
  title: string;
  city: string;
  country: string;
  category: string;
  description?: string;
  startTimes: string[]; // ISO date strings
  basePrice: number;
  currency: string;
  minGroup: number;
  maxGroup: number;
  durationMins: number;
  language: string;
  languages: string[];
  isPayWhatYouWant: boolean;
  status: string;
  createdAt: string;
  
  // Enhanced filtering fields
  travelStyles: string[];
  accessibility: string[];
  startWindow?: string;
  instantBook: boolean;
  hostRating?: number;
  cancellationPolicy: string;
  
  // Deal states
  isDropIn: boolean;
  isEarlyBird: boolean;
  
  // Location details
  latitude?: number | null;
  longitude?: number | null;
  meetingPoint?: string;
  
  // SEO and searchability
  tags: string[];
  searchKeywords: string[];
  
  // Tour details
  highlights?: string[];
  difficulty?: string;
  whatsIncluded?: string[];
  whatsExcluded?: string[];
  requirements?: string[];
  itinerary?: string;
  
  // Relations
  guide: Guide;
  media: TourMedia[];
  _count: {
    bookings: number;
  };
}

export interface TourQueryDto {
  // Pagination
  page?: number;
  limit?: number;

  // Search
  search?: string;

  // Location filters
  city?: string;
  country?: string;

  // Category filter
  category?: TourCategory;

  // Price range
  minPrice?: number;
  maxPrice?: number;

  // Group size
  minGroup?: number;
  maxGroup?: number;

  // Duration
  minDuration?: number;
  maxDuration?: number;

  // Language
  language?: string;
  languages?: string[];

  // Travel styles
  travelStyles?: string[];

  // Accessibility
  accessibility?: string[];

  // Start window
  startWindow?: string;

  // Instant book
  instantBook?: boolean;

  // Host rating
  minHostRating?: number;

  // Deal states
  isDropIn?: boolean;
  isEarlyBird?: boolean;

  // Status
  status?: string;

  // Sorting
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';

  // Date filters
  startDate?: string;
  endDate?: string;

  // Tags
  tags?: string[];
}

export interface ToursResponse {
  data: Tour[];
  meta: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
