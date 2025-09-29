"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  HeartIcon,
  MapPinIcon,
  ClockIcon,
  UserGroupIcon,
  StarIcon,
  CurrencyDollarIcon,
  LanguageIcon,
  CalendarIcon,
} from "@heroicons/react/24/outline";
import {
  HeartIcon as HeartSolidIcon,
} from "@heroicons/react/24/solid";
import { Tour } from "@/types/tour";

interface TourCardProps {
  tours: Tour[];
}

export default function TourCard({ tours }: TourCardProps) {
  const [isWishlisted, setIsWishlisted] = useState<Set<string>>(new Set());

  const toggleWishlist = (tourId: string) => {
    setIsWishlisted((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(tourId)) {
        newSet.delete(tourId);
      } else {
        newSet.add(tourId);
      }
      return newSet;
    });
  };

  const formatDuration = (minutes: number) => {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
  };

  const getCategoryBadgeColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'share_trip':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'private':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'group':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatCategoryName = (category: string) => {
    return category.replace('_', ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {tours.map((tour) => (
        <div
          key={tour.id}
          className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 cursor-pointer group"
          onClick={() => (window.location.href = `/tours/${tour.id}`)}
        >
          {/* Tour Image */}
          <div className="relative h-48">
            <Image
              src={tour.media?.[0]?.url || "/hero/travelhero.webp"}
              alt={tour.title}
              fill
              className="object-cover"
            />
            <button
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                toggleWishlist(tour.id);
              }}
              className="absolute top-4 right-4 p-2 bg-white/80 backdrop-blur-sm rounded-full hover:bg-white transition-colors z-10"
            >
              {isWishlisted.has(tour.id) ? (
                <HeartSolidIcon className="w-5 h-5 text-red-500" />
              ) : (
                <HeartIcon className="w-5 h-5 text-gray-600" />
              )}
            </button>

            {/* Category Badge */}
            <div className="absolute top-4 left-4">
              <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getCategoryBadgeColor(tour.category)}`}>
                {formatCategoryName(tour.category)}
              </span>
            </div>

            {/* Deal Badges */}
            <div className="absolute bottom-4 left-4 flex gap-2">
              {tour.isEarlyBird && (
                <span className="px-2 py-1 text-xs font-medium bg-orange-100 text-orange-800 rounded-full border border-orange-200">
                  Early Bird
                </span>
              )}
              {tour.isDropIn && (
                <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 rounded-full border border-yellow-200">
                  Drop-in
                </span>
              )}
            </div>
          </div>

          {/* Tour Details */}
          <div className="p-6">
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-xl font-semibold text-gray-900 line-clamp-2">
                {tour.title}
              </h3>
              <div className="text-right ml-2 flex-shrink-0">
                {tour.isPayWhatYouWant ? (
                  <div className="text-lg font-bold text-green-600">
                    Pay What You Want
                  </div>
                ) : (
                  <>
                    <div className="text-lg font-bold text-green-600">
                      ${(tour.basePrice / 100).toFixed(0)}
                    </div>
                    <div className="text-sm text-gray-500">per person</div>
                  </>
                )}
              </div>
            </div>

            <div className="flex items-center mb-3">
              <MapPinIcon className="w-4 h-4 text-gray-400 mr-1" />
              <span className="text-sm text-gray-600">
                {tour.city}, {tour.country}
              </span>
            </div>

            {/* Guide and Rating */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-gray-200 rounded-full mr-2 overflow-hidden">
                  {tour.guide.user.image ? (
                    <Image
                      src={tour.guide.user.image}
                      alt={tour.guide.user.name}
                      width={32}
                      height={32}
                      className="object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-blue-500 flex items-center justify-center text-white text-xs font-medium">
                      {tour.guide.user.name.charAt(0).toUpperCase()}
                    </div>
                  )}
                </div>
                <span className="text-sm text-gray-600">{tour.guide.user.name}</span>
              </div>

              {tour.guide.ratingAvg > 0 && (
                <div className="flex items-center">
                  <StarIcon className="w-4 h-4 text-yellow-400 fill-current mr-1" />
                  <span className="text-sm font-medium">{tour.guide.ratingAvg.toFixed(1)}</span>
                </div>
              )}
            </div>

            {/* Tour Meta */}
            <div className="grid grid-cols-2 gap-3 mb-4 text-sm text-gray-600">
              <div className="flex items-center">
                <ClockIcon className="w-4 h-4 mr-1" />
                <span>{formatDuration(tour.durationMins)}</span>
              </div>
              <div className="flex items-center">
                <UserGroupIcon className="w-4 h-4 mr-1" />
                <span>{tour.minGroup}-{tour.maxGroup} people</span>
              </div>
              <div className="flex items-center">
                <LanguageIcon className="w-4 h-4 mr-1" />
                <span>{tour.language}</span>
              </div>
              {tour.instantBook && (
                <div className="flex items-center text-green-600">
                  <CalendarIcon className="w-4 h-4 mr-1" />
                  <span>Instant Book</span>
                </div>
              )}
            </div>

            <p className="text-sm text-gray-600 mb-4 line-clamp-2">
              {tour.description}
            </p>

            {/* Travel Styles */}
            {tour.travelStyles && tour.travelStyles.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-4">
                {tour.travelStyles.slice(0, 3).map((style) => (
                  <div
                    key={style}
                    className="bg-gray-100 px-2 py-1 rounded-full text-xs text-gray-700"
                  >
                    {style}
                  </div>
                ))}
                {tour.travelStyles.length > 3 && (
                  <div className="bg-gray-100 px-2 py-1 rounded-full text-xs text-gray-700">
                    +{tour.travelStyles.length - 3} more
                  </div>
                )}
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3">
              <Link
                href={`/tours/${tour.id}`}
                className="flex-1 bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-colors text-center"
              >
                View Details
              </Link>
              <Link
                href={`/tours/${tour.id}#booking`}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Book Now
              </Link>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}