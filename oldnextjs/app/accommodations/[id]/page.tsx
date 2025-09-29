"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import { useState, useEffect } from "react";
import {
  HeartIcon,
  MapPinIcon,
  UsersIcon,
  HomeIcon,
  CheckCircleIcon,
  ShieldCheckIcon,
  BanknotesIcon,
  CakeIcon,
  XMarkIcon,
  CalendarDaysIcon,
  PhoneIcon,
  ClockIcon,
  StarIcon,
} from "@heroicons/react/24/outline";
import { HeartIcon as HeartSolidIcon } from "@heroicons/react/24/solid";
import { accommodationService } from "@/services/accommodation.service";

// Enhanced interfaces
interface Accommodation {
  id: string;
  title: string;
  location: string;
  city: string;
  country: string;
  address: string;
  description: string;
  pricePerNight: number;
  basePrice: number;
  images: string[];
  amenities: string[];
  rating: number;
  reviews: number;
  bedrooms: number;
  bathrooms: number;
  maxGuests: number;
  category: {
    sectionTitle: string;
  };
  host: {
    name: string;
    email: string;
  };
  latitude: number;
  longitude: number;
}

type RoomTypeKey = "standard" | "deluxe" | "suite";
type RatePlanKey = "flexible" | "nonRefundable" | "bedBreakfast";

interface RoomType {
  id: string;
  name: string;
  description: string;
  size: string;
  maxOccupancy: number;
  amenities: string[];
  images: string[];
  basePrice: number;
}

interface RatePlan {
  id: string;
  name: string;
  description: string;
  basePrice: number;
  priceMultiplier: number;
  cancellation: {
    policy: string;
    deadline: string;
    fee: string | number;
  };
  perks: string[];
  availability: string;
  color: string;
}

// Enhanced demo data
function getAccommodationById(id: string): Accommodation | null {
  const demoAccommodations: Record<string, Accommodation> = {
    "9088e33c-a62a-4e27-8909-962e73609403": {
      id: "9088e33c-a62a-4e27-8909-962e73609403",
      title: "Luxury Downtown Hotel Suite",
      location: "New York, NY",
      city: "New York",
      country: "United States",
      address: "123 Broadway, Manhattan, NY 10001",
      description:
        "Experience the pinnacle of luxury in our stunning downtown hotel suite. Located in the heart of Manhattan, this exquisite accommodation offers breathtaking city views, premium amenities, and unparalleled service. Perfect for business travelers, romantic getaways, or anyone seeking an unforgettable stay in the city that never sleeps.",
      pricePerNight: 120,
      basePrice: 12000, // in cents
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
      ],
      amenities: [
        "Free High-Speed WiFi",
        "Air Conditioning & Heating",
        "Fully Equipped Kitchen",
        "Free Parking",
        "Flat-screen TV with Cable",
        "Private Bathroom with Shower",
        "Balcony with City View",
        "In-room Safe",
        "Mini Refrigerator",
        "Coffee Machine",
        "24/7 Concierge Service",
        "Fitness Center Access",
      ],
      rating: 4.8,
      reviews: 124,
      bedrooms: 2,
      bathrooms: 2,
      maxGuests: 4,
      category: {
        sectionTitle: "Luxury Hotel",
      },
      host: {
        name: "Michael Johnson",
        email: "michael@luxuryhotels.com",
      },
      latitude: 40.7589,
      longitude: -73.9851,
    },
    "hotel-1": {
      id: "hotel-1",
      title: "Luxury Beach Resort & Spa",
      location: "Maldives",
      city: "Maldives",
      country: "Maldives",
      address: "Beach Road, Male, Maldives",
      description:
        "Experience paradise at our beachfront resort with private villas, world-class spa, and stunning ocean views. Perfect for romantic getaways and family vacations.",
      pricePerNight: 450,
      basePrice: 45000,
      images: [
        "/hero/travelhero.webp",
        "/hero/hotel.webp",
        "/hero/resort.webp",
        "/hero/villa.webp",
      ],
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
      rating: 4.9,
      reviews: 1247,
      bedrooms: 2,
      bathrooms: 2,
      maxGuests: 4,
      category: {
        sectionTitle: "Luxury Resorts",
      },
      host: {
        name: "Sarah Johnson",
        email: "sarah@luxuryresorts.com",
      },
      latitude: 3.2028,
      longitude: 73.2207,
    },
    "hotel-2": {
      id: "hotel-2",
      title: "Boutique City Hotel Downtown",
      location: "New York, USA",
      city: "New York",
      country: "USA",
      address: "123 Broadway, New York, NY",
      description:
        "Charming boutique hotel in the heart of the city with modern design, rooftop bar, and easy access to attractions. Ideal for business and leisure travelers.",
      pricePerNight: 250,
      basePrice: 25000,
      images: ["/hero/hero1.webp", "/hero/apartment.webp", "/hero/hotel.webp"],
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
      rating: 4.7,
      reviews: 892,
      bedrooms: 1,
      bathrooms: 1,
      maxGuests: 2,
      category: {
        sectionTitle: "Boutique Hotels",
      },
      host: {
        name: "Michael Chen",
        email: "michael@cityhotels.com",
      },
      latitude: 40.7128,
      longitude: -74.006,
    },
    "hotel-3": {
      id: "hotel-3",
      title: "Mountain Lodge Retreat",
      location: "Aspen, USA",
      city: "Aspen",
      country: "USA",
      address: "456 Mountain Road, Aspen, CO",
      description:
        "Cozy mountain lodge surrounded by breathtaking scenery. Perfect for nature lovers seeking peace and tranquility with hiking trails and hot springs nearby.",
      pricePerNight: 350,
      basePrice: 35000,
      images: [
        "/hero/treehouses.webp",
        "/hero/apartment.webp",
        "/hero/villa.webp",
      ],
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
      rating: 4.8,
      reviews: 634,
      bedrooms: 3,
      bathrooms: 2,
      maxGuests: 6,
      category: {
        sectionTitle: "Mountain Lodges",
      },
      host: {
        name: "Emma Rodriguez",
        email: "emma@mountainlodges.com",
      },
      latitude: 39.1911,
      longitude: -106.8175,
    },
    "hotel-4": {
      id: "hotel-4",
      title: "Historic Palace Hotel",
      location: "Paris, France",
      city: "Paris",
      country: "France",
      address: "789 Royal Street, Paris, France",
      description:
        "Stay in a beautifully restored historic palace with elegant architecture, antique furnishings, and modern amenities. A unique blend of history and luxury.",
      pricePerNight: 550,
      basePrice: 55000,
      images: ["/hero/hotel.webp", "/hero/travelhero.webp", "/hero/hero1.webp"],
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
      rating: 4.6,
      reviews: 743,
      bedrooms: 1,
      bathrooms: 1,
      maxGuests: 2,
      category: {
        sectionTitle: "Historic Hotels",
      },
      host: {
        name: "Pierre Dubois",
        email: "pierre@palacehotels.com",
      },
      latitude: 48.8566,
      longitude: 2.3522,
    },
    "hotel-5": {
      id: "hotel-5",
      title: "Desert Oasis Resort",
      location: "Dubai, UAE",
      city: "Dubai",
      country: "UAE",
      address: "321 Desert Road, Dubai, UAE",
      description:
        "Tranquil desert resort with palm-fringed pools, traditional architecture, and authentic local experiences. The perfect escape from city life.",
      pricePerNight: 280,
      basePrice: 28000,
      images: ["/hero/apartment.webp", "/hero/villa.webp", "/hero/resort.webp"],
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
      rating: 4.7,
      reviews: 521,
      bedrooms: 2,
      bathrooms: 2,
      maxGuests: 4,
      category: {
        sectionTitle: "Desert Resorts",
      },
      host: {
        name: "Ahmed Al-Saudi",
        email: "ahmed@desertoasis.com",
      },
      latitude: 25.2048,
      longitude: 55.2708,
    },
    "hotel-6": {
      id: "hotel-6",
      title: "Lakeview Cabin Resort",
      location: "Lake Tahoe, USA",
      city: "Lake Tahoe",
      country: "USA",
      address: "654 Lake Road, Lake Tahoe, CA",
      description:
        "Rustic cabin resort overlooking a pristine mountain lake. Enjoy fishing, boating, and stargazing in this peaceful natural setting.",
      pricePerNight: 200,
      basePrice: 20000,
      images: [
        "/hero/chalets.webp",
        "/hero/treehouses.webp",
        "/hero/apartment.webp",
      ],
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
      rating: 4.5,
      reviews: 387,
      bedrooms: 4,
      bathrooms: 3,
      maxGuests: 8,
      category: {
        sectionTitle: "Lake Cabins",
      },
      host: {
        name: "David Thompson",
        email: "david@lakeviewcabins.com",
      },
      latitude: 39.0968,
      longitude: -120.0324,
    },
    "1": {
      id: "1",
      title: "Modern Studio Apartment",
      location: "Limassol, Cyprus",
      city: "Limassol",
      country: "Cyprus",
      address: "Central Limassol",
      description:
        "A beautifully designed modern studio apartment with all amenities. Perfect for couples or solo travelers looking for comfort and style.",
      pricePerNight: 85,
      basePrice: 8500,
      images: [
        "/hero/apartment.webp",
        "/hero/hotel.webp",
        "/hero/villa.webp",
        "/hero/resort.webp",
        "/hero/chalets.webp",
        "/hero/hero1.webp",
        "/hero/travelhero.webp",
      ],
      amenities: [
        "WiFi",
        "Parking",
        "TV",
        "Kitchen",
        "Air Conditioning",
        "Balcony",
      ],
      rating: 4.8,
      reviews: 124,
      bedrooms: 1,
      bathrooms: 1,
      maxGuests: 2,
      category: {
        sectionTitle: "Apartments",
      },
      host: {
        name: "Ahmed Al-Jordan",
        email: "ahmed.jordan@example.com",
      },
      latitude: 34.7071,
      longitude: 33.0226,
    },
    "2": {
      id: "2",
      title: "Luxury Beachfront Apartment",
      location: "Paphos, Cyprus",
      city: "Paphos",
      country: "Cyprus",
      address: "Beachfront Paphos",
      description:
        "Stunning beachfront apartment with panoramic sea views. Features modern furnishings and direct beach access.",
      pricePerNight: 150,
      basePrice: 15000,
      images: [
        "/hero/villa.webp",
        "/hero/resort.webp",
        "/hero/apartment.webp",
        "/hero/hotel.webp",
        "/hero/treehouses.webp",
        "/hero/chalets.webp",
        "/hero/motels.webp",
        "/hero/hostels.webp",
        "/hero/caravan.webp",
      ],
      amenities: ["WiFi", "Parking", "TV", "Kitchen", "Pool", "Beach Access"],
      rating: 4.9,
      reviews: 89,
      bedrooms: 2,
      bathrooms: 2,
      maxGuests: 4,
      category: {
        sectionTitle: "Apartments",
      },
      host: {
        name: "Ahmed Al-Jordan",
        email: "ahmed.jordan@example.com",
      },
      latitude: 34.7768,
      longitude: 32.4245,
    },
    "demo-1": {
      id: "demo-1",
      title: "Luxury Downtown Hotel Suite",
      location: "New York, USA",
      city: "New York",
      country: "USA",
      address: "Downtown New York, NY, USA",
      description:
        "Experience the pinnacle of luxury in our stunning downtown hotel suite.",
      pricePerNight: 120,
      basePrice: 12000,
      images: ["/hero/hotel.webp"],
      amenities: [
        "WiFi",
        "Parking",
        "TV",
        "Kitchen",
        "Air Conditioning",
        "Room Service",
      ],
      rating: 4.8,
      reviews: 156,
      bedrooms: 1,
      bathrooms: 1,
      maxGuests: 2,
      category: {
        sectionTitle: "Hotels",
      },
      host: {
        name: "Luxury Hotels Inc",
        email: "info@luxuryhotels.com",
      },
      latitude: 40.7128,
      longitude: -74.006,
    },
    "demo-2": {
      id: "demo-2",
      title: "Mountain View Chalet",
      location: "Zermatt, Switzerland",
      city: "Zermatt",
      country: "Switzerland",
      address: "Alpine Road, Zermatt, Switzerland",
      description:
        "Rustic mountain chalet with stunning alpine views and modern amenities.",
      pricePerNight: 350,
      basePrice: 35000,
      images: ["/hero/chalets.webp"],
      amenities: [
        "WiFi",
        "Parking",
        "Fireplace",
        "Kitchen",
        "Mountain Views",
        "Ski Access",
      ],
      rating: 4.7,
      reviews: 203,
      bedrooms: 3,
      bathrooms: 2,
      maxGuests: 6,
      category: {
        sectionTitle: "Chalets",
      },
      host: {
        name: "Alpine Retreats",
        email: "info@alpineretreats.com",
      },
      latitude: 45.9767,
      longitude: 7.6586,
    },
    "demo-3": {
      id: "demo-3",
      title: "Beachfront Villa",
      location: "Malibu, USA",
      city: "Malibu",
      country: "USA",
      address: "Pacific Coast Highway, Malibu, CA, USA",
      description:
        "Luxurious beachfront villa with private pool and ocean views.",
      pricePerNight: 500,
      basePrice: 50000,
      images: ["/hero/villa.webp"],
      amenities: [
        "WiFi",
        "Private Pool",
        "Ocean Views",
        "Kitchen",
        "BBQ",
        "Beach Access",
      ],
      rating: 4.9,
      reviews: 78,
      bedrooms: 4,
      bathrooms: 3,
      maxGuests: 8,
      category: {
        sectionTitle: "Villas",
      },
      host: {
        name: "Coastal Properties",
        email: "info@coastalproperties.com",
      },
      latitude: 34.0259,
      longitude: -118.7798,
    },
  };

  return demoAccommodations[id] || null;
}

// Room types data
const roomTypes: Record<RoomTypeKey, RoomType> = {
  standard: {
    id: "standard",
    name: "Standard Room",
    description:
      "Comfortable room with essential amenities for a pleasant stay",
    size: "25 m²",
    maxOccupancy: 2,
    basePrice: 12000,
    amenities: [
      "Free Wi-Fi",
      "Air Conditioning",
      "Private Bathroom",
      "Flat-screen TV",
      "Mini Refrigerator",
      "Coffee Machine",
    ],
    images: ["/rooms/standard-1.jpg", "/rooms/standard-2.jpg"],
  },
  deluxe: {
    id: "deluxe",
    name: "Deluxe Room",
    description: "Spacious room with premium amenities and stunning city views",
    size: "35 m²",
    maxOccupancy: 3,
    basePrice: 15000,
    amenities: [
      "Free Wi-Fi",
      "Air Conditioning",
      "Private Bathroom",
      "Flat-screen TV",
      "Mini Bar",
      "City View",
      "Work Desk",
      "Premium Bedding",
      "Room Service",
    ],
    images: ["/rooms/deluxe-1.jpg", "/rooms/deluxe-2.jpg"],
  },
  suite: {
    id: "suite",
    name: "Executive Suite",
    description: "Luxury suite with separate living area and premium amenities",
    size: "55 m²",
    maxOccupancy: 4,
    basePrice: 25000,
    amenities: [
      "Free Wi-Fi",
      "Air Conditioning",
      "Private Bathroom",
      "Flat-screen TV",
      "Mini Bar",
      "City View",
      "Work Desk",
      "Separate Living Area",
      "Coffee Machine",
      "Balcony",
      "Premium Bathroom Amenities",
      "24/7 Concierge Service",
    ],
    images: ["/rooms/suite-1.jpg", "/rooms/suite-2.jpg"],
  },
};

// Rate plans data
const ratePlans: Record<RatePlanKey, RatePlan> = {
  flexible: {
    id: "flexible",
    name: "Flexible Rate",
    description:
      "Full flexibility with free cancellation up to 6 PM on check-in date",
    basePrice: 12000,
    priceMultiplier: 1.2,
    cancellation: {
      policy: "Free cancellation until 6 PM on your check-in date",
      deadline: "Same day",
      fee: 0,
    },
    perks: [
      "Free cancellation until 6 PM on check-in date",
      "Change dates without penalty",
      "Best rate guarantee",
      "Late checkout (subject to availability)",
      "Priority customer support",
    ],
    availability: "Available",
    color: "green",
  },
  nonRefundable: {
    id: "nonRefundable",
    name: "Non-Refundable Rate",
    description: "Best price with no refunds - save up to 15%",
    basePrice: 12000,
    priceMultiplier: 0.85,
    cancellation: {
      policy: "No refunds or changes allowed",
      deadline: "Non-refundable",
      fee: "100%",
    },
    perks: [
      "Lowest price guarantee - save up to 15%",
      "Immediate confirmation",
      "Priority room assignment",
      "Complimentary welcome drink",
    ],
    availability: "Limited availability",
    color: "red",
  },
  bedBreakfast: {
    id: "bedBreakfast",
    name: "Bed & Breakfast",
    description: "Includes daily breakfast for all guests",
    basePrice: 12000,
    priceMultiplier: 1.35,
    cancellation: {
      policy: "Free cancellation until 24 hours before check-in",
      deadline: "24 hours",
      fee: "First night charge",
    },
    perks: [
      "Daily breakfast included for all guests",
      "Early check-in (subject to availability)",
      "Complimentary bottled water daily",
      "Free newspaper delivery",
      "Priority Wi-Fi support",
      "Late checkout until 2 PM",
    ],
    availability: "Available",
    color: "blue",
  },
};

function getAmenityIcon(amenity: string) {
  // Simple icon mapping - in a real app this would be more sophisticated
  if (amenity.toLowerCase().includes("wifi")) return "📶";
  if (amenity.toLowerCase().includes("air conditioning")) return "❄️";
  if (amenity.toLowerCase().includes("kitchen")) return "🍳";
  if (amenity.toLowerCase().includes("parking")) return "🅿️";
  if (amenity.toLowerCase().includes("tv")) return "📺";
  if (amenity.toLowerCase().includes("bathroom")) return "🚿";
  if (amenity.toLowerCase().includes("balcony")) return "🏙️";
  if (amenity.toLowerCase().includes("safe")) return "🔒";
  if (amenity.toLowerCase().includes("coffee")) return "☕";
  if (amenity.toLowerCase().includes("fitness")) return "💪";
  return "✅";
}

export default function AccommodationDetail() {
  const params = useParams();
  const id = params.id as string;
  const [accommodation, setAccommodation] = useState<Accommodation | null>(
    null
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Lightbox state
  const [isLightboxOpen, setIsLightboxOpen] = useState(false);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [lightboxImages, setLightboxImages] = useState<string[]>([]);

  // Selection state
  const [selectedRoomType, setSelectedRoomType] =
    useState<RoomTypeKey>("standard");
  const [selectedRatePlan, setSelectedRatePlan] =
    useState<RatePlanKey>("flexible");
  const [isWishlisted, setIsWishlisted] = useState(false);

  // Booking state
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [guests, setGuests] = useState(1);

  useEffect(() => {
    if (id) {
      setLoading(true);
      console.log("Fetching accommodation with ID:", id);
      accommodationService
        .getAccommodationById(id)
        .then((acc) => {
          console.log("Accommodation fetch result:", acc);
          if (acc) {
            // Transform the API response to match the component's expected format
            const transformedAcc: Accommodation = {
              id: acc.id,
              title: acc.title,
              location: `${acc.city}, ${acc.country}`,
              city: acc.city,
              country: acc.country,
              address: acc.address,
              description: acc.description,
              pricePerNight: acc.basePrice / 100, // Convert from cents to dollars
              basePrice: acc.basePrice,
              images: acc.images || [],
              amenities: acc.amenities || [],
              rating: 4.5, // Default rating since it's not in the API response
              reviews: 0, // Default reviews count
              bedrooms: acc.bedrooms,
              bathrooms: acc.bathrooms,
              maxGuests: acc.maxGuests,
              category: {
                sectionTitle:
                  acc.category?.sectionTitle ||
                  acc.category?.title ||
                  "Accommodation",
              },
              host: {
                name: acc.host?.name || "Host",
                email: acc.host?.email || "",
              },
              latitude: acc.latitude || 0,
              longitude: acc.longitude || 0,
            };
            setAccommodation(transformedAcc);
            setError(null);
          } else {
            // Try local demo data as fallback
            console.log("Service returned null, trying local demo data");
            const localAcc = getAccommodationById(id);
            if (localAcc) {
              console.log("Found accommodation in local demo data:", localAcc);
              setAccommodation(localAcc);
              setError(null);
            } else {
              console.log("Accommodation not found in any demo data");
              setError("Accommodation not found");
            }
          }
          setLoading(false);
        })
        .catch((error) => {
          console.error("Error fetching accommodation:", error);
          // Try local demo data as final fallback
          console.log("Service failed, trying local demo data as fallback");
          const localAcc = getAccommodationById(id);
          if (localAcc) {
            console.log("Found accommodation in local demo data:", localAcc);
            setAccommodation(localAcc);
            setError(null);
          } else {
            setError("Failed to load accommodation");
          }
          setLoading(false);
        });
    }
  }, [id]);

  const openLightbox = (images: string[], index: number) => {
    setLightboxImages(images);
    setCurrentImageIndex(index);
    setIsLightboxOpen(true);
  };

  const closeLightbox = () => {
    setIsLightboxOpen(false);
  };

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % lightboxImages.length);
  };

  const prevImage = () => {
    setCurrentImageIndex(
      (prev) => (prev - 1 + lightboxImages.length) % lightboxImages.length
    );
  };

  // Keyboard navigation for lightbox
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (isLightboxOpen) {
        if (e.key === "ArrowRight") nextImage();
        if (e.key === "ArrowLeft") prevImage();
        if (e.key === "Escape") closeLightbox();
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [isLightboxOpen]);

  const toggleWishlist = () => {
    setIsWishlisted(!isWishlisted);
  };

  const calculateTotalPrice = () => {
    const roomType = roomTypes[selectedRoomType];
    const ratePlan = ratePlans[selectedRatePlan];
    const basePrice = roomType.basePrice / 100; // Convert from cents
    const finalPrice = basePrice * ratePlan.priceMultiplier;
    return Math.round(finalPrice);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading accommodation details...</p>
        </div>
      </div>
    );
  }

  if (error || !accommodation) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto mb-4"></div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            {error || "Accommodation not found"}
          </h1>
          <p className="text-gray-600 mb-6">
            The accommodation you&apos;re looking for doesn&apos;t exist or may
            have been removed.
          </p>
          <div className="space-x-4">
            <button
              onClick={() => window.history.back()}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              Go Back
            </button>
            <Link
              href="/accommodations"
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors inline-block"
            >
              Browse Accommodations
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <h1 className="text-2xl font-bold text-gray-900">
                {accommodation.title}
              </h1>
              <div className="flex items-center gap-2">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <StarIcon
                      key={i}
                      className={`w-4 h-4 ${
                        i < Math.floor(accommodation.rating)
                          ? "text-yellow-400 fill-current"
                          : "text-gray-300"
                      }`}
                    />
                  ))}
                </div>
                <span className="text-sm text-gray-600">
                  {accommodation.rating} ({accommodation.reviews} reviews)
                </span>
              </div>
            </div>
            <button
              onClick={toggleWishlist}
              className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            >
              {isWishlisted ? (
                <HeartSolidIcon className="w-6 h-6 text-red-500" />
              ) : (
                <HeartIcon className="w-6 h-6 text-gray-400" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Photo Gallery */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="relative">
          <div className="grid grid-cols-4 gap-3 h-[600px] rounded-2xl overflow-hidden shadow-2xl">
            {/* Main hero image */}
            <div
              className="col-span-2 relative cursor-pointer group overflow-hidden"
              onClick={() => openLightbox(accommodation.images, 0)}
            >
              <img
                src={accommodation.images[0]}
                alt={accommodation.title}
                className="w-full h-full object-cover transition-all duration-500 group-hover:scale-110 group-hover:brightness-105"
              />
              <div className="absolute inset-0 bg-gradient-to-br from-black/0 via-black/0 to-black/20 opacity-0 group-hover:opacity-100 transition-all duration-500"></div>
              <div className="absolute bottom-6 left-6 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-4 group-hover:translate-y-0">
                <button className="bg-white/90 backdrop-blur-sm text-gray-900 px-4 py-2 rounded-lg font-medium shadow-lg hover:bg-white transition-all">
                  View Gallery
                </button>
              </div>
            </div>

            {/* Smaller images grid */}
            <div className="col-span-2 grid grid-cols-2 grid-rows-2 gap-3">
              {accommodation.images.slice(1, 5).map((image, index) => (
                <div
                  key={index + 1}
                  className="relative cursor-pointer group overflow-hidden rounded-lg"
                  onClick={() => openLightbox(accommodation.images, index + 1)}
                >
                  <img
                    src={image}
                    alt={`${accommodation.title} photo ${index + 2}`}
                    className="w-full h-full object-cover transition-all duration-500 group-hover:scale-110 group-hover:brightness-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-br from-black/0 via-black/0 to-black/30 opacity-0 group-hover:opacity-100 transition-all duration-500"></div>

                  {index === 3 && accommodation.images.length > 5 && (
                    <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
                      <div className="text-white text-center">
                        <div className="text-2xl font-bold mb-1">
                          +{accommodation.images.length - 5}
                        </div>
                        <div className="text-sm font-medium">More Photos</div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div className="absolute top-6 right-6 bg-black/70 backdrop-blur-sm text-white px-4 py-2 rounded-xl text-sm font-medium shadow-lg flex items-center gap-2">
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            {accommodation.images.length} Photos
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 pb-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Main Info */}
          <div className="lg:col-span-2 space-y-8">
            {/* Basic Info */}
            <div>
              <div className="flex items-center text-gray-600 mb-4">
                <MapPinIcon className="w-5 h-5 mr-2" />
                <span className="text-lg">
                  {accommodation.city}, {accommodation.country}
                </span>
              </div>

              <div className="flex items-center gap-6 mb-6">
                <div className="flex items-center">
                  <UsersIcon className="w-5 h-5 text-blue-500 mr-2" />
                  <span className="font-semibold">
                    Up to {accommodation.maxGuests} guests
                  </span>
                </div>
                <div className="flex items-center">
                  <HomeIcon className="w-5 h-5 text-gray-400 mr-2" />
                  <span>
                    {accommodation.bedrooms} bedrooms •{" "}
                    {accommodation.bathrooms} bathrooms
                  </span>
                </div>
              </div>

              <p className="text-gray-700 leading-relaxed text-lg">
                {accommodation.description}
              </p>
            </div>

            {/* Room Type Selection */}
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                Choose Your Room
              </h2>
              <div className="grid gap-4">
                {Object.values(roomTypes).map((room) => (
                  <div
                    key={room.id}
                    className={`border-2 rounded-2xl p-6 cursor-pointer transition-all ${
                      selectedRoomType === room.id
                        ? "border-blue-500 bg-blue-50 shadow-lg"
                        : "border-gray-200 hover:border-gray-300 hover:shadow-md"
                    }`}
                    onClick={() => setSelectedRoomType(room.id as RoomTypeKey)}
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                          {room.name}
                        </h3>
                        <p className="text-gray-600 mb-2">{room.description}</p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <span>{room.size}</span>
                          <span>•</span>
                          <span>Up to {room.maxOccupancy} guests</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-blue-600">
                          ${room.basePrice / 100}
                        </div>
                        <div className="text-sm text-gray-500">per night</div>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                      {room.amenities.map((amenity) => (
                        <div key={amenity} className="flex items-center gap-2">
                          <CheckCircleIcon className="w-4 h-4 text-green-500" />
                          <span className="text-sm text-gray-700">
                            {amenity}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Rate Plan Selection */}
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                Choose Your Rate
              </h2>
              <div className="grid gap-4">
                {Object.values(ratePlans).map((plan) => (
                  <div
                    key={plan.id}
                    className={`border-2 rounded-2xl p-6 cursor-pointer transition-all ${
                      selectedRatePlan === plan.id
                        ? "border-blue-500 bg-blue-50 shadow-lg"
                        : "border-gray-200 hover:border-gray-300 hover:shadow-md"
                    }`}
                    onClick={() => setSelectedRatePlan(plan.id as RatePlanKey)}
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex items-center gap-4">
                        <div
                          className={`w-12 h-12 bg-${plan.color}-100 rounded-2xl flex items-center justify-center`}
                        >
                          {plan.id === "flexible" && (
                            <ShieldCheckIcon className="w-6 h-6 text-green-600" />
                          )}
                          {plan.id === "nonRefundable" && (
                            <BanknotesIcon className="w-6 h-6 text-red-600" />
                          )}
                          {plan.id === "bedBreakfast" && (
                            <CakeIcon className="w-6 h-6 text-blue-600" />
                          )}
                        </div>
                        <div>
                          <h3 className="text-xl font-semibold text-gray-900">
                            {plan.name}
                          </h3>
                          <p className="text-gray-600">{plan.description}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-gray-900">
                          $
                          {Math.round(
                            (roomTypes[selectedRoomType].basePrice / 100) *
                              plan.priceMultiplier
                          )}
                        </div>
                        <div className="text-sm text-gray-500">per night</div>
                        <div
                          className={`inline-block px-3 py-1 rounded-full text-xs font-medium bg-${plan.color}-100 text-${plan.color}-700 mt-2`}
                        >
                          {plan.availability}
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-3">
                          What&apos;s Included
                        </h4>
                        <div className="space-y-2">
                          {plan.perks.map((perk) => (
                            <div key={perk} className="flex items-center gap-2">
                              <CheckCircleIcon
                                className={`w-4 h-4 text-${plan.color}-500`}
                              />
                              <span className="text-sm text-gray-700">
                                {perk}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>

                      <div>
                        <h4 className="font-semibold text-gray-900 mb-3">
                          Cancellation Policy
                        </h4>
                        <div className="bg-gray-50 rounded-2xl p-4">
                          <div className="flex items-start gap-3">
                            {plan.id === "flexible" && (
                              <ShieldCheckIcon className="w-5 h-5 text-green-500 mt-0.5" />
                            )}
                            {plan.id === "nonRefundable" && (
                              <XMarkIcon className="w-5 h-5 text-red-500 mt-0.5" />
                            )}
                            {plan.id === "bedBreakfast" && (
                              <CalendarDaysIcon className="w-5 h-5 text-blue-500 mt-0.5" />
                            )}
                            <div>
                              <div className="font-medium text-gray-900 mb-1">
                                {plan.cancellation.policy}
                              </div>
                              <div className="text-sm text-gray-600">
                                Deadline: {plan.cancellation.deadline}
                              </div>
                              {plan.cancellation.fee !== 0 && (
                                <div className="text-sm text-red-600 mt-1">
                                  Fee: {plan.cancellation.fee}
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Amenities */}
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                Amenities
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {accommodation.amenities.map((amenity) => (
                  <div
                    key={amenity}
                    className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
                  >
                    <span className="text-2xl">{getAmenityIcon(amenity)}</span>
                    <span className="text-gray-700 font-medium">{amenity}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Location */}
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                Location
              </h2>
              <div className="bg-gray-100 rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <MapPinIcon className="w-6 h-6 text-gray-600 mt-1" />
                  <div>
                    <div className="font-medium text-gray-900 mb-1">
                      {accommodation.address}
                    </div>
                    <div className="text-gray-600">
                      {accommodation.city}, {accommodation.country}
                    </div>
                    <div className="text-sm text-gray-500 mt-2">
                      {accommodation.latitude &&
                      accommodation.longitude &&
                      (accommodation.latitude !== 0 ||
                        accommodation.longitude !== 0) ? (
                        <>
                          Coordinates: {accommodation.latitude.toFixed(4)},{" "}
                          {accommodation.longitude.toFixed(4)}
                        </>
                      ) : (
                        <>Coordinates: Not available</>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Host Info */}
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                Meet Your Host
              </h2>
              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                    {accommodation.host.name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">
                      Hosted by {accommodation.host.name}
                    </div>
                    <div className="text-gray-600 text-sm">
                      {accommodation.host.email}
                    </div>
                  </div>
                </div>
                <div className="space-y-2 text-sm text-gray-600 mb-4">
                  <div>Response time: within 2 hours</div>
                  <div>Languages: English, Spanish</div>
                  <div>Joined in 2020</div>
                </div>
                <div className="flex gap-2">
                  <button className="flex-1 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 transition-colors">
                    Message Host
                  </button>
                  <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                    <PhoneIcon className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Booking */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6 sticky top-24">
              <div className="mb-6">
                <div className="text-3xl font-bold text-blue-600">
                  ${calculateTotalPrice()}
                </div>
                <div className="text-gray-500">per night</div>
              </div>

              <div className="space-y-4 mb-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Check-in
                    </label>
                    <input
                      type="date"
                      value={checkIn}
                      onChange={(e) => setCheckIn(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Check-out
                    </label>
                    <input
                      type="date"
                      value={checkOut}
                      onChange={(e) => setCheckOut(e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Guests
                  </label>
                  <select
                    value={guests}
                    onChange={(e) => setGuests(parseInt(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    {Array.from(
                      { length: accommodation.maxGuests },
                      (_, i) => i + 1
                    ).map((num) => (
                      <option key={num} value={num}>
                        {num} guest{num !== 1 ? "s" : ""}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Selected Options Summary */}
              <div className="bg-gray-50 rounded-lg p-4 mb-6">
                <h4 className="font-semibold text-gray-900 mb-3">
                  Your Selection
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Room:</span>
                    <span className="font-medium">
                      {roomTypes[selectedRoomType].name}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Rate:</span>
                    <span className="font-medium">
                      {ratePlans[selectedRatePlan].name}
                    </span>
                  </div>
                </div>
              </div>

              {/* Price Breakdown */}
              <div className="bg-gray-50 rounded-lg p-4 mb-6">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Room Rate</span>
                  <span className="font-medium">${calculateTotalPrice()}</span>
                </div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Taxes & Fees</span>
                  <span className="font-medium">
                    ${Math.round(calculateTotalPrice() * 0.15)}
                  </span>
                </div>
                <div className="border-t pt-2 mt-2">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-gray-900">
                      Total per night
                    </span>
                    <span className="text-xl font-bold text-blue-600">
                      $
                      {calculateTotalPrice() +
                        Math.round(calculateTotalPrice() * 0.15)}
                    </span>
                  </div>
                </div>
              </div>

              <button className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-4 px-4 rounded-xl transition-all duration-200 hover:shadow-lg hover:shadow-blue-200/50 hover:-translate-y-0.5 mb-4">
                Reserve Now
              </button>

              <div className="text-center text-sm text-gray-500 mb-4">
                You won&apos;t be charged yet
              </div>

              {/* House Rules */}
              <div className="border-t pt-6">
                <h4 className="font-semibold text-gray-900 mb-4">
                  House Rules
                </h4>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <ClockIcon className="w-5 h-5 text-gray-400" />
                    <div>
                      <div className="font-medium text-gray-900">
                        Check-in: 3:00 PM
                      </div>
                      <div className="text-sm text-gray-600">
                        Check-out: 11:00 AM
                      </div>
                    </div>
                  </div>
                  <div className="text-sm text-gray-600 space-y-1">
                    <div>• No smoking</div>
                    <div>• No pets allowed</div>
                    <div>• No parties or events</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Lightbox Modal */}
      {isLightboxOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-95 z-50 flex items-center justify-center">
          <button
            onClick={closeLightbox}
            className="absolute top-6 right-6 text-white hover:text-gray-300 transition-colors z-60"
          >
            <svg
              className="w-8 h-8"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          {lightboxImages.length > 1 && (
            <>
              <button
                onClick={prevImage}
                className="absolute left-6 top-1/2 -translate-y-1/2 text-white hover:text-gray-300 transition-colors z-60"
              >
                <svg
                  className="w-10 h-10"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
              </button>
              <button
                onClick={nextImage}
                className="absolute right-6 top-1/2 -translate-y-1/2 text-white hover:text-gray-300 transition-colors z-60"
              >
                <svg
                  className="w-10 h-10"
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
              </button>
            </>
          )}

          <div className="max-w-7xl max-h-[90vh] mx-auto px-6">
            <img
              src={lightboxImages[currentImageIndex]}
              alt={`${accommodation.title} photo ${currentImageIndex + 1}`}
              className="max-h-[80vh] max-w-full object-contain rounded-lg shadow-2xl"
            />

            <div className="mt-4 text-white text-center">
              {currentImageIndex + 1} / {lightboxImages.length}
            </div>
          </div>

          <div className="absolute bottom-20 left-1/2 -translate-x-1/2 flex gap-2 overflow-x-auto px-4">
            {lightboxImages.map((image, index) => (
              <button
                key={index}
                onClick={() => setCurrentImageIndex(index)}
                className={`flex-shrink-0 w-16 h-12 rounded overflow-hidden transition-opacity ${
                  index === currentImageIndex
                    ? "ring-2 ring-white opacity-100"
                    : "opacity-60 hover:opacity-80"
                }`}
              >
                <img
                  src={image}
                  alt={`Thumbnail ${index + 1}`}
                  className="w-full h-full object-cover"
                />
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
