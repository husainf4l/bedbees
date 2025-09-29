"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  HeartIcon,
  MapPinIcon,
  BuildingOfficeIcon,
  WifiIcon,
  TruckIcon,
  TvIcon,
  HomeIcon,
  UsersIcon,
  StarIcon,
} from "@heroicons/react/24/outline";
import {
  HeartIcon as HeartSolidIcon,
  StarIcon as StarSolidIcon,
} from "@heroicons/react/24/solid";
import { AccommodationCardProps } from "@/types/common";

const getAmenityIcon = (amenity: string) => {
  const iconMap: { [key: string]: React.ReactElement } = {
    WiFi: <WifiIcon className="w-3 h-3" />,
    Parking: <TruckIcon className="w-3 h-3" />,
    TV: <TvIcon className="w-3 h-3" />,
    Kitchen: <HomeIcon className="w-3 h-3" />,
    Pool: <HomeIcon className="w-3 h-3" />,
    Spa: <HomeIcon className="w-3 h-3" />,
    "Beach Access": <HomeIcon className="w-3 h-3" />,
    "Room Service": <HomeIcon className="w-3 h-3" />,
    "Ocean View": <HomeIcon className="w-3 h-3" />,
    Gym: <HomeIcon className="w-3 h-3" />,
    "Rooftop Bar": <HomeIcon className="w-3 h-3" />,
    "Business Center": <HomeIcon className="w-3 h-3" />,
    Concierge: <HomeIcon className="w-3 h-3" />,
    Fireplace: <HomeIcon className="w-3 h-3" />,
    "Hot Tub": <HomeIcon className="w-3 h-3" />,
    "Mountain Views": <HomeIcon className="w-3 h-3" />,
    "Hiking Trails": <HomeIcon className="w-3 h-3" />,
  };
  return iconMap[amenity] || <HomeIcon className="w-3 h-3" />;
};

const renderStars = (rating: number) => {
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 !== 0;
  const stars = [];

  for (let i = 0; i < fullStars; i++) {
    stars.push(<StarSolidIcon key={i} className="w-4 h-4 text-yellow-400" />);
  }

  if (hasHalfStar) {
    stars.push(
      <div key="half" className="relative">
        <StarIcon className="w-4 h-4 text-yellow-400" />
        <div className="absolute inset-0 overflow-hidden w-1/2">
          <StarSolidIcon className="w-4 h-4 text-yellow-400" />
        </div>
      </div>
    );
  }

  const emptyStars = 5 - Math.ceil(rating);
  for (let i = 0; i < emptyStars; i++) {
    stars.push(
      <StarIcon key={`empty-${i}`} className="w-4 h-4 text-gray-300" />
    );
  }

  return stars;
};

export default function AccommodationCard({
  apartments,
}: AccommodationCardProps) {
  const [isWishlisted, setIsWishlisted] = useState<Set<string>>(new Set());

  const toggleWishlist = (apartmentId: string) => {
    setIsWishlisted((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(apartmentId)) {
        newSet.delete(apartmentId);
      } else {
        newSet.add(apartmentId);
      }
      return newSet;
    });
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {apartments.map((apartment) => (
        <div
          key={apartment.id}
          className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 cursor-pointer group"
          onClick={() =>
            (window.location.href = `/accommodations/${apartment.id}`)
          }
        >
          {/* Apartment Image */}
          <div className="relative h-48">
            <Image
              src={
                apartment.images && apartment.images.length > 0
                  ? apartment.images[0]
                  : "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjI0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjRjNGNEY2Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OTk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIEltYWdlIEF2YWlsYWJsZTwvdGV4dD48L3N2Zz4="
              }
              alt={apartment.title}
              fill
              className="object-cover"
            />
            <button
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                toggleWishlist(apartment.id);
              }}
              className="absolute top-4 right-4 p-2 bg-white/80 backdrop-blur-sm rounded-full hover:bg-white transition-colors z-10"
            >
              {isWishlisted.has(apartment.id) ? (
                <HeartSolidIcon className="w-5 h-5 text-red-500" />
              ) : (
                <HeartIcon className="w-5 h-5 text-gray-600" />
              )}
            </button>

            {/* Image Gallery Indicator */}
            {apartment.images && apartment.images.length > 1 && (
              <button
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  // Could implement image gallery modal here
                  console.log("View gallery for", apartment.title);
                }}
                className="absolute bottom-4 right-4 px-3 py-1 bg-black/60 backdrop-blur-sm text-white text-xs rounded-full hover:bg-black/80 transition-colors z-10"
              >
                📷 {apartment.images.length}
              </button>
            )}
          </div>

          {/* Apartment Details */}
          <div className="p-6">
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-xl font-semibold text-gray-900">
                {apartment.title}
              </h3>
              <div className="text-right">
                <div className="text-lg font-bold text-green-600">
                  ${(apartment.basePrice / 100).toFixed(0)}
                </div>
                <div className="text-sm text-gray-500">per night</div>
              </div>
            </div>

            {/* Rating and Reviews */}
            {apartment.rating && (
              <div className="flex items-center mb-3">
                <div className="flex items-center mr-2">
                  {renderStars(apartment.rating)}
                </div>
                <span className="text-sm font-medium text-gray-900 mr-1">
                  {apartment.rating.toFixed(1)}
                </span>
                {apartment.reviewCount && (
                  <span className="text-sm text-gray-600">
                    ({apartment.reviewCount} reviews)
                  </span>
                )}
              </div>
            )}

            <div className="flex items-center mb-3">
              <MapPinIcon className="w-4 h-4 text-gray-400 mr-1" />
              <span className="text-sm text-gray-600">
                {apartment.city}, {apartment.country}
              </span>
            </div>

            <div className="flex items-center mb-4">
              <div className="flex items-center mr-4">
                <UsersIcon className="w-4 h-4 text-blue-500 mr-1" />
                <span className="text-sm font-medium">
                  Up to {apartment.maxGuests} guests
                </span>
              </div>
              <span className="text-sm text-gray-500">
                Hosted by {apartment.host.name}
              </span>
            </div>

            <div className="flex items-center mb-4 text-sm text-gray-600">
              <BuildingOfficeIcon className="w-4 h-4 mr-1" />
              <span>
                {apartment.bedrooms} bed • {apartment.bathrooms} bath
              </span>
            </div>

            <p className="text-sm text-gray-600 mb-4 line-clamp-2">
              {apartment.description}
            </p>

            {/* Amenities */}
            <div className="flex flex-wrap gap-2 mb-4">
              {apartment.amenities.slice(0, 3).map((amenity) => (
                <div
                  key={amenity}
                  className="flex items-center bg-gray-100 px-2 py-1 rounded-full text-xs text-gray-700"
                >
                  {getAmenityIcon(amenity)}
                  <span className="ml-1">{amenity}</span>
                </div>
              ))}
              {apartment.amenities.length > 3 && (
                <div className="bg-gray-100 px-2 py-1 rounded-full text-xs text-gray-700">
                  +{apartment.amenities.length - 3} more
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <Link
                href={`/accommodations/${apartment.id}`}
                className="flex-1 bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-colors text-center"
              >
                View Details
              </Link>
              <Link
                href={`/accommodations/${apartment.id}#booking`}
                className="px-4 py-2 border border-green-600 text-green-600 hover:bg-green-50 rounded-lg transition-colors font-medium"
              >
                Quick Book
              </Link>
            </div>

            {/* Additional Info */}
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex items-center justify-between text-sm text-gray-600">
                <span>Free cancellation</span>
                <span className="text-green-600 font-medium">
                  Available now
                </span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
