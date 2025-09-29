"use client";

import Link from "next/link";
import AccommodationCard from "@/components/ui/AccommodationCard";
import { Apartment } from "@/types/common";

const sampleHotels: Apartment[] = [
  {
    id: "hotel-1",
    title: "Luxury Beach Resort & Spa",
    description:
      "Experience paradise at our beachfront resort with private villas, world-class spa, and stunning ocean views. Perfect for romantic getaways and family vacations.",
    categoryId: "luxury",
    hostId: "host-1",
    city: "Maldives",
    country: "Maldives",
    address: "Beach Road, Male, Maldives",
    latitude: 3.2028,
    longitude: 73.2207,
    basePrice: 45000, // $450 per night
    currency: "USD",
    maxGuests: 4,
    bedrooms: 2,
    bathrooms: 2,
    amenities: [
      "WiFi",
      "Pool",
      "Spa",
      "Beach Access",
      "Room Service",
      "Ocean View",
      "Private Balcony",
      "Mini Bar",
      "24/7 Concierge",
    ],
    images: [
      "/hero/travelhero.webp",
      "/hero/hotel.webp",
      "/hero/resort.webp",
      "/hero/villa.webp",
    ],
    isAvailable: true,
    status: "active",
    rating: 4.9,
    reviewCount: 1247,
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
    description:
      "Charming boutique hotel in the heart of the city with modern design, rooftop bar, and easy access to attractions. Ideal for business and leisure travelers.",
    categoryId: "boutique",
    hostId: "host-2",
    city: "New York",
    country: "USA",
    address: "123 Broadway, New York, NY",
    latitude: 40.7128,
    longitude: -74.006,
    basePrice: 25000, // $250 per night
    currency: "USD",
    maxGuests: 2,
    bedrooms: 1,
    bathrooms: 1,
    amenities: [
      "WiFi",
      "Gym",
      "Rooftop Bar",
      "Business Center",
      "Concierge",
      "Valet Parking",
      "Room Service",
      "Fitness Center",
    ],
    images: ["/hero/hero1.webp", "/hero/apartment.webp", "/hero/hotel.webp"],
    isAvailable: true,
    status: "active",
    rating: 4.7,
    reviewCount: 892,
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
    description:
      "Cozy mountain lodge surrounded by breathtaking scenery. Perfect for nature lovers seeking peace and tranquility with hiking trails and hot springs nearby.",
    categoryId: "lodge",
    hostId: "host-3",
    city: "Aspen",
    country: "USA",
    address: "456 Mountain Road, Aspen, CO",
    latitude: 39.1911,
    longitude: -106.8175,
    basePrice: 35000, // $350 per night
    currency: "USD",
    maxGuests: 6,
    bedrooms: 3,
    bathrooms: 2,
    amenities: [
      "WiFi",
      "Fireplace",
      "Hot Tub",
      "Mountain Views",
      "Hiking Trails",
      "Kitchen",
      "Game Room",
      "Ski Storage",
      "Outdoor Terrace",
    ],
    images: [
      "/hero/treehouses.webp",
      "/hero/apartment.webp",
      "/hero/villa.webp",
    ],
    isAvailable: true,
    status: "active",
    rating: 4.8,
    reviewCount: 634,
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
    host: {
      id: "host-3",
      name: "Emma Wilson",
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
    title: "Historic Palace Hotel",
    description:
      "Stay in a beautifully restored historic palace with elegant architecture, antique furnishings, and modern amenities. A unique blend of history and luxury.",
    categoryId: "historic",
    hostId: "host-4",
    city: "Paris",
    country: "France",
    address: "789 Royal Street, Paris, France",
    latitude: 48.8566,
    longitude: 2.3522,
    basePrice: 55000, // $550 per night
    currency: "USD",
    maxGuests: 2,
    bedrooms: 1,
    bathrooms: 1,
    amenities: [
      "WiFi",
      "Spa",
      "Historic Architecture",
      "Fine Dining",
      "Concierge",
      "City Views",
      "Antique Furnishings",
      "Private Tours",
      "Champagne Breakfast",
    ],
    images: ["/hero/hotel.webp", "/hero/travelhero.webp", "/hero/hero1.webp"],
    isAvailable: true,
    status: "active",
    rating: 4.6,
    reviewCount: 743,
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
    host: {
      id: "host-4",
      name: "Pierre Dubois",
      email: "pierre@historicpalace.com",
      image: null,
    },
    category: {
      id: "historic",
      type: "historic",
      title: "Historic Hotels",
      subtitle: "Step back in time",
      image: "/hero/hotel.webp",
      sectionTitle: "Historic Hotels",
      message: "Experience history",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  },
  {
    id: "hotel-5",
    title: "Desert Oasis Resort",
    description:
      "Tranquil desert resort with palm-fringed pools, traditional architecture, and authentic local experiences. The perfect escape from city life.",
    categoryId: "desert",
    hostId: "host-5",
    city: "Dubai",
    country: "UAE",
    address: "321 Desert Road, Dubai, UAE",
    latitude: 25.2048,
    longitude: 55.2708,
    basePrice: 28000, // $280 per night
    currency: "USD",
    maxGuests: 4,
    bedrooms: 2,
    bathrooms: 2,
    amenities: [
      "WiFi",
      "Pool",
      "Desert Tours",
      "Traditional Cuisine",
      "Spa",
      "Camel Riding",
      "Bedouin Experience",
      "Star Gazing",
      "Desert Safari",
    ],
    images: ["/hero/apartment.webp", "/hero/villa.webp", "/hero/resort.webp"],
    isAvailable: true,
    status: "active",
    rating: 4.7,
    reviewCount: 521,
    createdAt: "2024-01-01T00:00:00Z",
    updatedAt: "2024-01-01T00:00:00Z",
    host: {
      id: "host-5",
      name: "Ahmed Al-Saudi",
      email: "ahmed@desertoasis.com",
      image: null,
    },
    category: {
      id: "desert",
      type: "desert",
      title: "Desert Resorts",
      subtitle: "Discover the desert",
      image: "/hero/apartment.webp",
      sectionTitle: "Desert Resorts",
      message: "Experience the sands",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  },
  {
    id: "hotel-6",
    title: "Lakeview Cabin Resort",
    description:
      "Rustic cabin resort overlooking a pristine mountain lake. Enjoy fishing, boating, and stargazing in this peaceful natural setting.",
    categoryId: "cabin",
    hostId: "host-6",
    city: "Lake Tahoe",
    country: "USA",
    address: "654 Lake Road, Lake Tahoe, CA",
    latitude: 39.0968,
    longitude: -120.0324,
    basePrice: 20000, // $200 per night
    currency: "USD",
    maxGuests: 8,
    bedrooms: 4,
    bathrooms: 3,
    amenities: [
      "WiFi",
      "Lake Access",
      "Boating",
      "Fishing",
      "Fire Pit",
      "Kitchen",
      "Game Room",
      "Kayaks",
      "Hiking Trails",
      "BBQ Grill",
    ],
    images: [
      "/hero/chalets.webp",
      "/hero/treehouses.webp",
      "/hero/apartment.webp",
    ],
    isAvailable: true,
    status: "active",
    rating: 4.5,
    reviewCount: 387,
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
      subtitle: "Relax by the water",
      image: "/hero/chalets.webp",
      sectionTitle: "Lake Cabins",
      message: "Peaceful lake retreats",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    },
  },
];

export default function HotelsDemo() {
  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Featured Hotels & Accommodations
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Discover extraordinary places to stay around the world. From luxury
            resorts to cozy cabins, find your perfect accommodation for any
            occasion.
          </p>
        </div>

        <AccommodationCard apartments={sampleHotels} />

        <div className="text-center mt-12">
          <Link
            href="/accommodations"
            className="inline-flex items-center px-8 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors"
          >
            View All Accommodations
            <svg
              className="ml-2 w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </Link>
        </div>
      </div>
    </section>
  );
}
