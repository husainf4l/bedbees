"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { travelerService } from "@/services/traveler.service";
import { TravelerDashboard } from "@/types/traveler";

export default function Dashboard() {
  const router = useRouter();
  const [dashboardData, setDashboardData] = useState<TravelerDashboard | null>(
    null
  );
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const data = await travelerService.getDashboardDataSafe();
        setDashboardData(data);
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
        // Set empty dashboard data as fallback
        setDashboardData({
          stats: {
            totalTrips: 0,
            upcomingTrips: 0,
            totalSpent: 0,
            favoriteDestinations: 0,
          },
          upcomingBookings: [],
          recentActivity: [],
          favoriteDestinations: [],
          profile: {
            id: "",
            name: "User",
            email: "",
            image: undefined,
            joinedDate: new Date().toISOString(),
            totalTrips: 0,
            reviewsGiven: 0,
            averageRating: 0,
            preferredLanguages: [],
            travelStyles: [],
          },
        });
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!dashboardData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Failed to load dashboard data</p>
      </div>
    );
  }

  const { stats, profile } = dashboardData;

  return (
    <div className="max-w-7xl mx-auto">
      {/* Apple-style Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-light text-gray-900 tracking-tight">
          Welcome back, {profile.name}!
        </h1>
        <p className="text-lg text-gray-500 mt-3 font-light">
          Track your travel adventures and discover new experiences
        </p>
      </div>

      {/* Enhanced Stats cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8 hover:shadow-xl transition-all duration-300 hover:scale-105">
          <div className="flex items-center gap-6">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg">
              <svg
                className="w-8 h-8 text-white"
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
            <div>
              <p className="text-sm font-medium text-gray-500 mb-1">Total Trips</p>
              <p className="text-3xl font-semibold text-gray-900">
                {stats.totalTrips}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8 hover:shadow-xl transition-all duration-300 hover:scale-105">
          <div className="flex items-center gap-6">
            <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg">
              <svg
                className="w-8 h-8 text-white"
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
            <div>
              <p className="text-sm font-medium text-gray-500 mb-1">
                Upcoming Trips
              </p>
              <p className="text-3xl font-semibold text-gray-900">
                {stats.upcomingTrips}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8 hover:shadow-xl transition-all duration-300 hover:scale-105">
          <div className="flex items-center gap-6">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                />
              </svg>
            </div>
            <div>
              <p className="text-sm font-medium text-gray-500 mb-1">
                Favorite Destinations
              </p>
              <p className="text-3xl font-semibold text-gray-900">
                {stats.favoriteDestinations}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Content cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8">
          <h3 className="text-2xl font-medium text-gray-900 mb-6">
            Upcoming Trips
          </h3>
          {dashboardData.upcomingBookings.length > 0 ? (
            <div className="space-y-4">
              {dashboardData.upcomingBookings.map((booking) => (
                <div
                  key={booking.id}
                  className="flex justify-between items-center p-4 bg-gray-50 rounded-2xl border border-gray-100 hover:bg-gray-100 transition-colors"
                >
                  <div>
                    <p className="font-medium text-gray-900 mb-1">
                      {booking.tourTitle}
                    </p>
                    <p className="text-sm text-gray-500">
                      {booking.destination} •{" "}
                      {new Date(booking.startDate).toLocaleDateString()}
                    </p>
                  </div>
                  <span
                    className={`px-3 py-1 text-sm font-medium rounded-full ${
                      booking.status === "confirmed"
                        ? "bg-green-100 text-green-700"
                        : booking.status === "pending"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-blue-100 text-blue-700"
                    }`}
                  >
                    {booking.status.charAt(0).toUpperCase() +
                      booking.status.slice(1)}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <h4 className="text-lg font-medium text-gray-900 mb-2">
                No upcoming trips
              </h4>
              <p className="text-sm text-gray-500 mb-6">
                Start planning your next adventure!
              </p>
              <button
                onClick={() => router.push('/tours')}
                className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium rounded-2xl transition-all duration-200 hover:shadow-lg hover:shadow-blue-200/50 hover:-translate-y-0.5"
              >
                <svg
                  className="w-5 h-5 mr-2"
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
                Browse Tours
              </button>
            </div>
          )}
        </div>

        <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8">
          <h3 className="text-2xl font-medium text-gray-900 mb-6">
            Recent Activity
          </h3>
          {dashboardData.recentActivity.length > 0 ? (
            <div className="space-y-4">
              {dashboardData.recentActivity.slice(0, 4).map((activity) => (
                <div key={activity.id} className="flex items-start gap-4 p-4 bg-gray-50 rounded-2xl border border-gray-100 hover:bg-gray-100 transition-colors">
                  <div
                    className={`flex-shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center ${
                      activity.type === "booking"
                        ? "bg-blue-100"
                        : activity.type === "review"
                        ? "bg-yellow-100"
                        : activity.type === "favorite"
                        ? "bg-red-100"
                        : "bg-green-100"
                    }`}
                  >
                    {activity.type === "booking" && (
                      <svg
                        className="w-6 h-6 text-blue-600"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    )}
                    {activity.type === "review" && (
                      <svg
                        className="w-6 h-6 text-yellow-600"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    )}
                    {activity.type === "favorite" && (
                      <svg
                        className="w-6 h-6 text-red-600"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path
                          fillRule="evenodd"
                          d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                          clipRule="evenodd"
                        />
                      </svg>
                    )}
                    {activity.type === "share" && (
                      <svg
                        className="w-6 h-6 text-green-600"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
                      </svg>
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 mb-1">
                      {activity.title}
                    </p>
                    <p className="text-sm text-gray-500 mb-1">
                      {activity.description}
                    </p>
                    <p className="text-xs text-gray-400">
                      {new Date(activity.timestamp).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg
                  className="w-8 h-8 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <h4 className="text-lg font-medium text-gray-900 mb-2">
                No recent activity
              </h4>
              <p className="text-sm text-gray-500">
                Your travel activities will appear here once you start booking
                tours!
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Favorite Destinations */}
      <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-8">
        <h3 className="text-2xl font-medium text-gray-900 mb-6">
          Your Favorite Destinations
        </h3>
        {dashboardData.favoriteDestinations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {dashboardData.favoriteDestinations.map((destination) => (
              <div
                key={destination.id}
                className="relative group cursor-pointer hover:scale-105 transition-transform duration-200"
              >
                <div className="aspect-w-16 aspect-h-9 rounded-2xl overflow-hidden bg-gray-200 shadow-lg">
                  <div className="w-full h-40 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                    <span className="text-white font-semibold text-xl">
                      {destination.city}
                    </span>
                  </div>
                </div>
                <div className="mt-4">
                  <h4 className="font-medium text-gray-900 mb-1">
                    {destination.city}, {destination.country}
                  </h4>
                  <p className="text-sm text-gray-500">
                    {destination.visitCount} visit
                    {destination.visitCount !== 1 ? "s" : ""}
                    {destination.upcomingTrips > 0 &&
                      ` • ${destination.upcomingTrips} upcoming`}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="w-20 h-20 bg-gradient-to-br from-purple-100 to-pink-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <svg
                className="w-10 h-10 text-purple-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                />
              </svg>
            </div>
            <h4 className="text-xl font-medium text-gray-900 mb-3">
              No favorite destinations yet
            </h4>
            <p className="text-gray-500 mb-8 max-w-md mx-auto">
              Explore amazing destinations and add them to your favorites as
              you travel
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => router.push('/destinations')}
                className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-medium rounded-2xl transition-all duration-200 hover:shadow-lg hover:shadow-blue-200/50 hover:-translate-y-0.5"
              >
                <svg
                  className="w-5 h-5 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
                Explore Destinations
              </button>
              <button
                onClick={() => router.push('/tours')}
                className="inline-flex items-center px-6 py-3 border border-gray-200 text-gray-700 bg-white hover:bg-gray-50 font-medium rounded-2xl transition-all duration-200 hover:shadow-md hover:-translate-y-0.5"
              >
                <svg
                  className="w-5 h-5 mr-2"
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
                Browse Tours
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}