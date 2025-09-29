import { Tour, TourCategory } from "@/types/tour";
import { apiService } from "./api";

type TourCategoryInfo = {
  id: string;
  name: string;
  type: string;
  title: string;
  subtitle: string;
  image: string;
  sectionTitle: string;
  message: string;
};

// Demo data that will later be replaced with backend API calls
const demoTours: Tour[] = [
  {
    id: "1",
    guideId: "guide-1",
    title: "Historic Cyprus Cultural Walking Tour",
    city: "Nicosia",
    country: "Cyprus",
    category: "SHARE_TRIP",
    description: "Discover the rich history and culture of Cyprus's capital city through hidden alleys, ancient architecture, and local stories shared with fellow travelers.",
    startTimes: ["2025-09-20T09:00:00.000Z", "2025-09-20T14:00:00.000Z"],
    basePrice: 2500,
    currency: "USD",
    minGroup: 4,
    maxGroup: 12,
    durationMins: 180,
    language: "English",
    languages: ["English", "Greek"],
    isPayWhatYouWant: false,
    status: "active",
    createdAt: "2025-09-18T00:00:00.000Z",
    travelStyles: ["Cultural", "Walking", "History"],
    accessibility: ["Easy walking"],
    startWindow: "morning",
    instantBook: true,
    hostRating: 4.8,
    cancellationPolicy: "flexible",
    isDropIn: true,
    isEarlyBird: false,
    latitude: 35.1856,
    longitude: 33.3823,
    meetingPoint: "Ledra Street Crossing",
    tags: ["culture", "history", "walking", "cyprus"],
    searchKeywords: ["nicosia", "cultural", "walking", "history"],
    highlights: ["Visit the last divided capital in Europe", "Explore both Greek and Turkish quarters", "Taste traditional Cypriot coffee"],
    difficulty: "Easy",
    whatsIncluded: ["Professional guide", "Traditional coffee tasting", "Small group experience"],
    whatsExcluded: ["Personal expenses", "Transportation to meeting point"],
    requirements: ["Comfortable walking shoes", "Water bottle"],
    itinerary: "Meet at Ledra Street → Old Town exploration → Coffee break → Byzantine Museum → Buffer Zone explanation",
    guide: {
      id: "guide-1",
      userId: "user-1",
      bio: "Local historian and cultural enthusiast",
      kycStatus: "verified",
      payoutMethod: "stripe",
      stripeAccountId: "stripe-123",
      ratingAvg: 4.8,
      toursCount: 47,
      user: {
        id: "user-1",
        name: "Maria Constantinou",
        email: "maria@example.com",
        image: null,
      },
    },
    media: [
      {
        id: "media-1",
        url: "/hero/travelhero.webp",
        type: "image",
      },
    ],
    _count: {
      bookings: 23,
    },
  },
  {
    id: "2",
    guideId: "guide-2",
    title: "Private Troodos Mountains Adventure",
    city: "Troodos",
    country: "Cyprus",
    category: "PRIVATE",
    description: "Experience the stunning Troodos Mountains with a personalized private tour including waterfalls, traditional villages, and wine tasting.",
    startTimes: ["2025-09-21T08:00:00.000Z"],
    basePrice: 15000,
    currency: "USD",
    minGroup: 1,
    maxGroup: 6,
    durationMins: 480,
    language: "English",
    languages: ["English", "Greek", "German"],
    isPayWhatYouWant: false,
    status: "active",
    createdAt: "2025-09-18T00:00:00.000Z",
    travelStyles: ["Adventure", "Nature", "Wine", "Scenic"],
    accessibility: ["Moderate hiking"],
    startWindow: "morning",
    instantBook: false,
    hostRating: 4.9,
    cancellationPolicy: "standard",
    isDropIn: false,
    isEarlyBird: true,
    latitude: 34.9214,
    longitude: 32.8597,
    meetingPoint: "Troodos Square",
    tags: ["mountains", "nature", "wine", "private"],
    searchKeywords: ["troodos", "mountains", "private", "wine", "nature"],
    highlights: ["Kykkos Monastery visit", "Millomeris Waterfall hike", "Local winery experience", "Traditional village lunch"],
    difficulty: "Moderate",
    whatsIncluded: ["Private transportation", "Professional guide", "Wine tasting", "Traditional lunch"],
    whatsExcluded: ["Personal expenses", "Additional drinks"],
    requirements: ["Hiking shoes", "Sunhat", "Camera"],
    itinerary: "Hotel pickup → Kykkos Monastery → Millomeris Waterfall → Village lunch → Winery visit → Return",
    guide: {
      id: "guide-2",
      userId: "user-2",
      bio: "Mountain guide and wine expert",
      kycStatus: "verified",
      payoutMethod: "stripe",
      stripeAccountId: "stripe-456",
      ratingAvg: 4.9,
      toursCount: 31,
      user: {
        id: "user-2",
        name: "Andreas Georgiou",
        email: "andreas@example.com",
        image: null,
      },
    },
    media: [
      {
        id: "media-2",
        url: "/hero/hero1.webp",
        type: "image",
      },
    ],
    _count: {
      bookings: 18,
    },
  },
  {
    id: "3",
    guideId: "guide-3",
    title: "Paphos Archaeological Group Tour",
    city: "Paphos",
    country: "Cyprus",
    category: "GROUP",
    description: "Join a group of history enthusiasts to explore the UNESCO World Heritage archaeological sites of Paphos with an expert archaeologist guide.",
    startTimes: ["2025-09-22T10:00:00.000Z"],
    basePrice: 3500,
    currency: "USD",
    minGroup: 8,
    maxGroup: 20,
    durationMins: 240,
    language: "English",
    languages: ["English", "French"],
    isPayWhatYouWant: false,
    status: "active",
    createdAt: "2025-09-18T00:00:00.000Z",
    travelStyles: ["Archaeological", "Historical", "Educational"],
    accessibility: ["Easy walking", "Wheelchair accessible"],
    startWindow: "morning",
    instantBook: true,
    hostRating: 4.7,
    cancellationPolicy: "standard",
    isDropIn: false,
    isEarlyBird: false,
    latitude: 34.7568,
    longitude: 32.4054,
    meetingPoint: "Paphos Archaeological Park Entrance",
    tags: ["archaeology", "history", "unesco", "group"],
    searchKeywords: ["paphos", "archaeological", "history", "unesco"],
    highlights: ["House of Dionysus mosaics", "Tombs of the Kings", "Paphos Castle", "Roman Odeon"],
    difficulty: "Easy",
    whatsIncluded: ["Expert archaeologist guide", "Site entrance fees", "Group experience"],
    whatsExcluded: ["Transportation", "Personal expenses", "Food"],
    requirements: ["Comfortable shoes", "Sun protection", "Water"],
    itinerary: "Meet at entrance → House of Dionysus → Roman Villa → Tombs of Kings → Paphos Castle",
    guide: {
      id: "guide-3",
      userId: "user-3",
      bio: "Professional archaeologist and historian",
      kycStatus: "verified",
      payoutMethod: "stripe",
      stripeAccountId: "stripe-789",
      ratingAvg: 4.7,
      toursCount: 62,
      user: {
        id: "user-3",
        name: "Dr. Elena Pavlou",
        email: "elena@example.com",
        image: null,
      },
    },
    media: [
      {
        id: "media-3",
        url: "/hero/apartment.webp",
        type: "image",
      },
    ],
    _count: {
      bookings: 41,
    },
  },
  {
    id: "4",
    guideId: "guide-4",
    title: "Sinai Mountain Sunrise Trek",
    city: "Mount Sinai",
    country: "Egypt",
    category: "SHARE_TRIP",
    description: "Experience the breathtaking sunrise from the summit of Mount Sinai, following the ancient path of Moses. This spiritual journey combines physical challenge with profound natural beauty.",
    startTimes: ["2025-09-22T02:00:00.000Z"],
    basePrice: 8500,
    currency: "USD",
    minGroup: 4,
    maxGroup: 15,
    durationMins: 720,
    language: "English",
    languages: ["English", "Arabic"],
    isPayWhatYouWant: false,
    status: "active",
    createdAt: "2025-09-18T00:00:00.000Z",
    travelStyles: ["Adventure", "Spiritual", "Nature"],
    accessibility: ["Moderate hiking required"],
    startWindow: "night",
    instantBook: true,
    hostRating: 4.6,
    cancellationPolicy: "standard",
    isDropIn: false,
    isEarlyBird: true,
    latitude: 28.5397,
    longitude: 33.9751,
    meetingPoint: "Saint Catherine's Monastery",
    tags: ["adventure", "spiritual", "sunrise", "egypt"],
    searchKeywords: ["sinai", "mount sinai", "sunrise", "moses", "hiking"],
    highlights: [
      "Sunrise summit experience",
      "Ancient Moses trail",
      "Bedouin guide",
      "Spiritual atmosphere",
      "Stunning desert views",
    ],
    difficulty: "Advanced",
    whatsIncluded: [
      "Professional guide",
      "Transportation",
      "Breakfast",
      "Entrance fees",
    ],
    whatsExcluded: [
      "Personal expenses",
      "Water bottle",
      "Warm clothing",
    ],
    requirements: [
      "Good physical condition",
      "Warm clothing for early morning",
      "Sturdy walking shoes",
    ],
    itinerary: "02:00 - Pickup from hotel → 04:00 - Begin 3-hour trek → 07:00 - Sunrise ceremony at summit → 08:00 - Return trek → 10:00 - Breakfast at monastery → 12:00 - Return to hotel",
    guide: {
      id: "guide-4",
      userId: "user-4",
      bio: "Experienced mountain guide and Bedouin culture expert",
      kycStatus: "verified",
      payoutMethod: "stripe",
      stripeAccountId: "stripe-456",
      ratingAvg: 4.6,
      toursCount: 28,
      user: {
        id: "user-4",
        name: "Ahmed Hassan",
        email: "ahmed@example.com",
        image: null,
      },
    },
    media: [
      {
        id: "media-4",
        url: "/hero/villa.webp",
        type: "image",
      },
    ],
    _count: {
      bookings: 28,
    },
  },
  {
    id: "5",
    guideId: "guide-5",
    title: "Red Sea Scuba Diving Adventure",
    city: "Aqaba",
    country: "Jordan",
    category: "PRIVATE",
    description: "Explore the vibrant underwater world of the Red Sea with professional PADI-certified instructors. Perfect for both beginners and experienced divers.",
    startTimes: ["2025-09-23T08:00:00.000Z", "2025-09-23T13:00:00.000Z"],
    basePrice: 18500,
    currency: "USD",
    minGroup: 1,
    maxGroup: 6,
    durationMins: 300,
    language: "English",
    languages: ["English", "Russian"],
    isPayWhatYouWant: false,
    status: "active",
    createdAt: "2025-09-18T00:00:00.000Z",
    travelStyles: ["Adventure", "Water Sports", "Marine Life"],
    accessibility: ["Swimming ability required"],
    startWindow: "morning",
    instantBook: true,
    hostRating: 4.8,
    cancellationPolicy: "strict",
    isDropIn: false,
    isEarlyBird: false,
    latitude: 29.5319,
    longitude: 35.0078,
    meetingPoint: "Aqaba Dive Center",
    tags: ["diving", "scuba", "red sea", "marine", "jordan"],
    searchKeywords: ["aqaba", "diving", "scuba", "red sea", "coral"],
    highlights: [
      "2 dive sites",
      "Coral reef exploration",
      "Marine life observation",
      "Professional instruction",
      "PADI certification option",
    ],
    difficulty: "Intermediate",
    whatsIncluded: [
      "PADI certified instructor",
      "Full diving equipment",
      "Boat transportation",
      "Safety briefing",
      "Underwater photos",
    ],
    whatsExcluded: [
      "Diving certification",
      "Airport transfers",
      "Gratuities",
    ],
    requirements: [
      "Basic swimming skills",
      "Medical clearance for diving",
      "No recent flights",
    ],
    itinerary: "08:00 - Equipment fitting and safety briefing → 09:00 - First dive at coral reef → 11:00 - Surface interval and lunch → 12:00 - Second dive at marine site → 14:00 - Debrief and photos",
    guide: {
      id: "guide-5",
      userId: "user-5",
      bio: "PADI Master Instructor with 15+ years of Red Sea diving experience",
      kycStatus: "verified",
      payoutMethod: "stripe",
      stripeAccountId: "stripe-567",
      ratingAvg: 4.8,
      toursCount: 67,
      user: {
        id: "user-5",
        name: "Marina Petrova",
        email: "marina@example.com",
        image: null,
      },
    },
    media: [
      {
        id: "media-5",
        url: "/hero/resort.webp",
        type: "image",
      },
    ],
    _count: {
      bookings: 67,
    },
  },
  {
    id: "6",
    guideId: "guide-6",
    title: "Lebanon Paragliding Experience",
    city: "Harissa",
    country: "Lebanon",
    category: "PRIVATE",
    description: "Soar above the stunning Lebanese coastline and mountains in a tandem paragliding flight. Experience the thrill of free flight with breathtaking panoramic views.",
    startTimes: ["2025-09-24T09:00:00.000Z", "2025-09-24T14:00:00.000Z"],
    basePrice: 22000,
    currency: "USD",
    minGroup: 1,
    maxGroup: 4,
    durationMins: 180,
    language: "English",
    languages: ["English", "Arabic", "French"],
    isPayWhatYouWant: false,
    status: "active",
    createdAt: "2025-09-18T00:00:00.000Z",
    travelStyles: ["Adventure", "Air Sports", "Scenic"],
    accessibility: ["No special requirements"],
    startWindow: "morning",
    instantBook: true,
    hostRating: 4.5,
    cancellationPolicy: "flexible",
    isDropIn: false,
    isEarlyBird: true,
    latitude: 33.9817,
    longitude: 35.6464,
    meetingPoint: "Harissa Paragliding Center",
    tags: ["paragliding", "adventure", "lebanon", "views"],
    searchKeywords: ["harissa", "paragliding", "flying", "mountains"],
    highlights: [
      "Tandem paragliding flight",
      "Mountain and coastal views",
      "Professional pilot",
      "GoPro footage included",
      "Mediterranean scenery",
    ],
    difficulty: "Beginner",
    whatsIncluded: [
      "Professional pilot",
      "Safety equipment",
      "Ground transportation",
      "Flight video/photos",
      "Certificate",
    ],
    whatsExcluded: [
      "Personal insurance",
      "Airport transfers",
      "Gratuities",
    ],
    requirements: [
      "Weight between 40-110kg",
      "No medical conditions",
      "Comfortable clothing",
    ],
    itinerary: "09:00 - Arrival and safety briefing → 10:00 - Ground training and equipment fitting → 11:00 - Tandem paragliding flight (20-30 mins) → 12:00 - Debrief, photos, and certificate",
    guide: {
      id: "guide-6",
      userId: "user-6",
      bio: "Professional paragliding instructor and aerial photographer",
      kycStatus: "verified",
      payoutMethod: "stripe",
      stripeAccountId: "stripe-678",
      ratingAvg: 4.5,
      toursCount: 33,
      user: {
        id: "user-6",
        name: "Karim Al-Rashid",
        email: "karim@example.com",
        image: null,
      },
    },
    media: [
      {
        id: "media-6",
        url: "/hero/chalets.webp",
        type: "image",
      },
    ],
    _count: {
      bookings: 33,
    },
  },
];

class TourService {
  async getTours(): Promise<Tour[]> {
    try {
      const response = await apiService.get('/tours') as Tour[] | { data: Tour[] } | null;
      if (response === null) {
        // API returned null (404), use demo data
        return this.getDemoTours();
      }
      return Array.isArray(response) ? response : (response as { data: Tour[] }).data || [];
    } catch (error) {
      console.warn('Failed to fetch tours from API, using demo data:', error);
      // Fallback to demo data if API fails
      return this.getDemoTours();
    }
  }

  async getToursByCategory(type: string): Promise<Tour[]> {
    try {
      const response = await apiService.get(`/tours/categories/${type}/tours`) as Tour[] | { data: Tour[] };
      return Array.isArray(response) ? response : (response as { data: Tour[] }).data || [];
    } catch (error) {
      console.warn(`Failed to fetch tours for category ${type} from API, filtering demo data:`, error);
      // Fallback to filtering demo data by category
      const tours = this.getDemoTours();
      return tours.filter(tour => tour.category.toLowerCase() === type.toLowerCase());
    }
  }

  private getDemoTours(): Tour[] {
    return demoTours;
  }

  async getCategories(): Promise<TourCategoryInfo[]> {
    try {
      const response = await apiService.get('/tours/categories') as TourCategoryInfo[] | { data: TourCategoryInfo[] } | null;
      if (response === null) {
        // API returned null (404), use demo data
        return this.getDemoCategories();
      }
      return Array.isArray(response) ? response : (response as { data: TourCategoryInfo[] }).data || [];
    } catch (error) {
      console.warn('Failed to fetch tour categories from API, using demo data:', error);
      // Always fallback to demo categories if API fails
      return this.getDemoCategories();
    }
  }

  private getDemoCategories(): TourCategoryInfo[] {
    return [
      {
        id: "all",
        name: "All Tours",
        type: "all",
        title: "Discover Amazing Tours & Experiences",
        subtitle: "Join unique experiences with local guides and fellow travelers",
        image: "/hero/travelhero.webp",
        sectionTitle: "All Tours & Experiences",
        message: "Explore our curated collection of tours and experiences...",
      },
      {
        id: "share_trip",
        name: "Share Trip",
        type: "share_trip",
        title: "Join Fellow Travelers on Share Trips",
        subtitle: "Meet like-minded travelers and explore together",
        image: "/hero/travelhero.webp",
        sectionTitle: "Share Trip Experiences",
        message: "Connect with travelers and share unforgettable experiences...",
      },
      {
        id: "private",
        name: "Private Tours",
        type: "private",
        title: "Exclusive Private Tours & Experiences",
        subtitle: "Personalized tours tailored just for you",
        image: "/hero/hero1.webp",
        sectionTitle: "Private Experiences",
        message: "Enjoy personalized attention with our private tours...",
      },
      {
        id: "group",
        name: "Group Tours",
        type: "group",
        title: "Join Organized Group Tours",
        subtitle: "Explore with expert guides and fellow adventurers",
        image: "/hero/apartment.webp",
        sectionTitle: "Group Adventures",
        message: "Discover amazing places with our group tours...",
      },
    ];
  }

  async getCategoryContent(type: string) {
    try {
      const categories = await this.getCategories();
      const category = categories.find(cat => cat.type.toLowerCase() === type.toLowerCase());
      if (category) {
        return {
          title: category.title,
          subtitle: category.subtitle,
          image: category.image,
          sectionTitle: category.sectionTitle,
          message: category.message,
        };
      }
    } catch (error) {
      console.error('Failed to get category content:', error);
    }

    // Fallback to default
    return {
      title: "Discover Amazing Tours & Experiences",
      subtitle: "Join unique experiences with local guides and fellow travelers",
      image: "/hero/travelhero.webp",
      sectionTitle: "All Tours & Experiences",
      message: "Showing all available tours and experiences...",
    };
  }

  async getTourById(id: string): Promise<Tour | null> {
    try {
      const response = await apiService.get(`/tours/${id}`) as Tour | null;
      if (response) {
        return response;
      }
      // If API returns null (404), fall back to demo data
      const tours = this.getDemoTours();
      const demoTour = tours.find(tour => tour.id === id);
      return demoTour || null;
    } catch (error: unknown) {
      // For other errors, also try demo data as fallback
      console.error('Error fetching tour from API:', error);
      const tours = this.getDemoTours();
      const demoTour = tours.find(tour => tour.id === id);
      if (demoTour) {
        return demoTour;
      }
      // If not found in demo data either, re-throw the original error
      throw error;
    }
  }

  async searchTours(filters: {
    location?: string;
    category?: TourCategory;
    priceMin?: number;
    priceMax?: number;
    duration?: number;
    language?: string;
  }): Promise<Tour[]> {
    try {
      const queryParams = new URLSearchParams();
      if (filters.location) queryParams.append('location', filters.location);
      if (filters.category) queryParams.append('category', filters.category);
      if (filters.priceMin) queryParams.append('priceMin', filters.priceMin.toString());
      if (filters.priceMax) queryParams.append('priceMax', filters.priceMax.toString());
      if (filters.duration) queryParams.append('duration', filters.duration.toString());
      if (filters.language) queryParams.append('language', filters.language);

      const queryString = queryParams.toString();
      const endpoint = queryString ? `/tours/search?${queryString}` : '/tours';

      const response = await apiService.get(endpoint) as Tour[] | { data: Tour[] };
      return Array.isArray(response) ? response : (response as { data: Tour[] }).data || [];
    } catch (error) {
      console.error('Failed to search tours:', error);
      // Fallback to client-side filtering of demo data
      const tours = this.getDemoTours();
      return tours.filter(tour => {
        if (filters.location && !(`${tour.city}, ${tour.country}`).toLowerCase().includes(filters.location.toLowerCase())) {
          return false;
        }
        if (filters.category && tour.category !== filters.category) {
          return false;
        }
        if (filters.language && !tour.languages.includes(filters.language)) {
          return false;
        }
        return true;
      });
    }
  }

  async createTour(tourData: {
    title: string;
    description?: string;
    city: string;
    country: string;
    category: string;
    basePrice: number;
    currency?: string;
    maxParticipants: number;
    duration?: number;
    difficulty?: string;
    highlights?: string[];
    whatsIncluded?: string[];
    whatsExcluded?: string[];
    requirements?: string[];
    itinerary?: Record<string, unknown>[];
    images?: string[];
    latitude?: number;
    longitude?: number;
    guideId?: string;
    guideName?: string;
    guideEmail?: string;
    guideImage?: string;
    guideBio?: string;
  }): Promise<Tour> {
    try {
      // Use local API route instead of external backend
      const response = await fetch('/api/tours', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tourData)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create tour');
      }

      const result = await response.json();
      return result.data;
    } catch (error) {
      console.error('Failed to create tour:', error);
      throw error;
    }
  }
}

export const tourService = new TourService();
export default tourService;