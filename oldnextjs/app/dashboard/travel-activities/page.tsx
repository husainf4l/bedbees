"use client";

import { useState } from "react";
import {
  MapPinIcon,
  ClockIcon,
  UsersIcon,
  StarIcon,
  HeartIcon,
  ShoppingCartIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
  GlobeAltIcon,
  SunIcon,
  FireIcon,
  BuildingOfficeIcon,
  MusicalNoteIcon,
  EyeIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
import { HeartIcon as HeartIconSolid } from "@heroicons/react/24/solid";

interface Activity {
  id: string;
  title: string;
  description: string;
  shortDescription: string;
  location: string;
  country: string;
  duration: string;
  price: number;
  currency: string;
  rating: number;
  reviews: number;
  images: string[];
  category: string;
  difficulty: "Easy" | "Moderate" | "Challenging";
  groupSize: string;
  languages: string[];
  highlights: string[];
  included: string[];
  notIncluded: string[];
  meetingPoint: string;
  cancellationPolicy: string;
  provider: {
    name: string;
    rating: number;
    verified: boolean;
  };
  tags: string[];
  availability: string[];
  isWishlisted?: boolean;
}

const mockActivities: Activity[] = [
  {
    id: "1",
    title: "Petra Private Day Tour from Amman",
    description:
      "Embark on an unforgettable journey to one of the New Seven Wonders of the World. This private tour offers you the flexibility to explore Petra at your own pace with a professional guide who will unveil the secrets of this ancient Nabataean city. Walk through the narrow Siq, marvel at the iconic Treasury, and discover the Royal Tombs and Monastery.",
    shortDescription:
      "Private guided tour to the ancient city of Petra with personalized experience",
    location: "Petra",
    country: "Jordan",
    duration: "10 hours",
    price: 120,
    currency: "USD",
    rating: 4.8,
    reviews: 1247,
    images: [
      "/activities/petra-1.jpg",
      "/activities/petra-2.jpg",
      "/activities/petra-3.jpg",
    ],
    category: "Historical & Cultural",
    difficulty: "Moderate",
    groupSize: "Private (up to 8 people)",
    languages: ["English", "Arabic", "Spanish"],
    highlights: [
      "Walk through the iconic Siq canyon",
      "See the magnificent Treasury facade",
      "Explore the Royal Tombs complex",
      "Optional hike to the Monastery",
      "Learn about Nabataean history",
    ],
    included: [
      "Professional guide",
      "Private transportation",
      "Entry tickets",
      "Bottled water",
    ],
    notIncluded: ["Lunch", "Personal expenses", "Gratuities"],
    meetingPoint: "Hotel pickup in Amman",
    cancellationPolicy: "Free cancellation up to 24 hours before",
    provider: {
      name: "Jordan Heritage Tours",
      rating: 4.9,
      verified: true,
    },
    tags: ["UNESCO", "Ancient", "Photography", "Walking"],
    availability: ["Daily", "Morning departure"],
    isWishlisted: false,
  },
  {
    id: "2",
    title: "Dead Sea Float & Spa Experience",
    description:
      "Experience the therapeutic wonders of the Dead Sea, the lowest point on Earth. Float effortlessly in the mineral-rich waters, known for their healing properties. Indulge in a natural mud treatment and enjoy the stunning desert landscape surrounding this natural wonder.",
    shortDescription:
      "Relaxing day at the Dead Sea with floating and mud treatments",
    location: "Dead Sea",
    country: "Jordan",
    duration: "6 hours",
    price: 75,
    currency: "USD",
    rating: 4.6,
    reviews: 892,
    images: ["/activities/dead-sea-1.jpg", "/activities/dead-sea-2.jpg"],
    category: "Wellness & Relaxation",
    difficulty: "Easy",
    groupSize: "Small group (max 12)",
    languages: ["English", "Arabic"],
    highlights: [
      "Float in the unique Dead Sea waters",
      "Natural mud body treatment",
      "Stunning panoramic views",
      "Visit to local spa facilities",
      "Photo opportunities",
    ],
    included: ["Transportation", "Spa access", "Towels", "Shower facilities"],
    notIncluded: ["Lunch", "Spa treatments (optional)", "Personal items"],
    meetingPoint: "Amman city center",
    cancellationPolicy: "Free cancellation up to 48 hours before",
    provider: {
      name: "Wellness Jordan",
      rating: 4.7,
      verified: true,
    },
    tags: ["Relaxation", "Wellness", "Natural", "Photography"],
    availability: ["Daily", "All year round"],
    isWishlisted: true,
  },
  {
    id: "3",
    title: "Wadi Rum Desert Safari & Stargazing",
    description:
      "Venture into the mystical Wadi Rum desert, famously known as the 'Valley of the Moon.' This adventure combines thrilling 4x4 desert exploration with traditional Bedouin culture. End your day with a magical stargazing experience under one of the world's clearest night skies.",
    shortDescription:
      "Desert adventure with 4x4 safari, Bedouin culture, and stargazing",
    location: "Wadi Rum",
    country: "Jordan",
    duration: "8 hours",
    price: 95,
    currency: "USD",
    rating: 4.9,
    reviews: 1156,
    images: [
      "/activities/wadi-rum-1.jpg",
      "/activities/wadi-rum-2.jpg",
      "/activities/wadi-rum-3.jpg",
    ],
    category: "Adventure & Nature",
    difficulty: "Easy",
    groupSize: "Small group (max 8)",
    languages: ["English", "Arabic"],
    highlights: [
      "4x4 jeep safari through red sand dunes",
      "Visit ancient rock inscriptions",
      "Traditional Bedouin camp experience",
      "Camel riding opportunity",
      "Professional stargazing with telescope",
    ],
    included: [
      "4x4 transportation",
      "Bedouin guide",
      "Traditional dinner",
      "Stargazing equipment",
    ],
    notIncluded: ["Accommodation", "Personal expenses", "Extra activities"],
    meetingPoint: "Wadi Rum village",
    cancellationPolicy: "Free cancellation up to 12 hours before",
    provider: {
      name: "Desert Stars Adventures",
      rating: 4.8,
      verified: true,
    },
    tags: ["Desert", "Adventure", "Stargazing", "Cultural", "4x4"],
    availability: ["Daily", "Weather dependent"],
    isWishlisted: false,
  },
  {
    id: "4",
    title: "Amman City Walking Food Tour",
    description:
      "Discover the culinary heart of Amman through this immersive food walking tour. Taste authentic Jordanian dishes, visit local markets, and learn about the city's rich food culture from expert local guides. Perfect for food lovers wanting to experience the real flavors of Jordan.",
    shortDescription:
      "Culinary walking tour through Amman's best local eateries and markets",
    location: "Amman",
    country: "Jordan",
    duration: "4 hours",
    price: 55,
    currency: "USD",
    rating: 4.7,
    reviews: 543,
    images: ["/activities/amman-food-1.jpg", "/activities/amman-food-2.jpg"],
    category: "Food & Culture",
    difficulty: "Easy",
    groupSize: "Small group (max 10)",
    languages: ["English", "Arabic"],
    highlights: [
      "Taste 15+ local dishes and beverages",
      "Visit traditional markets and bakeries",
      "Learn about Jordanian food culture",
      "Meet local vendors and artisans",
      "Explore historic downtown Amman",
    ],
    included: [
      "Professional guide",
      "All food tastings",
      "Market visits",
      "Cultural insights",
    ],
    notIncluded: [
      "Transportation to meeting point",
      "Additional drinks",
      "Gratuities",
    ],
    meetingPoint: "Downtown Amman - Rainbow Street",
    cancellationPolicy: "Free cancellation up to 24 hours before",
    provider: {
      name: "Amman Food Adventures",
      rating: 4.6,
      verified: true,
    },
    tags: ["Food", "Cultural", "Walking", "Local Experience"],
    availability: ["Tuesday, Thursday, Saturday", "Morning only"],
    isWishlisted: true,
  },
  {
    id: "5",
    title: "Jerash Ancient City & Ajloun Castle",
    description:
      "Step back in time and explore two of Jordan's most significant historical sites. Visit the remarkably preserved Roman city of Jerash, often called the 'Pompeii of the East,' and the impressive 12th-century Ajloun Castle with its stunning views over the Jordan Valley.",
    shortDescription:
      "Full-day historical tour combining Roman ruins and medieval castle",
    location: "Jerash & Ajloun",
    country: "Jordan",
    duration: "9 hours",
    price: 85,
    currency: "USD",
    rating: 4.5,
    reviews: 721,
    images: ["/activities/jerash-1.jpg", "/activities/ajloun-1.jpg"],
    category: "Historical & Cultural",
    difficulty: "Moderate",
    groupSize: "Standard group (max 15)",
    languages: ["English", "Arabic", "French"],
    highlights: [
      "Explore the Roman ruins of Jerash",
      "Walk the ancient cardo and forums",
      "Visit Ajloun Castle fortress",
      "Panoramic views of Jordan Valley",
      "Learn about Roman and Islamic history",
    ],
    included: ["Professional guide", "Transportation", "Entry fees", "Lunch"],
    notIncluded: ["Personal expenses", "Optional activities", "Beverages"],
    meetingPoint: "Hotel pickup available",
    cancellationPolicy: "Free cancellation up to 48 hours before",
    provider: {
      name: "Jordan Historical Tours",
      rating: 4.4,
      verified: true,
    },
    tags: ["Historical", "Roman", "Castle", "Cultural", "Architecture"],
    availability: ["Daily except Friday", "Full day"],
    isWishlisted: false,
  },
];

const categories = [
  { id: "all", name: "All Categories", icon: GlobeAltIcon },
  {
    id: "Historical & Cultural",
    name: "Historical & Cultural",
    icon: BuildingOfficeIcon,
  },
  { id: "Adventure & Nature", name: "Adventure & Nature", icon: FireIcon },
  { id: "Wellness & Relaxation", name: "Wellness & Relaxation", icon: SunIcon },
  { id: "Food & Culture", name: "Food & Culture", icon: MusicalNoteIcon },
];

export default function TravelActivities() {
  const [activities, setActivities] = useState<Activity[]>(mockActivities);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(
    null
  );
  const [showFilters, setShowFilters] = useState(false);
  const [priceRange] = useState([0, 200]);
  const [sortBy, setSortBy] = useState("rating");

  const filteredActivities = activities
    .filter((activity) => {
      const matchesCategory =
        selectedCategory === "all" || activity.category === selectedCategory;
      const matchesSearch =
        activity.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        activity.location.toLowerCase().includes(searchQuery.toLowerCase()) ||
        activity.description.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesPrice =
        activity.price >= priceRange[0] && activity.price <= priceRange[1];

      return matchesCategory && matchesSearch && matchesPrice;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case "price-low":
          return a.price - b.price;
        case "price-high":
          return b.price - a.price;
        case "rating":
          return b.rating - a.rating;
        case "reviews":
          return b.reviews - a.reviews;
        default:
          return 0;
      }
    });

  const toggleWishlist = (activityId: string) => {
    setActivities((prev) =>
      prev.map((activity) =>
        activity.id === activityId
          ? { ...activity, isWishlisted: !activity.isWishlisted }
          : activity
      )
    );
  };

  const formatPrice = (price: number, currency: string) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency,
    }).format(price);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "Easy":
        return "text-green-700 bg-green-100";
      case "Moderate":
        return "text-yellow-700 bg-yellow-100";
      case "Challenging":
        return "text-red-700 bg-red-100";
      default:
        return "text-gray-700 bg-gray-100";
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Apple-style Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-light text-gray-900 tracking-tight">
          Travel Activities
        </h1>
        <p className="text-lg text-gray-500 mt-3 font-light">
          Discover and book exciting travel experiences around Jordan
        </p>
      </div>

      {/* Search and Filters */}
      <div className="mb-8 space-y-6">
        {/* Search Bar */}
        <div className="relative max-w-2xl">
          <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search activities, locations, or experiences..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-12 pr-4 py-4 bg-white border border-gray-200 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 placeholder-gray-500"
          />
        </div>

        {/* Category Filters */}
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => {
            const IconComponent = category.icon;
            return (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-2xl font-medium transition-all duration-200 ${
                  selectedCategory === category.id
                    ? "bg-blue-500 text-white shadow-lg"
                    : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"
                }`}
              >
                <IconComponent className="w-4 h-4" />
                {category.name}
              </button>
            );
          })}
        </div>

        {/* Sort and Filter Controls */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="rating">Highest Rated</option>
              <option value="reviews">Most Reviews</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
            </select>

            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors"
            >
              <FunnelIcon className="w-4 h-4" />
              Filters
            </button>
          </div>

          <div className="text-sm text-gray-500">
            {filteredActivities.length} activities found
          </div>
        </div>
      </div>

      {/* Activities Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
        {filteredActivities.map((activity) => (
          <div
            key={activity.id}
            className="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer group"
          >
            {/* Activity Image */}
            <div className="relative h-64">
              <div
                className="w-full h-full bg-gradient-to-br from-blue-400 to-purple-500"
                style={{
                  backgroundImage: `url(${activity.images[0]})`,
                  backgroundSize: "cover",
                  backgroundPosition: "center",
                }}
              >
                <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-all duration-300"></div>
              </div>

              {/* Wishlist Button */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  toggleWishlist(activity.id);
                }}
                className="absolute top-4 right-4 p-2 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-all duration-200"
              >
                {activity.isWishlisted ? (
                  <HeartIconSolid className="w-5 h-5 text-red-500" />
                ) : (
                  <HeartIcon className="w-5 h-5 text-gray-600" />
                )}
              </button>

              {/* Category Badge */}
              <div className="absolute top-4 left-4 px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full text-xs font-medium text-gray-800">
                {activity.category}
              </div>

              {/* Difficulty Badge */}
              <div
                className={`absolute bottom-4 left-4 px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(
                  activity.difficulty
                )}`}
              >
                {activity.difficulty}
              </div>
            </div>

            {/* Activity Content */}
            <div className="p-6">
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-xl font-medium text-gray-900 line-clamp-2 flex-1">
                  {activity.title}
                </h3>
              </div>

              {/* Rating and Reviews */}
              <div className="flex items-center gap-1 mb-3">
                <StarIcon className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                <span className="text-sm font-medium">{activity.rating}</span>
                <span className="text-sm text-gray-500">
                  ({activity.reviews} reviews)
                </span>
              </div>

              {/* Location and Duration */}
              <div className="space-y-2 mb-4">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <MapPinIcon className="w-4 h-4" />
                  <span>
                    {activity.location}, {activity.country}
                  </span>
                </div>

                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <ClockIcon className="w-4 h-4" />
                  <span>{activity.duration}</span>
                </div>

                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <UsersIcon className="w-4 h-4" />
                  <span>{activity.groupSize}</span>
                </div>
              </div>

              {/* Short Description */}
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                {activity.shortDescription}
              </p>

              {/* Tags */}
              <div className="flex flex-wrap gap-1 mb-4">
                {activity.tags.slice(0, 3).map((tag, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full"
                  >
                    {tag}
                  </span>
                ))}
                {activity.tags.length > 3 && (
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                    +{activity.tags.length - 3} more
                  </span>
                )}
              </div>

              {/* Price and Actions */}
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-2xl font-semibold text-gray-900">
                    {formatPrice(activity.price, activity.currency)}
                  </div>
                  <div className="text-xs text-gray-500">per person</div>
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedActivity(activity);
                    }}
                    className="p-2 bg-blue-100 text-blue-600 rounded-full hover:bg-blue-200 transition-colors"
                  >
                    <EyeIcon className="w-5 h-5" />
                  </button>

                  <button className="p-2 bg-green-100 text-green-600 rounded-full hover:bg-green-200 transition-colors">
                    <ShoppingCartIcon className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Detailed Activity Modal */}
      {selectedActivity && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="sticky top-0 bg-white rounded-t-3xl border-b border-gray-100 p-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-medium text-gray-900">
                  {selectedActivity.title}
                </h2>
                <button
                  onClick={() => setSelectedActivity(null)}
                  className="p-2 bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200 transition-colors"
                >
                  <XMarkIcon className="w-6 h-6" />
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6 space-y-8">
              {/* Activity Overview */}
              <div>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                  <div>
                    <h3 className="text-lg font-medium mb-2">Overview</h3>
                    <p className="text-gray-600 mb-4">
                      {selectedActivity.description}
                    </p>

                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <MapPinIcon className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">
                          {selectedActivity.location},{" "}
                          {selectedActivity.country}
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        <ClockIcon className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">
                          {selectedActivity.duration}
                        </span>
                      </div>

                      <div className="flex items-center gap-2">
                        <UsersIcon className="w-4 h-4 text-gray-400" />
                        <span className="text-sm">
                          {selectedActivity.groupSize}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="bg-gray-50 rounded-2xl p-4">
                      <div className="text-sm text-gray-600 mb-1">Price</div>
                      <div className="text-2xl font-semibold text-gray-900">
                        {formatPrice(
                          selectedActivity.price,
                          selectedActivity.currency
                        )}
                      </div>
                      <div className="text-sm text-gray-500">per person</div>
                    </div>

                    <div className="bg-gray-50 rounded-2xl p-4">
                      <div className="text-sm text-gray-600 mb-2">Rating</div>
                      <div className="flex items-center gap-2">
                        <div className="flex items-center gap-1">
                          <StarIcon className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                          <span className="font-medium">
                            {selectedActivity.rating}
                          </span>
                        </div>
                        <span className="text-sm text-gray-500">
                          ({selectedActivity.reviews} reviews)
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Highlights */}
              <div>
                <h4 className="text-lg font-medium mb-4">Highlights</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {selectedActivity.highlights.map((highlight, index) => (
                    <div key={index} className="flex items-start gap-2">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                      <span className="text-sm text-gray-700">{highlight}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* What's Included / Not Included */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-lg font-medium mb-4 text-green-700">
                    What&apos;s Included
                  </h4>
                  <div className="space-y-2">
                    {selectedActivity.included.map((item, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        </div>
                        <span className="text-sm">{item}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-lg font-medium mb-4 text-red-700">
                    Not Included
                  </h4>
                  <div className="space-y-2">
                    {selectedActivity.notIncluded.map((item, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <div className="w-5 h-5 bg-red-100 rounded-full flex items-center justify-center">
                          <XMarkIcon className="w-3 h-3 text-red-500" />
                        </div>
                        <span className="text-sm">{item}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Additional Information */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-lg font-medium mb-4">Details</h4>
                  <div className="space-y-3 text-sm">
                    <div>
                      <span className="font-medium">Languages:</span>
                      <span className="ml-2">
                        {selectedActivity.languages.join(", ")}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium">Meeting Point:</span>
                      <span className="ml-2">
                        {selectedActivity.meetingPoint}
                      </span>
                    </div>
                    <div>
                      <span className="font-medium">Availability:</span>
                      <span className="ml-2">
                        {selectedActivity.availability.join(", ")}
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-lg font-medium mb-4">Provider</h4>
                  <div className="bg-gray-50 rounded-2xl p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium">
                        {selectedActivity.provider.name}
                      </span>
                      {selectedActivity.provider.verified && (
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                          Verified
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-1">
                      <StarIcon className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      <span className="text-sm">
                        {selectedActivity.provider.rating} provider rating
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Cancellation Policy */}
              <div>
                <h4 className="text-lg font-medium mb-4">
                  Cancellation Policy
                </h4>
                <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-4">
                  <p className="text-sm text-yellow-800">
                    {selectedActivity.cancellationPolicy}
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4 pt-4">
                <button className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-4 rounded-2xl font-medium transition-colors flex items-center justify-center gap-2">
                  <ShoppingCartIcon className="w-5 h-5" />
                  Book Now -{" "}
                  {formatPrice(
                    selectedActivity.price,
                    selectedActivity.currency
                  )}
                </button>

                <button
                  onClick={() => toggleWishlist(selectedActivity.id)}
                  className={`px-6 py-4 rounded-2xl font-medium transition-colors flex items-center gap-2 ${
                    selectedActivity.isWishlisted
                      ? "bg-red-100 text-red-600 hover:bg-red-200"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                  }`}
                >
                  {selectedActivity.isWishlisted ? (
                    <HeartIconSolid className="w-5 h-5" />
                  ) : (
                    <HeartIcon className="w-5 h-5" />
                  )}
                  {selectedActivity.isWishlisted ? "Saved" : "Save"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {filteredActivities.length === 0 && (
        <div className="text-center py-16">
          <MagnifyingGlassIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-medium text-gray-900 mb-2">
            No activities found
          </h3>
          <p className="text-gray-500">
            Try adjusting your search criteria or browse all categories.
          </p>
        </div>
      )}
    </div>
  );
}
