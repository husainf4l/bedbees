"use client";

import React from "react";
import {
  HomeIcon,
  BuildingOfficeIcon,
  BuildingOffice2Icon,
  HomeModernIcon,
  BeakerIcon,
  MapIcon,
  TruckIcon,
  CubeIcon,
} from "@heroicons/react/24/outline";

interface PropertyType {
  id: string;
  name: string;
  icon: React.ReactNode;
  description: string;
  count: number;
  imageGradient: string;
  popularityBadge?: string;
}

const propertyTypes: PropertyType[] = [
  {
    id: "hotels",
    name: "Hotels",
    icon: <BuildingOfficeIcon className="w-8 h-8" />,
    description: "Comfortable stays with amenities",
    count: 2847,
    imageGradient: "from-blue-500 to-blue-600",
    popularityBadge: "Most Popular",
  },
  {
    id: "apartments",
    name: "Apartments",
    icon: <HomeModernIcon className="w-8 h-8" />,
    description: "Self-catering accommodations",
    count: 1923,
    imageGradient: "from-green-500 to-green-600",
  },
  {
    id: "villas",
    name: "Villas",
    icon: <HomeIcon className="w-8 h-8" />,
    description: "Luxury private homes",
    count: 654,
    imageGradient: "from-purple-500 to-purple-600",
    popularityBadge: "Luxury",
  },
  {
    id: "resorts",
    name: "Resorts",
    icon: <BeakerIcon className="w-8 h-8" />,
    description: "All-inclusive experiences",
    count: 432,
    imageGradient: "from-orange-500 to-orange-600",
  },
  {
    id: "hostels",
    name: "Hostels",
    icon: <BuildingOffice2Icon className="w-8 h-8" />,
    description: "Budget-friendly shared stays",
    count: 287,
    imageGradient: "from-teal-500 to-teal-600",
    popularityBadge: "Budget",
  },
  {
    id: "guesthouses",
    name: "Guesthouses",
    icon: <HomeIcon className="w-8 h-8" />,
    description: "Cozy local experiences",
    count: 198,
    imageGradient: "from-pink-500 to-pink-600",
  },
  {
    id: "camping",
    name: "Camping",
    icon: <MapIcon className="w-8 h-8" />,
    description: "Outdoor adventures",
    count: 156,
    imageGradient: "from-emerald-500 to-emerald-600",
  },
  {
    id: "unique",
    name: "Unique Stays",
    icon: <CubeIcon className="w-8 h-8" />,
    description: "Unusual & memorable places",
    count: 89,
    imageGradient: "from-indigo-500 to-indigo-600",
    popularityBadge: "Trending",
  },
];

export default function PropertyTypeGrid() {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Browse by Property Type
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            From budget hostels to luxury villas, find the perfect accommodation
            type for your next adventure
          </p>
        </div>

        {/* Property Types Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {propertyTypes.map((property, index) => (
            <div
              key={property.id}
              className={`group relative cursor-pointer bg-white rounded-2xl shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 overflow-hidden ${
                index === 0 ? "md:col-span-2" : ""
              } ${index === 2 ? "md:col-span-2" : ""}`}
            >
              {/* Background Gradient */}
              <div
                className={`absolute inset-0 bg-gradient-to-br ${property.imageGradient} opacity-90 group-hover:opacity-100 transition-opacity duration-300`}
              />

              {/* Popular Badge */}
              {property.popularityBadge && (
                <div className="absolute top-4 right-4 z-10">
                  <span className="bg-white/20 backdrop-blur-sm text-white px-3 py-1 text-xs font-bold rounded-full border border-white/30">
                    {property.popularityBadge}
                  </span>
                </div>
              )}

              {/* Content */}
              <div className="relative z-10 p-6 h-full flex flex-col justify-between min-h-[180px]">
                <div>
                  {/* Icon */}
                  <div className="text-white/90 group-hover:text-white transition-colors duration-300 mb-4">
                    {property.icon}
                  </div>

                  {/* Title & Description */}
                  <div className="mb-4">
                    <h3 className="text-xl font-bold text-white mb-2 group-hover:scale-105 transition-transform duration-300">
                      {property.name}
                    </h3>
                    <p className="text-white/80 text-sm leading-relaxed">
                      {property.description}
                    </p>
                  </div>
                </div>

                {/* Count & Arrow */}
                <div className="flex items-center justify-between">
                  <div className="text-white/90">
                    <span className="text-2xl font-bold block">
                      {property.count.toLocaleString()}
                    </span>
                    <span className="text-sm text-white/70">properties</span>
                  </div>
                  <div className="transform group-hover:translate-x-2 group-hover:scale-110 transition-all duration-300">
                    <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center backdrop-blur-sm">
                      <svg
                        className="w-4 h-4 text-white"
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
                    </div>
                  </div>
                </div>
              </div>

              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

              {/* Decorative Elements */}
              <div className="absolute -top-12 -right-12 w-24 h-24 bg-white/10 rounded-full group-hover:scale-125 transition-transform duration-500" />
              <div className="absolute -bottom-8 -left-8 w-16 h-16 bg-white/5 rounded-full group-hover:scale-150 transition-transform duration-700" />
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-12">
          <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Still Not Sure What You Want?
            </h3>
            <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
              Use our smart search to find accommodations based on your specific
              needs, budget, and travel style.
            </p>
            <button className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-200 hover:shadow-lg hover:scale-105">
              Start Smart Search
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
