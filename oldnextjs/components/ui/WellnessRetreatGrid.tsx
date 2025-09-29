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

interface WellnessRetreat {
  id: string;
  title: string;
  location: string;
  imageUrl: string;
  rating: number;
  reviewCount: number;
  duration: string;
  price: number;
  wellnessType: string;
  treatments: string[];
  includes: string[];
  relaxationLevel: "Gentle" | "Moderate" | "Intensive" | "Transformative";
  maxParticipants: number;
}

const wellnessRetreats: WellnessRetreat[] = [
  {
    id: "1",
    title: "Dead Sea Ultimate Wellness & Spa Retreat",
    location: "Dead Sea, Jordan",
    imageUrl: "/hero/treehouses.webp",
    rating: 4.9,
    reviewCount: 1847,
    duration: "Full day",
    price: 245,
    wellnessType: "Spa & Wellness",
    treatments: [
      "Dead Sea mud wraps",
      "Salt scrub therapy",
      "Mineral bath",
      "Relaxation massage",
    ],
    includes: [
      "Spa access",
      "Healthy lunch",
      "Relaxation area",
      "Wellness consultation",
    ],
    relaxationLevel: "Intensive",
    maxParticipants: 12,
  },
  {
    id: "2",
    title: "Desert Mindfulness & Yoga Retreat",
    location: "Wadi Rum, Jordan",
    imageUrl: "/hero/apartment.webp",
    rating: 4.8,
    reviewCount: 923,
    duration: "2 days",
    price: 385,
    wellnessType: "Yoga & Meditation",
    treatments: [
      "Sunrise yoga",
      "Desert meditation",
      "Sound healing",
      "Breathwork sessions",
    ],
    includes: [
      "Yoga equipment",
      "Vegetarian meals",
      "Desert camp",
      "Meditation guide",
    ],
    relaxationLevel: "Transformative",
    maxParticipants: 8,
  },
  {
    id: "3",
    title: "Lebanese Mountain Wellness Escape",
    location: "Cedars, Lebanon",
    imageUrl: "/hero/chalets.webp",
    rating: 4.7,
    reviewCount: 654,
    duration: "6 hours",
    price: 165,
    wellnessType: "Nature Therapy",
    treatments: [
      "Forest bathing",
      "Essential oils therapy",
      "Mountain air meditation",
      "Herbal treatments",
    ],
    includes: [
      "Nature walk",
      "Herbal tea ceremony",
      "Organic lunch",
      "Wellness kit",
    ],
    relaxationLevel: "Moderate",
    maxParticipants: 15,
  },
  {
    id: "4",
    title: "Dubai Luxury Spa Experience",
    location: "Dubai, UAE",
    imageUrl: "/hero/hotel.webp",
    rating: 4.6,
    reviewCount: 1234,
    duration: "4 hours",
    price: 320,
    wellnessType: "Luxury Spa",
    treatments: [
      "Gold facial",
      "Hot stone massage",
      "Aromatherapy",
      "Hammam experience",
    ],
    includes: [
      "Spa facilities",
      "Refreshments",
      "Relaxation lounge",
      "Welcome drink",
    ],
    relaxationLevel: "Intensive",
    maxParticipants: 6,
  },
  {
    id: "5",
    title: "Red Sea Thalassotherapy",
    location: "Aqaba, Jordan",
    imageUrl: "/hero/resort.webp",
    rating: 4.5,
    reviewCount: 567,
    duration: "5 hours",
    price: 195,
    wellnessType: "Marine Wellness",
    treatments: [
      "Seaweed wraps",
      "Sea salt therapy",
      "Marine algae masks",
      "Ocean meditation",
    ],
    includes: [
      "Beach access",
      "Healthy lunch",
      "Wellness consultation",
      "Take-home products",
    ],
    relaxationLevel: "Moderate",
    maxParticipants: 10,
  },
  {
    id: "6",
    title: "Cairo Ancient Healing Rituals",
    location: "Cairo, Egypt",
    imageUrl: "/hero/villa.webp",
    rating: 4.4,
    reviewCount: 432,
    duration: "3 hours",
    price: 125,
    wellnessType: "Traditional Healing",
    treatments: [
      "Traditional massage",
      "Herbal steam",
      "Energy healing",
      "Chakra balancing",
    ],
    includes: [
      "Ancient techniques",
      "Herbal remedies",
      "Meditation session",
      "Cultural insights",
    ],
    relaxationLevel: "Gentle",
    maxParticipants: 8,
  },
];

export default function WellnessRetreatGrid() {
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

  const getRelaxationColor = (level: string) => {
    switch (level) {
      case "Gentle":
        return "bg-green-100 text-green-800";
      case "Moderate":
        return "bg-blue-100 text-blue-800";
      case "Intensive":
        return "bg-purple-100 text-purple-800";
      case "Transformative":
        return "bg-pink-100 text-pink-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <section className="py-16 bg-gradient-to-br from-green-50 via-blue-50 to-purple-50">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="flex items-center justify-between mb-12">
          <div>
            <div className="flex items-center mb-4">
              <span className="text-4xl mr-3">🧘‍♀️</span>
              <h2 className="text-3xl font-bold text-gray-900">
                Wellness & Spa Retreats
              </h2>
            </div>
            <p className="text-lg text-gray-600 max-w-2xl">
              Rejuvenate your mind, body, and soul with our curated wellness
              experiences
            </p>
          </div>
          <Link
            href="/tours"
            className="flex items-center text-purple-600 hover:text-purple-700 font-semibold transition-colors group"
          >
            View all wellness
            <ChevronRightIcon className="w-5 h-5 ml-1 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {/* Wellness Retreats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {wellnessRetreats.map((retreat, index) => (
            <div
              key={retreat.id}
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
                  src={retreat.imageUrl}
                  alt={retreat.title}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />

                {/* Wellness Type Badge */}
                <div className="absolute top-4 left-4">
                  <span className="bg-purple-500 text-white px-3 py-1 text-sm font-semibold rounded-full shadow-lg">
                    {retreat.wellnessType}
                  </span>
                </div>

                {/* Relaxation Level */}
                <div className="absolute top-4 right-4">
                  <span
                    className={`px-3 py-1 text-xs font-semibold rounded-full ${getRelaxationColor(
                      retreat.relaxationLevel
                    )}`}
                  >
                    {retreat.relaxationLevel}
                  </span>
                </div>

                {/* Duration Badge */}
                <div className="absolute bottom-4 left-4">
                  <div className="bg-white/90 backdrop-blur-sm text-gray-900 px-3 py-2 rounded-lg font-medium text-sm">
                    <ClockIcon className="w-4 h-4 inline mr-1" />
                    {retreat.duration}
                  </div>
                </div>
              </div>

              {/* Content */}
              <div className="p-6">
                {/* Location */}
                <p className="text-sm text-gray-500 mb-2">{retreat.location}</p>

                {/* Title */}
                <h3
                  className={`font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-purple-600 transition-colors ${
                    index === 0 ? "text-xl" : "text-lg"
                  }`}
                >
                  {retreat.title}
                </h3>

                {/* Rating & Reviews */}
                <div className="flex items-center mb-4">
                  <div className="flex items-center">
                    {renderStars(retreat.rating)}
                  </div>
                  <span className="text-sm font-semibold text-gray-900 ml-2">
                    {retreat.rating}
                  </span>
                  <span className="text-sm text-gray-500 ml-1">
                    ({retreat.reviewCount.toLocaleString()})
                  </span>
                </div>

                {/* Group Size */}
                <div className="flex items-center text-sm text-gray-600 mb-4">
                  <UsersIcon className="w-4 h-4 mr-1" />
                  Small group (max {retreat.maxParticipants})
                </div>

                {/* Treatments Preview */}
                <div className="mb-4">
                  <h4 className="text-sm font-semibold text-gray-900 mb-2">
                    Treatments Include:
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {retreat.treatments.slice(0, 3).map((treatment, i) => (
                      <span
                        key={i}
                        className="text-xs bg-purple-50 text-purple-700 px-2 py-1 rounded-full"
                      >
                        {treatment}
                      </span>
                    ))}
                    {retreat.treatments.length > 3 && (
                      <span className="text-xs bg-gray-50 text-gray-600 px-2 py-1 rounded-full">
                        +{retreat.treatments.length - 3} more
                      </span>
                    )}
                  </div>
                </div>

                {/* Includes */}
                <div className="mb-6">
                  <ul className="text-sm text-gray-600 space-y-1">
                    {retreat.includes
                      .slice(0, index === 0 ? 4 : 3)
                      .map((include, i) => (
                        <li key={i} className="flex items-center">
                          <svg
                            className="w-3 h-3 text-purple-500 mr-2 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                          >
                            <path
                              fillRule="evenodd"
                              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                              clipRule="evenodd"
                            />
                          </svg>
                          {include}
                        </li>
                      ))}
                  </ul>
                </div>

                {/* Price & CTA */}
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-2xl font-bold text-gray-900">
                      ${retreat.price}
                    </span>
                    <span className="text-sm text-gray-500 ml-1">
                      per person
                    </span>
                  </div>
                  <Link
                    href={`/tours/${retreat.id}`}
                    className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors duration-200 inline-block text-center"
                  >
                    Book Retreat
                  </Link>
                </div>
              </div>

              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
            </div>
          ))}
        </div>

        {/* Wellness Benefits */}
        <div className="mt-12 bg-gradient-to-r from-green-50 to-blue-50 rounded-2xl p-8">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Why Choose Our Wellness Experiences?
            </h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-4xl mb-3">🌿</div>
              <h4 className="font-semibold text-gray-900 mb-2">
                Natural Healing
              </h4>
              <p className="text-sm text-gray-600">
                Authentic treatments using local natural resources
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-3">👨‍⚕️</div>
              <h4 className="font-semibold text-gray-900 mb-2">
                Expert Therapists
              </h4>
              <p className="text-sm text-gray-600">
                Certified wellness professionals and healers
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-3">🏞️</div>
              <h4 className="font-semibold text-gray-900 mb-2">
                Stunning Locations
              </h4>
              <p className="text-sm text-gray-600">
                Beautiful natural settings for ultimate relaxation
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-3">✨</div>
              <h4 className="font-semibold text-gray-900 mb-2">
                Holistic Approach
              </h4>
              <p className="text-sm text-gray-600">
                Mind, body, and spirit wellness integration
              </p>
            </div>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-12">
          <div className="bg-gradient-to-r from-purple-600 via-pink-600 to-indigo-600 rounded-2xl p-8 text-white">
            <div className="flex items-center justify-center mb-4">
              <span className="text-6xl mr-4">🕯️</span>
              <div>
                <h3 className="text-2xl font-bold mb-2">
                  Your Wellness Journey Awaits
                </h3>
                <p className="text-purple-100">
                  Discover inner peace and rejuvenation in breathtaking
                  locations
                </p>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-6">
              <Link
                href="/tours"
                className="bg-white text-purple-600 hover:bg-gray-100 font-bold py-3 px-8 rounded-xl transition-all duration-200 hover:shadow-lg inline-block text-center"
              >
                Explore All Wellness
              </Link>
              <button className="border-2 border-white text-white hover:bg-white hover:text-purple-600 font-bold py-3 px-8 rounded-xl transition-all duration-200">
                Personalized Wellness Plan
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
