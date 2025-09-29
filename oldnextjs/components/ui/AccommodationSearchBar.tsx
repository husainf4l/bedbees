"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  CalendarIcon,
  UserIcon,
  MapPinIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/24/outline";

interface SearchData {
  destination: string;
  checkIn: string;
  checkOut: string;
  guests: {
    adults: number;
    children: number;
    rooms: number;
  };
}

interface AccommodationSearchBarProps {
  onSearch?: (searchData: SearchData) => void;
  className?: string;
}

export default function AccommodationSearchBar({
  onSearch,
  className = "",
}: AccommodationSearchBarProps) {
  const [searchData, setSearchData] = useState<SearchData>({
    destination: "",
    checkIn: "",
    checkOut: "",
    guests: {
      adults: 2,
      children: 0,
      rooms: 1,
    },
  });

  const [showGuestDropdown, setShowGuestDropdown] = useState(false);
  const [showDestinationDropdown, setShowDestinationDropdown] = useState(false);
  const guestDropdownRef = useRef<HTMLDivElement>(null);
  const destinationRef = useRef<HTMLDivElement>(null);

  // Popular destinations for suggestions
  const popularDestinations = [
    "Amman, Jordan",
    "Petra, Jordan",
    "Aqaba, Jordan",
    "Dead Sea, Jordan",
    "Jerash, Jordan",
    "Wadi Rum, Jordan",
    "Cairo, Egypt",
    "Beirut, Lebanon",
    "Damascus, Syria",
    "Dubai, UAE",
  ];

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        guestDropdownRef.current &&
        !guestDropdownRef.current.contains(event.target as Node)
      ) {
        setShowGuestDropdown(false);
      }
      if (
        destinationRef.current &&
        !destinationRef.current.contains(event.target as Node)
      ) {
        setShowDestinationDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Set default dates (today and tomorrow)
  useEffect(() => {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);

    setSearchData((prev) => ({
      ...prev,
      checkIn: today.toISOString().split("T")[0],
      checkOut: tomorrow.toISOString().split("T")[0],
    }));
  }, []);

  const handleDestinationSelect = (destination: string) => {
    setSearchData((prev) => ({ ...prev, destination }));
    setShowDestinationDropdown(false);
  };

  const handleGuestChange = (
    type: "adults" | "children" | "rooms",
    increment: boolean
  ) => {
    setSearchData((prev) => ({
      ...prev,
      guests: {
        ...prev.guests,
        [type]: Math.max(
          type === "rooms" ? 1 : 0,
          prev.guests[type] + (increment ? 1 : -1)
        ),
      },
    }));
  };

  const handleSearch = () => {
    onSearch?.(searchData);
  };

  const formatGuestText = () => {
    const { adults, children, rooms } = searchData.guests;
    const guestText = `${adults + children} guest${
      adults + children !== 1 ? "s" : ""
    }`;
    const roomText = `${rooms} room${rooms !== 1 ? "s" : ""}`;
    return `${guestText}, ${roomText}`;
  };

  return (
    <div
      className={`bg-white rounded-2xl shadow-xl border border-gray-200 p-2 ${className}`}
    >
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-2">
        {/* Destination Input */}
        <div className="lg:col-span-4 relative" ref={destinationRef}>
          <div className="relative">
            <input
              type="text"
              placeholder="Where are you going?"
              value={searchData.destination}
              onChange={(e) => {
                setSearchData((prev) => ({
                  ...prev,
                  destination: e.target.value,
                }));
                setShowDestinationDropdown(true);
              }}
              onFocus={() => setShowDestinationDropdown(true)}
              className="w-full px-4 py-4 pl-12 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            />
            <MapPinIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          </div>

          {/* Destination Dropdown */}
          {showDestinationDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-lg z-50 max-h-60 overflow-y-auto">
              {popularDestinations
                .filter(
                  (dest) =>
                    searchData.destination === "" ||
                    dest
                      .toLowerCase()
                      .includes(searchData.destination.toLowerCase())
                )
                .map((destination, index) => (
                  <button
                    key={index}
                    onClick={() => handleDestinationSelect(destination)}
                    className="w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors duration-150 border-b border-gray-100 last:border-b-0"
                  >
                    <div className="flex items-center">
                      <MapPinIcon className="h-4 w-4 text-gray-400 mr-3" />
                      <span className="text-gray-700">{destination}</span>
                    </div>
                  </button>
                ))}
            </div>
          )}
        </div>

        {/* Check-in Date */}
        <div className="lg:col-span-2">
          <div className="relative">
            <input
              type="date"
              value={searchData.checkIn}
              onChange={(e) =>
                setSearchData((prev) => ({ ...prev, checkIn: e.target.value }))
              }
              className="w-full px-4 py-4 pl-12 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            />
            <CalendarIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <label className="absolute -top-2 left-3 px-1 bg-white text-xs font-medium text-gray-500">
              Check-in
            </label>
          </div>
        </div>

        {/* Check-out Date */}
        <div className="lg:col-span-2">
          <div className="relative">
            <input
              type="date"
              value={searchData.checkOut}
              onChange={(e) =>
                setSearchData((prev) => ({ ...prev, checkOut: e.target.value }))
              }
              className="w-full px-4 py-4 pl-12 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
            />
            <CalendarIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <label className="absolute -top-2 left-3 px-1 bg-white text-xs font-medium text-gray-500">
              Check-out
            </label>
          </div>
        </div>

        {/* Guests & Rooms */}
        <div className="lg:col-span-3 relative" ref={guestDropdownRef}>
          <div className="relative">
            <button
              onClick={() => setShowGuestDropdown(!showGuestDropdown)}
              className="w-full px-4 py-4 pl-12 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-left"
            >
              {formatGuestText()}
            </button>
            <UserIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <label className="absolute -top-2 left-3 px-1 bg-white text-xs font-medium text-gray-500">
              Guests & Rooms
            </label>
          </div>

          {/* Guest Dropdown */}
          {showGuestDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-lg z-50 p-4">
              <div className="space-y-4">
                {/* Adults */}
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">Adults</div>
                    <div className="text-sm text-gray-500">
                      Ages 13 or above
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => handleGuestChange("adults", false)}
                      disabled={searchData.guests.adults <= 1}
                      className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      -
                    </button>
                    <span className="w-8 text-center font-medium">
                      {searchData.guests.adults}
                    </span>
                    <button
                      onClick={() => handleGuestChange("adults", true)}
                      className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                    >
                      +
                    </button>
                  </div>
                </div>

                {/* Children */}
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">Children</div>
                    <div className="text-sm text-gray-500">Ages 0-12</div>
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => handleGuestChange("children", false)}
                      disabled={searchData.guests.children <= 0}
                      className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      -
                    </button>
                    <span className="w-8 text-center font-medium">
                      {searchData.guests.children}
                    </span>
                    <button
                      onClick={() => handleGuestChange("children", true)}
                      className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                    >
                      +
                    </button>
                  </div>
                </div>

                {/* Rooms */}
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium text-gray-900">Rooms</div>
                    <div className="text-sm text-gray-500">Number of rooms</div>
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => handleGuestChange("rooms", false)}
                      disabled={searchData.guests.rooms <= 1}
                      className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      -
                    </button>
                    <span className="w-8 text-center font-medium">
                      {searchData.guests.rooms}
                    </span>
                    <button
                      onClick={() => handleGuestChange("rooms", true)}
                      className="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center hover:bg-gray-50"
                    >
                      +
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Search Button */}
        <div className="lg:col-span-1">
          <button
            onClick={handleSearch}
            className="w-full h-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-xl font-medium transition-all duration-200 hover:shadow-lg hover:scale-105 flex items-center justify-center px-4 py-4"
          >
            <MagnifyingGlassIcon className="h-6 w-6 lg:h-5 lg:w-5" />
            <span className="ml-2 lg:hidden">Search</span>
          </button>
        </div>
      </div>
    </div>
  );
}
