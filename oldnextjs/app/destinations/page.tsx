"use client";

import React, { useState, useRef } from "react";
import Image from "next/image";
import {
  ChevronRightIcon,
  MapPinIcon,
  StarIcon,
  ClockIcon,
  UsersIcon,
  MagnifyingGlassIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
import { StarIcon as StarIconSolid } from "@heroicons/react/24/solid";

interface Destination {
  id: string;
  name: string;
  country: string;
  imageUrl: string;
  description: string;
  highlights: string[];
  bestTimeToVisit: string;
  duration: string;
  groupSize: string;
  rating: number;
  reviewCount: number;
  startingPrice: number;
  currency: string;
  activities: string[];
  category: string;
}

const destinations: Destination[] = [
  {
    id: "1",
    name: "Petra",
    country: "Jordan",
    imageUrl: "/hero/chalets.webp",
    description:
      "Discover the ancient Nabatean city carved into rose-red cliffs, a UNESCO World Heritage Site and one of the Seven Wonders of the World.",
    highlights: [
      "Treasury Building",
      "Monastery",
      "Royal Tombs",
      "Siq Canyon",
      "Bedouin Culture",
    ],
    bestTimeToVisit: "March to May, September to November",
    duration: "1-2 days",
    groupSize: "Small groups (2-12 people)",
    rating: 4.8,
    reviewCount: 2450,
    startingPrice: 85,
    currency: "USD",
    activities: [
      "Historical Tours",
      "Camel Riding",
      "Hiking",
      "Cultural Experiences",
    ],
    category: "Historical",
  },
  {
    id: "2",
    name: "Dubai",
    country: "UAE",
    imageUrl: "/hero/hotel.webp",
    description:
      "Experience the ultimate luxury destination with futuristic skyscrapers, world-class shopping, and desert adventures in one of the most modern cities on Earth.",
    highlights: [
      "Burj Khalifa",
      "Palm Jumeirah",
      "Dubai Mall",
      "Desert Safari",
      "Gold Souk",
    ],
    bestTimeToVisit: "November to March",
    duration: "3-5 days",
    groupSize: "Private or small groups",
    rating: 4.6,
    reviewCount: 3200,
    startingPrice: 150,
    currency: "USD",
    activities: [
      "City Tours",
      "Desert Activities",
      "Shopping",
      "Luxury Experiences",
    ],
    category: "Modern",
  },
  {
    id: "3",
    name: "Jerusalem",
    country: "Palestine",
    imageUrl: "/hero/travelhero.webp",
    description:
      "Explore the holy city that holds immense religious significance for Judaism, Christianity, and Islam, featuring ancient walls, sacred sites, and vibrant markets.",
    highlights: [
      "Western Wall",
      "Church of the Holy Sepulchre",
      "Dome of the Rock",
      "Old City",
      "Mount of Olives",
    ],
    bestTimeToVisit: "March to May, September to November",
    duration: "2-3 days",
    groupSize: "Small guided groups",
    rating: 4.7,
    reviewCount: 2100,
    startingPrice: 95,
    currency: "USD",
    activities: [
      "Religious Tours",
      "Historical Sites",
      "Market Exploration",
      "Cultural Experiences",
    ],
    category: "Historical",
  },
  {
    id: "4",
    name: "Mecca",
    country: "Saudi Arabia",
    imageUrl: "/hero/caravan.webp",
    description:
      "Visit the holiest city in Islam, home to the Kaaba and the Grand Mosque, where millions of pilgrims gather for Hajj and Umrah.",
    highlights: [
      "Kaaba",
      "Grand Mosque",
      "Mount Arafat",
      "Zamzam Well",
      "Islamic History",
    ],
    bestTimeToVisit: "All year round (best outside Hajj season)",
    duration: "3-7 days",
    groupSize: "Large pilgrimage groups",
    rating: 4.9,
    reviewCount: 1800,
    startingPrice: 200,
    currency: "USD",
    activities: [
      "Religious Pilgrimage",
      "Islamic Studies",
      "Historical Tours",
      "Spiritual Retreats",
    ],
    category: "Cultural",
  },
  {
    id: "5",
    name: "Doha",
    country: "Qatar",
    imageUrl: "/hero/apartment.webp",
    description:
      "Experience Qatar's modern capital city, blending traditional Islamic architecture with cutting-edge contemporary design and world-class museums.",
    highlights: [
      "Museum of Islamic Art",
      "Souq Waqif",
      "Katara Cultural Village",
      "Desert Adventures",
      "Luxury Shopping",
    ],
    bestTimeToVisit: "November to March",
    duration: "2-4 days",
    groupSize: "Private or small groups",
    rating: 4.4,
    reviewCount: 1420,
    startingPrice: 135,
    currency: "USD",
    activities: [
      "Museum Tours",
      "Cultural Experiences",
      "Desert Activities",
      "Shopping",
    ],
    category: "Cultural",
  },
  {
    id: "6",
    name: "Riyadh",
    country: "Saudi Arabia",
    imageUrl: "/hero/caravan.webp",
    description:
      "Explore Saudi Arabia's dynamic capital, where ancient traditions meet modern innovation, featuring stunning mosques and vibrant modern culture.",
    highlights: [
      "Masmak Fortress",
      "Souq Al Zal",
      "Murabba Palace",
      "Wadi Hanifa",
      "Modern Architecture",
    ],
    bestTimeToVisit: "October to April",
    duration: "3-5 days",
    groupSize: "Private tours recommended",
    rating: 4.3,
    reviewCount: 1680,
    startingPrice: 125,
    currency: "USD",
    activities: [
      "Historical Tours",
      "Cultural Experiences",
      "Market Visits",
      "Modern Attractions",
    ],
    category: "Cultural",
  },
  {
    id: "7",
    name: "Kuwait City",
    country: "Kuwait",
    imageUrl: "/hero/travelhero.webp",
    description:
      "Discover Kuwait's modern capital with its impressive skyline, traditional souks, and rich maritime heritage along the Persian Gulf.",
    highlights: [
      "Kuwait Towers",
      "Souq Mubarakiya",
      "Liberation Tower",
      "Tareq Rajab Museum",
      "Marina Bay",
    ],
    bestTimeToVisit: "November to March",
    duration: "2-3 days",
    groupSize: "Small groups",
    rating: 4.2,
    reviewCount: 920,
    startingPrice: 95,
    currency: "USD",
    activities: [
      "City Tours",
      "Museum Visits",
      "Market Exploration",
      "Cultural Experiences",
    ],
    category: "Modern",
  },
  {
    id: "8",
    name: "Manama",
    country: "Bahrain",
    imageUrl: "/hero/apartment.webp",
    description:
      "Explore Bahrain's vibrant capital, known for its ancient forts, modern financial district, and rich pearl diving heritage.",
    highlights: [
      "Bahrain Fort",
      "Bab Al Bahrain",
      "Gold Souq",
      "Formula 1 Circuit",
      "Pearl Diving History",
    ],
    bestTimeToVisit: "November to March",
    duration: "2-3 days",
    groupSize: "Small groups",
    rating: 4.1,
    reviewCount: 1100,
    startingPrice: 85,
    currency: "USD",
    activities: [
      "Historical Tours",
      "Market Visits",
      "Cultural Experiences",
      "Modern Attractions",
    ],
    category: "Cultural",
  },
  {
    id: "9",
    name: "Amman",
    country: "Jordan",
    imageUrl: "/hero/chalets.webp",
    description:
      "Discover Jordan's modern capital, blending ancient Roman ruins with contemporary culture and serving as a gateway to Petra and other wonders.",
    highlights: [
      "Roman Theater",
      "Citadel",
      "Rainbow Street",
      "Royal Automobile Museum",
      "Modern Art Scene",
    ],
    bestTimeToVisit: "March to May, September to November",
    duration: "2-3 days",
    groupSize: "Small groups",
    rating: 4.3,
    reviewCount: 1350,
    startingPrice: 75,
    currency: "USD",
    activities: [
      "Historical Tours",
      "Cultural Experiences",
      "Modern Attractions",
      "Market Exploration",
    ],
    category: "Cultural",
  },
  {
    id: "10",
    name: "Muscat",
    country: "Oman",
    imageUrl: "/hero/hotel.webp",
    description:
      "Experience Oman's elegant capital, known for its stunning coastline, Portuguese forts, and traditional souks along the Arabian Sea.",
    highlights: [
      "Sultan Qaboos Grand Mosque",
      "Mutrah Souq",
      "Al Alam Palace",
      "Portuguese Forts",
      "Coastal Beauty",
    ],
    bestTimeToVisit: "October to April",
    duration: "2-4 days",
    groupSize: "Small private groups",
    rating: 4.5,
    reviewCount: 980,
    startingPrice: 110,
    currency: "USD",
    activities: [
      "Historical Tours",
      "Market Visits",
      "Coastal Activities",
      "Cultural Experiences",
    ],
    category: "Cultural",
  },
  {
    id: "11",
    name: "Damascus",
    country: "Syria",
    imageUrl: "/hero/treehouses.webp",
    description:
      "Visit one of the world's oldest continuously inhabited cities, known as the 'City of Jasmine' with its rich history and architectural wonders.",
    highlights: [
      "Umayyad Mosque",
      "Citadel of Damascus",
      "Souq Hamidiyeh",
      "Azem Palace",
      "Ancient City Walls",
    ],
    bestTimeToVisit: "March to May, October to November",
    duration: "2-3 days",
    groupSize: "Small private groups",
    rating: 4.0,
    reviewCount: 650,
    startingPrice: 65,
    currency: "USD",
    activities: [
      "Historical Tours",
      "Cultural Experiences",
      "Market Visits",
      "Architectural Sites",
    ],
    category: "Historical",
  },
  {
    id: "12",
    name: "Baghdad",
    country: "Iraq",
    imageUrl: "/hero/motels.webp",
    description:
      "Explore Iraq's historic capital, once the center of the Islamic Golden Age, featuring ancient monuments and vibrant modern culture.",
    highlights: [
      "Mustansiriya Madrasa",
      "Al-Kadhimiya Mosque",
      "Baghdad Zoo",
      "Mutanabbi Street",
      "Archaeological Sites",
    ],
    bestTimeToVisit: "October to April",
    duration: "2-3 days",
    groupSize: "Private tours with security",
    rating: 3.8,
    reviewCount: 420,
    startingPrice: 70,
    currency: "USD",
    activities: [
      "Historical Tours",
      "Cultural Experiences",
      "Market Visits",
      "Educational Tours",
    ],
    category: "Historical",
  },
  {
    id: "13",
    name: "Sana'a",
    country: "Yemen",
    imageUrl: "/hero/hostels.webp",
    description:
      "Discover Yemen's ancient capital, a UNESCO World Heritage city famous for its unique architecture and rich cultural heritage.",
    highlights: [
      "Old City of Sana'a",
      "Great Mosque of Sana'a",
      "Sabaean Temples",
      "Traditional Architecture",
      "Local Markets",
    ],
    bestTimeToVisit: "November to February",
    duration: "2-3 days",
    groupSize: "Small private groups",
    rating: 3.9,
    reviewCount: 380,
    startingPrice: 80,
    currency: "USD",
    activities: [
      "Historical Tours",
      "Cultural Experiences",
      "Architectural Walks",
      "Market Exploration",
    ],
    category: "Historical",
  },
  {
    id: "14",
    name: "Ramallah",
    country: "Palestine",
    imageUrl: "/hero/caravan.webp",
    description:
      "Experience the cultural and political heart of Palestine, offering insights into Palestinian culture, history, and contemporary life.",
    highlights: [
      "Yasser Arafat Museum",
      "Ramallah Cultural Palace",
      "Local Markets",
      "Olive Groves",
      "Cultural Centers",
    ],
    bestTimeToVisit: "March to May, September to November",
    duration: "1-2 days",
    groupSize: "Small educational groups",
    rating: 4.1,
    reviewCount: 520,
    startingPrice: 45,
    currency: "USD",
    activities: [
      "Cultural Tours",
      "Historical Sites",
      "Market Visits",
      "Educational Experiences",
    ],
    category: "Cultural",
  },
];

const categories = ["All", "Historical", "Cultural", "Modern"];

export default function DestinationsPage() {
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchTerm, setSearchTerm] = useState("");
  const [isSearchFocused, setIsSearchFocused] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);

  const filteredDestinations = destinations.filter((destination) => {
    const matchesCategory =
      selectedCategory === "All" || destination.category === selectedCategory;

    if (!searchTerm.trim()) {
      return matchesCategory;
    }

    const searchLower = searchTerm.toLowerCase();
    const matchesSearch =
      destination.name.toLowerCase().includes(searchLower) ||
      destination.country.toLowerCase().includes(searchLower) ||
      destination.description.toLowerCase().includes(searchLower) ||
      destination.highlights.some((highlight) =>
        highlight.toLowerCase().includes(searchLower)
      ) ||
      destination.activities.some((activity) =>
        activity.toLowerCase().includes(searchLower)
      ) ||
      destination.category.toLowerCase().includes(searchLower);

    return matchesCategory && matchesSearch;
  });

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const clearSearch = () => {
    setSearchTerm("");
    searchInputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Escape") {
      clearSearch();
    }
  };

  // Get search suggestions
  const getSearchSuggestions = () => {
    if (!searchTerm.trim() || !isSearchFocused) return [];

    const suggestions = new Set<string>();
    const searchLower = searchTerm.toLowerCase();

    destinations.forEach((destination) => {
      // Add destination names
      if (destination.name.toLowerCase().includes(searchLower)) {
        suggestions.add(destination.name);
      }
      // Add countries
      if (destination.country.toLowerCase().includes(searchLower)) {
        suggestions.add(destination.country);
      }
      // Add highlights
      destination.highlights.forEach((highlight) => {
        if (highlight.toLowerCase().includes(searchLower)) {
          suggestions.add(highlight);
        }
      });
      // Add activities
      destination.activities.forEach((activity) => {
        if (activity.toLowerCase().includes(searchLower)) {
          suggestions.add(activity);
        }
      });
    });

    return Array.from(suggestions).slice(0, 5); // Limit to 5 suggestions
  };

  const suggestions = getSearchSuggestions();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section
        className="relative bg-gradient-to-r from-orange-600 to-red-600 text-white py-24 min-h-[60vh] bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage:
            "url('/hero/handsome-tourist-with-summer-hat-reading-map-looking-sightseeing-vacation-standing-blue-ba.jpg')",
        }}
      >
        <div className="absolute inset-0 bg-black/40"></div>
        <div className="relative max-w-7xl mx-auto px-6 text-center">
          <h1 className="text-5xl font-bold mb-6">
            Discover the Middle East & Gulf
          </h1>
          <p className="text-xl mb-8 max-w-3xl mx-auto">
            Explore ancient wonders, modern marvels, and rich cultural
            experiences across 14 incredible destinations
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <div className="relative w-full sm:w-80">
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  ref={searchInputRef}
                  type="text"
                  placeholder="Search destinations, countries, activities..."
                  value={searchTerm}
                  onChange={handleSearchChange}
                  onKeyDown={handleKeyDown}
                  onFocus={() => setIsSearchFocused(true)}
                  onBlur={() =>
                    setTimeout(() => setIsSearchFocused(false), 200)
                  }
                  className="w-full pl-10 pr-10 py-3 rounded-lg bg-white/95 backdrop-blur-sm text-gray-900 border-2 border-white/30 focus:outline-none focus:ring-2 focus:ring-white focus:border-white placeholder-gray-600 shadow-lg"
                />
                {searchTerm && (
                  <button
                    onClick={clearSearch}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 transition-colors"
                  >
                    <XMarkIcon className="w-5 h-5" />
                  </button>
                )}
              </div>

              {/* Search Suggestions */}
              {suggestions.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white rounded-lg shadow-lg border z-50 max-h-60 overflow-y-auto">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => setSearchTerm(suggestion)}
                      className="w-full text-left px-4 py-2 hover:bg-gray-50 first:rounded-t-lg last:rounded-b-lg transition-colors"
                    >
                      <div className="flex items-center">
                        <MagnifyingGlassIcon className="w-4 h-4 text-gray-400 mr-2" />
                        <span className="text-gray-700">{suggestion}</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
            <div className="flex gap-2">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    selectedCategory === category
                      ? "bg-white text-orange-600"
                      : "bg-white/20 text-white hover:bg-white/30"
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white border-b">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">14</div>
              <div className="text-gray-600">Destinations</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">
                1000+
              </div>
              <div className="text-gray-600">Activities</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">4.5</div>
              <div className="text-gray-600">Average Rating</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">
                24/7
              </div>
              <div className="text-gray-600">Support</div>
            </div>
          </div>
        </div>
      </section>

      {/* Destinations Grid */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-6">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              {searchTerm
                ? `Search Results for "${searchTerm}"`
                : "Explore All Destinations"}
            </h2>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <p className="text-lg text-gray-600">
                {searchTerm
                  ? `Found ${filteredDestinations.length} destination${
                      filteredDestinations.length !== 1 ? "s" : ""
                    } matching your search`
                  : `Showing ${filteredDestinations.length} of ${destinations.length} destinations`}
              </p>
              {searchTerm && (
                <button
                  onClick={clearSearch}
                  className="inline-flex items-center px-4 py-2 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 transition-colors text-sm font-medium"
                >
                  <XMarkIcon className="w-4 h-4 mr-2" />
                  Clear Search
                </button>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredDestinations.length > 0 ? (
              filteredDestinations.map((destination) => (
                <div
                  key={destination.id}
                  className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 group"
                >
                  {/* Image */}
                  <div className="relative h-64 overflow-hidden">
                    <Image
                      src={destination.imageUrl}
                      alt={destination.name}
                      fill
                      className="object-cover group-hover:scale-110 transition-transform duration-500"
                    />
                    <div className="absolute top-4 left-4">
                      <span className="bg-orange-500 text-white px-3 py-1 text-sm font-semibold rounded-full">
                        {destination.category}
                      </span>
                    </div>
                    <div className="absolute top-4 right-4">
                      <div className="flex items-center bg-white/90 backdrop-blur-sm rounded-lg px-2 py-1">
                        <StarIconSolid className="w-4 h-4 text-yellow-400" />
                        <span className="text-sm font-semibold ml-1">
                          {destination.rating}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Content */}
                  <div className="p-6">
                    <div className="mb-3">
                      <h3 className="text-2xl font-bold text-gray-900 mb-1 group-hover:text-orange-600 transition-colors">
                        {destination.name}
                      </h3>
                      <div className="flex items-center text-gray-600 mb-2">
                        <MapPinIcon className="w-4 h-4 mr-1" />
                        <span>{destination.country}</span>
                      </div>
                      <p className="text-gray-600 text-sm line-clamp-2">
                        {destination.description}
                      </p>
                    </div>

                    {/* Highlights */}
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-2">
                        Highlights:
                      </h4>
                      <div className="flex flex-wrap gap-1">
                        {destination.highlights
                          .slice(0, 3)
                          .map((highlight, index) => (
                            <span
                              key={index}
                              className="bg-gray-100 text-gray-700 px-2 py-1 text-xs rounded-full"
                            >
                              {highlight}
                            </span>
                          ))}
                        {destination.highlights.length > 3 && (
                          <span className="text-gray-500 text-xs">
                            +{destination.highlights.length - 3} more
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Details */}
                    <div className="flex items-center justify-between text-sm text-gray-600 mb-4">
                      <div className="flex items-center">
                        <ClockIcon className="w-4 h-4 mr-1" />
                        <span>{destination.duration}</span>
                      </div>
                      <div className="flex items-center">
                        <UsersIcon className="w-4 h-4 mr-1" />
                        <span>{destination.groupSize}</span>
                      </div>
                    </div>

                    {/* Price and CTA */}
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-2xl font-bold text-gray-900">
                          ${destination.startingPrice}
                        </div>
                        <div className="text-sm text-gray-600">per person</div>
                      </div>
                      <button className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-3 rounded-xl font-semibold transition-all duration-200 hover:shadow-lg hover:shadow-orange-200/50 flex items-center gap-2 group-hover:translate-x-1">
                        Explore
                        <ChevronRightIcon className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="col-span-full text-center py-16">
                <div className="max-w-md mx-auto">
                  <MagnifyingGlassIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    No destinations found
                  </h3>
                  <p className="text-gray-600 mb-6">
                    We couldn&apos;t find any destinations matching &quot;
                    {searchTerm}&quot;. Try adjusting your search terms or
                    browse all destinations.
                  </p>
                  <div className="flex flex-col sm:flex-row gap-3 justify-center">
                    <button
                      onClick={clearSearch}
                      className="bg-orange-600 text-white px-6 py-2 rounded-lg hover:bg-orange-700 transition-colors"
                    >
                      Clear Search
                    </button>
                    <button
                      onClick={() => setSelectedCategory("All")}
                      className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      View All Destinations
                    </button>
                  </div>
                  <div className="mt-6">
                    <p className="text-sm text-gray-500 mb-3">
                      Popular searches:
                    </p>
                    <div className="flex flex-wrap gap-2 justify-center">
                      {[
                        "Petra",
                        "Dubai",
                        "Jerusalem",
                        "Historical",
                        "Cultural",
                      ].map((term) => (
                        <button
                          key={term}
                          onClick={() => setSearchTerm(term)}
                          className="bg-gray-100 text-gray-700 px-3 py-1 text-sm rounded-full hover:bg-gray-200 transition-colors"
                        >
                          {term}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 bg-gradient-to-r from-orange-600 to-red-600 text-white">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Start Your Middle East Adventure?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Book your personalized experience today and discover the magic of
            the Middle East and Gulf region
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-orange-600 px-8 py-4 rounded-xl font-bold text-lg hover:bg-gray-100 transition-all duration-200 hover:shadow-lg">
              Start Planning
            </button>
            <button className="border-2 border-white text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-white/10 transition-all duration-200">
              Contact Us
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
