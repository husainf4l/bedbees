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

interface FoodExperience {
  id: string;
  title: string;
  location: string;
  imageUrl: string;
  rating: number;
  reviewCount: number;
  duration: string;
  price: number;
  cuisine: string;
  highlights: string[];
  difficulty: "Easy" | "Moderate" | "Expert";
  includedMeals: number;
}

const foodExperiences: FoodExperience[] = [
  {
    id: "1",
    title: "Traditional Lebanese Mezze Cooking Class",
    location: "Beirut, Lebanon",
    imageUrl: "/hero/resort.webp",
    rating: 4.9,
    reviewCount: 847,
    duration: "4 hours",
    price: 65,
    cuisine: "Lebanese",
    highlights: [
      "Hands-on cooking",
      "Market tour",
      "Recipe book",
      "Wine pairing",
    ],
    difficulty: "Easy",
    includedMeals: 1,
  },
  {
    id: "2",
    title: "Dubai Street Food & Spice Souk Tour",
    location: "Dubai, UAE",
    imageUrl: "/hero/hotel.webp",
    rating: 4.8,
    reviewCount: 1243,
    duration: "5 hours",
    price: 89,
    cuisine: "Middle Eastern",
    highlights: [
      "10+ food tastings",
      "Spice market",
      "Local guide",
      "Cultural insights",
    ],
    difficulty: "Easy",
    includedMeals: 1,
  },
  {
    id: "3",
    title: "Jordanian Mansaf Masterclass",
    location: "Amman, Jordan",
    imageUrl: "/hero/chalets.webp",
    rating: 4.7,
    reviewCount: 452,
    duration: "6 hours",
    price: 75,
    cuisine: "Jordanian",
    highlights: [
      "Traditional recipe",
      "Family experience",
      "Cultural history",
      "Take-home spices",
    ],
    difficulty: "Moderate",
    includedMeals: 2,
  },
  {
    id: "4",
    title: "Egyptian Falafel & Ful Making Workshop",
    location: "Cairo, Egypt",
    imageUrl: "/hero/villa.webp",
    rating: 4.6,
    reviewCount: 623,
    duration: "3 hours",
    price: 45,
    cuisine: "Egyptian",
    highlights: [
      "Ancient recipes",
      "Street food secrets",
      "Local ingredients",
      "Breakfast tradition",
    ],
    difficulty: "Easy",
    includedMeals: 1,
  },
];

export default function FoodExperiencesGrid() {
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
      case "Easy":
        return "bg-green-100 text-green-800";
      case "Moderate":
        return "bg-yellow-100 text-yellow-800";
      case "Expert":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <section className="py-16 bg-gradient-to-br from-orange-50 to-red-50">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="flex items-center justify-between mb-12">
          <div>
            <div className="flex items-center mb-4">
              <span className="text-4xl mr-3">🍽️</span>
              <h2 className="text-3xl font-bold text-gray-900">
                Culinary Experiences
              </h2>
            </div>
            <p className="text-lg text-gray-600 max-w-2xl">
              Discover authentic flavors and cooking traditions with local chefs
              and food experts
            </p>
          </div>
          <Link
            href="/tours"
            className="flex items-center text-orange-600 hover:text-orange-700 font-semibold transition-colors group"
          >
            View all food tours
            <ChevronRightIcon className="w-5 h-5 ml-1 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {/* Food Experiences Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {foodExperiences.map((experience) => (
            <div
              key={experience.id}
              className="group cursor-pointer bg-white rounded-2xl shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 overflow-hidden"
            >
              {/* Image Container */}
              <div className="relative h-48 overflow-hidden">
                <Image
                  src={experience.imageUrl}
                  alt={experience.title}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />

                {/* Cuisine Badge */}
                <div className="absolute top-4 left-4">
                  <span className="bg-orange-500 text-white px-3 py-1 text-sm font-semibold rounded-full shadow-lg">
                    {experience.cuisine}
                  </span>
                </div>

                {/* Difficulty Badge */}
                <div className="absolute top-4 right-4">
                  <span
                    className={`px-3 py-1 text-xs font-semibold rounded-full ${getDifficultyColor(
                      experience.difficulty
                    )}`}
                  >
                    {experience.difficulty}
                  </span>
                </div>
              </div>

              {/* Content */}
              <div className="p-5">
                {/* Location */}
                <p className="text-sm text-gray-500 mb-2">
                  {experience.location}
                </p>

                {/* Title */}
                <h3 className="text-lg font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-orange-600 transition-colors">
                  {experience.title}
                </h3>

                {/* Rating & Reviews */}
                <div className="flex items-center mb-3">
                  <div className="flex items-center">
                    {renderStars(experience.rating)}
                  </div>
                  <span className="text-sm font-semibold text-gray-900 ml-2">
                    {experience.rating}
                  </span>
                  <span className="text-sm text-gray-500 ml-1">
                    ({experience.reviewCount})
                  </span>
                </div>

                {/* Details */}
                <div className="flex items-center text-sm text-gray-600 mb-3 space-x-3">
                  <div className="flex items-center">
                    <ClockIcon className="w-4 h-4 mr-1" />
                    {experience.duration}
                  </div>
                  <div className="flex items-center">
                    <span className="mr-1">🍽️</span>
                    {experience.includedMeals} meal
                    {experience.includedMeals > 1 ? "s" : ""}
                  </div>
                </div>

                {/* Highlights */}
                <div className="mb-4">
                  <ul className="text-sm text-gray-600 space-y-1">
                    {experience.highlights.slice(0, 3).map((highlight, i) => (
                      <li key={i} className="flex items-center">
                        <span className="w-1.5 h-1.5 bg-orange-400 rounded-full mr-2 flex-shrink-0" />
                        {highlight}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Price & CTA */}
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-2xl font-bold text-gray-900">
                      ${experience.price}
                    </span>
                    <span className="text-sm text-gray-500 ml-1">
                      per person
                    </span>
                  </div>
                  <Link
                    href={`/tours/${experience.id}`}
                    className="bg-orange-600 hover:bg-orange-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-200 text-sm inline-block text-center"
                  >
                    Book Now
                  </Link>
                </div>
              </div>

              {/* Hover Overlay */}
              <div className="absolute inset-0 bg-orange-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
            </div>
          ))}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-12">
          <div className="bg-white rounded-2xl p-8 shadow-lg">
            <div className="flex items-center justify-center mb-4">
              <span className="text-6xl mr-4">👨‍🍳</span>
              <div>
                <h3 className="text-2xl font-bold text-gray-900">
                  Become a Culinary Explorer
                </h3>
                <p className="text-gray-600">
                  Learn to cook authentic dishes from local experts
                </p>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-6">
              <Link
                href="/tours"
                className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 px-8 rounded-xl transition-all duration-200 hover:shadow-lg inline-block text-center"
              >
                Browse All Food Experiences
              </Link>
              <button className="border border-orange-600 text-orange-600 hover:bg-orange-50 font-bold py-3 px-8 rounded-xl transition-all duration-200">
                Private Chef Experience
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
