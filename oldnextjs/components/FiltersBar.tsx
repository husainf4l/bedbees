"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import {
  MapPinIcon,
  UsersIcon,
  StarIcon,
  ChevronDownIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/24/outline";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Slider } from "@/components/ui/slider";

export type FilterMode = "hotels" | "tours";

export interface HotelFilters {
  destination: string;
  checkIn: string;
  checkOut: string;
  adults: number;
  children: number;
  childrenAges: number[];
  rooms: number;
  propertyType: string[];
  priceMin: number;
  priceMax: number;
  rating: number;
  amenities: string[];
  freeCancellation: boolean;
  payAtProperty: boolean;
  sort: string;
}

export interface TourFilters {
  destination: string;
  startDate: string;
  endDate: string;
  adults: number;
  children: number;
  category: string[];
  duration: string[];
  language: string[];
  priceMin: number;
  priceMax: number;
  features: string[];
  sort: string;
}

export interface Filters {
  mode: FilterMode;
  hotels: HotelFilters;
  tours: TourFilters;
}

const defaultHotelFilters: HotelFilters = {
  destination: "",
  checkIn: "",
  checkOut: "",
  adults: 2,
  children: 0,
  childrenAges: [],
  rooms: 1,
  propertyType: [],
  priceMin: 0,
  priceMax: 1000,
  rating: 0,
  amenities: [],
  freeCancellation: false,
  payAtProperty: false,
  sort: "recommended",
};

const defaultTourFilters: TourFilters = {
  destination: "",
  startDate: "",
  endDate: "",
  adults: 2,
  children: 0,
  category: [],
  duration: [],
  language: [],
  priceMin: 0,
  priceMax: 500,
  features: [],
  sort: "recommended",
};

const propertyTypes = [
  { id: "hotel", label: "Hotels" },
  { id: "apartment", label: "Apartments" },
  { id: "villa", label: "Villas" },
  { id: "hostel", label: "Hostels" },
  { id: "resort", label: "Resorts" },
  { id: "motel", label: "Motels" },
  { id: "guesthouse", label: "Guesthouses" },
  { id: "boutique", label: "Boutique Hotels" },
  { id: "luxury", label: "Luxury Hotels" },
  { id: "budget", label: "Budget Hotels" },
  { id: "cabin", label: "Cabins" },
  { id: "cottage", label: "Cottages" },
  { id: "bungalow", label: "Bungalows" },
  { id: "chalet", label: "Chalets" },
  { id: "farm", label: "Farm Stays" },
  { id: "houseboat", label: "Houseboats" },
];

const amenities = [
  // Internet & Technology
  { id: "wifi", label: "Free WiFi", category: "internet" },

  // Parking
  { id: "parking", label: "Free Parking", category: "parking" },
  {
    id: "paid-parking",
    label: "Paid parking on premises",
    category: "parking",
  },

  // Pool & Spa
  { id: "pool", label: "Swimming Pool", category: "pool" },
  { id: "spa", label: "Spa", category: "pool" },

  // Fitness & Wellness
  { id: "gym", label: "Fitness Center", category: "fitness" },

  // Food & Drink
  { id: "breakfast", label: "Free Breakfast", category: "food" },
  { id: "restaurant", label: "Restaurant", category: "food" },
  { id: "bar", label: "Bar", category: "food" },
  { id: "room-service", label: "Room service", category: "food" },

  // Climate Control
  { id: "ac", label: "Air Conditioning", category: "climate" },

  // Building Features
  { id: "elevator", label: "Elevator", category: "building" },
  {
    id: "wheelchair-accessible",
    label: "Wheelchair accessible",
    category: "building",
  },
  { id: "pet-friendly", label: "Pet friendly", category: "building" },
  { id: "family-rooms", label: "Family rooms", category: "building" },
  { id: "non-smoking-rooms", label: "Non-smoking rooms", category: "building" },

  // Room Facilities
  { id: "private-bathroom", label: "Private bathroom", category: "bathroom" },
  { id: "tv", label: "TV", category: "room" },
  { id: "safe", label: "Safe", category: "room" },
  { id: "desk", label: "Desk", category: "room" },
  { id: "balcony", label: "Balcony", category: "view" },

  // Views & Location
  { id: "sea-view", label: "Sea view", category: "view" },
  { id: "city-view", label: "City view", category: "view" },

  // Services
  { id: "24hr-front-desk", label: "24-hour front desk", category: "services" },
  { id: "concierge", label: "Concierge service", category: "services" },
];

const tourCategories = [
  { id: "walking", label: "Walking Tours" },
  { id: "museum", label: "Museum Tours" },
  { id: "day-trip", label: "Day Trips" },
  { id: "adventure", label: "Adventure" },
  { id: "food", label: "Food Tours" },
  { id: "water", label: "Water Activities" },
  { id: "desert", label: "Desert Tours" },
  { id: "cultural", label: "Cultural Experiences" },
];

const tourDurations = [
  { id: "0-2h", label: "0-2 hours" },
  { id: "2-4h", label: "2-4 hours" },
  { id: "4-8h", label: "4-8 hours" },
  { id: "full-day", label: "Full Day" },
  { id: "multi-day", label: "Multi-day" },
];

const tourFeatures = [
  { id: "instant-confirmation", label: "Instant Confirmation" },
  { id: "skip-the-line", label: "Skip the Line" },
  { id: "private", label: "Private Tour" },
  { id: "hotel-pickup", label: "Hotel Pickup" },
  { id: "free-cancel", label: "Free Cancellation" },
];

const sortOptions = [
  { id: "recommended", label: "Recommended" },
  { id: "price-asc", label: "Price: Low to High" },
  { id: "price-desc", label: "Price: High to Low" },
  { id: "rating", label: "Highest Rated" },
  { id: "distance", label: "Distance" },
];

interface FiltersBarProps {
  mode?: FilterMode;
  onModeChange?: (mode: FilterMode) => void;
}

export default function FiltersBar({
  mode = "hotels",
  onModeChange,
}: FiltersBarProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [filters, setFilters] = useState<Filters>({
    mode,
    hotels: defaultHotelFilters,
    tours: defaultTourFilters,
  });

  // State for managing expanded sections
  const [expandedSections, setExpandedSections] = useState<
    Record<string, boolean>
  >({
    propertyType: false,
    amenities: false,
    facilities: false,
    roomFacilities: false,
    accessibility: false,
  });

  // Load filters from URL on mount
  useEffect(() => {
    const urlMode = (searchParams.get("mode") as FilterMode) || "hotels";
    const newFilters: Filters = {
      mode: urlMode,
      hotels: { ...defaultHotelFilters },
      tours: { ...defaultTourFilters },
    };

    // Parse hotel filters
    if (urlMode === "hotels") {
      newFilters.hotels = {
        destination: searchParams.get("destination") || "",
        checkIn: searchParams.get("checkIn") || "",
        checkOut: searchParams.get("checkOut") || "",
        adults: parseInt(searchParams.get("adults") || "2"),
        children: parseInt(searchParams.get("children") || "0"),
        childrenAges:
          searchParams
            .get("childrenAges")
            ?.split(",")
            .map(Number)
            .filter(Boolean) || [],
        rooms: parseInt(searchParams.get("rooms") || "1"),
        propertyType: searchParams.get("propertyType")?.split(",") || [],
        priceMin: parseInt(searchParams.get("priceMin") || "0"),
        priceMax: parseInt(searchParams.get("priceMax") || "1000"),
        rating: parseInt(searchParams.get("rating") || "0"),
        amenities: searchParams.get("amenities")?.split(",") || [],
        freeCancellation: searchParams.get("freeCancellation") === "true",
        payAtProperty: searchParams.get("payAtProperty") === "true",
        sort: searchParams.get("sort") || "recommended",
      };
    }

    // Parse tour filters
    if (urlMode === "tours") {
      newFilters.tours = {
        destination: searchParams.get("destination") || "",
        startDate: searchParams.get("startDate") || "",
        endDate: searchParams.get("endDate") || "",
        adults: parseInt(searchParams.get("adults") || "2"),
        children: parseInt(searchParams.get("children") || "0"),
        category: searchParams.get("category")?.split(",") || [],
        duration: searchParams.get("duration")?.split(",") || [],
        language: searchParams.get("language")?.split(",") || [],
        priceMin: parseInt(searchParams.get("priceMin") || "0"),
        priceMax: parseInt(searchParams.get("priceMax") || "500"),
        features: searchParams.get("features")?.split(",") || [],
        sort: searchParams.get("sort") || "recommended",
      };
    }

    setFilters(newFilters);
    if (onModeChange && urlMode !== mode) {
      onModeChange(urlMode);
    }
  }, [searchParams, mode, onModeChange]);

  const updateFilters = useCallback((newFilters: Partial<Filters>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  }, []);

  const updateHotelFilters = useCallback(
    (hotelFilters: Partial<HotelFilters>) => {
      setFilters((prev) => ({
        ...prev,
        hotels: { ...prev.hotels, ...hotelFilters },
      }));
    },
    []
  );

  const updateTourFilters = useCallback((tourFilters: Partial<TourFilters>) => {
    setFilters((prev) => ({
      ...prev,
      tours: { ...prev.tours, ...tourFilters },
    }));
  }, []);

  const applyFilters = useCallback(() => {
    const params = new URLSearchParams();
    params.set("mode", filters.mode);

    if (filters.mode === "hotels") {
      const h = filters.hotels;
      if (h.destination) params.set("destination", h.destination);
      if (h.checkIn) params.set("checkIn", h.checkIn);
      if (h.checkOut) params.set("checkOut", h.checkOut);
      if (h.adults !== 2) params.set("adults", h.adults.toString());
      if (h.children > 0) params.set("children", h.children.toString());
      if (h.childrenAges.length > 0)
        params.set("childrenAges", h.childrenAges.join(","));
      if (h.rooms !== 1) params.set("rooms", h.rooms.toString());
      if (h.propertyType.length > 0)
        params.set("propertyType", h.propertyType.join(","));
      if (h.priceMin > 0) params.set("priceMin", h.priceMin.toString());
      if (h.priceMax < 1000) params.set("priceMax", h.priceMax.toString());
      if (h.rating > 0) params.set("rating", h.rating.toString());
      if (h.amenities.length > 0)
        params.set("amenities", h.amenities.join(","));
      if (h.freeCancellation) params.set("freeCancellation", "true");
      if (h.payAtProperty) params.set("payAtProperty", "true");
      if (h.sort !== "recommended") params.set("sort", h.sort);
    } else {
      const t = filters.tours;
      if (t.destination) params.set("destination", t.destination);
      if (t.startDate) params.set("startDate", t.startDate);
      if (t.endDate) params.set("endDate", t.endDate);
      if (t.adults !== 2) params.set("adults", t.adults.toString());
      if (t.children > 0) params.set("children", t.children.toString());
      if (t.category.length > 0) params.set("category", t.category.join(","));
      if (t.duration.length > 0) params.set("duration", t.duration.join(","));
      if (t.language.length > 0) params.set("language", t.language.join(","));
      if (t.priceMin > 0) params.set("priceMin", t.priceMin.toString());
      if (t.priceMax < 500) params.set("priceMax", t.priceMax.toString());
      if (t.features.length > 0) params.set("features", t.features.join(","));
      if (t.sort !== "recommended") params.set("sort", t.sort);
    }

    const newUrl = `?${params.toString()}`;
    router.push(newUrl, { scroll: false });
  }, [filters, router]);

  const clearFilters = useCallback(() => {
    setFilters({
      mode: filters.mode,
      hotels: { ...defaultHotelFilters },
      tours: { ...defaultTourFilters },
    });
    router.push(`?mode=${filters.mode}`, { scroll: false });
  }, [filters.mode, router]);

  const handleModeChange = (newMode: FilterMode) => {
    updateFilters({ mode: newMode });
    if (onModeChange) {
      onModeChange(newMode);
    }
  };

  const currentFilters =
    filters.mode === "hotels" ? filters.hotels : filters.tours;
  const hasActiveFilters =
    filters.mode === "hotels"
      ? Object.entries(filters.hotels).some(([key, value]) => {
          if (key === "sort") return value !== "recommended";
          if (key === "adults") return value !== 2;
          if (key === "rooms") return value !== 1;
          if (key === "priceMin") return value > 0;
          if (key === "priceMax") return value < 1000;
          if (Array.isArray(value)) return value.length > 0;
          if (typeof value === "boolean") return value;
          if (typeof value === "number") return value > 0;
          return Boolean(value);
        })
      : Object.entries(filters.tours).some(([key, value]) => {
          if (key === "sort") return value !== "recommended";
          if (key === "adults") return value !== 2;
          if (key === "priceMin") return value > 0;
          if (key === "priceMax") return value < 500;
          if (Array.isArray(value)) return value.length > 0;
          if (typeof value === "number") return value > 0;
          return Boolean(value);
        });

  return (
    <div className="w-72 bg-white/95 backdrop-blur-xl border-r border-gray-200/50 shadow-xl h-full overflow-y-auto mt-16">
      {/* Mode Tabs */}
      <div className="p-6 border-b border-gray-100/50">
        <div className="flex flex-col space-y-3">
          <button
            onClick={() => handleModeChange("hotels")}
            className={`px-5 py-4 rounded-2xl font-semibold text-sm transition-all duration-300 text-left ${
              filters.mode === "hotels"
                ? "bg-blue-600 text-white shadow-lg shadow-blue-600/25"
                : "text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 border border-gray-200/50 hover:border-blue-200/50"
            }`}
          >
            🏨 Hotels
          </button>
          <button
            onClick={() => handleModeChange("tours")}
            className={`px-5 py-4 rounded-2xl font-semibold text-sm transition-all duration-300 text-left ${
              filters.mode === "tours"
                ? "bg-blue-600 text-white shadow-lg shadow-blue-600/25"
                : "text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 border border-gray-200/50 hover:border-blue-200/50"
            }`}
          >
            🚗 Tours
          </button>
        </div>
      </div>

      {/* Filters Content */}
      <div className="p-6 space-y-8">
        {/* Destination */}
        <div>
          <Label
            htmlFor="destination"
            className="text-sm font-semibold text-gray-900 block mb-3"
          >
            Destination
          </Label>
          <div className="relative">
            <MapPinIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <Input
              id="destination"
              type="text"
              placeholder="Where are you going?"
              value={currentFilters.destination}
              onChange={(e) => {
                if (filters.mode === "hotels") {
                  updateHotelFilters({ destination: e.target.value });
                } else {
                  updateTourFilters({ destination: e.target.value });
                }
              }}
              className="pl-12 pr-4 py-3 w-full bg-gray-50/50 border border-gray-200/50 rounded-2xl focus:bg-white focus:border-blue-300 focus:ring-2 focus:ring-blue-100 transition-all duration-200 text-gray-900 placeholder:text-gray-500"
            />
          </div>
        </div>

        {/* Dates */}
        <div>
          <Label className="text-sm font-semibold text-gray-900 block mb-3">
            {filters.mode === "hotels" ? "Check-in / Check-out" : "Tour Date"}
          </Label>
          <div className="space-y-3">
            <div>
              <Label htmlFor="checkin" className="sr-only">
                {filters.mode === "hotels" ? "Check-in" : "Start Date"}
              </Label>
              <Input
                id="checkin"
                type="date"
                value={
                  filters.mode === "hotels"
                    ? filters.hotels.checkIn
                    : filters.tours.startDate
                }
                onChange={(e) => {
                  if (filters.mode === "hotels") {
                    updateHotelFilters({ checkIn: e.target.value });
                  } else {
                    updateTourFilters({ startDate: e.target.value });
                  }
                }}
                className="w-full bg-gray-50/50 border border-gray-200/50 rounded-2xl px-4 py-3 focus:bg-white focus:border-blue-300 focus:ring-2 focus:ring-blue-100 transition-all duration-200 text-gray-900"
                min={new Date().toISOString().split("T")[0]}
              />
            </div>
            <div>
              <Label htmlFor="checkout" className="sr-only">
                {filters.mode === "hotels" ? "Check-out" : "End Date"}
              </Label>
              <Input
                id="checkout"
                type="date"
                value={
                  filters.mode === "hotels"
                    ? filters.hotels.checkOut
                    : filters.tours.endDate
                }
                onChange={(e) => {
                  if (filters.mode === "hotels") {
                    updateHotelFilters({ checkOut: e.target.value });
                  } else {
                    updateTourFilters({ endDate: e.target.value });
                  }
                }}
                className="w-full bg-gray-50/50 border border-gray-200/50 rounded-2xl px-4 py-3 focus:bg-white focus:border-blue-300 focus:ring-2 focus:ring-blue-100 transition-all duration-200 text-gray-900"
                min={
                  filters.mode === "hotels"
                    ? filters.hotels.checkIn ||
                      new Date().toISOString().split("T")[0]
                    : filters.tours.startDate ||
                      new Date().toISOString().split("T")[0]
                }
              />
            </div>
          </div>
        </div>

        {/* Guests/Party Size */}
        <div>
          <Label className="text-sm font-semibold text-gray-900 block mb-3">
            {filters.mode === "hotels" ? "Guests & Rooms" : "Party Size"}
          </Label>
          <GuestSelector
            mode={filters.mode}
            adults={currentFilters.adults}
            numChildren={currentFilters.children}
            childrenAges={
              filters.mode === "hotels" ? filters.hotels.childrenAges : []
            }
            rooms={filters.mode === "hotels" ? filters.hotels.rooms : 1}
            onAdultsChange={(adults) => {
              if (filters.mode === "hotels") {
                updateHotelFilters({ adults });
              } else {
                updateTourFilters({ adults });
              }
            }}
            onChildrenChange={(children, childrenAges) => {
              if (filters.mode === "hotels") {
                updateHotelFilters({ children, childrenAges });
              } else {
                updateTourFilters({ children });
              }
            }}
            onRoomsChange={
              filters.mode === "hotels"
                ? (rooms) => updateHotelFilters({ rooms })
                : undefined
            }
          />
        </div>

        {/* Property Type / Category */}
        <div>
          <Label className="text-sm font-semibold text-gray-900 block mb-4">
            {filters.mode === "hotels" ? "Property Type" : "Category"}
          </Label>
          <div className="space-y-3">
            {(filters.mode === "hotels" ? propertyTypes : tourCategories)
              .slice(
                0,
                expandedSections.propertyType
                  ? filters.mode === "hotels"
                    ? propertyTypes.length
                    : tourCategories.length
                  : 5
              )
              .map((item) => (
                <div key={item.id} className="flex items-center space-x-3">
                  <Checkbox
                    id={item.id}
                    checked={
                      filters.mode === "hotels"
                        ? filters.hotels.propertyType.includes(item.id)
                        : filters.tours.category.includes(item.id)
                    }
                    onCheckedChange={(checked) => {
                      if (filters.mode === "hotels") {
                        const propertyType = checked
                          ? [...filters.hotels.propertyType, item.id]
                          : filters.hotels.propertyType.filter(
                              (id) => id !== item.id
                            );
                        updateHotelFilters({ propertyType });
                      } else {
                        const category = checked
                          ? [...filters.tours.category, item.id]
                          : filters.tours.category.filter(
                              (id) => id !== item.id
                            );
                        updateTourFilters({ category });
                      }
                    }}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                  />
                  <Label
                    htmlFor={item.id}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {item.label}
                  </Label>
                </div>
              ))}
            {(filters.mode === "hotels"
              ? propertyTypes.length
              : tourCategories.length) > 5 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() =>
                  setExpandedSections((prev) => ({
                    ...prev,
                    propertyType: !prev.propertyType,
                  }))
                }
                className="text-blue-600 hover:text-blue-700 hover:bg-blue-50/50 p-0 h-auto font-medium text-sm"
              >
                {expandedSections.propertyType
                  ? "Show Less"
                  : `Show ${
                      (filters.mode === "hotels"
                        ? propertyTypes.length
                        : tourCategories.length) - 5
                    } More`}
              </Button>
            )}
          </div>
        </div>

        {/* Price Range */}
        <div>
          <Label className="text-sm font-semibold text-gray-900 block mb-4">
            Price Range
          </Label>
          <div className="space-y-6">
            <div className="px-3">
              <Slider
                value={[
                  filters.mode === "hotels"
                    ? filters.hotels.priceMin
                    : filters.tours.priceMin,
                  filters.mode === "hotels"
                    ? filters.hotels.priceMax
                    : filters.tours.priceMax,
                ]}
                onValueChange={(value: number[]) => {
                  const [min, max] = value;
                  if (filters.mode === "hotels") {
                    updateHotelFilters({ priceMin: min, priceMax: max });
                  } else {
                    updateTourFilters({ priceMin: min, priceMax: max });
                  }
                }}
                max={filters.mode === "hotels" ? 1000 : 500}
                step={10}
                className="w-full"
              />
            </div>
            <div className="flex items-center justify-between text-sm text-gray-600 font-medium">
              <span className="bg-gray-100/50 px-3 py-1 rounded-full">
                ${" "}
                {filters.mode === "hotels"
                  ? filters.hotels.priceMin
                  : filters.tours.priceMin}
              </span>
              <span className="bg-gray-100/50 px-3 py-1 rounded-full">
                ${" "}
                {filters.mode === "hotels"
                  ? filters.hotels.priceMax
                  : filters.tours.priceMax}
              </span>
            </div>
          </div>
        </div>

        {/* Rating / Duration */}
        <div>
          <Label className="text-sm font-semibold text-gray-900 block mb-4">
            {filters.mode === "hotels" ? "Rating" : "Duration"}
          </Label>
          {filters.mode === "hotels" ? (
            <RadioGroup
              value={filters.hotels.rating.toString()}
              onValueChange={(value) =>
                updateHotelFilters({ rating: parseInt(value) })
              }
            >
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <RadioGroupItem
                    value="0"
                    id="rating-0"
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600"
                  />
                  <Label
                    htmlFor="rating-0"
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    Any Rating
                  </Label>
                </div>
                {[5, 4, 3, 2, 1].map((rating) => (
                  <div key={rating} className="flex items-center space-x-3">
                    <RadioGroupItem
                      value={rating.toString()}
                      id={`rating-${rating}`}
                      className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600"
                    />
                    <Label
                      htmlFor={`rating-${rating}`}
                      className="text-sm text-gray-700 font-medium cursor-pointer flex items-center"
                    >
                      {[...Array(rating)].map((_, i) => (
                        <StarIcon
                          key={i}
                          className="w-4 h-4 text-yellow-400 fill-current mr-1"
                        />
                      ))}
                      <span className="ml-1">& Up</span>
                    </Label>
                  </div>
                ))}
              </div>
            </RadioGroup>
          ) : (
            <div className="space-y-3">
              {tourDurations.map((duration) => (
                <div key={duration.id} className="flex items-center space-x-3">
                  <Checkbox
                    id={duration.id}
                    checked={filters.tours.duration.includes(duration.id)}
                    onCheckedChange={(checked) => {
                      const newDuration = checked
                        ? [...filters.tours.duration, duration.id]
                        : filters.tours.duration.filter(
                            (id) => id !== duration.id
                          );
                      updateTourFilters({ duration: newDuration });
                    }}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                  />
                  <Label
                    htmlFor={duration.id}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {duration.label}
                  </Label>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Amenities / Features */}
        <div>
          <Label className="text-sm font-semibold text-gray-900 block mb-4">
            {filters.mode === "hotels" ? "Amenities" : "Features"}
          </Label>
          <div className="space-y-3">
            {(filters.mode === "hotels" ? amenities : tourFeatures)
              .slice(
                0,
                expandedSections.amenities
                  ? filters.mode === "hotels"
                    ? amenities.length
                    : tourFeatures.length
                  : 5
              )
              .map((item) => (
                <div key={item.id} className="flex items-center space-x-3">
                  <Checkbox
                    id={item.id}
                    checked={
                      filters.mode === "hotels"
                        ? filters.hotels.amenities.includes(item.id)
                        : filters.tours.features.includes(item.id)
                    }
                    onCheckedChange={(checked) => {
                      if (filters.mode === "hotels") {
                        const amenities = checked
                          ? [...filters.hotels.amenities, item.id]
                          : filters.hotels.amenities.filter(
                              (id) => id !== item.id
                            );
                        updateHotelFilters({ amenities });
                      } else {
                        const features = checked
                          ? [...filters.tours.features, item.id]
                          : filters.tours.features.filter(
                              (id) => id !== item.id
                            );
                        updateTourFilters({ features });
                      }
                    }}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                  />
                  <Label
                    htmlFor={item.id}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {item.label}
                  </Label>
                </div>
              ))}
            {(filters.mode === "hotels"
              ? amenities.length
              : tourFeatures.length) > 5 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() =>
                  setExpandedSections((prev) => ({
                    ...prev,
                    amenities: !prev.amenities,
                  }))
                }
                className="text-blue-600 hover:text-blue-700 hover:bg-blue-50/50 p-0 h-auto font-medium text-sm"
              >
                {expandedSections.amenities
                  ? "Show Less"
                  : `Show ${
                      (filters.mode === "hotels"
                        ? amenities.length
                        : tourFeatures.length) - 5
                    } More`}
              </Button>
            )}
          </div>
        </div>

        {/* Tour Type - Tours Only */}
        {filters.mode === "tours" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Tour Type
            </Label>
            <div className="space-y-3">
              {[
                { id: "private", label: "Private Tour" },
                { id: "small-group", label: "Small Group (2-12 people)" },
                { id: "large-group", label: "Large Group (13+ people)" },
                { id: "family-friendly", label: "Family Friendly" },
                { id: "romantic", label: "Romantic/Getaway" },
                { id: "adventure", label: "Adventure Tour" },
                { id: "cultural", label: "Cultural Experience" },
                { id: "food-wine", label: "Food & Wine Tour" },
              ]
                .slice(0, expandedSections.facilities ? 8 : 5)
                .map((tourType) => (
                  <div
                    key={tourType.id}
                    className="flex items-center space-x-3"
                  >
                    <Checkbox
                      id={tourType.id}
                      checked={filters.tours.features.includes(tourType.id)}
                      onCheckedChange={(checked) => {
                        const features = checked
                          ? [...filters.tours.features, tourType.id]
                          : filters.tours.features.filter(
                              (id) => id !== tourType.id
                            );
                        updateTourFilters({ features });
                      }}
                      className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                    />
                    <Label
                      htmlFor={tourType.id}
                      className="text-sm text-gray-700 font-medium cursor-pointer"
                    >
                      {tourType.label}
                    </Label>
                  </div>
                ))}
              {8 > 5 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() =>
                    setExpandedSections((prev) => ({
                      ...prev,
                      facilities: !prev.facilities,
                    }))
                  }
                  className="text-blue-600 hover:text-blue-700 hover:bg-blue-50/50 p-0 h-auto font-medium text-sm"
                >
                  {expandedSections.facilities
                    ? "Show Less"
                    : `Show ${8 - 5} More`}
                </Button>
              )}
            </div>
          </div>
        )}

        {/* Difficulty Level - Tours Only */}
        {filters.mode === "tours" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Difficulty Level
            </Label>
            <div className="space-y-3">
              {[
                {
                  id: "easy",
                  label: "Easy - Minimal walking, suitable for all ages",
                },
                {
                  id: "moderate",
                  label: "Moderate - Some walking, light activity",
                },
                {
                  id: "challenging",
                  label: "Challenging - Extended walking, physical activity",
                },
                { id: "strenuous", label: "Strenuous - High physical demands" },
              ].map((difficulty) => (
                <div
                  key={difficulty.id}
                  className="flex items-center space-x-3"
                >
                  <Checkbox
                    id={difficulty.id}
                    checked={filters.tours.features.includes(difficulty.id)}
                    onCheckedChange={(checked) => {
                      const features = checked
                        ? [...filters.tours.features, difficulty.id]
                        : filters.tours.features.filter(
                            (id) => id !== difficulty.id
                          );
                      updateTourFilters({ features });
                    }}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                  />
                  <Label
                    htmlFor={difficulty.id}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {difficulty.label}
                  </Label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* What's Included - Tours Only */}
        {filters.mode === "tours" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              What&apos;s Included
            </Label>
            <div className="space-y-3">
              {[
                { id: "meals", label: "Meals Included" },
                { id: "drinks", label: "Drinks Included" },
                { id: "transportation", label: "Transportation" },
                { id: "guide", label: "Professional Guide" },
                { id: "entrance-fees", label: "Entrance Fees" },
                { id: "equipment", label: "Equipment Provided" },
                { id: "insurance", label: "Travel Insurance" },
                { id: "accommodation", label: "Accommodation" },
              ]
                .slice(0, expandedSections.roomFacilities ? 8 : 5)
                .map((included) => (
                  <div
                    key={included.id}
                    className="flex items-center space-x-3"
                  >
                    <Checkbox
                      id={included.id}
                      checked={filters.tours.features.includes(included.id)}
                      onCheckedChange={(checked) => {
                        const features = checked
                          ? [...filters.tours.features, included.id]
                          : filters.tours.features.filter(
                              (id) => id !== included.id
                            );
                        updateTourFilters({ features });
                      }}
                      className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                    />
                    <Label
                      htmlFor={included.id}
                      className="text-sm text-gray-700 font-medium cursor-pointer"
                    >
                      {included.label}
                    </Label>
                  </div>
                ))}
              {8 > 5 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() =>
                    setExpandedSections((prev) => ({
                      ...prev,
                      roomFacilities: !prev.roomFacilities,
                    }))
                  }
                  className="text-blue-600 hover:text-blue-700 hover:bg-blue-50/50 p-0 h-auto font-medium text-sm"
                >
                  {expandedSections.roomFacilities
                    ? "Show Less"
                    : `Show ${8 - 5} More`}
                </Button>
              )}
            </div>
          </div>
        )}

        {/* Departure Location - Tours Only */}
        {filters.mode === "tours" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Departure Location
            </Label>
            <div className="space-y-3">
              {[
                { id: "city-center", label: "City Center" },
                { id: "hotel-pickup", label: "Hotel Pickup Available" },
                { id: "airport", label: "Airport" },
                { id: "train-station", label: "Train Station" },
                { id: "port", label: "Port/Harbor" },
                { id: "meeting-point", label: "Designated Meeting Point" },
              ].map((departure) => (
                <div key={departure.id} className="flex items-center space-x-3">
                  <Checkbox
                    id={departure.id}
                    checked={filters.tours.features.includes(departure.id)}
                    onCheckedChange={(checked) => {
                      const features = checked
                        ? [...filters.tours.features, departure.id]
                        : filters.tours.features.filter(
                            (id) => id !== departure.id
                          );
                      updateTourFilters({ features });
                    }}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                  />
                  <Label
                    htmlFor={departure.id}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {departure.label}
                  </Label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tour Highlights - Tours Only */}
        {filters.mode === "tours" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Tour Highlights
            </Label>
            <div className="space-y-3">
              {[
                { id: "historical-sites", label: "Historical Sites" },
                { id: "museums", label: "Museums & Art Galleries" },
                { id: "nature", label: "Natural Landscapes" },
                { id: "beaches", label: "Beaches & Coastlines" },
                { id: "mountains", label: "Mountains & Hiking" },
                { id: "cities", label: "City Exploration" },
                { id: "food-tasting", label: "Local Food & Wine Tasting" },
                { id: "shopping", label: "Shopping & Markets" },
                { id: "wildlife", label: "Wildlife & Safari" },
                { id: "photography", label: "Photography Opportunities" },
              ]
                .slice(0, expandedSections.accessibility ? 10 : 5)
                .map((highlight) => (
                  <div
                    key={highlight.id}
                    className="flex items-center space-x-3"
                  >
                    <Checkbox
                      id={highlight.id}
                      checked={filters.tours.features.includes(highlight.id)}
                      onCheckedChange={(checked) => {
                        const features = checked
                          ? [...filters.tours.features, highlight.id]
                          : filters.tours.features.filter(
                              (id) => id !== highlight.id
                            );
                        updateTourFilters({ features });
                      }}
                      className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                    />
                    <Label
                      htmlFor={highlight.id}
                      className="text-sm text-gray-700 font-medium cursor-pointer"
                    >
                      {highlight.label}
                    </Label>
                  </div>
                ))}
              {10 > 5 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() =>
                    setExpandedSections((prev) => ({
                      ...prev,
                      accessibility: !prev.accessibility,
                    }))
                  }
                  className="text-blue-600 hover:text-blue-700 hover:bg-blue-50/50 p-0 h-auto font-medium text-sm"
                >
                  {expandedSections.accessibility
                    ? "Show Less"
                    : `Show ${10 - 5} More`}
                </Button>
              )}
            </div>
          </div>
        )}

        {/* Sort */}
        <div>
          <Label className="text-sm font-semibold text-gray-900 block mb-4">
            Sort
          </Label>
          <RadioGroup
            value={currentFilters.sort}
            onValueChange={(sort) => {
              if (filters.mode === "hotels") {
                updateHotelFilters({ sort });
              } else {
                updateTourFilters({ sort });
              }
            }}
          >
            <div className="space-y-3">
              {sortOptions.map((option) => (
                <div key={option.id} className="flex items-center space-x-3">
                  <RadioGroupItem
                    value={option.id}
                    id={`sort-${option.id}`}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600"
                  />
                  <Label
                    htmlFor={`sort-${option.id}`}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {option.label}
                  </Label>
                </div>
              ))}
            </div>
          </RadioGroup>
        </div>

        {/* Review Score */}
        {filters.mode === "hotels" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Review Score
            </Label>
            <RadioGroup
              value={filters.hotels.rating.toString()}
              onValueChange={(value) =>
                updateHotelFilters({ rating: parseInt(value) })
              }
            >
              <div className="space-y-3">
                <div className="flex items-center space-x-3">
                  <RadioGroupItem
                    value="0"
                    id="review-0"
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600"
                  />
                  <Label
                    htmlFor="review-0"
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    Any Score
                  </Label>
                </div>
                {[9, 8, 7, 6].map((score) => (
                  <div key={score} className="flex items-center space-x-3">
                    <RadioGroupItem
                      value={score.toString()}
                      id={`review-${score}`}
                      className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600"
                    />
                    <Label
                      htmlFor={`review-${score}`}
                      className="text-sm text-gray-700 font-medium cursor-pointer flex items-center"
                    >
                      {score}+ Excellent
                      <span className="ml-2 text-yellow-500">★★★★★</span>
                    </Label>
                  </div>
                ))}
              </div>
            </RadioGroup>
          </div>
        )}

        {/* Distance from Centre */}
        {filters.mode === "hotels" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Distance from Centre
            </Label>
            <div className="space-y-3">
              {[
                { id: "city-center", label: "City Centre (0-1 km)" },
                { id: "near-center", label: "Near City Centre (1-3 km)" },
                { id: "outskirts", label: "City Outskirts (3-5 km)" },
                { id: "suburban", label: "Suburban Area (5+ km)" },
              ].map((distance) => (
                <div key={distance.id} className="flex items-center space-x-3">
                  <Checkbox
                    id={distance.id}
                    checked={filters.hotels.amenities.includes(distance.id)}
                    onCheckedChange={(checked) => {
                      const amenities = checked
                        ? [...filters.hotels.amenities, distance.id]
                        : filters.hotels.amenities.filter(
                            (id) => id !== distance.id
                          );
                      updateHotelFilters({ amenities });
                    }}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                  />
                  <Label
                    htmlFor={distance.id}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {distance.label}
                  </Label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Highly Rated Features */}
        {filters.mode === "hotels" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Highly Rated Features
            </Label>
            <div className="space-y-3">
              {[
                { id: "excellent-cleanliness", label: "Excellent Cleanliness" },
                { id: "great-location", label: "Great Location" },
                { id: "friendly-staff", label: "Friendly Staff" },
                { id: "comfortable-beds", label: "Comfortable Beds" },
                { id: "free-wifi", label: "Free WiFi" },
                { id: "value-for-money", label: "Value for Money" },
              ].map((feature) => (
                <div key={feature.id} className="flex items-center space-x-3">
                  <Checkbox
                    id={feature.id}
                    checked={filters.hotels.amenities.includes(feature.id)}
                    onCheckedChange={(checked) => {
                      const amenities = checked
                        ? [...filters.hotels.amenities, feature.id]
                        : filters.hotels.amenities.filter(
                            (id) => id !== feature.id
                          );
                      updateHotelFilters({ amenities });
                    }}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                  />
                  <Label
                    htmlFor={feature.id}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {feature.label}
                  </Label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Entire Places for Apartments */}
        {filters.mode === "hotels" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Entire Places
            </Label>
            <div className="space-y-3">
              {[
                { id: "entire-apartment", label: "Entire Apartment" },
                { id: "entire-house", label: "Entire House" },
                { id: "entire-villa", label: "Entire Villa" },
                { id: "entire-cabin", label: "Entire Cabin" },
                { id: "entire-cottage", label: "Entire Cottage" },
              ].map((place) => (
                <div key={place.id} className="flex items-center space-x-3">
                  <Checkbox
                    id={place.id}
                    checked={filters.hotels.propertyType.includes(place.id)}
                    onCheckedChange={(checked) => {
                      const propertyType = checked
                        ? [...filters.hotels.propertyType, place.id]
                        : filters.hotels.propertyType.filter(
                            (id) => id !== place.id
                          );
                      updateHotelFilters({ propertyType });
                    }}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                  />
                  <Label
                    htmlFor={place.id}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {place.label}
                  </Label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Facilities */}
        {filters.mode === "hotels" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Facilities
            </Label>
            <div className="space-y-3">
              {[
                { id: "free-parking", label: "Free Parking" },
                { id: "paid-parking", label: "Paid Parking" },
                { id: "parking-garage", label: "Parking Garage" },
                { id: "street-parking", label: "Street Parking" },
                { id: "valet-parking", label: "Valet Parking" },
                {
                  id: "electric-vehicle-charging",
                  label: "Electric Vehicle Charging",
                },
              ].map((facility) => (
                <div key={facility.id} className="flex items-center space-x-3">
                  <Checkbox
                    id={facility.id}
                    checked={filters.hotels.amenities.includes(facility.id)}
                    onCheckedChange={(checked) => {
                      const amenities = checked
                        ? [...filters.hotels.amenities, facility.id]
                        : filters.hotels.amenities.filter(
                            (id) => id !== facility.id
                          );
                      updateHotelFilters({ amenities });
                    }}
                    className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                  />
                  <Label
                    htmlFor={facility.id}
                    className="text-sm text-gray-700 font-medium cursor-pointer"
                  >
                    {facility.label}
                  </Label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Property Accessibility */}
        {filters.mode === "hotels" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Property Accessibility
            </Label>
            <div className="space-y-3">
              {[
                { id: "wheelchair-accessible", label: "Wheelchair Accessible" },
                { id: "elevator", label: "Elevator" },
                { id: "accessible-parking", label: "Accessible Parking" },
                { id: "roll-in-shower", label: "Roll-in Shower" },
                { id: "grab-rails", label: "Grab Rails" },
                { id: "visual-aids", label: "Visual Aids" },
                { id: "hearing-accessible", label: "Hearing Accessible" },
              ]
                .slice(0, expandedSections.accessibility ? 7 : 5)
                .map((accessibility) => (
                  <div
                    key={accessibility.id}
                    className="flex items-center space-x-3"
                  >
                    <Checkbox
                      id={accessibility.id}
                      checked={filters.hotels.amenities.includes(
                        accessibility.id
                      )}
                      onCheckedChange={(checked) => {
                        const amenities = checked
                          ? [...filters.hotels.amenities, accessibility.id]
                          : filters.hotels.amenities.filter(
                              (id) => id !== accessibility.id
                            );
                        updateHotelFilters({ amenities });
                      }}
                      className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                    />
                    <Label
                      htmlFor={accessibility.id}
                      className="text-sm text-gray-700 font-medium cursor-pointer"
                    >
                      {accessibility.label}
                    </Label>
                  </div>
                ))}
              {7 > 5 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() =>
                    setExpandedSections((prev) => ({
                      ...prev,
                      accessibility: !prev.accessibility,
                    }))
                  }
                  className="text-blue-600 hover:text-blue-700 hover:bg-blue-50/50 p-0 h-auto font-medium text-sm"
                >
                  {expandedSections.accessibility
                    ? "Show Less"
                    : `Show ${7 - 5} More`}
                </Button>
              )}
            </div>
          </div>
        )}

        {/* Room Accessibility */}
        {filters.mode === "hotels" && (
          <div>
            <Label className="text-sm font-semibold text-gray-900 block mb-4">
              Room Accessibility
            </Label>
            <div className="space-y-3">
              {[
                {
                  id: "room-wheelchair-accessible",
                  label: "Wheelchair Accessible Room",
                },
                {
                  id: "room-elevator-access",
                  label: "Elevator Access to Room",
                },
                { id: "room-ground-floor", label: "Ground Floor Room" },
                { id: "room-wide-entrance", label: "Wide Entrance" },
                {
                  id: "room-accessible-bathroom",
                  label: "Accessible Bathroom",
                },
                { id: "room-raised-toilet", label: "Raised Toilet" },
                { id: "room-lowered-sink", label: "Lowered Sink" },
              ]
                .slice(0, expandedSections.roomFacilities ? 7 : 5)
                .map((accessibility) => (
                  <div
                    key={accessibility.id}
                    className="flex items-center space-x-3"
                  >
                    <Checkbox
                      id={accessibility.id}
                      checked={filters.hotels.amenities.includes(
                        accessibility.id
                      )}
                      onCheckedChange={(checked) => {
                        const amenities = checked
                          ? [...filters.hotels.amenities, accessibility.id]
                          : filters.hotels.amenities.filter(
                              (id) => id !== accessibility.id
                            );
                        updateHotelFilters({ amenities });
                      }}
                      className="w-5 h-5 border-2 border-gray-300/50 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600 transition-all duration-200"
                    />
                    <Label
                      htmlFor={accessibility.id}
                      className="text-sm text-gray-700 font-medium cursor-pointer"
                    >
                      {accessibility.label}
                    </Label>
                  </div>
                ))}
              {7 > 5 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() =>
                    setExpandedSections((prev) => ({
                      ...prev,
                      roomFacilities: !prev.roomFacilities,
                    }))
                  }
                  className="text-blue-600 hover:text-blue-700 hover:bg-blue-50/50 p-0 h-auto font-medium text-sm"
                >
                  {expandedSections.roomFacilities
                    ? "Show Less"
                    : `Show ${7 - 5} More`}
                </Button>
              )}
            </div>
          </div>
        )}

        {/* Apply Button */}
        <Button
          onClick={applyFilters}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 rounded-2xl shadow-lg shadow-blue-600/25 transition-all duration-200 hover:shadow-xl hover:shadow-blue-600/30"
        >
          <MagnifyingGlassIcon className="w-5 h-5 mr-3" />
          Search
        </Button>

        {/* Clear Filters */}
        {hasActiveFilters && (
          <Button
            variant="outline"
            onClick={clearFilters}
            className="w-full border-2 border-gray-200/50 bg-gray-50/50 hover:bg-white hover:border-blue-300/50 text-gray-700 font-semibold py-4 rounded-2xl transition-all duration-200"
          >
            Clear All Filters
          </Button>
        )}
      </div>
    </div>
  );
}

// Helper Components
function GuestSelector({
  mode,
  adults,
  numChildren,
  childrenAges,
  rooms,
  onAdultsChange,
  onChildrenChange,
  onRoomsChange,
}: {
  mode: FilterMode;
  adults: number;
  numChildren: number;
  childrenAges: number[];
  rooms?: number;
  onAdultsChange: (adults: number) => void;
  onChildrenChange: (children: number, childrenAges?: number[]) => void;
  onRoomsChange?: (rooms: number) => void;
}) {
  const [isOpen, setIsOpen] = useState(false);

  const guestSummary = `${adults} adult${adults !== 1 ? "s" : ""}${
    numChildren > 0
      ? `, ${numChildren} child${numChildren !== 1 ? "ren" : ""}`
      : ""
  }${
    mode === "hotels" && rooms ? `, ${rooms} room${rooms !== 1 ? "s" : ""}` : ""
  }`;

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className="w-full flex items-center justify-between border-gray-200/50 bg-gray-50/50 hover:bg-white hover:border-blue-300/50 text-gray-900 font-medium shadow-sm rounded-2xl px-4 py-3 transition-all duration-200"
        >
          <div className="flex items-center space-x-3">
            <UsersIcon className="w-5 h-5 text-gray-500" />
            <span className="text-sm">{guestSummary}</span>
          </div>
          <ChevronDownIcon className="w-5 h-5 text-gray-400" />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-72 bg-white/95 backdrop-blur-xl border border-gray-200/50 shadow-xl rounded-2xl"
        align="start"
      >
        <div className="space-y-6 p-2">
          <div className="flex items-center justify-between">
            <Label
              htmlFor="adults"
              className="text-sm font-semibold text-gray-900"
            >
              Adults
            </Label>
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => onAdultsChange(Math.max(1, adults - 1))}
                disabled={adults <= 1}
                className="w-8 h-8 rounded-full border-gray-200/50 hover:border-blue-300/50 hover:bg-blue-50/50 transition-all duration-200"
              >
                −
              </Button>
              <span className="w-8 text-center font-semibold text-gray-900">
                {adults}
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onAdultsChange(adults + 1)}
                className="w-8 h-8 rounded-full border-gray-200/50 hover:border-blue-300/50 hover:bg-blue-50/50 transition-all duration-200"
              >
                +
              </Button>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <Label
              htmlFor="children"
              className="text-sm font-semibold text-gray-900"
            >
              Children
            </Label>
            <div className="flex items-center space-x-3">
              <Button
                variant="outline"
                size="sm"
                onClick={() => onChildrenChange(Math.max(0, numChildren - 1))}
                disabled={numChildren <= 0}
                className="w-8 h-8 rounded-full border-gray-200/50 hover:border-blue-300/50 hover:bg-blue-50/50 transition-all duration-200"
              >
                −
              </Button>
              <span className="w-8 text-center font-semibold text-gray-900">
                {numChildren}
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onChildrenChange(numChildren + 1)}
                className="w-8 h-8 rounded-full border-gray-200/50 hover:border-blue-300/50 hover:bg-blue-50/50 transition-all duration-200"
              >
                +
              </Button>
            </div>
          </div>

          {mode === "hotels" && onRoomsChange && (
            <div className="flex items-center justify-between">
              <Label
                htmlFor="rooms"
                className="text-sm font-semibold text-gray-900"
              >
                Rooms
              </Label>
              <div className="flex items-center space-x-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onRoomsChange(Math.max(1, (rooms || 1) - 1))}
                  disabled={(rooms || 1) <= 1}
                  className="w-8 h-8 rounded-full border-gray-200/50 hover:border-blue-300/50 hover:bg-blue-50/50 transition-all duration-200"
                >
                  −
                </Button>
                <span className="w-8 text-center font-semibold text-gray-900">
                  {rooms || 1}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => onRoomsChange((rooms || 1) + 1)}
                  className="w-8 h-8 rounded-full border-gray-200/50 hover:border-blue-300/50 hover:bg-blue-50/50 transition-all duration-200"
                >
                  +
                </Button>
              </div>
            </div>
          )}

          {numChildren > 0 && mode === "hotels" && (
            <div className="space-y-3">
              <Label className="text-sm font-semibold text-gray-900">
                Children&apos;s Ages
              </Label>
              <div className="grid grid-cols-3 gap-3">
                {Array.from({ length: numChildren }, (_, i) => (
                  <select
                    key={i}
                    value={childrenAges[i] || ""}
                    onChange={(e) => {
                      const newAges = [...childrenAges];
                      newAges[i] = parseInt(e.target.value);
                      onChildrenChange(numChildren, newAges);
                    }}
                    className="px-3 py-2 text-sm border border-gray-200/50 rounded-xl bg-gray-50/50 focus:bg-white focus:border-blue-300 focus:ring-2 focus:ring-blue-100 transition-all duration-200 text-gray-900"
                  >
                    <option value="">Age</option>
                    {Array.from({ length: 18 }, (_, age) => (
                      <option key={age} value={age}>
                        {age}
                      </option>
                    ))}
                  </select>
                ))}
              </div>
            </div>
          )}
        </div>
      </PopoverContent>
    </Popover>
  );
}
