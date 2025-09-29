"use client";

import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import ExperienceSearchBar from "@/components/ui/ExperienceSearchBar";
import {
  HeartIcon,
  MapPinIcon,
  UsersIcon,
  ClockIcon,
  CheckCircleIcon,
  StarIcon,
  LanguageIcon,
  CalendarIcon,
  CurrencyDollarIcon,
  XMarkIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  GlobeAltIcon,
  ShieldCheckIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/outline";
import { HeartIcon as HeartSolidIcon } from "@heroicons/react/24/solid";
import { Tour } from "@/types/tour";
import { tourService } from "@/services/tour.service";

// Enhanced interfaces for tour details
interface BookingOption {
  id: string;
  date: string;
  time: string;
  availableSpots: number;
  price: number;
  isEarlyBird?: boolean;
  isLastMinute?: boolean;
}

const bookingOptions: BookingOption[] = [
  {
    id: "1",
    date: "2025-09-20",
    time: "09:00",
    availableSpots: 8,
    price: 2500,
    isEarlyBird: true,
  },
  {
    id: "2",
    date: "2025-09-20",
    time: "14:00",
    availableSpots: 5,
    price: 2500,
  },
  {
    id: "3",
    date: "2025-09-21",
    time: "09:00",
    availableSpots: 12,
    price: 2500,
  },
  {
    id: "4",
    date: "2025-09-22",
    time: "10:00",
    availableSpots: 2,
    price: 2800,
    isLastMinute: true,
  },
];

export default function TourDetail() {
  const params = useParams();
  const id = params.id as string;
  const [tour, setTour] = useState<Tour | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Lightbox state
  const [isLightboxOpen, setIsLightboxOpen] = useState(false);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [lightboxImages, setLightboxImages] = useState<string[]>([]);

  // Booking state
  const [selectedBookingOption, setSelectedBookingOption] =
    useState<string>("");
  const [participants, setParticipants] = useState(1);
  const [isWishlisted, setIsWishlisted] = useState(false);

  // Tour sections
  const [activeSection, setActiveSection] = useState("overview");

  useEffect(() => {
    if (id) {
      setLoading(true);
      const fetchTour = async () => {
        try {
          const tourData = await tourService.getTourById(id);
          if (tourData) {
            setTour(tourData);
            setError(null);
          } else {
            setError("Tour not found");
          }
        } catch (err: unknown) {
          console.error("Error fetching tour:", err);
          // Check if it's a specific "not found" error
          const errorMessage = err instanceof Error ? err.message : String(err);
          const isNotFoundError =
            errorMessage.includes("Tour not found") ||
            errorMessage.includes("Resource not found") ||
            errorMessage.includes("404") ||
            (typeof err === "object" &&
              err !== null &&
              "status" in err &&
              (err as { status?: number }).status === 404);

          if (isNotFoundError) {
            setError("Tour not found");
          } else if (errorMessage.includes("Network")) {
            setError(
              "Network error - please check your connection and try again"
            );
          } else {
            setError("Failed to load tour details");
          }
        } finally {
          setLoading(false);
        }
      };
      fetchTour();
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

  const formatDuration = (minutes: number) => {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
  };

  const getCategoryBadgeColor = (category: string) => {
    switch (category.toLowerCase()) {
      case "share_trip":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "private":
        return "bg-purple-100 text-purple-800 border-purple-200";
      case "group":
        return "bg-green-100 text-green-800 border-green-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  const formatCategoryName = (category: string) => {
    return category
      .replace("_", " ")
      .toLowerCase()
      .replace(/\b\w/g, (l) => l.toUpperCase());
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const formatTime = (timeString: string) => {
    const [hours, minutes] = timeString.split(":");
    const date = new Date();
    date.setHours(parseInt(hours), parseInt(minutes));
    return date.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
  };

  const calculateTotalPrice = () => {
    const selectedOption = bookingOptions.find(
      (option) => option.id === selectedBookingOption
    );
    if (!selectedOption) return 0;
    return (selectedOption.price / 100) * participants;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading tour details...</p>
        </div>
      </div>
    );
  }

  if (error || !tour) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            {error || "Tour not found"}
          </h1>
          <p className="text-gray-600 mb-4">
            The tour you&apos;re looking for doesn&apos;t exist or has been
            removed.
          </p>
          <button
            onClick={() => window.history.back()}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const tourImages = tour.media.map((media) => media.url);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <h1 className="text-2xl font-bold text-gray-900">{tour.title}</h1>
              <span
                className={`px-3 py-1 text-sm font-medium rounded-full border ${getCategoryBadgeColor(
                  tour.category
                )}`}
              >
                {formatCategoryName(tour.category)}
              </span>
              {tour.isEarlyBird && (
                <span className="px-3 py-1 text-sm font-medium bg-orange-100 text-orange-800 rounded-full border border-orange-200">
                  Early Bird
                </span>
              )}
              {tour.isDropIn && (
                <span className="px-3 py-1 text-sm font-medium bg-yellow-100 text-yellow-800 rounded-full border border-yellow-200">
                  Drop-in
                </span>
              )}
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <StarIcon
                      key={i}
                      className={`w-4 h-4 ${
                        i < Math.floor(tour.guide.ratingAvg)
                          ? "text-yellow-400 fill-current"
                          : "text-gray-300"
                      }`}
                    />
                  ))}
                </div>
                <span className="text-sm text-gray-600">
                  {tour.guide.ratingAvg.toFixed(1)} ({tour._count.bookings}{" "}
                  reviews)
                </span>
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
      </div>

      {/* Experience Search Bar - Compact Version */}
      <div className="bg-gradient-to-b from-gray-50 to-white py-8">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-2">
              Looking for more experiences?
            </h2>
            <p className="text-gray-600">
              Discover other amazing tours and activities
            </p>
          </div>
          <ExperienceSearchBar
            onSearch={(searchData) => {
              console.log("Experience search:", searchData);
              // Here you can implement navigation to tours page with search filters
              window.location.href = `/tours?search=${encodeURIComponent(
                JSON.stringify(searchData)
              )}`;
            }}
            className="max-w-4xl mx-auto"
          />
        </div>
      </div>

      {/* Photo Gallery */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="relative">
          <div className="grid grid-cols-4 gap-3 h-[600px] rounded-2xl overflow-hidden shadow-2xl">
            {/* Main hero image */}
            <div
              className="col-span-2 relative cursor-pointer group overflow-hidden"
              onClick={() => openLightbox(tourImages, 0)}
            >
              <img
                src={tourImages[0] || "/hero/travelhero.webp"}
                alt={tour.title}
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
              {[1, 2, 3, 4].map((index) => (
                <div
                  key={index}
                  className="relative cursor-pointer group overflow-hidden rounded-lg"
                  onClick={() => openLightbox(tourImages, index)}
                >
                  <img
                    src={tourImages[index] || "/hero/travelhero.webp"}
                    alt={`${tour.title} photo ${index + 1}`}
                    className="w-full h-full object-cover transition-all duration-500 group-hover:scale-110 group-hover:brightness-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-br from-black/0 via-black/0 to-black/30 opacity-0 group-hover:opacity-100 transition-all duration-500"></div>

                  {index === 3 && tourImages.length > 5 && (
                    <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
                      <div className="text-white text-center">
                        <div className="text-2xl font-bold mb-1">
                          +{tourImages.length - 5}
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
            {tourImages.length} Photos
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
                  {tour.city}, {tour.country}
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
                <div className="flex items-center">
                  <ClockIcon className="w-5 h-5 text-blue-500 mr-2" />
                  <div>
                    <div className="font-semibold">
                      {formatDuration(tour.durationMins)}
                    </div>
                    <div className="text-sm text-gray-500">Duration</div>
                  </div>
                </div>
                <div className="flex items-center">
                  <UsersIcon className="w-5 h-5 text-green-500 mr-2" />
                  <div>
                    <div className="font-semibold">
                      {tour.minGroup}-{tour.maxGroup}
                    </div>
                    <div className="text-sm text-gray-500">Group Size</div>
                  </div>
                </div>
                <div className="flex items-center">
                  <LanguageIcon className="w-5 h-5 text-purple-500 mr-2" />
                  <div>
                    <div className="font-semibold">{tour.language}</div>
                    <div className="text-sm text-gray-500">Language</div>
                  </div>
                </div>
                <div className="flex items-center">
                  <CalendarIcon className="w-5 h-5 text-orange-500 mr-2" />
                  <div>
                    <div className="font-semibold">
                      {tour.instantBook ? "Instant" : "Request"}
                    </div>
                    <div className="text-sm text-gray-500">Booking</div>
                  </div>
                </div>
              </div>

              <p className="text-gray-700 leading-relaxed text-lg">
                {tour.description}
              </p>
            </div>

            {/* Tab Navigation */}
            <div className="border-b border-gray-200">
              <nav className="flex space-x-8">
                {[
                  { id: "overview", label: "Overview" },
                  { id: "itinerary", label: "Itinerary" },
                  { id: "included", label: "What's Included" },
                  { id: "guide", label: "Your Guide" },
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveSection(tab.id)}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeSection === tab.id
                        ? "border-blue-500 text-blue-600"
                        : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </nav>
            </div>

            {/* Tab Content */}
            <div>
              {activeSection === "overview" && (
                <div className="space-y-6">
                  {/* Highlights */}
                  {tour.highlights && tour.highlights.length > 0 && (
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-4">
                        Tour Highlights
                      </h3>
                      <div className="grid gap-3">
                        {tour.highlights.map((highlight, index) => (
                          <div key={index} className="flex items-start gap-3">
                            <CheckCircleIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-700">{highlight}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Travel Styles */}
                  {tour.travelStyles && tour.travelStyles.length > 0 && (
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-4">
                        Experience Style
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {tour.travelStyles.map((style) => (
                          <span
                            key={style}
                            className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                          >
                            {style}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Difficulty */}
                  {tour.difficulty && (
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-4">
                        Difficulty Level
                      </h3>
                      <div className="flex items-center gap-3">
                        <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm font-medium">
                          {tour.difficulty}
                        </span>
                        {tour.accessibility &&
                          tour.accessibility.length > 0 && (
                            <span className="text-sm text-gray-600">
                              • {tour.accessibility.join(", ")}
                            </span>
                          )}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {activeSection === "itinerary" && (
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    Tour Itinerary
                  </h3>
                  {tour.itinerary ? (
                    <div className="bg-gray-50 rounded-lg p-6">
                      <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                        {tour.itinerary}
                      </p>
                    </div>
                  ) : (
                    <p className="text-gray-600">
                      Detailed itinerary will be provided upon booking.
                    </p>
                  )}
                </div>
              )}

              {activeSection === "included" && (
                <div className="space-y-6">
                  {/* What's Included */}
                  {tour.whatsIncluded && tour.whatsIncluded.length > 0 && (
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-4">
                        What&apos;s Included
                      </h3>
                      <div className="grid gap-3">
                        {tour.whatsIncluded.map((item, index) => (
                          <div key={index} className="flex items-start gap-3">
                            <CheckCircleIcon className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-700">{item}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* What's Excluded */}
                  {tour.whatsExcluded && tour.whatsExcluded.length > 0 && (
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-4">
                        What&apos;s Not Included
                      </h3>
                      <div className="grid gap-3">
                        {tour.whatsExcluded.map((item, index) => (
                          <div key={index} className="flex items-start gap-3">
                            <XMarkIcon className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-700">{item}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Requirements */}
                  {tour.requirements && tour.requirements.length > 0 && (
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-4">
                        What to Bring
                      </h3>
                      <div className="grid gap-3">
                        {tour.requirements.map((requirement, index) => (
                          <div key={index} className="flex items-start gap-3">
                            <ExclamationTriangleIcon className="w-5 h-5 text-orange-500 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-700">{requirement}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {activeSection === "guide" && (
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-6">
                    Meet Your Guide
                  </h3>
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <div className="flex items-start gap-6">
                      <div className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold flex-shrink-0">
                        {tour.guide.user.name.charAt(0).toUpperCase()}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-4 mb-3">
                          <h4 className="text-2xl font-semibold text-gray-900">
                            {tour.guide.user.name}
                          </h4>
                          <div className="flex items-center gap-2">
                            <div className="flex items-center">
                              {[...Array(5)].map((_, i) => (
                                <StarIcon
                                  key={i}
                                  className={`w-4 h-4 ${
                                    i < Math.floor(tour.guide.ratingAvg)
                                      ? "text-yellow-400 fill-current"
                                      : "text-gray-300"
                                  }`}
                                />
                              ))}
                            </div>
                            <span className="text-sm text-gray-600">
                              {tour.guide.ratingAvg.toFixed(1)} (
                              {tour.guide.toursCount} tours)
                            </span>
                          </div>
                        </div>

                        {tour.guide.bio && (
                          <p className="text-gray-700 mb-4 leading-relaxed">
                            {tour.guide.bio}
                          </p>
                        )}

                        <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-4">
                          <div>Response time: Usually within 2 hours</div>
                          <div>Languages: {tour.languages.join(", ")}</div>
                          <div>Total tours: {tour.guide.toursCount}</div>
                          <div>
                            KYC Status:{" "}
                            {tour.guide.kycStatus === "verified"
                              ? "✅ Verified"
                              : "Pending"}
                          </div>
                        </div>

                        <div className="flex gap-3">
                          <button className="flex-1 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-50 transition-colors">
                            Message Guide
                          </button>
                          <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                            <GlobeAltIcon className="w-5 h-5" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Meeting Point */}
            <div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                Meeting Point
              </h2>
              <div className="bg-gray-100 rounded-lg p-6">
                <div className="flex items-start gap-4">
                  <MapPinIcon className="w-6 h-6 text-gray-600 mt-1" />
                  <div>
                    <div className="font-medium text-gray-900 mb-1">
                      {tour.meetingPoint ||
                        "Meeting point will be confirmed upon booking"}
                    </div>
                    <div className="text-gray-600">
                      {tour.city}, {tour.country}
                    </div>
                    {tour.latitude && tour.longitude && (
                      <div className="text-sm text-gray-500 mt-2">
                        Coordinates: {tour.latitude.toFixed(4)},{" "}
                        {tour.longitude.toFixed(4)}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Booking */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6 sticky top-24">
              <div className="mb-6">
                {tour.isPayWhatYouWant ? (
                  <div className="text-3xl font-bold text-green-600">
                    Pay What You Want
                  </div>
                ) : (
                  <>
                    <div className="text-3xl font-bold text-blue-600">
                      ${(tour.basePrice / 100).toFixed(0)}
                    </div>
                    <div className="text-gray-500">per person</div>
                  </>
                )}
              </div>

              {/* Available Dates */}
              <div className="mb-6">
                <h4 className="font-semibold text-gray-900 mb-4">
                  Select Date & Time
                </h4>
                <div className="space-y-3">
                  {bookingOptions.map((option) => (
                    <div
                      key={option.id}
                      className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                        selectedBookingOption === option.id
                          ? "border-blue-500 bg-blue-50"
                          : "border-gray-200 hover:border-gray-300"
                      }`}
                      onClick={() => setSelectedBookingOption(option.id)}
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <div className="font-medium text-gray-900">
                            {formatDate(option.date)}
                          </div>
                          <div className="text-sm text-gray-600">
                            {formatTime(option.time)}
                          </div>
                          <div className="text-sm text-gray-500 mt-1">
                            {option.availableSpots} spots available
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-bold text-gray-900">
                            ${(option.price / 100).toFixed(0)}
                          </div>
                          {option.isEarlyBird && (
                            <span className="inline-block px-2 py-1 text-xs bg-orange-100 text-orange-800 rounded-full mt-1">
                              Early Bird
                            </span>
                          )}
                          {option.isLastMinute && (
                            <span className="inline-block px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full mt-1">
                              Last Minute
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Participants */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Participants
                </label>
                <select
                  value={participants}
                  onChange={(e) => setParticipants(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {Array.from({ length: tour.maxGroup }, (_, i) => i + 1).map(
                    (num) => (
                      <option key={num} value={num}>
                        {num} participant{num !== 1 ? "s" : ""}
                      </option>
                    )
                  )}
                </select>
              </div>

              {/* Price Breakdown */}
              {selectedBookingOption && (
                <div className="bg-gray-50 rounded-lg p-4 mb-6">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-gray-600">Base price</span>
                    <span className="font-medium">
                      ${calculateTotalPrice()}
                    </span>
                  </div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-gray-600">Service fee</span>
                    <span className="font-medium">
                      ${Math.round(calculateTotalPrice() * 0.1)}
                    </span>
                  </div>
                  <div className="border-t pt-2 mt-2">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-gray-900">Total</span>
                      <span className="text-xl font-bold text-blue-600">
                        $
                        {calculateTotalPrice() +
                          Math.round(calculateTotalPrice() * 0.1)}
                      </span>
                    </div>
                  </div>
                </div>
              )}

              <button
                disabled={!selectedBookingOption}
                className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed text-white font-semibold py-4 px-4 rounded-xl transition-all duration-200 hover:shadow-lg hover:shadow-blue-200/50 hover:-translate-y-0.5 mb-4"
              >
                {tour.instantBook ? "Book Instantly" : "Request to Book"}
              </button>

              <div className="text-center text-sm text-gray-500 mb-4">
                {tour.instantBook
                  ? "Instant confirmation"
                  : "You won't be charged until confirmed"}
              </div>

              {/* Cancellation Policy */}
              <div className="border-t pt-6">
                <h4 className="font-semibold text-gray-900 mb-4">
                  Cancellation Policy
                </h4>
                <div className="flex items-start gap-3">
                  <ShieldCheckIcon className="w-5 h-5 text-green-500 mt-0.5" />
                  <div>
                    <div className="font-medium text-gray-900 mb-1">
                      {tour.cancellationPolicy === "flexible" &&
                        "Free cancellation until 24 hours before"}
                      {tour.cancellationPolicy === "standard" &&
                        "Free cancellation until 48 hours before"}
                      {tour.cancellationPolicy === "strict" &&
                        "Free cancellation until 7 days before"}
                    </div>
                    <div className="text-sm text-gray-600">
                      Full refund if cancelled within the policy timeframe
                    </div>
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
            <XMarkIcon className="w-8 h-8" />
          </button>

          {lightboxImages.length > 1 && (
            <>
              <button
                onClick={prevImage}
                className="absolute left-6 top-1/2 -translate-y-1/2 text-white hover:text-gray-300 transition-colors z-60"
              >
                <ChevronLeftIcon className="w-10 h-10" />
              </button>
              <button
                onClick={nextImage}
                className="absolute right-6 top-1/2 -translate-y-1/2 text-white hover:text-gray-300 transition-colors z-60"
              >
                <ChevronRightIcon className="w-10 h-10" />
              </button>
            </>
          )}

          <div className="max-w-7xl max-h-[90vh] mx-auto px-6">
            <img
              src={lightboxImages[currentImageIndex]}
              alt={`${tour.title} photo ${currentImageIndex + 1}`}
              className="max-h-[80vh] max-w-full object-contain rounded-lg shadow-2xl"
            />

            <div className="mt-4 text-white text-center">
              {currentImageIndex + 1} / {lightboxImages.length}
            </div>
          </div>

          {lightboxImages.length > 1 && (
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
          )}
        </div>
      )}
    </div>
  );
}
