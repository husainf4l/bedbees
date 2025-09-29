"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  ChevronDownIcon,
  PhotoIcon,
  MapPinIcon,
  CurrencyDollarIcon,
  UserGroupIcon,
  ClockIcon,
  CheckCircleIcon,
} from "@heroicons/react/24/outline";
import { StarIcon } from "@heroicons/react/24/solid";
import Image from "next/image";

// Tour categories from destinations page
const tourCategories = ["Historical", "Cultural", "Modern", "Adventure"];

// Popular destinations from Header component
const popularDestinations = [
  {
    name: "Petra",
    country: "Jordan",
    tours: "450+ tours",
    href: "/countries/jordan",
  },
  {
    name: "Dubai",
    country: "UAE",
    tours: "800+ tours",
    href: "/countries/uae",
  },
  {
    name: "Cairo",
    country: "Egypt",
    tours: "600+ tours",
    href: "/countries/egypt",
  },
  {
    name: "Beirut",
    country: "Lebanon",
    tours: "350+ tours",
    href: "/countries/lebanon",
  },
  {
    name: "Doha",
    country: "Qatar",
    tours: "280+ tours",
    href: "/countries/qatar",
  },
  {
    name: "Riyadh",
    country: "Saudi Arabia",
    tours: "420+ tours",
    href: "/countries/saudi-arabia",
  },
  {
    name: "Kuwait City",
    country: "Kuwait",
    tours: "190+ tours",
    href: "/countries/kuwait",
  },
  {
    name: "Manama",
    country: "Bahrain",
    tours: "150+ tours",
    href: "/countries/bahrain",
  },
  {
    name: "Muscat",
    country: "Oman",
    tours: "220+ tours",
    href: "/countries/oman",
  },
  {
    name: "Istanbul",
    country: "Turkey",
    tours: "950+ tours",
    href: "/countries/turkey",
  },
  {
    name: "Damascus",
    country: "Syria",
    tours: "120+ tours",
    href: "/countries/syria",
  },
  {
    name: "Baghdad",
    country: "Iraq",
    tours: "140+ tours",
    href: "/countries/iraq",
  },
  {
    name: "Amman",
    country: "Jordan",
    tours: "380+ tours",
    href: "/countries/jordan",
  },
  {
    name: "Sana'a",
    country: "Yemen",
    tours: "80+ tours",
    href: "/countries/yemen",
  },
  {
    name: "Ramallah",
    country: "Palestine",
    tours: "90+ tours",
    href: "/countries/palestine",
  },
];

// Cities by country
const citiesByCountry: { [key: string]: string[] } = {
  Jordan: [
    "Petra",
    "Amman",
    "Aqaba",
    "Jerash",
    "Madaba",
    "Karak",
    "Dead Sea",
    "Wadi Rum",
  ],
  UAE: [
    "Dubai",
    "Abu Dhabi",
    "Sharjah",
    "Ajman",
    "Ras Al Khaimah",
    "Fujairah",
    "Umm Al Quwain",
  ],
  Egypt: [
    "Cairo",
    "Alexandria",
    "Luxor",
    "Aswan",
    "Sharm El Sheikh",
    "Hurghada",
    "Giza",
    "Port Said",
  ],
  Lebanon: [
    "Beirut",
    "Tripoli",
    "Sidon",
    "Tyre",
    "Byblos",
    "Baalbek",
    "Jounieh",
  ],
  Qatar: [
    "Doha",
    "Al Wakrah",
    "Al Khor",
    "Umm Salal",
    "Al Rayyan",
    "Al Daayen",
  ],
  "Saudi Arabia": [
    "Riyadh",
    "Jeddah",
    "Mecca",
    "Medina",
    "Dammam",
    "Khobar",
    "Taif",
    "Abha",
  ],
  Kuwait: [
    "Kuwait City",
    "Hawalli",
    "Farwaniya",
    "Mubarak Al-Kabeer",
    "Ahmadi",
    "Jahra",
  ],
  Bahrain: [
    "Manama",
    "Muharraq",
    "Riffa",
    "Hamad Town",
    "A'ali",
    "Isa Town",
    "Sitra",
  ],
  Oman: ["Muscat", "Salalah", "Sohar", "Nizwa", "Sur", "Ibri", "Saham"],
  Turkey: [
    "Istanbul",
    "Ankara",
    "Izmir",
    "Antalya",
    "Bursa",
    "Adana",
    "Gaziantep",
  ],
  Syria: [
    "Damascus",
    "Aleppo",
    "Homs",
    "Hama",
    "Latakia",
    "Deir ez-Zor",
    "Raqqa",
  ],
  Iraq: ["Baghdad", "Basra", "Mosul", "Erbil", "Karbala", "Najaf", "Kirkuk"],
  Yemen: [
    "Sana'a",
    "Aden",
    "Taiz",
    "Al Hudaydah",
    "Ibb",
    "Dhamar",
    "Al Mukalla",
  ],
  Palestine: [
    "Ramallah",
    "Gaza City",
    "Hebron",
    "Nablus",
    "Bethlehem",
    "Jericho",
    "Jenin",
  ],
};

interface AccommodationFormData {
  title: string;
  description: string;
  category: string;
  country: string;
  city: string;
  address: string;
  pricePerNight: string;
  currency: string;
  maxGuests: string;
  bedrooms: string;
  bathrooms: string;
  amenities: string[];
  images: File[];
  hostRules: string;
  cancellationPolicy: string;
  checkInTime: string;
  checkOutTime: string;
  minimumStay: string;
  maximumStay: string;
}

const initialFormData: AccommodationFormData = {
  title: "",
  description: "",
  category: "",
  country: "",
  city: "",
  address: "",
  pricePerNight: "",
  currency: "USD",
  maxGuests: "",
  bedrooms: "",
  bathrooms: "",
  amenities: [],
  images: [],
  hostRules: "",
  cancellationPolicy: "flexible",
  checkInTime: "14:00",
  checkOutTime: "11:00",
  minimumStay: "1",
  maximumStay: "30",
};

const amenitiesList = [
  "WiFi",
  "Kitchen",
  "Washer",
  "Dryer",
  "Air conditioning",
  "Heating",
  "TV",
  "Hair dryer",
  "Iron",
  "Workspace",
  "Pool",
  "Hot tub",
  "Free parking",
  "EV charger",
  "Gym",
  "BBQ grill",
  "Breakfast",
  "Beach access",
  "Mountain view",
  "City view",
  "Garden",
  "Patio",
];

export default function NewAccommodationPage() {
  const router = useRouter();
  const [formData, setFormData] =
    useState<AccommodationFormData>(initialFormData);
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const handleInputChange = (
    field: keyof AccommodationFormData,
    value: unknown
  ) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: "" }));
    }
  };

  const handleAmenityToggle = (amenity: string) => {
    setFormData((prev) => ({
      ...prev,
      amenities: prev.amenities.includes(amenity)
        ? prev.amenities.filter((a) => a !== amenity)
        : [...prev.amenities, amenity],
    }));
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    setFormData((prev) => ({
      ...prev,
      images: [...prev.images, ...files],
    }));
  };

  const removeImage = (index: number) => {
    setFormData((prev) => ({
      ...prev,
      images: prev.images.filter((_, i) => i !== index),
    }));
  };

  const validateStep = (step: number): boolean => {
    const newErrors: { [key: string]: string } = {};

    switch (step) {
      case 1:
        if (!formData.title.trim()) newErrors.title = "Title is required";
        if (!formData.description.trim())
          newErrors.description = "Description is required";
        if (!formData.category) newErrors.category = "Category is required";
        break;
      case 2:
        if (!formData.country) newErrors.country = "Country is required";
        if (!formData.city) newErrors.city = "City is required";
        if (!formData.address.trim()) newErrors.address = "Address is required";
        break;
      case 3:
        if (
          !formData.pricePerNight ||
          parseFloat(formData.pricePerNight) <= 0
        ) {
          newErrors.pricePerNight = "Valid price is required";
        }
        if (!formData.maxGuests || parseInt(formData.maxGuests) <= 0) {
          newErrors.maxGuests = "Valid number of guests is required";
        }
        if (!formData.bedrooms || parseInt(formData.bedrooms) <= 0) {
          newErrors.bedrooms = "Valid number of bedrooms is required";
        }
        if (!formData.bathrooms || parseInt(formData.bathrooms) <= 0) {
          newErrors.bathrooms = "Valid number of bathrooms is required";
        }
        break;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep((prev) => Math.min(prev + 1, 4));
    }
  };

  const prevStep = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 1));
  };

  const handleSubmit = async () => {
    if (!validateStep(currentStep)) return;

    setIsSubmitting(true);
    try {
      // Here you would typically send the data to your backend
      console.log("Submitting accommodation:", formData);

      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 2000));

      // Redirect to success page or accommodation management
      router.push("/hostdashboard/accommodations");
    } catch (error) {
      console.error("Error submitting accommodation:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const availableCities = citiesByCountry[formData.country] || [];

  // Get unique countries from popular destinations
  const availableCountries = [
    ...new Set(popularDestinations.map((dest) => dest.country)),
  ].sort();

  // Get cities from popular destinations for the selected country
  const navbarCities = popularDestinations
    .filter((dest) => dest.country === formData.country)
    .map((dest) => dest.name);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              List Your Accommodation
            </h1>
            <div className="flex items-center space-x-2">
              {[1, 2, 3, 4].map((step) => (
                <div key={step} className="flex items-center">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                      step < currentStep
                        ? "bg-green-500 text-white"
                        : step === currentStep
                        ? "bg-blue-500 text-white"
                        : "bg-gray-200 text-gray-600"
                    }`}
                  >
                    {step < currentStep ? (
                      <CheckCircleIcon className="w-5 h-5" />
                    ) : (
                      step
                    )}
                  </div>
                  {step < 4 && (
                    <div
                      className={`w-12 h-0.5 mx-2 ${
                        step < currentStep ? "bg-green-500" : "bg-gray-200"
                      }`}
                    />
                  )}
                </div>
              ))}
            </div>
          </div>
          <div className="mt-2 text-sm text-gray-600">
            Step {currentStep} of 4:{" "}
            {currentStep === 1
              ? "Basic Information"
              : currentStep === 2
              ? "Location Details"
              : currentStep === 3
              ? "Accommodation Details"
              : "Review & Publish"}
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Step 1: Basic Information */}
        {currentStep === 1 && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Accommodation Title *
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => handleInputChange("title", e.target.value)}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.title ? "border-red-300" : "border-gray-300"
                }`}
                placeholder="e.g., Cozy Beachfront Villa in Dubai"
              />
              {errors.title && (
                <p className="mt-1 text-sm text-red-600">{errors.title}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description *
              </label>
              <textarea
                value={formData.description}
                onChange={(e) =>
                  handleInputChange("description", e.target.value)
                }
                rows={4}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.description ? "border-red-300" : "border-gray-300"
                }`}
                placeholder="Describe your accommodation, its unique features, and what makes it special..."
              />
              {errors.description && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.description}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tour Category *
              </label>
              <div className="relative">
                <select
                  value={formData.category}
                  onChange={(e) =>
                    handleInputChange("category", e.target.value)
                  }
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none ${
                    errors.category ? "border-red-300" : "border-gray-300"
                  }`}
                >
                  <option value="">Select a category</option>
                  {tourCategories.map((category) => (
                    <option key={category} value={category}>
                      {category}
                    </option>
                  ))}
                </select>
                <ChevronDownIcon className="absolute right-3 top-3.5 w-5 h-5 text-gray-400 pointer-events-none" />
              </div>
              {errors.category && (
                <p className="mt-1 text-sm text-red-600">{errors.category}</p>
              )}
            </div>
          </div>
        )}

        {/* Step 2: Location Details */}
        {currentStep === 2 && (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Country *
              </label>
              <div className="relative">
                <select
                  value={formData.country}
                  onChange={(e) => handleInputChange("country", e.target.value)}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none ${
                    errors.country ? "border-red-300" : "border-gray-300"
                  }`}
                >
                  <option value="">Select a country</option>
                  {availableCountries.map((country) => (
                    <option key={country} value={country}>
                      {country}
                    </option>
                  ))}
                </select>
                <ChevronDownIcon className="absolute right-3 top-3.5 w-5 h-5 text-gray-400 pointer-events-none" />
              </div>
              {errors.country && (
                <p className="mt-1 text-sm text-red-600">{errors.country}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                City *
              </label>
              <div className="relative">
                <select
                  value={formData.city}
                  onChange={(e) => handleInputChange("city", e.target.value)}
                  disabled={!formData.country || navbarCities.length === 0}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none disabled:bg-gray-100 disabled:cursor-not-allowed ${
                    errors.city ? "border-red-300" : "border-gray-300"
                  }`}
                >
                  <option value="">
                    {formData.country
                      ? navbarCities.length > 0
                        ? "Select a city"
                        : "No cities available for this country"
                      : "Please select a country first"}
                  </option>
                  {navbarCities.map((city) => (
                    <option key={city} value={city}>
                      {city}
                    </option>
                  ))}
                </select>
                <ChevronDownIcon className="absolute right-3 top-3.5 w-5 h-5 text-gray-400 pointer-events-none" />
              </div>
              {errors.city && (
                <p className="mt-1 text-sm text-red-600">{errors.city}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Street Address *
              </label>
              <input
                type="text"
                value={formData.address}
                onChange={(e) => handleInputChange("address", e.target.value)}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.address ? "border-red-300" : "border-gray-300"
                }`}
                placeholder="e.g., 123 Palm Street, Jumeirah Beach"
              />
              {errors.address && (
                <p className="mt-1 text-sm text-red-600">{errors.address}</p>
              )}
            </div>
          </div>
        )}

        {/* Step 3: Accommodation Details */}
        {currentStep === 3 && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Price per Night *
                </label>
                <div className="relative">
                  <CurrencyDollarIcon className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                  <input
                    type="number"
                    value={formData.pricePerNight}
                    onChange={(e) =>
                      handleInputChange("pricePerNight", e.target.value)
                    }
                    className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      errors.pricePerNight
                        ? "border-red-300"
                        : "border-gray-300"
                    }`}
                    placeholder="0.00"
                    min="0"
                    step="0.01"
                  />
                </div>
                {errors.pricePerNight && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.pricePerNight}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Currency
                </label>
                <select
                  value={formData.currency}
                  onChange={(e) =>
                    handleInputChange("currency", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="USD">USD ($)</option>
                  <option value="EUR">EUR (€)</option>
                  <option value="GBP">GBP (£)</option>
                  <option value="AED">AED (د.إ)</option>
                  <option value="SAR">SAR (﷼)</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Guests *
                </label>
                <div className="relative">
                  <UserGroupIcon className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
                  <input
                    type="number"
                    value={formData.maxGuests}
                    onChange={(e) =>
                      handleInputChange("maxGuests", e.target.value)
                    }
                    className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      errors.maxGuests ? "border-red-300" : "border-gray-300"
                    }`}
                    placeholder="4"
                    min="1"
                  />
                </div>
                {errors.maxGuests && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.maxGuests}
                  </p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Bedrooms *
                </label>
                <input
                  type="number"
                  value={formData.bedrooms}
                  onChange={(e) =>
                    handleInputChange("bedrooms", e.target.value)
                  }
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.bedrooms ? "border-red-300" : "border-gray-300"
                  }`}
                  placeholder="2"
                  min="0"
                />
                {errors.bedrooms && (
                  <p className="mt-1 text-sm text-red-600">{errors.bedrooms}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Bathrooms *
                </label>
                <input
                  type="number"
                  value={formData.bathrooms}
                  onChange={(e) =>
                    handleInputChange("bathrooms", e.target.value)
                  }
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.bathrooms ? "border-red-300" : "border-gray-300"
                  }`}
                  placeholder="1"
                  min="0"
                  step="0.5"
                />
                {errors.bathrooms && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.bathrooms}
                  </p>
                )}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Amenities
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {amenitiesList.map((amenity) => (
                  <label
                    key={amenity}
                    className="flex items-center space-x-2 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={formData.amenities.includes(amenity)}
                      onChange={() => handleAmenityToggle(amenity)}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700">{amenity}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Photos
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
                <div className="text-center">
                  <PhotoIcon className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="mt-4">
                    <label htmlFor="photo-upload" className="cursor-pointer">
                      <span className="mt-2 block text-sm font-medium text-blue-600 hover:text-blue-500">
                        Upload photos
                      </span>
                    </label>
                    <input
                      id="photo-upload"
                      type="file"
                      multiple
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                  </div>
                  <p className="mt-1 text-xs text-gray-500">
                    PNG, JPG, GIF up to 10MB each
                  </p>
                </div>
              </div>

              {formData.images.length > 0 && (
                <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                  {formData.images.map((image, index) => (
                    <div key={index} className="relative">
                      <Image
                        src={URL.createObjectURL(image)}
                        alt={`Upload ${index + 1}`}
                        width={150}
                        height={150}
                        className="w-full h-32 object-cover rounded-lg"
                      />
                      <button
                        onClick={() => removeImage(index)}
                        className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Step 4: Review & Publish */}
        {currentStep === 4 && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Review Your Listing
              </h3>

              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-900">
                    {formData.title}
                  </h4>
                  <p className="text-sm text-gray-600 mt-1">
                    {formData.description}
                  </p>
                </div>

                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <span className="flex items-center">
                    <MapPinIcon className="w-4 h-4 mr-1" />
                    {formData.city}, {formData.country}
                  </span>
                  <span className="flex items-center">
                    <CurrencyDollarIcon className="w-4 h-4 mr-1" />
                    {formData.pricePerNight} {formData.currency} per night
                  </span>
                  <span className="flex items-center">
                    <UserGroupIcon className="w-4 h-4 mr-1" />
                    Up to {formData.maxGuests} guests
                  </span>
                </div>

                <div>
                  <p className="text-sm font-medium text-gray-700">
                    Category: {formData.category}
                  </p>
                  <p className="text-sm text-gray-600">
                    Address: {formData.address}
                  </p>
                  <p className="text-sm text-gray-600">
                    {formData.bedrooms} bedrooms • {formData.bathrooms}{" "}
                    bathrooms
                  </p>
                </div>

                {formData.amenities.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-2">
                      Amenities:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {formData.amenities.map((amenity) => (
                        <span
                          key={amenity}
                          className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                        >
                          {amenity}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {formData.images.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-2">
                      Photos ({formData.images.length}):
                    </p>
                    <div className="grid grid-cols-4 gap-2">
                      {formData.images.slice(0, 4).map((image, index) => (
                        <Image
                          key={index}
                          src={URL.createObjectURL(image)}
                          alt={`Preview ${index + 1}`}
                          width={100}
                          height={100}
                          className="w-full h-20 object-cover rounded"
                        />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-8 pt-6 border-t">
          <button
            onClick={prevStep}
            disabled={currentStep === 1}
            className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>

          {currentStep < 4 ? (
            <button
              onClick={nextStep}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Next
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? "Publishing..." : "Publish Listing"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
