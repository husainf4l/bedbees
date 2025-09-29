"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  MagnifyingGlassIcon,
  MapPinIcon,
  CalendarDaysIcon,
  AdjustmentsHorizontalIcon,
  UsersIcon,
  TagIcon,
  GlobeAltIcon,
} from "@heroicons/react/24/outline";

interface ExperienceSearchData {
  destination: string;
  date: string;
  category: string;
  duration: string;
  priceRange: string;
  groupSize: number;
}

interface ExperienceSearchBarProps {
  onSearch?: (searchData: ExperienceSearchData) => void;
  className?: string;
}

export default function ExperienceSearchBar({
  onSearch,
  className = "",
}: ExperienceSearchBarProps) {
  const [searchData, setSearchData] = useState<ExperienceSearchData>({
    destination: "",
    date: "",
    category: "all",
    duration: "any",
    priceRange: "any",
    groupSize: 1,
  });

  const [showFilters, setShowFilters] = useState(false);
  const [showDestinationDropdown, setShowDestinationDropdown] = useState(false);
  const [showCategoryDropdown, setShowCategoryDropdown] = useState(false);

  const filtersRef = useRef<HTMLDivElement>(null);
  const destinationRef = useRef<HTMLDivElement>(null);
  const categoryRef = useRef<HTMLDivElement>(null);

  // Popular destinations for experiences
  const popularDestinations = [
    { name: "Petra, Jordan", type: "Historical" },
    { name: "Wadi Rum, Jordan", type: "Adventure" },
    { name: "Amman, Jordan", type: "City Tours" },
    { name: "Dead Sea, Jordan", type: "Wellness" },
    { name: "Jerash, Jordan", type: "Cultural" },
    { name: "Aqaba, Jordan", type: "Water Sports" },
    { name: "Cairo, Egypt", type: "Historical" },
    { name: "Pyramids of Giza", type: "Historical" },
    { name: "Beirut, Lebanon", type: "City Tours" },
    { name: "Dubai, UAE", type: "Luxury" },
  ];

  // Experience categories
  const experienceCategories = [
    { id: "all", name: "All Experiences" },
    { id: "cultural", name: "Cultural Tours" },
    { id: "adventure", name: "Adventure" },
    { id: "food", name: "Food & Drink" },
    { id: "nature", name: "Nature & Wildlife" },
    { id: "water", name: "Water Activities" },
    { id: "historical", name: "Historical Sites" },
    { id: "wellness", name: "Wellness & Spa" },
    { id: "art", name: "Art & Museums" },
    { id: "nightlife", name: "Nightlife" },
  ];

  // Duration options
  const durationOptions = [
    { id: "any", name: "Any duration" },
    { id: "1-3", name: "1-3 hours" },
    { id: "4-6", name: "4-6 hours" },
    { id: "full-day", name: "Full day (7+ hours)" },
    { id: "multi-day", name: "Multi-day" },
  ];

  // Price ranges
  const priceRanges = [
    { id: "any", name: "Any price" },
    { id: "0-25", name: "Under $25" },
    { id: "25-50", name: "$25 - $50" },
    { id: "50-100", name: "$50 - $100" },
    { id: "100+", name: "$100+" },
  ];

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        filtersRef.current &&
        !filtersRef.current.contains(event.target as Node)
      ) {
        setShowFilters(false);
      }
      if (
        destinationRef.current &&
        !destinationRef.current.contains(event.target as Node)
      ) {
        setShowDestinationDropdown(false);
      }
      if (
        categoryRef.current &&
        !categoryRef.current.contains(event.target as Node)
      ) {
        setShowCategoryDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleDestinationSelect = (destination: string) => {
    setSearchData((prev) => ({ ...prev, destination }));
    setShowDestinationDropdown(false);
  };

  const handleCategorySelect = (category: string) => {
    setSearchData((prev) => ({ ...prev, category }));
    setShowCategoryDropdown(false);
  };

  const handleSearch = () => {
    onSearch?.(searchData);
  };

  const resetFilters = () => {
    setSearchData({
      destination: "",
      date: "",
      category: "all",
      duration: "any",
      priceRange: "any",
      groupSize: 1,
    });
  };

  const getSelectedCategoryName = () => {
    const category = experienceCategories.find(
      (cat) => cat.id === searchData.category
    );
    return category?.name || "All Experiences";
  };

  const hasActiveFilters = () => {
    return (
      searchData.category !== "all" ||
      searchData.duration !== "any" ||
      searchData.priceRange !== "any" ||
      searchData.groupSize > 1
    );
  };

  return (
    <div
      className={`bg-white rounded-2xl shadow-xl border border-gray-100 p-4 ${className}`}
    >
      {/* Main Search Row */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-3 mb-4">
        {/* Destination Search */}
        <div className="lg:col-span-4 relative" ref={destinationRef}>
          <div className="relative">
            <input
              type="text"
              placeholder="Where do you want to explore?"
              value={searchData.destination}
              onChange={(e) => {
                setSearchData((prev) => ({
                  ...prev,
                  destination: e.target.value,
                }));
                setShowDestinationDropdown(true);
              }}
              onFocus={() => setShowDestinationDropdown(true)}
              className="w-full px-4 py-4 pl-12 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 placeholder-gray-500"
            />
            <MapPinIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          </div>

          {/* Destination Dropdown */}
          {showDestinationDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-lg z-50 max-h-80 overflow-y-auto">
              <div className="p-2">
                <div className="text-xs font-semibold text-gray-500 px-3 py-2 border-b border-gray-100">
                  Popular Destinations
                </div>
                {popularDestinations
                  .filter(
                    (dest) =>
                      searchData.destination === "" ||
                      dest.name
                        .toLowerCase()
                        .includes(searchData.destination.toLowerCase())
                  )
                  .map((destination, index) => (
                    <button
                      key={index}
                      onClick={() => handleDestinationSelect(destination.name)}
                      className="w-full text-left px-3 py-3 hover:bg-gray-50 transition-colors duration-150 rounded-lg"
                    >
                      <div className="flex items-center">
                        <div>
                          <div className="font-medium text-gray-900">
                            {destination.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {destination.type}
                          </div>
                        </div>
                      </div>
                    </button>
                  ))}
              </div>
            </div>
          )}
        </div>

        {/* Date Picker */}
        <div className="lg:col-span-3">
          <div className="relative">
            <input
              type="date"
              value={searchData.date}
              onChange={(e) =>
                setSearchData((prev) => ({ ...prev, date: e.target.value }))
              }
              className="w-full px-4 py-4 pl-12 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200"
            />
            <CalendarDaysIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <label className="absolute -top-2 left-3 px-1 bg-white text-xs font-medium text-gray-500">
              When?
            </label>
          </div>
        </div>

        {/* Category Quick Select */}
        <div className="lg:col-span-3 relative" ref={categoryRef}>
          <button
            onClick={() => setShowCategoryDropdown(!showCategoryDropdown)}
            className="w-full px-4 py-4 pl-12 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 text-left"
          >
            {getSelectedCategoryName()}
          </button>
          <TagIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />

          {/* Category Dropdown */}
          {showCategoryDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-lg z-50 max-h-60 overflow-y-auto">
              <div className="p-2">
                {experienceCategories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => handleCategorySelect(category.id)}
                    className={`w-full text-left px-3 py-2 hover:bg-gray-50 transition-colors duration-150 rounded-lg ${
                      searchData.category === category.id
                        ? "bg-orange-50 text-orange-700"
                        : ""
                    }`}
                  >
                    {category.name}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Search Button */}
        <div className="lg:col-span-2">
          <button
            onClick={handleSearch}
            className="w-full h-full bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white rounded-xl font-medium transition-all duration-200 hover:shadow-lg hover:scale-105 flex items-center justify-center px-4 py-4"
          >
            <MagnifyingGlassIcon className="h-5 w-5 lg:mr-2" />
            <span className="hidden lg:block">Search</span>
            <span className="lg:hidden">Search Experiences</span>
          </button>
        </div>
      </div>

      {/* Advanced Filters Toggle */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center text-sm text-gray-600 hover:text-orange-600 transition-colors duration-200"
        >
          <AdjustmentsHorizontalIcon className="h-4 w-4 mr-1" />
          Advanced Filters
          {hasActiveFilters() && (
            <span className="ml-2 bg-orange-100 text-orange-700 px-2 py-1 rounded-full text-xs font-medium">
              Active
            </span>
          )}
        </button>

        {hasActiveFilters() && (
          <button
            onClick={resetFilters}
            className="text-sm text-gray-500 hover:text-gray-700 underline"
          >
            Reset all
          </button>
        )}
      </div>

      {/* Advanced Filters Panel */}
      {showFilters && (
        <div
          className="mt-4 p-4 bg-gray-50 rounded-xl border border-gray-200"
          ref={filtersRef}
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Duration Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Duration
              </label>
              <select
                value={searchData.duration}
                onChange={(e) =>
                  setSearchData((prev) => ({
                    ...prev,
                    duration: e.target.value,
                  }))
                }
                className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                {durationOptions.map((option) => (
                  <option key={option.id} value={option.id}>
                    {option.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Price Range Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Price Range
              </label>
              <select
                value={searchData.priceRange}
                onChange={(e) =>
                  setSearchData((prev) => ({
                    ...prev,
                    priceRange: e.target.value,
                  }))
                }
                className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                {priceRanges.map((range) => (
                  <option key={range.id} value={range.id}>
                    {range.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Group Size Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Group Size
              </label>
              <div className="flex items-center">
                <UsersIcon className="h-5 w-5 text-gray-400 mr-2" />
                <input
                  type="number"
                  min="1"
                  max="20"
                  value={searchData.groupSize}
                  onChange={(e) =>
                    setSearchData((prev) => ({
                      ...prev,
                      groupSize: Math.max(1, parseInt(e.target.value) || 1),
                    }))
                  }
                  className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
