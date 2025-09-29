"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { useAuth } from "@/providers/AuthContext";
import {
  CalendarIcon,
  MapPinIcon,
  UsersIcon,
  CurrencyDollarIcon,
  StarIcon,
  ChevronDownIcon,
  ChevronUpIcon,
} from "@heroicons/react/24/outline";
import {
  CheckCircleIcon as CheckCircleSolidIcon,
  XCircleIcon as XCircleSolidIcon,
  ExclamationTriangleIcon as ExclamationTriangleSolidIcon,
} from "@heroicons/react/24/solid";

interface Booking {
  id: string;
  type: "tour" | "accommodation";
  title: string;
  location: string;
  image: string;
  startDate: string;
  endDate: string;
  status: "confirmed" | "pending" | "cancelled" | "completed";
  totalPrice: number;
  currency: string;
  guests: number;
  bookingReference: string;
  bookingDate: string;
  provider: {
    name: string;
    rating: number;
    reviews: number;
  };
  cancellationPolicy?: string;
  specialRequests?: string;
  contactInfo: {
    phone: string;
    email: string;
  };
}

const statusConfig = {
  confirmed: {
    label: "Confirmed",
    color: "bg-green-100 text-green-800",
    icon: CheckCircleSolidIcon,
    description: "Your booking is confirmed",
  },
  pending: {
    label: "Pending",
    color: "bg-yellow-100 text-yellow-800",
    icon: ExclamationTriangleSolidIcon,
    description: "Awaiting confirmation",
  },
  cancelled: {
    label: "Cancelled",
    color: "bg-red-100 text-red-800",
    icon: XCircleSolidIcon,
    description: "Booking has been cancelled",
  },
  completed: {
    label: "Completed",
    color: "bg-blue-100 text-blue-800",
    icon: CheckCircleSolidIcon,
    description: "Trip completed successfully",
  },
};

const mockBookings: Booking[] = [
  {
    id: "BK-2025-001",
    type: "tour",
    title: "Historic Cyprus Cultural Walking Tour",
    location: "Nicosia, Cyprus",
    image: "/hero/apartment.webp",
    startDate: "2025-10-15",
    endDate: "2025-10-15",
    status: "confirmed",
    totalPrice: 2500,
    currency: "USD",
    guests: 2,
    bookingReference: "CY-001-2025",
    bookingDate: "2025-09-20",
    provider: {
      name: "Cyprus Cultural Tours",
      rating: 4.8,
      reviews: 1247,
    },
    cancellationPolicy: "Free cancellation up to 24 hours before",
    specialRequests: "Vegetarian meals preferred",
    contactInfo: {
      phone: "+357 22 123456",
      email: "info@cyprus-tours.com",
    },
  },
  {
    id: "BK-2025-002",
    type: "accommodation",
    title: "Luxury Downtown Hotel Suite",
    location: "New York, NY, USA",
    image: "/hero/hotel.webp",
    startDate: "2025-11-01",
    endDate: "2025-11-05",
    status: "confirmed",
    totalPrice: 48000,
    currency: "USD",
    guests: 2,
    bookingReference: "NY-002-2025",
    bookingDate: "2025-09-18",
    provider: {
      name: "Grand Hotel Manhattan",
      rating: 4.6,
      reviews: 2156,
    },
    cancellationPolicy: "Free cancellation up to 48 hours before",
    specialRequests: "Late check-out requested",
    contactInfo: {
      phone: "+1 (555) 123-4567",
      email: "reservations@grandhotel.com",
    },
  },
  {
    id: "BK-2025-003",
    type: "tour",
    title: "Wadi Rum Desert Safari Adventure",
    location: "Wadi Rum, Jordan",
    image: "/hero/villa.webp",
    startDate: "2025-12-10",
    endDate: "2025-12-10",
    status: "pending",
    totalPrice: 14500,
    currency: "USD",
    guests: 4,
    bookingReference: "JO-003-2025",
    bookingDate: "2025-09-22",
    provider: {
      name: "Desert Adventures Co.",
      rating: 4.9,
      reviews: 892,
    },
    cancellationPolicy: "Free cancellation up to 72 hours before",
    specialRequests: "All participants are experienced hikers",
    contactInfo: {
      phone: "+962 3 123456",
      email: "bookings@desert-adventures.com",
    },
  },
  {
    id: "BK-2025-004",
    type: "accommodation",
    title: "Mountain View Chalet",
    location: "Zermatt, Switzerland",
    image: "/hero/chalets.webp",
    startDate: "2025-09-25",
    endDate: "2025-09-28",
    status: "completed",
    totalPrice: 14000,
    currency: "USD",
    guests: 3,
    bookingReference: "CH-004-2025",
    bookingDate: "2025-08-15",
    provider: {
      name: "Alpine Chalets",
      rating: 4.7,
      reviews: 634,
    },
    cancellationPolicy: "Free cancellation up to 7 days before",
    specialRequests: "Ski equipment rental needed",
    contactInfo: {
      phone: "+41 27 123 4567",
      email: "info@alpine-chalets.ch",
    },
  },
];

export default function BookingsPage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [filterType, setFilterType] = useState<string>("all");
  const [expandedBooking, setExpandedBooking] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<string>("date-desc");

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
      return;
    }

    // Load mock bookings data
    setBookings(mockBookings);
  }, [user, loading, router]);

  const filteredBookings = bookings
    .filter(
      (booking) => filterStatus === "all" || booking.status === filterStatus
    )
    .filter((booking) => filterType === "all" || booking.type === filterType)
    .sort((a, b) => {
      switch (sortBy) {
        case "date-desc":
          return (
            new Date(b.bookingDate).getTime() -
            new Date(a.bookingDate).getTime()
          );
        case "date-asc":
          return (
            new Date(a.bookingDate).getTime() -
            new Date(b.bookingDate).getTime()
          );
        case "price-desc":
          return b.totalPrice - a.totalPrice;
        case "price-asc":
          return a.totalPrice - b.totalPrice;
        default:
          return 0;
      }
    });

  const toggleExpanded = (bookingId: string) => {
    setExpandedBooking(expandedBooking === bookingId ? null : bookingId);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      weekday: "short",
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const formatPrice = (price: number, currency: string) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency,
    }).format(price / 100); // Assuming price is in cents
  };

  const getStatusBadge = (status: Booking["status"]) => {
    const config = statusConfig[status];
    const Icon = config.icon;
    return (
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}
      >
        <Icon className="w-3 h-3 mr-1" />
        {config.label}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your bookings...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Access Denied
          </h1>
          <p className="text-gray-600 mb-6">
            Please log in to view your bookings.
          </p>
          <button
            onClick={() => router.push("/login")}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Log In
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Bookings</h1>
              <p className="text-gray-600 mt-1">
                Manage your trip reservations and bookings
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                {filteredBookings.length} booking
                {filteredBookings.length !== 1 ? "s" : ""}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Filters and Sorting */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex flex-wrap gap-4 items-center">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Status</option>
                <option value="confirmed">Confirmed</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Types</option>
                <option value="tour">Tours</option>
                <option value="accommodation">Accommodations</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Sort By
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="date-desc">Newest First</option>
                <option value="date-asc">Oldest First</option>
                <option value="price-desc">Highest Price</option>
                <option value="price-asc">Lowest Price</option>
              </select>
            </div>
          </div>
        </div>

        {/* Bookings List */}
        <div className="space-y-6">
          {filteredBookings.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm p-12 text-center">
              <CalendarIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No bookings found
              </h3>
              <p className="text-gray-600 mb-6">
                {filterStatus !== "all" || filterType !== "all"
                  ? "Try adjusting your filters to see more bookings."
                  : "You haven't made any bookings yet. Start exploring amazing destinations!"}
              </p>
              {(filterStatus !== "all" || filterType !== "all") && (
                <button
                  onClick={() => {
                    setFilterStatus("all");
                    setFilterType("all");
                  }}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Clear Filters
                </button>
              )}
            </div>
          ) : (
            filteredBookings.map((booking) => (
              <div
                key={booking.id}
                className="bg-white rounded-lg shadow-sm overflow-hidden"
              >
                {/* Booking Header */}
                <div className="p-6 border-b border-gray-200">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-4">
                      <div className="relative w-20 h-20 rounded-lg overflow-hidden flex-shrink-0">
                        <Image
                          src={booking.image}
                          alt={booking.title}
                          fill
                          className="object-cover"
                        />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <h3 className="text-lg font-semibold text-gray-900">
                              {booking.title}
                            </h3>
                            <div className="flex items-center text-gray-600 mt-1">
                              <MapPinIcon className="w-4 h-4 mr-1" />
                              {booking.location}
                            </div>
                          </div>
                          {getStatusBadge(booking.status)}
                        </div>

                        <div className="flex items-center space-x-6 mt-3 text-sm text-gray-600">
                          <div className="flex items-center">
                            <CalendarIcon className="w-4 h-4 mr-1" />
                            {formatDate(booking.startDate)}
                            {booking.startDate !== booking.endDate &&
                              ` - ${formatDate(booking.endDate)}`}
                          </div>
                          <div className="flex items-center">
                            <UsersIcon className="w-4 h-4 mr-1" />
                            {booking.guests} guest
                            {booking.guests !== 1 ? "s" : ""}
                          </div>
                          <div className="flex items-center">
                            <CurrencyDollarIcon className="w-4 h-4 mr-1" />
                            {formatPrice(booking.totalPrice, booking.currency)}
                          </div>
                        </div>

                        <div className="flex items-center mt-2">
                          <span className="text-sm text-gray-500">
                            Booked on {formatDate(booking.bookingDate)}
                          </span>
                          <span className="mx-2 text-gray-300">•</span>
                          <span className="text-sm text-gray-500">
                            Ref: {booking.bookingReference}
                          </span>
                        </div>
                      </div>
                    </div>

                    <button
                      onClick={() => toggleExpanded(booking.id)}
                      className="flex items-center text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      {expandedBooking === booking.id ? (
                        <ChevronUpIcon className="w-5 h-5" />
                      ) : (
                        <ChevronDownIcon className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                </div>

                {/* Expanded Details */}
                {expandedBooking === booking.id && (
                  <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                      {/* Provider Info */}
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">
                          Provider Information
                        </h4>
                        <div className="space-y-2">
                          <p className="text-sm text-gray-600">
                            <span className="font-medium">Name:</span>{" "}
                            {booking.provider.name}
                          </p>
                          <div className="flex items-center">
                            <div className="flex items-center mr-2">
                              {[...Array(5)].map((_, i) => (
                                <StarIcon
                                  key={i}
                                  className={`w-4 h-4 ${
                                    i < Math.floor(booking.provider.rating)
                                      ? "text-yellow-400 fill-current"
                                      : "text-gray-300"
                                  }`}
                                />
                              ))}
                            </div>
                            <span className="text-sm text-gray-600">
                              {booking.provider.rating} (
                              {booking.provider.reviews} reviews)
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Contact Info */}
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">
                          Contact Information
                        </h4>
                        <div className="space-y-2">
                          <p className="text-sm text-gray-600">
                            <span className="font-medium">Phone:</span>{" "}
                            <a
                              href={`tel:${booking.contactInfo.phone}`}
                              className="text-blue-600 hover:underline"
                            >
                              {booking.contactInfo.phone}
                            </a>
                          </p>
                          <p className="text-sm text-gray-600">
                            <span className="font-medium">Email:</span>{" "}
                            <a
                              href={`mailto:${booking.contactInfo.email}`}
                              className="text-blue-600 hover:underline"
                            >
                              {booking.contactInfo.email}
                            </a>
                          </p>
                        </div>
                      </div>

                      {/* Booking Details */}
                      <div>
                        <h4 className="font-medium text-gray-900 mb-3">
                          Booking Details
                        </h4>
                        <div className="space-y-2">
                          <p className="text-sm text-gray-600">
                            <span className="font-medium">Reference:</span>{" "}
                            {booking.bookingReference}
                          </p>
                          <p className="text-sm text-gray-600">
                            <span className="font-medium">Booked on:</span>{" "}
                            {formatDate(booking.bookingDate)}
                          </p>
                          <p className="text-sm text-gray-600">
                            <span className="font-medium">Type:</span>{" "}
                            {booking.type === "tour"
                              ? "Tour Experience"
                              : "Accommodation"}
                          </p>
                          <p className="text-sm text-gray-600">
                            <span className="font-medium">Status:</span>{" "}
                            <span
                              className={`px-2 py-1 rounded-full text-xs font-medium ${
                                statusConfig[booking.status].color
                              }`}
                            >
                              {statusConfig[booking.status].label}
                            </span>
                          </p>
                        </div>
                      </div>

                      {/* Cancellation Policy */}
                      {booking.cancellationPolicy && (
                        <div className="lg:col-span-2">
                          <h4 className="font-medium text-gray-900 mb-2">
                            Cancellation Policy
                          </h4>
                          <p className="text-sm text-gray-600 bg-white p-3 rounded-lg border">
                            {booking.cancellationPolicy}
                          </p>
                        </div>
                      )}

                      {/* Special Requests */}
                      {booking.specialRequests && (
                        <div className="lg:col-span-1">
                          <h4 className="font-medium text-gray-900 mb-2">
                            Special Requests
                          </h4>
                          <p className="text-sm text-gray-600 bg-white p-3 rounded-lg border">
                            {booking.specialRequests}
                          </p>
                        </div>
                      )}

                      {/* Payment Information */}
                      <div className="lg:col-span-3">
                        <h4 className="font-medium text-gray-900 mb-3">
                          Payment Information
                        </h4>
                        <div className="bg-white p-4 rounded-lg border">
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                              <p className="text-sm text-gray-500">
                                Total Amount
                              </p>
                              <p className="text-lg font-semibold text-gray-900">
                                {formatPrice(
                                  booking.totalPrice,
                                  booking.currency
                                )}
                              </p>
                            </div>
                            <div>
                              <p className="text-sm text-gray-500">
                                Payment Status
                              </p>
                              <p className="text-sm font-medium text-green-600">
                                Paid in Full
                              </p>
                            </div>
                            <div>
                              <p className="text-sm text-gray-500">
                                Payment Method
                              </p>
                              <p className="text-sm font-medium text-gray-900">
                                Credit Card
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-wrap gap-3 mt-6 pt-4 border-t border-gray-200">
                      <button
                        onClick={() =>
                          setExpandedBooking(
                            expandedBooking === booking.id ? null : booking.id
                          )
                        }
                        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
                      >
                        <ChevronUpIcon className="w-4 h-4 mr-2" />
                        {expandedBooking === booking.id
                          ? "Hide Details"
                          : "View Details"}
                      </button>

                      {booking.status === "completed" && (
                        <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center">
                          <StarIcon className="w-4 h-4 mr-2" />
                          Leave Review
                        </button>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
