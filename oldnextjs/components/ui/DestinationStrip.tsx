"use client";

import React from "react";
import Image from "next/image";
import { ChevronRightIcon } from "@heroicons/react/24/outline";

interface Destination {
  id: string;
  name: string;
  country: string;
  imageUrl: string;
  activitiesCount: number;
  startingPrice: number;
  isPopular?: boolean;
}

const destinations: Destination[] = [
  {
    id: "1",
    name: "Petra",
    country: "Jordan",
    imageUrl: "/hero/chalets.webp",
    activitiesCount: 120,
    startingPrice: 25,
    isPopular: true,
  },
  {
    id: "2",
    name: "Dubai",
    country: "UAE",
    imageUrl: "/hero/hotel.webp",
    activitiesCount: 450,
    startingPrice: 35,
    isPopular: true,
  },
  {
    id: "3",
    name: "Cairo",
    country: "Egypt",
    imageUrl: "/hero/villa.webp",
    activitiesCount: 200,
    startingPrice: 20,
  },
  {
    id: "4",
    name: "Beirut",
    country: "Lebanon",
    imageUrl: "/hero/resort.webp",
    activitiesCount: 95,
    startingPrice: 30,
  },
  {
    id: "5",
    name: "Doha",
    country: "Qatar",
    imageUrl: "/hero/motels.webp",
    activitiesCount: 75,
    startingPrice: 45,
  },
  {
    id: "6",
    name: "Riyadh",
    country: "Saudi Arabia",
    imageUrl: "/hero/caravan.webp",
    activitiesCount: 180,
    startingPrice: 42,
    isPopular: true,
  },
  {
    id: "7",
    name: "Kuwait City",
    country: "Kuwait",
    imageUrl: "/hero/travelhero.webp",
    activitiesCount: 90,
    startingPrice: 35,
  },
  {
    id: "8",
    name: "Manama",
    country: "Bahrain",
    imageUrl: "/hero/apartment.webp",
    activitiesCount: 65,
    startingPrice: 28,
  },
  {
    id: "9",
    name: "Muscat",
    country: "Oman",
    imageUrl: "/hero/resort.webp",
    activitiesCount: 110,
    startingPrice: 48,
  },
  {
    id: "10",
    name: "Istanbul",
    country: "Turkey",
    imageUrl: "/hero/chalets.webp",
    activitiesCount: 380,
    startingPrice: 18,
    isPopular: true,
  },
  {
    id: "11",
    name: "Damascus",
    country: "Syria",
    imageUrl: "/hero/treehouses.webp",
    activitiesCount: 70,
    startingPrice: 15,
  },
  {
    id: "12",
    name: "Baghdad",
    country: "Iraq",
    imageUrl: "/hero/motels.webp",
    activitiesCount: 85,
    startingPrice: 20,
  },
  {
    id: "13",
    name: "Sana'a",
    country: "Yemen",
    imageUrl: "/hero/hostels.webp",
    activitiesCount: 45,
    startingPrice: 25,
  },
  {
    id: "14",
    name: "Ramallah",
    country: "Palestine",
    imageUrl: "/hero/caravan.webp",
    activitiesCount: 55,
    startingPrice: 12,
  },
];

export default function DestinationStrip() {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Popular Destinations
            </h2>
            <p className="text-lg text-gray-600">
              Discover amazing experiences in these trending locations
            </p>
          </div>
          <button className="flex items-center text-orange-600 hover:text-orange-700 font-semibold transition-colors group">
            View all destinations
            <ChevronRightIcon className="w-5 h-5 ml-1 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>

        {/* Destinations Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {destinations.map((destination, index) => (
            <div
              key={destination.id}
              className={`group cursor-pointer transform transition-all duration-300 hover:scale-105 hover:shadow-xl ${
                index < 4 ? "" : "hidden lg:block"
              }`}
            >
              <div className="relative overflow-hidden rounded-2xl bg-white shadow-lg">
                {/* Popular Badge */}
                {destination.isPopular && (
                  <div className="absolute top-3 left-3 z-10">
                    <span className="bg-orange-500 text-white px-3 py-1 text-sm font-semibold rounded-full shadow-lg">
                      Popular
                    </span>
                  </div>
                )}

                {/* Destination Image */}
                <div className="relative h-48 overflow-hidden">
                  <Image
                    src={destination.imageUrl}
                    alt={`${destination.name}, ${destination.country}`}
                    fill
                    className="object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
                </div>

                {/* Content */}
                <div className="p-5">
                  <div className="mb-3">
                    <h3 className="text-xl font-bold text-gray-900 mb-1 group-hover:text-orange-600 transition-colors">
                      {destination.name}
                    </h3>
                    <p className="text-gray-600 font-medium">
                      {destination.country}
                    </p>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-500 mb-1">
                        {destination.activitiesCount}+ activities
                      </p>
                      <p className="text-lg font-bold text-gray-900">
                        From ${destination.startingPrice}
                      </p>
                    </div>
                    <div className="bg-orange-50 p-3 rounded-full group-hover:bg-orange-100 transition-colors">
                      <ChevronRightIcon className="w-5 h-5 text-orange-600 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </div>
                </div>

                {/* Hover Overlay */}
                <div className="absolute inset-0 bg-orange-500/0 group-hover:bg-orange-500/10 transition-all duration-300 rounded-2xl" />
              </div>
            </div>
          ))}
        </div>

        {/* Mobile View All Button */}
        <div className="mt-8 text-center lg:hidden">
          <button className="bg-orange-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-orange-700 transition-colors shadow-lg">
            Explore All Destinations
          </button>
        </div>
      </div>
    </section>
  );
}
