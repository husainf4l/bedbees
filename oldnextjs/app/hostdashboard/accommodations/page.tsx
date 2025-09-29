"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/providers/AuthContext";
import { Accommodation } from "@/types/accommodation";

// Demo data for development when backend is not available
const demoHostAccommodations: Accommodation[] = [
  {
    id: "demo-1",
    title: "Luxury Downtown Hotel Suite",
    description:
      "Experience the pinnacle of luxury in our stunning downtown hotel suite with breathtaking city views.",
    category: "HOTEL",
    location: "New York, NY, USA",
    price: 120,
    currency: "USD",
    bedrooms: 1,
    bathrooms: 1,
    maxGuests: 2,
    images: ["/hero/hotel.webp"],
    status: "active",
    createdAt: "2025-09-18",
    bookings: 15,
  },
  {
    id: "demo-2",
    title: "Mountain View Chalet",
    description:
      "Rustic mountain chalet with stunning alpine views and modern amenities.",
    category: "CHALET",
    location: "Zermatt, Switzerland",
    price: 350,
    currency: "USD",
    bedrooms: 3,
    bathrooms: 2,
    maxGuests: 6,
    images: ["/hero/chalets.webp"],
    status: "active",
    createdAt: "2025-09-15",
    bookings: 8,
  },
  {
    id: "demo-3",
    title: "Beachfront Villa",
    description:
      "Luxurious beachfront villa with private pool and ocean views.",
    category: "VILLA",
    location: "Malibu, CA, USA",
    price: 500,
    currency: "USD",
    bedrooms: 4,
    bathrooms: 3,
    maxGuests: 8,
    images: ["/hero/villa.webp"],
    status: "draft",
    createdAt: "2025-09-20",
    bookings: 0,
  },
];

export default function AccommodationsPage() {
  const router = useRouter();
  const { user } = useAuth();
  const [accommodations, setAccommodations] = useState<Accommodation[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedStatus, setSelectedStatus] = useState<string>("all");
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [lightboxImages, setLightboxImages] = useState<string[]>([]);
  const [lightboxIndex, setLightboxIndex] = useState(0);

  // Keyboard navigation for lightbox
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (!lightboxOpen) return;

      if (event.key === "Escape") {
        closeLightbox();
      } else if (event.key === "ArrowLeft") {
        prevLightboxImage();
      } else if (event.key === "ArrowRight") {
        nextLightboxImage();
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [lightboxOpen, lightboxImages.length]);

  // Fetch accommodations from API
  useEffect(() => {
    const fetchAccommodations = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem("accessToken");

        if (!token) {
          console.error("No auth token found");
          setLoading(false);
          return;
        }

        let response;
        try {
          response = await fetch("/api/accommodations", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          });
        } catch (fetchError) {
          console.log(
            "API unavailable, falling back to demo host accommodations data"
          );
          setAccommodations(demoHostAccommodations);
          setLoading(false);
          return;
        }

        if (response.ok) {
          const data = await response.json();
          console.log("Fetched accommodations:", data);

          // Transform backend data to match frontend interface
          let transformedData: Accommodation[] = data.data.map((acc: Record<string, unknown>) => ({
            id: acc.id,
            title: acc.title,
            description: acc.description || "",
            category: acc.category?.type || acc.category || "unknown",
            location: `${acc.city}, ${acc.country}`,
            price: acc.basePrice,
            currency: acc.currency,
            bedrooms: acc.bedrooms || 0,
            bathrooms: acc.bathrooms || 0,
            maxGuests: acc.maxGuests,
            images: acc.images || [],
            status: acc.status as "active" | "draft" | "paused",
            createdAt: new Date(acc.createdAt).toISOString().split("T")[0],
            bookings: 0, // We'll add booking count later
          }));

          // Filter accommodations by current user's hostId if user is logged in
          if (user && user.id) {
            transformedData = transformedData.filter((acc) => {
              // For demo purposes, we'll check if the accommodation's hostId matches the user ID
              // In a real app, this filtering should happen on the backend
              const accommodationData = data.data.find(
                (apiAcc: Record<string, unknown>) => apiAcc.id === acc.id
              );
              return accommodationData && accommodationData.hostId === user.id;
            });
          }

          setAccommodations(transformedData);
        } else {
          console.error("Failed to fetch accommodations:", response.statusText);
          // Fallback to demo data for development
          console.log("Falling back to demo host accommodations data");
          setAccommodations(demoHostAccommodations);
        }
      } catch (error) {
        console.error("Error fetching accommodations:", error);
        // Fallback to demo data for development when backend is unavailable
        console.log(
          "Backend unavailable, falling back to demo host accommodations data"
        );
        setAccommodations(demoHostAccommodations);
      } finally {
        setLoading(false);
      }
    };

    fetchAccommodations();
  }, []);

  const filteredAccommodations = accommodations.filter(
    (acc) => selectedStatus === "all" || acc.status === selectedStatus
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-green-100 text-green-800";
      case "draft":
        return "bg-gray-100 text-gray-800";
      case "paused":
        return "bg-yellow-100 text-yellow-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const openLightbox = (images: string[], startIndex: number = 0) => {
    console.log(
      "Opening lightbox with images:",
      images,
      "at index:",
      startIndex
    );
    setLightboxImages(images);
    setLightboxIndex(startIndex);
    setLightboxOpen(true);
  };

  const closeLightbox = () => {
    console.log("Closing lightbox");
    setLightboxOpen(false);
    setLightboxImages([]);
    setLightboxIndex(0);
  };

  const nextLightboxImage = () => {
    console.log(
      "Next image, current index:",
      lightboxIndex,
      "of",
      lightboxImages.length
    );
    setLightboxIndex((prev) => (prev + 1) % lightboxImages.length);
  };

  const prevLightboxImage = () => {
    console.log(
      "Previous image, current index:",
      lightboxIndex,
      "of",
      lightboxImages.length
    );
    setLightboxIndex(
      (prev) => (prev - 1 + lightboxImages.length) % lightboxImages.length
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-300 rounded w-64 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((n) => (
                <div
                  key={n}
                  className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
                >
                  <div className="h-48 bg-gray-300 rounded mb-4"></div>
                  <div className="h-4 bg-gray-300 rounded mb-2"></div>
                  <div className="h-4 bg-gray-300 rounded w-3/4"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="flex mb-6" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-4">
            <li>
              <button
                onClick={() => router.push("/hostdashboard")}
                className="text-gray-400 hover:text-gray-500 transition-colors"
              >
                Host Dashboard
              </button>
            </li>
            <li>
              <svg
                className="flex-shrink-0 h-5 w-5 text-gray-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            </li>
            <li>
              <span className="text-gray-500">My Accommodations</span>
            </li>
          </ol>
        </nav>

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              My Accommodations
            </h1>
            <p className="text-gray-600">
              Manage your properties and track bookings
            </p>
          </div>
          <div className="mt-4 sm:mt-0">
            <button
              onClick={() => router.push("/hostdashboard")}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium flex items-center gap-2"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>
              Add New Property
            </button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100">
                <svg
                  className="w-6 h-6 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">
                  Total Properties
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {accommodations.length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100">
                <svg
                  className="w-6 h-6 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">
                  Active Properties
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {
                    accommodations.filter((acc) => acc.status === "active")
                      .length
                  }
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-purple-100">
                <svg
                  className="w-6 h-6 text-purple-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 7V3a4 4 0 118 0v4m-4 8a4 4 0 11-8 0v1h16v-1a4 4 0 11-8 0z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">
                  Total Bookings
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {accommodations.reduce((sum, acc) => sum + acc.bookings, 0)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-yellow-100">
                <svg
                  className="w-6 h-6 text-yellow-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Revenue</p>
                <p className="text-2xl font-bold text-gray-900">
                  $
                  {accommodations.reduce(
                    (sum, acc) => sum + acc.price * acc.bookings,
                    0
                  )}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex flex-wrap gap-3">
            <label className="text-sm font-medium text-gray-700">
              Filter by status:
            </label>
            {["all", "active", "draft", "paused"].map((status) => (
              <button
                key={status}
                onClick={() => setSelectedStatus(status)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedStatus === status
                    ? "bg-green-100 text-green-700 border border-green-200"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Accommodations Grid */}
        {filteredAccommodations.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
            <svg
              className="w-16 h-16 mx-auto mb-4 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
              />
            </svg>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              No accommodations found
            </h3>
            <p className="text-gray-600 mb-6">
              {selectedStatus === "all"
                ? "You haven't added any properties yet."
                : `You don't have any ${selectedStatus} properties.`}
            </p>
            <button
              onClick={() => router.push("/hostdashboard")}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium"
            >
              Add Your First Property
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAccommodations.map((accommodation) => (
              <div
                key={accommodation.id}
                className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
              >
                {/* Simplified Mosaic Image Gallery */}
                <div className="relative overflow-hidden rounded-t-lg">
                  <div className="aspect-video bg-gray-100">
                    {/* Debug: Show what we have */}
                    <div className="absolute top-2 left-2 z-20 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded">
                      {accommodation.images?.length || 0} images
                    </div>

                    {/* Always show at least one image or placeholder */}
                    {!accommodation.images ||
                    accommodation.images.length === 0 ? (
                      <div className="w-full h-full bg-red-200 flex items-center justify-center">
                        <div className="text-red-600 text-center">
                          <p className="text-sm font-bold">❌ NO IMAGES</p>
                          <p className="text-xs">
                            Check console for debug info
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="w-full h-full">
                        {/* Single image layout */}
                        {accommodation.images.length === 1 && (
                          <img
                            src={accommodation.images[0]}
                            alt={accommodation.title}
                            className="w-full h-full object-cover cursor-pointer hover:opacity-95"
                            onClick={() =>
                              openLightbox(accommodation.images, 0)
                            }
                            onLoad={() =>
                              console.log("✅ Loaded:", accommodation.images[0])
                            }
                            onError={(e) => {
                              console.error(
                                "❌ Failed to load:",
                                accommodation.images[0]
                              );
                              const img = e.target as HTMLImageElement;
                              img.src = "/hero/hero1.webp";
                            }}
                          />
                        )}

                        {/* Multiple images - mosaic layout */}
                        {accommodation.images.length >= 2 && (
                          <div className="grid grid-cols-2 gap-1 h-full">
                            {/* Main large image */}
                            <div className="row-span-2">
                              <img
                                src={accommodation.images[0]}
                                alt={`${accommodation.title} 1`}
                                className="w-full h-full object-cover cursor-pointer hover:opacity-95"
                                onClick={() =>
                                  openLightbox(accommodation.images, 0)
                                }
                                onLoad={() =>
                                  console.log(
                                    "✅ Loaded main:",
                                    accommodation.images[0]
                                  )
                                }
                                onError={(e) => {
                                  console.error(
                                    "❌ Failed main:",
                                    accommodation.images[0]
                                  );
                                  const img = e.target as HTMLImageElement;
                                  img.src = "/hero/hero1.webp";
                                }}
                              />
                            </div>

                            {/* Smaller images */}
                            <div className="grid grid-rows-2 gap-1 h-full">
                              {accommodation.images
                                .slice(1, 3)
                                .map((image, index) => (
                                  <div key={index + 1} className="relative">
                                    <img
                                      src={image}
                                      alt={`${accommodation.title} ${
                                        index + 2
                                      }`}
                                      className="w-full h-full object-cover cursor-pointer hover:opacity-95"
                                      onClick={() =>
                                        openLightbox(
                                          accommodation.images,
                                          index + 1
                                        )
                                      }
                                      onLoad={() =>
                                        console.log(
                                          `✅ Loaded ${index + 2}:`,
                                          image
                                        )
                                      }
                                      onError={(e) => {
                                        console.error(
                                          `❌ Failed ${index + 2}:`,
                                          image
                                        );
                                        const img =
                                          e.target as HTMLImageElement;
                                        img.src = "/hero/hero1.webp";
                                      }}
                                    />

                                    {/* Show "+X more" overlay on last image if needed */}
                                    {index === 1 &&
                                      accommodation.images.length > 3 && (
                                        <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center text-white font-bold cursor-pointer hover:bg-opacity-40">
                                          +{accommodation.images.length - 3}{" "}
                                          more
                                        </div>
                                      )}
                                  </div>
                                ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Status badge overlay */}
                  <div className="absolute top-3 right-3 z-10">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium shadow-lg ${getStatusColor(
                        accommodation.status
                      )}`}
                    >
                      {accommodation.status.charAt(0).toUpperCase() +
                        accommodation.status.slice(1)}
                    </span>
                  </div>
                </div>

                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                    {accommodation.title}
                  </h3>

                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {accommodation.description}
                  </p>

                  <div className="space-y-2 mb-4">
                    <div className="flex items-center text-sm text-gray-500">
                      <svg
                        className="w-4 h-4 mr-2"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                        />
                      </svg>
                      {accommodation.location}
                    </div>

                    <div className="flex items-center text-sm text-gray-500">
                      <svg
                        className="w-4 h-4 mr-2"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2 2z"
                        />
                      </svg>
                      {accommodation.bedrooms} bed • {accommodation.bathrooms}{" "}
                      bath • {accommodation.maxGuests} guests
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-2xl font-bold text-gray-900">
                        ${accommodation.price}
                      </span>
                      <span className="text-gray-500 text-sm"> / night</span>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-500">
                        {accommodation.bookings} bookings
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-2 mt-4">
                    <button
                      onClick={() =>
                        router.push(`/accommodations/${accommodation.id}/edit`)
                      }
                      className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() =>
                        router.push(`/accommodations/${accommodation.id}`)
                      }
                      className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm font-medium"
                    >
                      View
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Lightbox Modal */}
      {lightboxOpen && (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-90 flex items-center justify-center">
          <div className="relative w-full h-full flex items-center justify-center p-4">
            {/* Close button */}
            <button
              onClick={closeLightbox}
              className="absolute top-6 right-6 z-50 bg-black bg-opacity-50 hover:bg-opacity-75 text-white p-3 rounded-full transition-all"
            >
              <svg
                className="w-6 h-6"
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

            {/* Image counter */}
            <div className="absolute top-6 left-6 z-50 bg-black bg-opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium">
              {lightboxIndex + 1} / {lightboxImages.length}
            </div>

            {/* Navigation arrows */}
            {lightboxImages.length > 1 && (
              <>
                <button
                  onClick={prevLightboxImage}
                  className="absolute left-6 top-1/2 -translate-y-1/2 z-50 bg-black bg-opacity-50 hover:bg-opacity-75 text-white p-4 rounded-full transition-all"
                >
                  <svg
                    className="w-6 h-6"
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
                  onClick={nextLightboxImage}
                  className="absolute right-6 top-1/2 -translate-y-1/2 z-50 bg-black bg-opacity-50 hover:bg-opacity-75 text-white p-4 rounded-full transition-all"
                >
                  <svg
                    className="w-6 h-6"
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

            {/* Main image */}
            <div className="max-w-5xl max-h-full flex items-center justify-center">
              <img
                src={lightboxImages[lightboxIndex]}
                alt={`Gallery image ${lightboxIndex + 1}`}
                className="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
                onClick={(e) => e.stopPropagation()}
              />
            </div>

            {/* Thumbnail navigation */}
            {lightboxImages.length > 1 && (
              <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-50">
                <div className="flex gap-2 bg-black bg-opacity-50 p-3 rounded-lg max-w-md overflow-x-auto">
                  {lightboxImages.map((image, index) => (
                    <button
                      key={index}
                      onClick={() => setLightboxIndex(index)}
                      className={`flex-shrink-0 w-16 h-12 rounded overflow-hidden transition-all ${
                        index === lightboxIndex
                          ? "ring-2 ring-white scale-110"
                          : "opacity-70 hover:opacity-100"
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

            {/* Click outside to close */}
            <div className="absolute inset-0 -z-10" onClick={closeLightbox} />
          </div>
        </div>
      )}
    </div>
  );
}
