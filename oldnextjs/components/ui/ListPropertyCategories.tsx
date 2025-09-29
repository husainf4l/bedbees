"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import { accommodationService } from "@/services/accommodation.service";

// Types from the header component
type AccommodationType = {
  id: string;
  name: string;
  type: string;
  title: string;
  subtitle: string;
  image: string;
  sectionTitle: string;
  message: string;
};

type TourCategory = {
  name: string;
  href: string;
  description: string;
  category: string;
};

interface ListPropertyCategoriesProps {
  onCategorySelect?: (category: string, subcategory?: string) => void;
}

export default function ListPropertyCategories({
  onCategorySelect,
}: ListPropertyCategoriesProps) {
  const [selectedMainCategory, setSelectedMainCategory] = useState<
    string | null
  >(null);
  const [accommodationTypes, setAccommodationTypes] = useState<
    AccommodationType[]
  >([]);
  const [loading, setLoading] = useState(false);

  // Tour categories from the header
  const tourCategories: TourCategory[] = [
    {
      name: "Tours & Sightseeing",
      href: "/tours?category=sightseeing",
      description: "Discover iconic landmarks",
      category: "sightseeing",
    },
    {
      name: "Cultural Experiences",
      href: "/tours?category=culture",
      description: "Immerse in local culture",
      category: "culture",
    },
    {
      name: "Adventure & Outdoor",
      href: "/tours?category=adventure",
      description: "Thrilling outdoor activities",
      category: "adventure",
    },
    {
      name: "Food Tours",
      href: "/tours?category=food",
      description: "Culinary adventures",
      category: "food",
    },
    {
      name: "Walking Tours",
      href: "/tours?category=walking",
      description: "Explore on foot",
      category: "walking",
    },
    {
      name: "Share Tours",
      href: "/share-tours",
      description: "Join group experiences",
      category: "share",
    },
    {
      name: "Private Tours",
      href: "/tours?type=private",
      description: "Exclusive experiences",
      category: "private",
    },
  ];

  // Default accommodation types (fallback)
  const defaultAccommodationTypes = useMemo<AccommodationType[]>(
    () => [
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
        image: "",
        sectionTitle: "Guest Houses",
        message: "Showing guest houses...",
      },
      {
        id: "vacation-homes",
        name: "Vacation Homes",
        type: "vacation-homes",
        title: "Entire Vacation Homes",
        subtitle: "Entire homes for your vacation",
        image: "",
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
    ],
    []
  );

  const fetchAccommodationTypes = useCallback(async () => {
    setLoading(true);
    try {
      const categories = await accommodationService.getCategories();
      if (categories.length > 0) {
        setAccommodationTypes(categories);
      } else {
        setAccommodationTypes(defaultAccommodationTypes);
      }
    } catch (error) {
      console.error("Failed to fetch accommodation types:", error);
      setAccommodationTypes(defaultAccommodationTypes);
    } finally {
      setLoading(false);
    }
  }, [defaultAccommodationTypes]);

  // Load accommodation types when accommodations is selected
  useEffect(() => {
    if (selectedMainCategory === "accommodations") {
      fetchAccommodationTypes();
    }
  }, [selectedMainCategory, fetchAccommodationTypes]);

  const handleMainCategorySelect = (category: string) => {
    setSelectedMainCategory(category);
    if (category === "tours") {
      onCategorySelect?.(category);
    } else if (category === "accommodations") {
      onCategorySelect?.(category, "default");
    }
  };

  const handleSubcategorySelect = (subcategory: string) => {
    onCategorySelect?.(selectedMainCategory!, subcategory);
  };

  const handleBackToMain = () => {
    setSelectedMainCategory(null);
  };

  // Main category selection
  if (!selectedMainCategory) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          What would you like to list?
        </h2>
        <p className="text-gray-600 mb-8">
          Choose the type of property or experience you want to offer
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Tours Card */}
          <div
            onClick={() => handleMainCategorySelect("tours")}
            className="p-8 border-2 border-gray-200 rounded-xl hover:border-green-500 hover:bg-green-50 transition-all duration-200 cursor-pointer group"
          >
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-green-100 transition-colors">
                <svg
                  className="w-8 h-8 text-blue-600 group-hover:text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Tours & Experiences
              </h3>
              <p className="text-gray-600">
                Share your knowledge and create memorable experiences for
                travelers
              </p>
            </div>
          </div>

          {/* Accommodations Card */}
          <div
            onClick={() => handleMainCategorySelect("accommodations")}
            className="p-8 border-2 border-gray-200 rounded-xl hover:border-green-500 hover:bg-green-50 transition-all duration-200 cursor-pointer group"
          >
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-green-100 transition-colors">
                <svg
                  className="w-8 h-8 text-purple-600 group-hover:text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h4a1 1 0 011 1v5m-6 0h6"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Accommodations
              </h3>
              <p className="text-gray-600">
                List your property and provide comfortable stays for guests
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Tours subcategories
  if (selectedMainCategory === "tours") {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={handleBackToMain}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg
              className="w-5 h-5 text-gray-600"
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
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Tour Categories
            </h2>
            <p className="text-gray-600">
              Select the type of tour or experience you want to offer
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tourCategories.map((tour) => (
            <div
              key={tour.category}
              onClick={() => handleSubcategorySelect(tour.category)}
              className="p-6 border border-gray-200 rounded-lg hover:border-green-500 hover:bg-green-50 transition-all duration-200 cursor-pointer group"
            >
              <div className="flex items-start gap-3">
                <div className="w-3 h-3 bg-blue-500 rounded-full mt-2 group-hover:bg-green-500 transition-colors"></div>
                <div>
                  <h3 className="font-medium text-gray-900 group-hover:text-green-700 transition-colors">
                    {tour.name}
                  </h3>
                  <p className="text-sm text-gray-500 mt-1 group-hover:text-green-600 transition-colors">
                    {tour.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Accommodations subcategories
  if (selectedMainCategory === "accommodations") {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={handleBackToMain}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg
              className="w-5 h-5 text-gray-600"
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
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Accommodation Types
            </h2>
            <p className="text-gray-600">
              Choose the type of accommodation you want to list
            </p>
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[...Array(6)].map((_, index) => (
              <div
                key={index}
                className="p-6 border border-gray-200 rounded-lg animate-pulse"
              >
                <div className="flex items-start gap-3">
                  <div className="w-3 h-3 bg-gray-300 rounded-full mt-2"></div>
                  <div className="flex-1">
                    <div className="h-4 bg-gray-300 rounded mb-2"></div>
                    <div className="h-3 bg-gray-300 rounded w-3/4"></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {accommodationTypes.map((accommodation) => (
              <div
                key={accommodation.id}
                onClick={() => handleSubcategorySelect(accommodation.type)}
                className="p-6 border border-gray-200 rounded-lg hover:border-green-500 hover:bg-green-50 transition-all duration-200 cursor-pointer group"
              >
                <div className="flex items-start gap-3">
                  <div className="w-3 h-3 bg-purple-500 rounded-full mt-2 group-hover:bg-green-500 transition-colors"></div>
                  <div>
                    <h3 className="font-medium text-gray-900 group-hover:text-green-700 transition-colors">
                      {accommodation.sectionTitle}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1 group-hover:text-green-600 transition-colors">
                      {accommodation.subtitle}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  return null;
}
