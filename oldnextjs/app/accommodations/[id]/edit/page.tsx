"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import AccommodationRegistrationForm from "@/components/ui/AccommodationRegistrationForm";
import { AccommodationFormData, Accommodation } from "@/types/accommodation";
import { accommodationService } from "@/services/accommodation.service";
import { Apartment } from "@/types/common";

export default function EditAccommodationPage() {
  const params = useParams();
  const router = useRouter();
  const [accommodation, setAccommodation] = useState<Accommodation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({
    totalBookings: 0,
    totalRevenue: 0,
    averageRating: 0,
    totalReviews: 0,
    viewsThisMonth: 0,
  });

  useEffect(() => {
    const fetchAccommodation = async () => {
      try {
        setLoading(true);
        const id = params.id as string;

        // Try to get from API first, fallback to demo data
        // Try to get from API first
        const accommodationData =
          await accommodationService.getAccommodationById(id);

        if (!accommodationData) {
          setError("Accommodation not found");
          return;
        }

        // Fetch accommodation statistics (mock data for now)
        const accommodationStats = {
          totalBookings: Math.floor(Math.random() * 50) + 10,
          totalRevenue: Math.floor(Math.random() * 5000) + 1000,
          averageRating: Math.round((Math.random() * 2 + 3) * 10) / 10, // 3.0-5.0
          totalReviews: Math.floor(Math.random() * 20) + 5,
          viewsThisMonth: Math.floor(Math.random() * 200) + 50,
        };
        setStats(accommodationStats);

        // Transform API data to form data
        const formData: AccommodationFormData = {
          title: accommodationData.title || "",
          description: accommodationData.description || "",
          categoryId: accommodationData.categoryId || "default",
          city: accommodationData.city || "",
          country: accommodationData.country || "",
          address: accommodationData.address || "",
          latitude: accommodationData.latitude,
          longitude: accommodationData.longitude,
          basePrice: accommodationData.basePrice || 100,
          currency: accommodationData.currency || "USD",
          maxGuests: accommodationData.maxGuests || 2,
          bedrooms: accommodationData.bedrooms || 1,
          bathrooms: accommodationData.bathrooms || 1,
          amenities: accommodationData.amenities || [],
          images: accommodationData.images || [],
          isAvailable: accommodationData.isAvailable !== false,
          roomTypes: [], // Will be populated if available
          // Additional fields with defaults since Apartment interface doesn't have them
          starRating: undefined,
          languagesSpoken: [],
          neighborhoodHighlights: [],
          roomSize: undefined,
          checkInOutTimes: {
            checkInTime: "15:00",
            checkOutTime: "11:00",
            earlyCheckIn: false,
            lateCheckOut: false,
            earlyCheckInFee: 0,
            lateCheckOutFee: 0,
          },
          cancellationPolicy: "Standard",
          safetyCompliance: {
            smokeDetectors: false,
            carbonMonoxideDetectors: false,
            firstAidKit: false,
            fireExtinguishers: false,
            securityCameras: false,
            emergencyContact: "",
          },
        };

        setAccommodation(formData);
      } catch (err) {
        console.error("Error fetching accommodation:", err);
        setError("Failed to load accommodation");
      } finally {
        setLoading(false);
      }
    };

    if (params.id) {
      fetchAccommodation();
    }
  }, [params.id]);

  const handleSubmit = async (formData: AccommodationFormData) => {
    try {
      // Extract only the fields that the update API expects
      const updateData = {
        title: formData.title,
        description: formData.description,
        categoryId: formData.categoryId,
        city: formData.city,
        country: formData.country,
        address: formData.address,
        latitude: formData.latitude,
        longitude: formData.longitude,
        basePrice: formData.basePrice,
        currency: formData.currency,
        maxGuests: formData.maxGuests,
        bedrooms: formData.bedrooms,
        bathrooms: formData.bathrooms,
        amenities: formData.amenities,
        images: formData.images,
        isAvailable: formData.isAvailable,
      };

      await accommodationService.updateAccommodation(
        params.id as string,
        updateData
      );

      // Redirect back to the accommodations list
      router.push("/hostdashboard/accommodations");
    } catch (err) {
      console.error("Error updating accommodation:", err);
      setError("Failed to update accommodation");
    }
  };

  const handleCancel = () => {
    router.push("/hostdashboard/accommodations");
  };

  const toggleAvailability = async () => {
    if (!accommodation) return;

    try {
      const updatedData = {
        ...accommodation,
        isAvailable: !accommodation.isAvailable,
      };

      await accommodationService.updateAccommodation(params.id as string, {
        title: updatedData.title,
        description: updatedData.description,
        categoryId: updatedData.categoryId,
        city: updatedData.city,
        country: updatedData.country,
        address: updatedData.address,
        latitude: updatedData.latitude,
        longitude: updatedData.longitude,
        basePrice: updatedData.basePrice,
        currency: updatedData.currency,
        maxGuests: updatedData.maxGuests,
        bedrooms: updatedData.bedrooms,
        bathrooms: updatedData.bathrooms,
        amenities: updatedData.amenities,
        images: updatedData.images,
        isAvailable: updatedData.isAvailable,
      });

      setAccommodation(updatedData);
    } catch (err) {
      console.error("Error updating availability:", err);
      setError("Failed to update availability");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading accommodation...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-xl font-semibold mb-4">Error</div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => router.push("/hostdashboard/accommodations")}
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Back to Accommodations
          </button>
        </div>
      </div>
    );
  }

  if (!accommodation) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-600 text-xl">Accommodation not found</div>
          <button
            onClick={() => router.push("/hostdashboard/accommodations")}
            className="mt-4 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Back to Accommodations
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-8 px-4">
        {/* Header Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Edit Accommodation
              </h1>
              <p className="text-gray-600 mt-2">
                Update your accommodation details and manage your listing
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={toggleAvailability}
                className={`px-4 py-2 rounded-lg font-medium ${
                  accommodation?.isAvailable
                    ? "bg-green-100 text-green-800 hover:bg-green-200"
                    : "bg-red-100 text-red-800 hover:bg-red-200"
                }`}
              >
                {accommodation?.isAvailable ? "✓ Available" : "✗ Unavailable"}
              </button>
              <button
                onClick={() => router.push(`/accommodations/${params.id}`)}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
              >
                View Public Page
              </button>
            </div>
          </div>
        </div>

        {/* Stats Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
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
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">
                  Total Bookings
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.totalBookings}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
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
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">
                  Total Revenue
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  ${stats.totalRevenue}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
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
                    d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">
                  Average Rating
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.averageRating}
                </p>
                <p className="text-sm text-gray-500">
                  {stats.totalReviews} reviews
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
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
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">
                  Views This Month
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stats.viewsThisMonth}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Accommodation Details Form */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              Accommodation Details
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              Update your accommodation information
            </p>
          </div>
          <div className="p-6">
            <AccommodationRegistrationForm
              selectedCategory=""
              onSubmit={handleSubmit}
              onCancel={handleCancel}
              initialData={accommodation}
              isEditMode={true}
            />
          </div>
        </div>

        {/* Additional Information Section */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Image Gallery Preview */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">
                Image Gallery
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Current images in your listing
              </p>
            </div>
            <div className="p-6">
              {accommodation?.images && accommodation.images.length > 0 ? (
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {accommodation.images
                    .slice(0, 6)
                    .map((image: string, index: number) => (
                      <div
                        key={index}
                        className="aspect-square rounded-lg overflow-hidden bg-gray-100"
                      >
                        <img
                          src={image}
                          alt={`Accommodation ${index + 1}`}
                          className="w-full h-full object-cover"
                        />
                      </div>
                    ))}
                  {accommodation.images.length > 6 && (
                    <div className="aspect-square rounded-lg bg-gray-100 flex items-center justify-center">
                      <span className="text-gray-500 text-sm">
                        +{accommodation.images.length - 6} more
                      </span>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <svg
                    className="w-12 h-12 mx-auto mb-4 text-gray-300"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                  <p>No images uploaded yet</p>
                </div>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">
                Quick Actions
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Common management tasks
              </p>
            </div>
            <div className="p-6 space-y-4">
              <button
                onClick={() =>
                  router.push(
                    `/hostdashboard/accommodations/${params.id}/bookings`
                  )
                }
                className="w-full flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center">
                  <svg
                    className="w-5 h-5 text-blue-600 mr-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                  <div>
                    <p className="font-medium text-gray-900">Manage Bookings</p>
                    <p className="text-sm text-gray-600">
                      View and manage reservations
                    </p>
                  </div>
                </div>
                <svg
                  className="w-5 h-5 text-gray-400"
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

              <button
                onClick={() =>
                  router.push(
                    `/hostdashboard/accommodations/${params.id}/analytics`
                  )
                }
                className="w-full flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center">
                  <svg
                    className="w-5 h-5 text-green-600 mr-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                  </svg>
                  <div>
                    <p className="font-medium text-gray-900">View Analytics</p>
                    <p className="text-sm text-gray-600">
                      Performance and insights
                    </p>
                  </div>
                </div>
                <svg
                  className="w-5 h-5 text-gray-400"
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

              <button
                onClick={() =>
                  router.push(
                    `/hostdashboard/accommodations/${params.id}/reviews`
                  )
                }
                className="w-full flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center">
                  <svg
                    className="w-5 h-5 text-yellow-600 mr-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                    />
                  </svg>
                  <div>
                    <p className="font-medium text-gray-900">Manage Reviews</p>
                    <p className="text-sm text-gray-600">
                      Read and respond to guest reviews
                    </p>
                  </div>
                </div>
                <svg
                  className="w-5 h-5 text-gray-400"
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
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
