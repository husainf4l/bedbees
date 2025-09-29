import { Apartment } from "@/types/common";
import { apiService } from "./api";

type AccommodationCategory = {
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
const demoApartments: Apartment[] = [
  {
    id: "1",
    title: "Modern Studio Apartment",
    description: "A beautifully designed modern studio apartment with all amenities. Perfect for couples or solo travelers looking for comfort and style.",
    categoryId: "0a2cb33b-b8c3-451c-9040-900f10a6907d",
    hostId: "d3b296ee-0c12-4cbd-bd59-bd65723f2f7a",
    city: "Limassol",
    country: "Cyprus",
    address: "Central Limassol",
    latitude: 34.7071,
    longitude: 33.0226,
    basePrice: 8500,
    currency: "USD",
    maxGuests: 2,
    bedrooms: 1,
    bathrooms: 1,
    amenities: ["WiFi", "Parking", "TV", "Kitchen", "Air Conditioning", "Balcony"],
    images: [
      "/hero/apartment.webp",
      "/hero/hotel.webp",
      "/hero/villa.webp",
      "/hero/resort.webp",
      "/hero/chalets.webp",
      "/hero/hero1.webp",
      "/hero/travelhero.webp"
    ],
    isAvailable: true,
    status: "active",
    createdAt: "2025-09-17T00:19:35.758Z",
    updatedAt: "2025-09-17T00:45:58.042Z",
    host: {
      id: "d3b296ee-0c12-4cbd-bd59-bd65723f2f7a",
      name: "Ahmed Al-Jordan",
      email: "ahmed.jordan@example.com",
      image: null,
    },
    category: {
      id: "0a2cb33b-b8c3-451c-9040-900f10a6907d",
      type: "apartment",
      title: "Find Your Perfect Apartment",
      subtitle: "Self-catering apartments and studios",
      image: "https://www.saiihotels.com/wp-content/uploads/2025/05/250310-Saii-Samui-0010.webp",
      sectionTitle: "Apartments",
      message: "Showing apartments...",
      createdAt: "2025-09-17T00:19:35.758Z",
      updatedAt: "2025-09-17T00:31:24.534Z",
    },
  },
  {
    id: "2",
    title: "Luxury Beachfront Apartment",
    description: "Stunning beachfront apartment with panoramic sea views. Features modern furnishings and direct beach access.",
    categoryId: "0a2cb33b-b8c3-451c-9040-900f10a6907d",
    hostId: "d3b296ee-0c12-4cbd-bd59-bd65723f2f7a",
    city: "Paphos",
    country: "Cyprus",
    address: "Beachfront Paphos",
    latitude: 34.7768,
    longitude: 32.4245,
    basePrice: 15000,
    currency: "USD",
    maxGuests: 4,
    bedrooms: 2,
    bathrooms: 2,
    amenities: ["WiFi", "Parking", "TV", "Kitchen", "Pool", "Beach Access"],
    images: [
      "/hero/villa.webp",
      "/hero/resort.webp",
      "/hero/apartment.webp",
      "/hero/hotel.webp",
      "/hero/treehouses.webp",
      "/hero/chalets.webp",
      "/hero/motels.webp",
      "/hero/hostels.webp",
      "/hero/caravan.webp"
    ],
    isAvailable: true,
    status: "active",
    createdAt: "2025-09-17T00:19:35.758Z",
    updatedAt: "2025-09-17T00:45:58.042Z",
    host: {
      id: "d3b296ee-0c12-4cbd-bd59-bd65723f2f7a",
      name: "Ahmed Al-Jordan",
      email: "ahmed.jordan@example.com",
      image: null,
    },
    category: {
      id: "0a2cb33b-b8c3-451c-9040-900f10a6907d",
      type: "apartment",
      title: "Find Your Perfect Apartment",
      subtitle: "Self-catering apartments and studios",
      image: "https://www.saiihotels.com/wp-content/uploads/2025/05/250310-Saii-Samui-0010.webp",
      sectionTitle: "Apartments",
      message: "Showing apartments...",
      createdAt: "2025-09-17T00:19:35.758Z",
      updatedAt: "2025-09-17T00:31:24.534Z",
    },
  },
  {
    id: "9088e33c-a62a-4e27-8909-962e73609403",
    title: "Cozy Downtown Apartment with Amazing Views",
    description: "Beautiful 2-bedroom apartment in the heart of downtown with stunning city views, modern amenities, and easy access to all attractions. Perfect for business travelers or tourists.",
    categoryId: "0a2cb33b-b8c3-451c-9040-900f10a6907d",
    hostId: "d3b296ee-0c12-4cbd-bd59-bd65723f2f7a",
    city: "Downtown",
    country: "Jordan",
    address: "City Center, Downtown",
    latitude: 31.9539,
    longitude: 35.9106,
    basePrice: 12000,
    currency: "USD",
    maxGuests: 4,
    bedrooms: 2,
    bathrooms: 1,
    amenities: ["WiFi", "Kitchen", "Air Conditioning", "Parking", "TV", "Balcony", "City View"],
    images: [
      "/hero/apartment.webp",
      "/hero/hotel.webp",
      "/hero/villa.webp",
      "/hero/resort.webp",
      "/hero/chalets.webp",
      "/hero/motels.webp",
      "/hero/treehouses.webp",
      "/hero/hostels.webp",
      "/hero/caravan.webp",
      "/hero/hero1.webp",
      "/hero/travelhero.webp",
      "/hero/apartment.webp",
      "/hero/hotel.webp",
      "/hero/villa.webp",
      "/hero/resort.webp"
    ],
    isAvailable: true,
    status: "active",
    createdAt: "2025-09-17T00:19:35.758Z",
    updatedAt: "2025-09-17T00:45:58.042Z",
    host: {
      id: "d3b296ee-0c12-4cbd-bd59-bd65723f2f7a",
      name: "Ahmed Al-Jordan",
      email: "ahmed.jordan@example.com",
      image: null,
    },
    category: {
      id: "0a2cb33b-b8c3-451c-9040-900f10a6907d",
      type: "apartment",
      title: "Find Your Perfect Apartment",
      subtitle: "Self-catering apartments and studios",
      image: "https://www.saiihotels.com/wp-content/uploads/2025/05/250310-Saii-Samui-0010.webp",
      sectionTitle: "Apartments",
      message: "Showing apartments...",
      createdAt: "2025-09-17T00:19:35.758Z",
      updatedAt: "2025-09-17T00:31:24.534Z",
    },
  },
  {
    id: "hotel-1",
    title: "Luxury Beach Resort & Spa",
    description: "Experience paradise at our beachfront resort with private villas, world-class spa, and stunning ocean views. Perfect for romantic getaways and family vacations.",
    categoryId: "luxury",
    hostId: "host-1",
    city: "Maldives",
    country: "Maldives",
    address: "Beach Road, Male, Maldives",
    latitude: 3.2028,
    longitude: 73.2207,
    basePrice: 45000,
    currency: "USD",
    maxGuests: 4,
    bedrooms: 2,
    bathrooms: 2,
    amenities: ["WiFi", "Pool", "Spa", "Beach Access", "Room Service", "Ocean View"],
    images: ["/hero/travelhero.webp"],
    isAvailable: true,
    status: "active",
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
    host: {
      id: "host-1",
      name: "Sarah Johnson",
      email: "sarah@luxuryresorts.com",
      image: null,
    },
    category: {
      id: "luxury",
      type: "luxury",
      title: "Luxury Resorts",
      subtitle: "Indulge in the finest accommodations",
      image: "/hero/travelhero.webp",
      sectionTitle: "Luxury Resorts",
      message: "Experience world-class luxury",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  },
  {
    id: "hotel-2",
    title: "Boutique City Hotel Downtown",
    description: "Charming boutique hotel in the heart of the city with modern design, rooftop bar, and easy access to attractions. Ideal for business and leisure travelers.",
    categoryId: "boutique",
    hostId: "host-2",
    city: "New York",
    country: "USA",
    address: "123 Broadway, New York, NY",
    latitude: 40.7128,
    longitude: -74.0060,
    basePrice: 25000,
    currency: "USD",
    maxGuests: 2,
    bedrooms: 1,
    bathrooms: 1,
    amenities: ["WiFi", "Gym", "Rooftop Bar", "Business Center", "Concierge"],
    images: ["/hero/hero1.webp"],
    isAvailable: true,
    status: "active",
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
    host: {
      id: "host-2",
      name: "Michael Chen",
      email: "michael@cityhotels.com",
      image: null,
    },
    category: {
      id: "boutique",
      type: "boutique",
      title: "Boutique Hotels",
      subtitle: "Unique and stylish accommodations",
      image: "/hero/hero1.webp",
      sectionTitle: "Boutique Hotels",
      message: "Discover unique stays",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  },
  {
    id: "hotel-3",
    title: "Mountain Lodge Retreat",
    description: "Cozy mountain lodge surrounded by breathtaking scenery. Perfect for nature lovers seeking peace and tranquility with hiking trails and hot springs nearby.",
    categoryId: "lodge",
    hostId: "host-3",
    city: "Aspen",
    country: "USA",
    address: "456 Mountain Road, Aspen, CO",
    latitude: 39.1911,
    longitude: -106.8175,
    basePrice: 35000,
    currency: "USD",
    maxGuests: 6,
    bedrooms: 3,
    bathrooms: 2,
    amenities: ["WiFi", "Fireplace", "Hot Tub", "Hiking Trails", "Mountain Views", "Kitchen"],
    images: ["/hero/treehouses.webp"],
    isAvailable: true,
    status: "active",
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
    host: {
      id: "host-3",
      name: "Emma Rodriguez",
      email: "emma@mountainlodges.com",
      image: null,
    },
    category: {
      id: "lodge",
      type: "lodge",
      title: "Mountain Lodges",
      subtitle: "Escape to the mountains",
      image: "/hero/treehouses.webp",
      sectionTitle: "Mountain Lodges",
      message: "Find peace in nature",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  },
  {
    id: "hotel-4",
    title: "Desert Oasis Resort",
    description: "Tranquil desert resort with traditional architecture, palm gardens, and authentic Bedouin hospitality. Experience the magic of the desert with modern comforts.",
    categoryId: "resort",
    hostId: "host-4",
    city: "Wadi Rum",
    country: "Jordan",
    address: "Desert Highway, Wadi Rum, Jordan",
    latitude: 29.6271,
    longitude: 35.4444,
    basePrice: 28000,
    currency: "USD",
    maxGuests: 4,
    bedrooms: 2,
    bathrooms: 2,
    amenities: ["WiFi", "Pool", "Desert Tours", "Traditional Meals", "Campfire", "Star Gazing"],
    images: ["/hero/apartment.webp"],
    isAvailable: true,
    status: "active",
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
    host: {
      id: "host-4",
      name: "Omar Al-Saudi",
      email: "omar@desertoasis.com",
      image: null,
    },
    category: {
      id: "resort",
      type: "resort",
      title: "Desert Resorts",
      subtitle: "Experience desert luxury",
      image: "/hero/apartment.webp",
      sectionTitle: "Desert Resorts",
      message: "Discover desert paradise",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  },
  {
    id: "hotel-5",
    title: "Desert Oasis Resort",
    description: "Tranquil desert resort with palm-fringed pools, traditional architecture, and authentic local experiences. The perfect escape from city life.",
    categoryId: "resort",
    hostId: "host-5",
    city: "Dubai",
    country: "UAE",
    address: "321 Desert Road, Dubai, UAE",
    latitude: 25.2048,
    longitude: 55.2708,
    basePrice: 28000,
    currency: "USD",
    maxGuests: 4,
    bedrooms: 2,
    bathrooms: 2,
    amenities: ["WiFi", "Pool", "Desert Tours", "Traditional Cuisine", "Spa", "Camel Riding", "Bedouin Experience", "Star Gazing", "Desert Safari"],
    images: ["/hero/apartment.webp", "/hero/villa.webp", "/hero/resort.webp"],
    isAvailable: true,
    status: "active",
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
    host: {
      id: "host-5",
      name: "Ahmed Al-Saudi",
      email: "ahmed@desertoasis.com",
      image: null,
    },
    category: {
      id: "resort",
      type: "resort",
      title: "Desert Resorts",
      subtitle: "Experience desert luxury",
      image: "/hero/resort.webp",
      sectionTitle: "Desert Resorts",
      message: "Discover desert paradise",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  },
  {
    id: "hotel-6",
    title: "Lakeview Cabin Resort",
    description: "Rustic cabin resort overlooking a pristine mountain lake. Enjoy fishing, boating, and stargazing in this peaceful natural setting.",
    categoryId: "cabin",
    hostId: "host-6",
    city: "Lake Tahoe",
    country: "USA",
    address: "654 Lake Road, Lake Tahoe, CA",
    latitude: 39.0968,
    longitude: -120.0324,
    basePrice: 20000,
    currency: "USD",
    maxGuests: 8,
    bedrooms: 4,
    bathrooms: 3,
    amenities: ["WiFi", "Lake Access", "Boating", "Fishing", "Fire Pit", "Kitchen", "Game Room", "Kayaks", "Hiking Trails", "BBQ Grill"],
    images: ["/hero/chalets.webp", "/hero/treehouses.webp", "/hero/apartment.webp"],
    isAvailable: true,
    status: "active",
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
    host: {
      id: "host-6",
      name: "David Thompson",
      email: "david@lakeviewcabins.com",
      image: null,
    },
    category: {
      id: "cabin",
      type: "cabin",
      title: "Lake Cabins",
      subtitle: "Rustic lakeside retreats",
      image: "/hero/chalets.webp",
      sectionTitle: "Lake Cabins",
      message: "Enjoy lakeside living",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  },
  // Host dashboard demo accommodations
  {
    id: "demo-1",
    title: "Luxury Downtown Hotel Suite",
    description: "Experience the pinnacle of luxury in our stunning downtown hotel suite with breathtaking city views.",
    categoryId: "hotel",
    hostId: "host-demo-1",
    city: "New York",
    country: "USA",
    address: "Downtown New York, NY, USA",
    latitude: 40.7128,
    longitude: -74.0060,
    basePrice: 12000, // $120 per night
    currency: "USD",
    maxGuests: 2,
    bedrooms: 1,
    bathrooms: 1,
    amenities: ["WiFi", "Parking", "TV", "Kitchen", "Air Conditioning", "Room Service"],
    images: ["/hero/hotel.webp"],
    isAvailable: true,
    status: "active",
    createdAt: "2025-09-18T00:00:00Z",
    updatedAt: "2025-09-18T00:00:00Z",
    host: {
      id: "host-demo-1",
      name: "Luxury Hotels Inc",
      email: "info@luxuryhotels.com",
      image: null,
    },
    category: {
      id: "hotel",
      type: "hotel",
      title: "Find Your Perfect Hotel",
      subtitle: "Luxury and budget hotels worldwide",
      image: "/hero/hotel.webp",
      sectionTitle: "Hotels",
      message: "Showing hotels...",
      createdAt: "2025-09-18T00:00:00Z",
      updatedAt: "2025-09-18T00:00:00Z",
    },
  },
  {
    id: "demo-2",
    title: "Mountain View Chalet",
    description: "Rustic mountain chalet with stunning alpine views and modern amenities.",
    categoryId: "chalets",
    hostId: "host-demo-2",
    city: "Zermatt",
    country: "Switzerland",
    address: "Alpine Road, Zermatt, Switzerland",
    latitude: 45.9767,
    longitude: 7.6586,
    basePrice: 35000, // $350 per night
    currency: "USD",
    maxGuests: 6,
    bedrooms: 3,
    bathrooms: 2,
    amenities: ["WiFi", "Parking", "Fireplace", "Kitchen", "Mountain Views", "Ski Access"],
    images: ["/hero/chalets.webp"],
    isAvailable: true,
    status: "active",
    createdAt: "2025-09-15T00:00:00Z",
    updatedAt: "2025-09-15T00:00:00Z",
    host: {
      id: "host-demo-2",
      name: "Alpine Retreats",
      email: "info@alpineretreats.com",
      image: null,
    },
    category: {
      id: "chalets",
      type: "chalets",
      title: "Cozy Mountain Chalets",
      subtitle: "Rustic alpine accommodations",
      image: "/hero/chalets.webp",
      sectionTitle: "Chalets",
      message: "Showing chalets...",
      createdAt: "2025-09-15T00:00:00Z",
      updatedAt: "2025-09-15T00:00:00Z",
    },
  },
  {
    id: "demo-3",
    title: "Beachfront Villa",
    description: "Luxurious beachfront villa with private pool and ocean views.",
    categoryId: "villa",
    hostId: "host-demo-3",
    city: "Malibu",
    country: "USA",
    address: "Pacific Coast Highway, Malibu, CA, USA",
    latitude: 34.0259,
    longitude: -118.7798,
    basePrice: 50000, // $500 per night
    currency: "USD",
    maxGuests: 8,
    bedrooms: 4,
    bathrooms: 3,
    amenities: ["WiFi", "Private Pool", "Ocean Views", "Kitchen", "BBQ", "Beach Access"],
    images: ["/hero/villa.webp"],
    isAvailable: true,
    status: "draft",
    createdAt: "2025-09-20T00:00:00Z",
    updatedAt: "2025-09-20T00:00:00Z",
    host: {
      id: "host-demo-3",
      name: "Coastal Properties",
      email: "info@coastalproperties.com",
      image: null,
    },
    category: {
      id: "villa",
      type: "villa",
      title: "Luxury Villas",
      subtitle: "Private villas worldwide",
      image: "/hero/villa.webp",
      sectionTitle: "Villas",
      message: "Showing villas...",
      createdAt: "2025-09-20T00:00:00Z",
      updatedAt: "2025-09-20T00:00:00Z",
    },
  },
];

class AccommodationService {
  async getAccommodations(): Promise<Apartment[]> {
    try {
      const response = await apiService.get('/accommodations') as Apartment[] | { data: Apartment[] };
      // The API returns the array directly, not wrapped in a data property
      return Array.isArray(response) ? response : (response as { data: Apartment[] }).data || [];
    } catch (error) {
      console.warn('Failed to fetch accommodations from API, using demo data:', error);
      // Fallback to demo data if API fails
      return this.getDemoApartments();
    }
  }

  async getAccommodationsByCategory(type: string): Promise<Apartment[]> {
    try {
      const response = await apiService.get(`/accommodations/categories/${type}/accommodations`) as Apartment[] | { data: Apartment[] };
      // The API returns the array directly, not wrapped in a data property
      return Array.isArray(response) ? response : (response as { data: Apartment[] }).data || [];
    } catch (error) {
      console.warn(`Failed to fetch accommodations for category ${type} from API, filtering demo data:`, error);
      // Fallback to filtering demo data by category
      const accommodations = this.getDemoApartments();
      return accommodations.filter(apt => apt.category.type === type);
    }
  }

  private getDemoApartments(): Apartment[] {
    return demoApartments;
  }

  async getCategories(): Promise<AccommodationCategory[]> {
    try {
      const response = await apiService.get('/accommodations/categories') as AccommodationCategory[] | { data: AccommodationCategory[] };
      // The API returns the array directly, not wrapped in a data property
      return Array.isArray(response) ? response : (response as { data: AccommodationCategory[] }).data || [];
    } catch (error) {
      console.warn('Failed to fetch accommodation categories from API, using demo data:', error);
      // Fallback to demo categories if API fails
      return this.getDemoCategories();
    }
  }

  private getDemoCategories(): AccommodationCategory[] {
    return [
      {
        id: "hotel",
        name: "Hotels",
        type: "hotel",
        title: "Find Your Perfect Hotel",
        subtitle: "Luxury and budget hotels worldwide",
        image: "/hero/hotel.webp",
        sectionTitle: "Hotels",
        message: "Showing hotels...",
      },
      {
        id: "apartment",
        name: "Apartments",
        type: "apartment",
        title: "Find Your Perfect Apartment",
        subtitle: "Self-catering apartments and studios",
        image: "/hero/apartment.webp",
        sectionTitle: "Apartments",
        message: "Showing apartments...",
      },
      {
        id: "resorts",
        name: "Resorts",
        type: "resorts",
        title: "Luxury Resorts & Spas",
        subtitle: "All-inclusive resorts and spas",
        image: "/hero/resort.webp",
        sectionTitle: "Resorts",
        message: "Showing resorts...",
      },
      {
        id: "hostels",
        name: "Hostels",
        type: "hostels",
        title: "Budget-Friendly Hostels",
        subtitle: "Budget-friendly shared accommodations",
        image: "/hero/hostels.webp",
        sectionTitle: "Hostels",
        message: "Showing hostels...",
      },
      {
        id: "motel",
        name: "Motels",
        type: "motel",
        title: "Convenient Motels for Your Stay",
        subtitle: "Convenient roadside accommodations",
        image: "/hero/motels.webp",
        sectionTitle: "Motels",
        message: "Showing motels...",
      },
      {
        id: "villas",
        name: "Villas",
        type: "villas",
        title: "Private Villas & Vacation Homes",
        subtitle: "Private villas and vacation homes",
        image: "/hero/villa.webp",
        sectionTitle: "Villas",
        message: "Showing villas...",
      },
      {
        id: "chalets",
        name: "Chalets",
        type: "chalets",
        title: "Mountain Chalets & Cabins",
        subtitle: "Mountain chalets and cabins",
        image: "/hero/chalets.webp",
        sectionTitle: "Chalets",
        message: "Showing chalets...",
      },
      {
        id: "treehouses",
        name: "Treehouses",
        type: "treehouses",
        title: "Unique Treehouse Accommodations",
        subtitle: "Unique treehouse accommodations",
        image: "/hero/treehouses.webp",
        sectionTitle: "Treehouses",
        message: "Showing treehouses...",
      },
      {
        id: "guest-houses",
        name: "Guest Houses",
        type: "guest-houses",
        title: "Homely Guest Houses & B&Bs",
        subtitle: "Homely guest houses and B&Bs",
        image: "/hero/villa.jpg",
        sectionTitle: "Guest Houses",
        message: "Showing guest houses...",
      },
      {
        id: "vacation-homes",
        name: "Vacation Homes",
        type: "vacation-homes",
        title: "Entire Vacation Homes",
        subtitle: "Entire homes for your vacation",
        image: "/hero/villa.jpg",
        sectionTitle: "Vacation Homes",
        message: "Showing vacation homes...",
      },
      {
        id: "caravans",
        name: "Caravans",
        type: "caravans",
        title: "Mobile Caravans & RVs",
        subtitle: "Mobile caravans and RVs",
        image: "/hero/caravan.webp",
        sectionTitle: "Caravans",
        message: "Showing caravans...",
      },
    ];
  }

  async getCategoryContent(type: string) {
    try {
      const categories = await this.getCategories();
      const category = categories.find(cat => cat.type === type);
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
      title: "Find Your Perfect Accommodation",
      subtitle: "Discover hotels, apartments, resorts and more worldwide",
      image: "/hero/hero1.webp",
      sectionTitle: "All Accommodations",
      message: "Showing all accommodations...",
    };
  }

  async getAccommodationById(id: string): Promise<Apartment | null> {
    try {
      const response = await apiService.get(`/accommodations/${id}`) as Apartment | { data: Apartment } | null;
      // Handle both direct object response and wrapped response
      const accommodation = response && typeof response === 'object' && 'data' in response ? response.data : response;
      return accommodation || null;
    } catch (error) {
      console.warn(`Failed to fetch accommodation ${id} from API, falling back to demo data:`, error);
      // Fallback to finding in demo data
      const accommodations = this.getDemoApartments();
      return accommodations.find(apt => apt.id === id) || null;
    }
  }

  async createAccommodation(accommodationData: {
    title: string;
    description: string;
    categoryId: string;
    city: string;
    country: string;
    address: string;
    latitude?: number;
    longitude?: number;
    basePrice: number;
    currency: string;
    maxGuests: number;
    bedrooms: number;
    bathrooms: number;
    amenities: string[];
    images: string[];
    isAvailable: boolean;
    hostId?: string;
  }) {
    try {
      console.log('Creating accommodation with data:', accommodationData);
      const response = await apiService.post('/accommodations', accommodationData);
      console.log('Accommodation created successfully:', response);
      // Handle both direct object response and wrapped response
      return response && typeof response === 'object' && 'data' in response ? response.data : response;
    } catch (error) {
      console.error('Failed to create accommodation:', error);
      throw error;
    }
  }

  async updateAccommodation(id: string, accommodationData: {
    title: string;
    description: string;
    categoryId: string;
    city: string;
    country: string;
    address: string;
    latitude?: number;
    longitude?: number;
    basePrice: number;
    currency: string;
    maxGuests: number;
    bedrooms: number;
    bathrooms: number;
    amenities: string[];
    images: string[];
    isAvailable: boolean;
    hostId?: string;
  }) {
    try {
      const response = await apiService.put(`/accommodations/${id}`, accommodationData);
      return response;
    } catch (error) {
      console.error('Failed to update accommodation:', error);
      throw error;
    }
  }

  // TODO: Implement when backend endpoint is available
  async searchAccommodations(filters: {
    location?: string;
    type?: string;
    priceMin?: number;
    priceMax?: number;
    bedrooms?: number;
    bathrooms?: number;
  }): Promise<Apartment[]> {
    try {
      // Build query parameters from filters
      const queryParams = new URLSearchParams();
      if (filters.location) queryParams.append('location', filters.location);
      if (filters.type) queryParams.append('type', filters.type);
      if (filters.priceMin) queryParams.append('priceMin', filters.priceMin.toString());
      if (filters.priceMax) queryParams.append('priceMax', filters.priceMax.toString());
      if (filters.bedrooms) queryParams.append('bedrooms', filters.bedrooms.toString());
      if (filters.bathrooms) queryParams.append('bathrooms', filters.bathrooms.toString());

      const queryString = queryParams.toString();
      const endpoint = queryString ? `/accommodations/search?${queryString}` : '/accommodations';

      const response = await apiService.get(endpoint) as Apartment[] | { data: Apartment[] };
      // The API returns the array directly, not wrapped in a data property
      return Array.isArray(response) ? response : (response as { data: Apartment[] }).data || [];
    } catch (error) {
      console.error('Failed to search accommodations:', error);
      // Fallback to client-side filtering of demo data
      const accommodations = this.getDemoApartments();
      return accommodations.filter(apt => {
        if (filters.location && !(`${apt.city}, ${apt.country}`).toLowerCase().includes(filters.location.toLowerCase())) {
          return false;
        }
        if (filters.bedrooms && apt.bedrooms < filters.bedrooms) {
          return false;
        }
        if (filters.bathrooms && apt.bathrooms < filters.bathrooms) {
          return false;
        }
        return true;
      });
    }
  }
}

export const accommodationService = new AccommodationService();
export default accommodationService;