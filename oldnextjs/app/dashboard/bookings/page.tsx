"use client";

import { useState } from "react";
import {
  CalendarIcon,
  MapPinIcon,
  UsersIcon,
  ClockIcon,
  PhoneIcon,
  EnvelopeIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  EyeIcon,
  DocumentTextIcon,
  StarIcon,
} from "@heroicons/react/24/outline";

interface Booking {
  id: string;
  title: string;
  type: "tour" | "accommodation" | "activity";
  status: "confirmed" | "pending" | "cancelled" | "completed";
  date: string;
  time: string;
  duration: string;
  location: string;
  price: number;
  currency: string;
  guests: number;
  bookingReference: string;
  createdAt: string;
  image: string;
  description: string;
  provider: {
    name: string;
    phone: string;
    email: string;
  };
  cancellationPolicy: string;
  amenities?: string[];
  rating?: number;
  reviews?: number;
}

// Mock data for demonstration
const mockBookings: Booking[] = [
  {
    id: "1",
    title: "Petra Day Trip from Amman",
    type: "tour",
    status: "confirmed",
    date: "2024-12-15",
    time: "08:00",
    duration: "10 hours",
    location: "Petra, Jordan",
    price: 120,
    currency: "USD",
    guests: 2,
    bookingReference: "BK-2024-001",
    createdAt: "2024-11-20",
    image: "/tours/petra.jpg",
    description:
      "Explore the ancient city of Petra with expert guides. Visit the Treasury, Royal Tombs, and hike to the Monastery.",
    provider: {
      name: "Jordan Adventures",
      phone: "+962 6 123 4567",
      email: "info@jordanadventures.com",
    },
    cancellationPolicy: "Free cancellation up to 24 hours before the tour",
    amenities: [
      "Professional Guide",
      "Transportation",
      "Entry Tickets",
      "Lunch",
    ],
    rating: 4.8,
    reviews: 245,
  },
  {
    id: "2",
    title: "Luxury Hotel Suite - Dead Sea Resort",
    type: "accommodation",
    status: "pending",
    date: "2024-12-20",
    time: "15:00",
    duration: "3 nights",
    location: "Dead Sea, Jordan",
    price: 450,
    currency: "USD",
    guests: 2,
    bookingReference: "BK-2024-002",
    createdAt: "2024-11-25",
    image: "/hotels/dead-sea.jpg",
    description:
      "Luxurious suite overlooking the Dead Sea with private balcony, spa access, and all amenities.",
    provider: {
      name: "Dead Sea Luxury Resort",
      phone: "+962 5 123 4567",
      email: "reservations@deadsearesort.com",
    },
    cancellationPolicy: "Free cancellation up to 48 hours before check-in",
    amenities: ["Spa Access", "Private Balcony", "WiFi", "Pool", "Breakfast"],
    rating: 4.9,
    reviews: 189,
  },
  {
    id: "3",
    title: "Desert Safari & Stargazing",
    type: "activity",
    status: "completed",
    date: "2024-11-10",
    time: "16:00",
    duration: "6 hours",
    location: "Wadi Rum, Jordan",
    price: 85,
    currency: "USD",
    guests: 4,
    bookingReference: "BK-2024-003",
    createdAt: "2024-10-15",
    image: "/activities/desert-safari.jpg",
    description:
      "Experience the magic of Wadi Rum desert with camel rides, traditional dinner, and stargazing.",
    provider: {
      name: "Wadi Rum Adventures",
      phone: "+962 3 123 4567",
      email: "info@wadirumadventures.com",
    },
    cancellationPolicy: "Free cancellation up to 12 hours before the activity",
    amenities: [
      "Camel Ride",
      "Traditional Dinner",
      "Stargazing",
      "Transportation",
    ],
    rating: 4.7,
    reviews: 156,
  },
];

const statusConfig = {
  confirmed: {
    color: "text-green-700 bg-green-100",
    icon: CheckCircleIcon,
    label: "Confirmed",
  },
  pending: {
    color: "text-yellow-700 bg-yellow-100",
    icon: ExclamationTriangleIcon,
    label: "Pending",
  },
  cancelled: {
    color: "text-red-700 bg-red-100",
    icon: XCircleIcon,
    label: "Cancelled",
  },
  completed: {
    color: "text-blue-700 bg-blue-100",
    icon: CheckCircleIcon,
    label: "Completed",
  },
};

export default function Bookings() {
  const [selectedBooking, setSelectedBooking] = useState<Booking | null>(null);
  const [filter, setFilter] = useState<string>("all");

  const filteredBookings = mockBookings.filter((booking) => {
    if (filter === "all") return true;
    return booking.status === filter;
  });

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const formatPrice = (price: number, currency: string) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency,
    }).format(price);
  };

  return (
    <div className="max-w-7xl mx-auto">
      {/* Apple-style Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-light text-gray-900 tracking-tight">
          My Bookings
        </h1>
        <p className="text-lg text-gray-500 mt-3 font-light">
          Manage your travel bookings and reservations
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="mb-8">
        <div className="flex space-x-1 bg-gray-100 rounded-2xl p-1 w-fit">
          {[
            { key: "all", label: "All Bookings" },
            { key: "confirmed", label: "Confirmed" },
            { key: "pending", label: "Pending" },
            { key: "completed", label: "Completed" },
            { key: "cancelled", label: "Cancelled" },
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setFilter(tab.key)}
              className={`px-6 py-2 rounded-xl font-medium transition-all duration-200 ${
                filter === tab.key
                  ? "bg-white text-blue-600 shadow-sm"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Bookings Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredBookings.map((booking) => {
          const StatusIcon = statusConfig[booking.status].icon;

          return (
            <div
              key={booking.id}
              className="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer"
              onClick={() => setSelectedBooking(booking)}
            >
              {/* Booking Image */}
              <div className="relative h-48">
                <div
                  className="w-full h-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center"
                  style={{
                    backgroundImage: `url(${booking.image})`,
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                  }}
                >
                  <div className="absolute inset-0 bg-black/20"></div>
                </div>

                {/* Status Badge */}
                <div
                  className={`absolute top-4 right-4 px-3 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${
                    statusConfig[booking.status].color
                  }`}
                >
                  <StatusIcon className="w-3 h-3" />
                  {statusConfig[booking.status].label}
                </div>

                {/* Type Badge */}
                <div className="absolute top-4 left-4 px-3 py-1 bg-white/90 backdrop-blur-sm rounded-full text-xs font-medium text-gray-800 capitalize">
                  {booking.type}
                </div>
              </div>

              {/* Booking Content */}
              <div className="p-6">
                <h3 className="text-xl font-medium text-gray-900 mb-2 line-clamp-2">
                  {booking.title}
                </h3>

                {/* Rating */}
                {booking.rating && (
                  <div className="flex items-center gap-1 mb-3">
                    <StarIcon className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    <span className="text-sm font-medium">
                      {booking.rating}
                    </span>
                    <span className="text-sm text-gray-500">
                      ({booking.reviews} reviews)
                    </span>
                  </div>
                )}

                {/* Key Details */}
                <div className="space-y-2 mb-4">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <CalendarIcon className="w-4 h-4" />
                    <span>{formatDate(booking.date)}</span>
                  </div>

                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <ClockIcon className="w-4 h-4" />
                    <span>
                      {booking.time} • {booking.duration}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <MapPinIcon className="w-4 h-4" />
                    <span>{booking.location}</span>
                  </div>

                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <UsersIcon className="w-4 h-4" />
                    <span>
                      {booking.guests}{" "}
                      {booking.guests === 1 ? "Guest" : "Guests"}
                    </span>
                  </div>
                </div>

                {/* Price and Reference */}
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-2xl font-semibold text-gray-900">
                      {formatPrice(booking.price, booking.currency)}
                    </div>
                    <div className="text-xs text-gray-500">
                      Ref: {booking.bookingReference}
                    </div>
                  </div>

                  <button className="p-2 bg-blue-100 text-blue-600 rounded-full hover:bg-blue-200 transition-colors">
                    <EyeIcon className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Detailed Booking Modal */}
      {selectedBooking && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="sticky top-0 bg-white rounded-t-3xl border-b border-gray-100 p-6">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-medium text-gray-900">
                  Booking Details
                </h2>
                <button
                  onClick={() => setSelectedBooking(null)}
                  className="p-2 bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200 transition-colors"
                >
                  <XCircleIcon className="w-6 h-6" />
                </button>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6 space-y-8">
              {/* Booking Overview */}
              <div>
                <h3 className="text-xl font-medium mb-4">
                  {selectedBooking.title}
                </h3>
                <p className="text-gray-600 mb-4">
                  {selectedBooking.description}
                </p>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 rounded-2xl p-4">
                    <div className="text-sm text-gray-600 mb-1">Status</div>
                    <div
                      className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${
                        statusConfig[selectedBooking.status].color
                      }`}
                    >
                      {(() => {
                        const StatusIcon =
                          statusConfig[selectedBooking.status].icon;
                        return <StatusIcon className="w-4 h-4" />;
                      })()}
                      {statusConfig[selectedBooking.status].label}
                    </div>
                  </div>

                  <div className="bg-gray-50 rounded-2xl p-4">
                    <div className="text-sm text-gray-600 mb-1">
                      Total Price
                    </div>
                    <div className="text-xl font-semibold text-gray-900">
                      {formatPrice(
                        selectedBooking.price,
                        selectedBooking.currency
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Trip Details */}
              <div>
                <h4 className="text-lg font-medium mb-4">Trip Details</h4>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <CalendarIcon className="w-5 h-5 text-gray-400" />
                    <div>
                      <div className="font-medium">
                        {formatDate(selectedBooking.date)}
                      </div>
                      <div className="text-sm text-gray-600">
                        {selectedBooking.time} • {selectedBooking.duration}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <MapPinIcon className="w-5 h-5 text-gray-400" />
                    <div className="font-medium">
                      {selectedBooking.location}
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <UsersIcon className="w-5 h-5 text-gray-400" />
                    <div className="font-medium">
                      {selectedBooking.guests}{" "}
                      {selectedBooking.guests === 1 ? "Guest" : "Guests"}
                    </div>
                  </div>
                </div>
              </div>

              {/* Amenities */}
              {selectedBooking.amenities && (
                <div>
                  <h4 className="text-lg font-medium mb-4">
                    What&apos;s Included
                  </h4>
                  <div className="grid grid-cols-2 gap-2">
                    {selectedBooking.amenities.map((amenity, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <CheckCircleIcon className="w-4 h-4 text-green-500" />
                        <span className="text-sm">{amenity}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Provider Information */}
              <div>
                <h4 className="text-lg font-medium mb-4">
                  Provider Information
                </h4>
                <div className="bg-gray-50 rounded-2xl p-4 space-y-3">
                  <div className="font-medium">
                    {selectedBooking.provider.name}
                  </div>

                  <div className="flex items-center gap-3">
                    <PhoneIcon className="w-4 h-4 text-gray-400" />
                    <span className="text-sm">
                      {selectedBooking.provider.phone}
                    </span>
                  </div>

                  <div className="flex items-center gap-3">
                    <EnvelopeIcon className="w-4 h-4 text-gray-400" />
                    <span className="text-sm">
                      {selectedBooking.provider.email}
                    </span>
                  </div>
                </div>
              </div>

              {/* Booking Information */}
              <div>
                <h4 className="text-lg font-medium mb-4">
                  Booking Information
                </h4>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Booking Reference</span>
                    <span className="font-medium">
                      {selectedBooking.bookingReference}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-gray-600">Booking Date</span>
                    <span className="font-medium">
                      {formatDate(selectedBooking.createdAt)}
                    </span>
                  </div>

                  <div className="flex justify-between">
                    <span className="text-gray-600">Cancellation Policy</span>
                    <span className="font-medium text-right max-w-xs">
                      {selectedBooking.cancellationPolicy}
                    </span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3 pt-4">
                <button className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-2xl font-medium transition-colors flex items-center justify-center gap-2">
                  <DocumentTextIcon className="w-5 h-5" />
                  View Voucher
                </button>

                <button className="flex-1 border border-gray-200 text-gray-700 py-3 rounded-2xl font-medium hover:bg-gray-50 transition-colors flex items-center justify-center gap-2">
                  <PhoneIcon className="w-5 h-5" />
                  Contact Provider
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {filteredBookings.length === 0 && (
        <div className="text-center py-16">
          <CalendarIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-medium text-gray-900 mb-2">
            No bookings found
          </h3>
          <p className="text-gray-500">
            {filter === "all"
              ? "You don't have any bookings yet."
              : `No ${filter} bookings found.`}
          </p>
        </div>
      )}
    </div>
  );
}
