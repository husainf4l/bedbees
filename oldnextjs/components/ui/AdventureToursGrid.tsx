"use client";

import React from "react";
import Image from "next/image";
import Link from "next/link";
import {
  StarIcon,
  ClockIcon,
  UsersIcon,
  ChevronRightIcon,
} from "@heroicons/react/24/outline";
import { StarIcon as StarSolidIcon } from "@heroicons/react/24/solid";

interface AdventureTour {
  id: string;
  title: string;
  location: string;
  imageUrl: string;
  rating: number;
  reviewCount: number;
  duration: string;
  price: number;
  adventureType: string;
  difficulty: "Beginner" | "Intermediate" | "Advanced" | "Expert";
  maxGroupSize: number;
  highlights: string[];
  adrenalineLevel: "Low" | "Medium" | "High" | "Extreme";
}

const adventureTours: AdventureTour[] = [
  {
    id: "1",
    title: "Wadi Rum 4WD Desert Safari & Rock Climbing",
    location: "Wadi Rum, Jordan",
    imageUrl: "/hero/apartment.webp",
    rating: 4.9,
    reviewCount: 1247,
    duration: "8 hours",
    price: 145,
    adventureType: "Desert Adventure",
    difficulty: "Intermediate",
    maxGroupSize: 8,
    highlights: [
      "4WD dune bashing",
      "Rock climbing",
      "Sunset viewing",
      "Bedouin camp",
    ],
    adrenalineLevel: "High",
  },
  {
    id: "2",
    title: "Dubai Skydiving Over Palm Jumeirah",
    location: "Dubai, UAE",
    imageUrl: "/hero/hotel.webp",
    rating: 4.8,
    reviewCount: 892,
    duration: "4 hours",
    price: 599,
    adventureType: "Extreme Sports",
    difficulty: "Beginner",
    maxGroupSize: 12,
    highlights: [
      "Tandem skydive",
      "13,000ft altitude",
      "Professional instructor",
      "Video package",
    ],
    adrenalineLevel: "Extreme",
  },
  {
    id: "3",
    title: "Dead Sea Canyoning & Hot Springs",
    location: "Dead Sea, Jordan",
    imageUrl: "/hero/treehouses.webp",
    rating: 4.7,
    reviewCount: 634,
    duration: "6 hours",
    price: 125,
    adventureType: "Water Adventure",
    difficulty: "Intermediate",
    maxGroupSize: 10,
    highlights: [
      "Canyon rappelling",
      "Natural pools",
      "Hot springs",
      "Waterfall climbing",
    ],
    adrenalineLevel: "High",
  },
  {
    id: "4",
    title: "Sinai Mountain Hiking & Sunrise Trek",
    location: "Mount Sinai, Egypt",
    imageUrl: "/hero/villa.webp",
    rating: 4.6,
    reviewCount: 743,
    duration: "12 hours",
    price: 95,
    adventureType: "Mountain Trekking",
    difficulty: "Advanced",
    maxGroupSize: 15,
    highlights: [
      "Night trek",
      "Sunrise summit",
      "Historical sites",
      "Bedouin guide",
    ],
    adrenalineLevel: "Medium",
  },
  {
    id: "5",
    title: "Red Sea Scuba Diving Adventure",
    location: "Aqaba, Jordan",
    imageUrl: "/hero/resort.webp",
    rating: 4.8,
    reviewCount: 1156,
    duration: "5 hours",
    price: 185,
    adventureType: "Water Sports",
    difficulty: "Intermediate",
    maxGroupSize: 6,
    highlights: [
      "2 dive sites",
      "Coral reef exploration",
      "Marine life",
      "PADI certified",
    ],
    adrenalineLevel: "Medium",
  },
  {
    id: "6",
    title: "Lebanon Paragliding & Mountain Views",
    location: "Harissa, Lebanon",
    imageUrl: "/hero/chalets.webp",
    rating: 4.5,
    reviewCount: 421,
    duration: "3 hours",
    price: 220,
    adventureType: "Air Sports",
    difficulty: "Beginner",
    maxGroupSize: 4,
    highlights: [
      "Tandem flight",
      "Mountain views",
      "Mediterranean coast",
      "GoPro footage",
    ],
    adrenalineLevel: "High",
  },
];

export default function AdventureToursGrid() {
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

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "Beginner":
        return "bg-green-100 text-green-800";
      case "Intermediate":
        return "bg-yellow-100 text-yellow-800";
      case "Advanced":
        return "bg-orange-100 text-orange-800";
      case "Expert":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getAdrenalineColor = (level: string) => {
    switch (level) {
      case "Low":
        return "bg-blue-500";
      case "Medium":
        return "bg-yellow-500";
      case "High":
        return "bg-orange-500";
      case "Extreme":
        return "bg-red-500";
      default:
        return "bg-gray-500";
    }
  };

  return (
    <section className="py-16 bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="flex items-center justify-between mb-12">
          <div>
            <div className="flex items-center mb-4">
              <span className="text-4xl mr-3">🏔️</span>
              <h2 className="text-3xl font-bold text-gray-900">
                Adventure Tours
              </h2>
            </div>
            <p className="text-lg text-gray-600 max-w-2xl">
              Push your limits with thrilling adventures and adrenaline-pumping
              experiences
            </p>
          </div>
          <button className="flex items-center text-blue-600 hover:text-blue-700 font-semibold transition-colors group">
            View all adventures
            <ChevronRightIcon className="w-5 h-5 ml-1 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>

        {/* Adventure Tours Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {adventureTours.map((tour, index) => (
            <div
              key={tour.id}
              className={`group cursor-pointer bg-white rounded-2xl shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 overflow-hidden ${
                index === 0 ? "lg:col-span-2" : ""
              }`}
            >
              {/* Image Container */}
              <div
                className={`relative overflow-hidden ${
                  index === 0 ? "h-64" : "h-48"
                }`}
              >
                <Image
                  src={tour.imageUrl}
                  alt={tour.title}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />

                {/* Adventure Type Badge */}
                <div className="absolute top-4 left-4">
                  <span className="bg-blue-500 text-white px-3 py-1 text-sm font-semibold rounded-full shadow-lg">
                    {tour.adventureType}
                  </span>
                </div>

                {/* Difficulty & Adrenaline Level */}
                <div className="absolute top-4 right-4 flex flex-col gap-2">
                  <span
                    className={`px-3 py-1 text-xs font-semibold rounded-full ${getDifficultyColor(
                      tour.difficulty
                    )}`}
                  >
                    {tour.difficulty}
                  </span>
                  <div className="flex items-center bg-white/20 backdrop-blur-sm rounded-full px-2 py-1">
                    <span
                      className={`w-2 h-2 rounded-full ${getAdrenalineColor(
                        tour.adrenalineLevel
                      )} mr-2`}
                    />
                    <span className="text-white text-xs font-medium">
                      {tour.adrenalineLevel}
                    </span>
                  </div>
                </div>

                {/* Price Badge */}
                <div className="absolute bottom-4 left-4">
                  <div className="bg-white/90 backdrop-blur-sm text-gray-900 px-3 py-2 rounded-lg font-bold">
                    ${tour.price}
                  </div>
                </div>
              </div>

              {/* Content */}
              <div className="p-6">
                {/* Location */}
                <p className="text-sm text-gray-500 mb-2">{tour.location}</p>

                {/* Title */}
                <h3
                  className={`font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-blue-600 transition-colors ${
                    index === 0 ? "text-xl" : "text-lg"
                  }`}
                >
                  {tour.title}
                </h3>

                {/* Rating & Reviews */}
                <div className="flex items-center mb-4">
                  <div className="flex items-center">
                    {renderStars(tour.rating)}
                  </div>
                  <span className="text-sm font-semibold text-gray-900 ml-2">
                    {tour.rating}
                  </span>
                  <span className="text-sm text-gray-500 ml-1">
                    ({tour.reviewCount.toLocaleString()})
                  </span>
                </div>

                {/* Tour Details */}
                <div className="flex items-center text-sm text-gray-600 mb-4 space-x-4">
                  <div className="flex items-center">
                    <ClockIcon className="w-4 h-4 mr-1" />
                    {tour.duration}
                  </div>
                  <div className="flex items-center">
                    <UsersIcon className="w-4 h-4 mr-1" />
                    Max {tour.maxGroupSize}
                  </div>
                </div>

                {/* Highlights */}
                <div className="mb-6">
                  <ul className="text-sm text-gray-600 space-y-1">
                    {tour.highlights
                      .slice(0, index === 0 ? 4 : 3)
                      .map((highlight, i) => (
                        <li key={i} className="flex items-center">
                          <svg
                            className="w-3 h-3 text-blue-500 mr-2 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                          >
                            <path
                              fillRule="evenodd"
                              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                              clipRule="evenodd"
                            />
                          </svg>
                          {highlight}
                        </li>
                      ))}
                  </ul>
                </div>

                {/* CTA */}
                <Link
                  href={`/tours/${tour.id}`}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-colors duration-200 inline-block text-center"
                >
                  Book Adventure
                </Link>
              </div>

              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
            </div>
          ))}
        </div>

        {/* Safety Notice */}
        <div className="mt-12 bg-yellow-50 border border-yellow-200 rounded-2xl p-6">
          <div className="flex items-center mb-4">
            <span className="text-2xl mr-3">⚠️</span>
            <h3 className="text-xl font-bold text-gray-900">Safety First</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-700">
            <div className="flex items-center">
              <span className="text-lg mr-2">🦺</span>
              Professional safety equipment included
            </div>
            <div className="flex items-center">
              <span className="text-lg mr-2">👨‍🏫</span>
              Certified and experienced guides
            </div>
            <div className="flex items-center">
              <span className="text-lg mr-2">📋</span>
              Comprehensive safety briefings
            </div>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-12">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-8 text-white">
            <div className="flex items-center justify-center mb-4">
              <span className="text-6xl mr-4">🎯</span>
              <div>
                <h3 className="text-2xl font-bold mb-2">
                  Ready for Your Next Adventure?
                </h3>
                <p className="text-blue-100">
                  From beginner-friendly to extreme challenges - find your
                  perfect thrill
                </p>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-6">
              <Link
                href="/tours"
                className="bg-white text-blue-600 hover:bg-gray-100 font-bold py-3 px-8 rounded-xl transition-all duration-200 hover:shadow-lg inline-block text-center"
              >
                Explore All Adventures
              </Link>
              <button className="border-2 border-white text-white hover:bg-white hover:text-blue-600 font-bold py-3 px-8 rounded-xl transition-all duration-200">
                Custom Adventure Planning
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
