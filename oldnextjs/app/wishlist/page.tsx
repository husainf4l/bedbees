"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { useAuth } from "@/providers/AuthContext";
import {
  HeartIcon,
  MapPinIcon,
  StarIcon,
  ClockIcon,
  UsersIcon,
  XMarkIcon,
  AdjustmentsHorizontalIcon,
} from "@heroicons/react/24/outline";
import { HeartIcon as HeartSolidIcon } from "@heroicons/react/24/solid";

interface WishlistItem {
  id: string;
  type: "tour" | "accommodation" | "experience";
  title: string;
  location: string;
  image: string;
  price: number;
  currency: string;
  rating: number;
  reviews: number;
  duration?: string;
  guests?: number;
  description: string;
  addedDate: string;
  provider: {
    name: string;
    verified: boolean;
  };
  tags: string[];
}

const mockWishlistItems: WishlistItem[] = [
  {
    id: "WL-001",
    type: "tour",
    title: "Desert Safari Adventure",
    location: "Dubai, UAE",
    image: "/hero/villa.webp",
    price: 8500,
    currency: "AED",
    rating: 4.8,
    reviews: 1247,
    duration: "6 hours",
    description:
      "Experience the thrill of dune bashing, camel riding, and traditional Bedouin camp with BBQ dinner under the stars.",
    addedDate: "2025-09-20",
    provider: {
      name: "Desert Adventures Dubai",
      verified: true,
    },
    tags: ["Adventure", "Desert", "Cultural"],
  },
  {
    id: "WL-002",
    type: "accommodation",
    title: "Burj Al Arab Luxury Suite",
    location: "Dubai, UAE",
    image: "/hero/hotel.webp",
    price: 25000,
    currency: "AED",
    rating: 4.9,
    reviews: 2156,
    guests: 2,
    description:
      "World-famous luxury hotel with stunning views of the Arabian Gulf, private beach, and 7-star service.",
    addedDate: "2025-09-18",
    provider: {
      name: "Burj Al Arab Jumeirah",
      verified: true,
    },
    tags: ["Luxury", "Beachfront", "5-Star"],
  },
  {
    id: "WL-003",
    type: "experience",
    title: "Traditional Arabic Cooking Class",
    location: "Abu Dhabi, UAE",
    image: "/hero/apartment.webp",
    price: 1200,
    currency: "AED",
    rating: 4.7,
    reviews: 892,
    duration: "3 hours",
    guests: 8,
    description:
      "Learn to cook authentic Emirati dishes with a local chef in a traditional majlis setting.",
    addedDate: "2025-09-15",
    provider: {
      name: "Emirati Culinary Arts",
      verified: true,
    },
    tags: ["Cooking", "Cultural", "Food"],
  },
  {
    id: "WL-004",
    type: "tour",
    title: "Mountain Hiking in Ras Al Khaimah",
    location: "Ras Al Khaimah, UAE",
    image: "/hero/treehouses.webp",
    price: 6500,
    currency: "AED",
    rating: 4.6,
    reviews: 634,
    duration: "8 hours",
    description:
      "Guided hiking tour through the stunning Hajar Mountains with breathtaking views and local wildlife.",
    addedDate: "2025-09-12",
    provider: {
      name: "RAK Outdoor Adventures",
      verified: false,
    },
    tags: ["Hiking", "Nature", "Adventure"],
  },
  {
    id: "WL-005",
    type: "accommodation",
    title: "Desert Camp Glamping",
    location: "Liwa Oasis, UAE",
    image: "/hero/chalets.webp",
    price: 18000,
    currency: "AED",
    rating: 4.5,
    reviews: 423,
    guests: 4,
    description:
      "Luxury glamping experience in the heart of the desert with air-conditioned tents and private bathrooms.",
    addedDate: "2025-09-10",
    provider: {
      name: "Liwa Desert Retreats",
      verified: true,
    },
    tags: ["Glamping", "Desert", "Luxury"],
  },
  {
    id: "WL-006",
    type: "experience",
    title: "Dhow Cruise Dinner",
    location: "Dubai Marina, UAE",
    image: "/hero/travelhero.webp",
    price: 9500,
    currency: "AED",
    rating: 4.8,
    reviews: 1156,
    duration: "3 hours",
    guests: 20,
    description:
      "Romantic dinner cruise on a traditional wooden dhow with live entertainment and Arabian Gulf views.",
    addedDate: "2025-09-08",
    provider: {
      name: "Dubai Marina Cruises",
      verified: true,
    },
    tags: ["Cruise", "Dinner", "Romantic"],
  },
];

export default function WishlistPage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [wishlistItems, setWishlistItems] = useState<WishlistItem[]>([]);
  const [filterType, setFilterType] = useState<string>("all");
  const [filterLocation, setFilterLocation] = useState<string>("all");
  const [sortBy, setSortBy] = useState<string>("date-desc");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
      return;
    }

    // Load mock wishlist data
    setWishlistItems(mockWishlistItems);
  }, [user, loading, router]);

  const filteredItems = wishlistItems
    .filter((item) => filterType === "all" || item.type === filterType)
    .filter(
      (item) =>
        filterLocation === "all" || item.location.includes(filterLocation)
    )
    .sort((a, b) => {
      switch (sortBy) {
        case "date-desc":
          return (
            new Date(b.addedDate).getTime() - new Date(a.addedDate).getTime()
          );
        case "date-asc":
          return (
            new Date(a.addedDate).getTime() - new Date(b.addedDate).getTime()
          );
        case "price-desc":
          return b.price - a.price;
        case "price-asc":
          return a.price - b.price;
        case "rating-desc":
          return b.rating - a.rating;
        case "rating-asc":
          return a.rating - b.rating;
        default:
          return 0;
      }
    });

  const removeFromWishlist = (itemId: string) => {
    setWishlistItems((prevItems) =>
      prevItems.filter((item) => item.id !== itemId)
    );
  };

  const formatPrice = (price: number, currency: string) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency === "AED" ? "AED" : "USD",
      minimumFractionDigits: 0,
    }).format(price / 100);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case "tour":
        return "bg-blue-100 text-blue-800";
      case "accommodation":
        return "bg-green-100 text-green-800";
      case "experience":
        return "bg-purple-100 text-purple-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your wishlist...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Access Denied
          </h1>
          <p className="text-gray-600 mb-6">
            Please log in to view your wishlist.
          </p>
          <button
            onClick={() => router.push("/login")}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Log In
          </button>
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
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Wishlist</h1>
              <p className="text-gray-600 mt-1">
                Your saved experiences and favorite destinations
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                {filteredItems.length} item
                {filteredItems.length !== 1 ? "s" : ""}
              </span>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setViewMode("grid")}
                  className={`p-2 rounded-lg ${
                    viewMode === "grid"
                      ? "bg-blue-100 text-blue-600"
                      : "text-gray-400 hover:text-gray-600"
                  }`}
                >
                  <AdjustmentsHorizontalIcon className="w-5 h-5" />
                </button>
                <button
                  onClick={() => setViewMode("list")}
                  className={`p-2 rounded-lg ${
                    viewMode === "list"
                      ? "bg-blue-100 text-blue-600"
                      : "text-gray-400 hover:text-gray-600"
                  }`}
                >
                  <div className="w-5 h-5 flex flex-col space-y-0.5">
                    <div className="h-0.5 bg-current rounded"></div>
                    <div className="h-0.5 bg-current rounded"></div>
                    <div className="h-0.5 bg-current rounded"></div>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Filters and Sorting */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex flex-wrap gap-4 items-center">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Types</option>
                <option value="tour">Tours</option>
                <option value="accommodation">Accommodations</option>
                <option value="experience">Experiences</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Location
              </label>
              <select
                value={filterLocation}
                onChange={(e) => setFilterLocation(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Locations</option>
                <option value="Dubai">Dubai</option>
                <option value="Abu Dhabi">Abu Dhabi</option>
                <option value="Ras Al Khaimah">Ras Al Khaimah</option>
                <option value="Liwa">Liwa Oasis</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Sort By
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="date-desc">Recently Added</option>
                <option value="date-asc">Oldest First</option>
                <option value="price-desc">Highest Price</option>
                <option value="price-asc">Lowest Price</option>
                <option value="rating-desc">Highest Rated</option>
                <option value="rating-asc">Lowest Rated</option>
              </select>
            </div>
          </div>
        </div>

        {/* Wishlist Items */}
        {filteredItems.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <HeartIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Your wishlist is empty
            </h3>
            <p className="text-gray-600 mb-6">
              Start exploring amazing destinations and save your favorites here.
            </p>
            <button
              onClick={() => router.push("/")}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Explore Destinations
            </button>
          </div>
        ) : (
          <div
            className={
              viewMode === "grid"
                ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                : "space-y-4"
            }
          >
            {filteredItems.map((item) => (
              <div
                key={item.id}
                className={`bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow ${
                  viewMode === "list" ? "flex" : ""
                }`}
              >
                {/* Image */}
                <div
                  className={`relative ${
                    viewMode === "grid" ? "h-48" : "w-48 h-32 flex-shrink-0"
                  }`}
                >
                  <Image
                    src={item.image}
                    alt={item.title}
                    fill
                    className="object-cover"
                  />
                  <button
                    onClick={() => removeFromWishlist(item.id)}
                    className="absolute top-3 right-3 p-1.5 bg-white/80 backdrop-blur-sm rounded-full hover:bg-white transition-colors"
                  >
                    <XMarkIcon className="w-4 h-4 text-gray-600" />
                  </button>
                  <div className="absolute top-3 left-3">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(
                        item.type
                      )}`}
                    >
                      {item.type}
                    </span>
                  </div>
                </div>

                {/* Content */}
                <div className={`p-4 ${viewMode === "list" ? "flex-1" : ""}`}>
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">
                        {item.title}
                      </h3>
                      <div className="flex items-center text-gray-600 text-sm mb-2">
                        <MapPinIcon className="w-4 h-4 mr-1" />
                        {item.location}
                      </div>
                    </div>
                    <div className="text-right ml-4">
                      <div className="text-lg font-bold text-gray-900">
                        {formatPrice(item.price, item.currency)}
                      </div>
                      {item.duration && (
                        <div className="text-sm text-gray-600 flex items-center">
                          <ClockIcon className="w-3 h-3 mr-1" />
                          {item.duration}
                        </div>
                      )}
                      {item.guests && (
                        <div className="text-sm text-gray-600 flex items-center">
                          <UsersIcon className="w-3 h-3 mr-1" />
                          Up to {item.guests}
                        </div>
                      )}
                    </div>
                  </div>

                  <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                    {item.description}
                  </p>

                  {/* Rating and Provider */}
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center">
                      <div className="flex items-center mr-2">
                        {[...Array(5)].map((_, i) => (
                          <StarIcon
                            key={i}
                            className={`w-4 h-4 ${
                              i < Math.floor(item.rating)
                                ? "text-yellow-400 fill-current"
                                : "text-gray-300"
                            }`}
                          />
                        ))}
                      </div>
                      <span className="text-sm text-gray-600">
                        {item.rating} ({item.reviews} reviews)
                      </span>
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      {item.provider.verified && (
                        <span className="text-green-600 font-medium mr-1">
                          ✓
                        </span>
                      )}
                      {item.provider.name}
                    </div>
                  </div>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-1 mb-3">
                    {item.tags.slice(0, 3).map((tag, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  {/* Actions */}
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      Added {formatDate(item.addedDate)}
                    </span>
                    <div className="flex space-x-2">
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
                        Book Now
                      </button>
                      <button className="flex items-center text-gray-400 hover:text-red-500 transition-colors">
                        <HeartSolidIcon className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
