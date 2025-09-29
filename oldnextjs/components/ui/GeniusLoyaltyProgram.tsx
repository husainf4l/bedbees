"use client";

import React, { useState } from "react";
import {
  StarIcon,
  TrophyIcon,
  GiftIcon,
  ShieldCheckIcon,
  ClockIcon,
  TagIcon,
  CreditCardIcon,
  SparklesIcon,
  ChevronRightIcon,
  HeartIcon,
  MapPinIcon,
} from "@heroicons/react/24/outline";
import {
  StarIcon as StarSolidIcon,
  TrophyIcon as TrophySolidIcon,
} from "@heroicons/react/24/solid";

interface LoyaltyBenefit {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  available: boolean;
  tier?: "genius1" | "genius2" | "genius3";
}

interface UserLoyaltyData {
  currentTier: "member" | "genius1" | "genius2" | "genius3";
  completedBookings: number;
  nextTierBookings: number;
  totalSavings: number;
  memberSince: string;
  pointsBalance: number;
  nextReward: number;
}

const loyaltyData: UserLoyaltyData = {
  currentTier: "genius2",
  completedBookings: 7,
  nextTierBookings: 15,
  totalSavings: 485,
  memberSince: "2023-04-15",
  pointsBalance: 2450,
  nextReward: 5000,
};

const tierInfo = {
  member: {
    name: "Explorer",
    color: "from-gray-500 to-gray-600",
    bgColor: "bg-gray-50",
    textColor: "text-gray-700",
    icon: <MapPinIcon className="w-6 h-6" />,
    requirement: "Join ShareTrip",
  },
  genius1: {
    name: "Genius Level 1",
    color: "from-blue-500 to-blue-600",
    bgColor: "bg-blue-50",
    textColor: "text-blue-700",
    icon: <StarSolidIcon className="w-6 h-6" />,
    requirement: "Complete 2 qualified bookings",
  },
  genius2: {
    name: "Genius Level 2",
    color: "from-purple-500 to-purple-600",
    bgColor: "bg-purple-50",
    textColor: "text-purple-700",
    icon: <TrophySolidIcon className="w-6 h-6" />,
    requirement: "Complete 5 qualified bookings",
  },
  genius3: {
    name: "Genius Level 3",
    color: "from-yellow-500 to-orange-500",
    bgColor: "bg-yellow-50",
    textColor: "text-yellow-700",
    icon: <SparklesIcon className="w-6 h-6" />,
    requirement: "Complete 15 qualified bookings",
  },
};

const allBenefits: LoyaltyBenefit[] = [
  // Level 1 Benefits
  {
    id: "1",
    title: "10% Discounts on Stays",
    description: "Applied to the price before taxes & charges",
    icon: <TagIcon className="w-5 h-5" />,
    available: loyaltyData.currentTier !== "member",
    tier: "genius1",
  },
  {
    id: "2",
    title: "10% Discounts on Rental Cars",
    description: "Applies to cost of car only",
    icon: <MapPinIcon className="w-5 h-5" />,
    available: loyaltyData.currentTier !== "member",
    tier: "genius1",
  },
  {
    id: "3",
    title: "Free Cancellation",
    description: "Cancel bookings for free, even on non-refundable rates",
    icon: <ShieldCheckIcon className="w-5 h-5" />,
    available: loyaltyData.currentTier !== "member",
    tier: "genius1",
  },
  {
    id: "4",
    title: "Member Prices",
    description: "Exclusive discounts on selected accommodations and tours",
    icon: <GiftIcon className="w-5 h-5" />,
    available: loyaltyData.currentTier !== "member",
    tier: "genius1",
  },
  // Level 2 Benefits
  {
    id: "5",
    title: "10-15% Discounts on Stays",
    description: "Applied to the price before taxes & charges",
    icon: <TagIcon className="w-5 h-5" />,
    available: ["genius2", "genius3"].includes(loyaltyData.currentTier),
    tier: "genius2",
  },
  {
    id: "6",
    title: "10-15% Discounts on Rental Cars",
    description: "Applies to cost of car only",
    icon: <MapPinIcon className="w-5 h-5" />,
    available: ["genius2", "genius3"].includes(loyaltyData.currentTier),
    tier: "genius2",
  },
  {
    id: "7",
    title: "Free Breakfasts",
    description:
      "Waking up is easy with complimentary breakfast, available on select stays",
    icon: <GiftIcon className="w-5 h-5" />,
    available: ["genius2", "genius3"].includes(loyaltyData.currentTier),
    tier: "genius2",
  },
  {
    id: "8",
    title: "Free Room Upgrades",
    description:
      "Travel in style with free upgrades, automatically applied to select stays",
    icon: <StarIcon className="w-5 h-5" />,
    available: ["genius2", "genius3"].includes(loyaltyData.currentTier),
    tier: "genius2",
  },
  // Level 3 Benefits
  {
    id: "9",
    title: "10-20% Discounts on Stays",
    description: "Applied to the price before taxes & charges",
    icon: <TagIcon className="w-5 h-5" />,
    available: loyaltyData.currentTier === "genius3",
    tier: "genius3",
  },
  {
    id: "10",
    title: "10-15% Discounts on Rental Cars",
    description: "Applies to cost of car only",
    icon: <MapPinIcon className="w-5 h-5" />,
    available: loyaltyData.currentTier === "genius3",
    tier: "genius3",
  },
  {
    id: "11",
    title: "Priority Support on Stays",
    description:
      "Get direct access to a live agent to discuss or modify any of your stays",
    icon: <HeartIcon className="w-5 h-5" />,
    available: loyaltyData.currentTier === "genius3",
    tier: "genius3",
  },
];

const recentDeals = [
  {
    id: "1",
    title: "Petra Luxury Resort",
    location: "Petra, Jordan",
    discount: "15%",
    originalPrice: 180,
    geniusPrice: 153,
    image: "/hero/resort.webp",
    rating: 4.8,
  },
  {
    id: "2",
    title: "Dubai Marina Hotel",
    location: "Dubai, UAE",
    discount: "12%",
    originalPrice: 220,
    geniusPrice: 194,
    image: "/hero/hotel.webp",
    rating: 4.7,
  },
  {
    id: "3",
    title: "Dead Sea Spa Resort",
    location: "Dead Sea, Jordan",
    discount: "18%",
    originalPrice: 165,
    geniusPrice: 135,
    image: "/hero/villa.webp",
    rating: 4.9,
  },
];

export default function GeniusLoyaltyProgram() {
  const [activeTab, setActiveTab] = useState<"benefits" | "progress" | "deals">(
    "benefits"
  );

  const currentTierInfo = tierInfo[loyaltyData.currentTier];
  const progressPercentage =
    (loyaltyData.completedBookings / loyaltyData.nextTierBookings) * 100;

  const getNextTier = () => {
    if (loyaltyData.currentTier === "member") return "genius1";
    if (loyaltyData.currentTier === "genius1") return "genius2";
    if (loyaltyData.currentTier === "genius2") return "genius3";
    return "genius3";
  };

  const nextTierInfo = tierInfo[getNextTier()];
  const bookingsNeeded =
    loyaltyData.nextTierBookings - loyaltyData.completedBookings;

  const getBenefitsForTier = (tier: string) => {
    return allBenefits.filter(
      (benefit) =>
        !benefit.tier ||
        (tier === "genius1" && ["genius1"].includes(benefit.tier)) ||
        (tier === "genius2" && ["genius1", "genius2"].includes(benefit.tier)) ||
        (tier === "genius3" &&
          ["genius1", "genius2", "genius3"].includes(benefit.tier))
    );
  };

  const availableBenefits = getBenefitsForTier(loyaltyData.currentTier);

  return (
    <div className="max-w-6xl mx-auto p-4">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-yellow-500 rounded-3xl p-6 text-white mb-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center mb-4">
              <div className={`p-3 bg-white/20 rounded-full mr-4`}>
                {currentTierInfo.icon}
              </div>
              <div>
                <h1 className="text-2xl font-bold mb-2">
                  ShareTrip {currentTierInfo.name}
                </h1>
                <p className="text-blue-100">
                  Member since{" "}
                  {new Date(loyaltyData.memberSince).toLocaleDateString(
                    "en-US",
                    {
                      month: "long",
                      year: "numeric",
                    }
                  )}
                </p>
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold mb-2">
              ${loyaltyData.totalSavings}
            </div>
            <div className="text-blue-100">Total Saved</div>
          </div>
        </div>

        {/* Progress to Next Level */}
        {loyaltyData.currentTier !== "genius3" && (
          <div className="mt-6 p-4 bg-white/10 backdrop-blur-sm rounded-2xl">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold">
                  Progress to {nextTierInfo.name}
                </h3>
                <p className="text-blue-100">
                  {bookingsNeeded} more booking{bookingsNeeded !== 1 ? "s" : ""}{" "}
                  needed
                </p>
              </div>
              <div className="text-2xl font-bold">
                {loyaltyData.completedBookings}/{loyaltyData.nextTierBookings}
              </div>
            </div>
            <div className="w-full bg-white/20 rounded-full h-3">
              <div
                className="bg-gradient-to-r from-yellow-400 to-orange-400 h-3 rounded-full transition-all duration-500"
                style={{ width: `${Math.min(progressPercentage, 100)}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Navigation Tabs */}
      <div className="flex space-x-1 bg-gray-100 rounded-2xl p-1 mb-8">
        {[
          {
            key: "benefits",
            label: "My Benefits",
            icon: <GiftIcon className="w-5 h-5" />,
          },
          {
            key: "progress",
            label: "Progress",
            icon: <TrophyIcon className="w-5 h-5" />,
          },
          {
            key: "deals",
            label: "Genius Deals",
            icon: <TagIcon className="w-5 h-5" />,
          },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as string)}
            className={`flex-1 flex items-center justify-center px-6 py-3 rounded-xl transition-all duration-200 ${
              activeTab === tab.key
                ? "bg-white text-blue-600 shadow-lg font-semibold"
                : "text-gray-600 hover:text-blue-600"
            }`}
          >
            {tab.icon}
            <span className="ml-2">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === "benefits" && (
        <div className="space-y-6">
          {/* Current Benefits */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Your {currentTierInfo.name} Benefits
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {availableBenefits.map((benefit) => (
                <div
                  key={benefit.id}
                  className={`p-4 rounded-2xl border-2 transition-all duration-200 ${
                    benefit.available
                      ? "border-green-200 bg-green-50 hover:shadow-lg"
                      : "border-gray-200 bg-gray-50"
                  }`}
                >
                  <div className="flex items-center mb-4">
                    <div
                      className={`p-2 rounded-full ${
                        benefit.available
                          ? "bg-green-100 text-green-600"
                          : "bg-gray-100 text-gray-400"
                      }`}
                    >
                      {benefit.icon}
                    </div>
                    {benefit.available && (
                      <div className="ml-auto">
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      </div>
                    )}
                  </div>
                  <h3
                    className={`font-semibold mb-2 ${
                      benefit.available ? "text-gray-900" : "text-gray-500"
                    }`}
                  >
                    {benefit.title}
                  </h3>
                  <p
                    className={`text-sm ${
                      benefit.available ? "text-gray-600" : "text-gray-400"
                    }`}
                  >
                    {benefit.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === "progress" && (
        <div className="space-y-6">
          {/* Tier Progression */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Loyalty Tier Progression
            </h2>
            <div className="space-y-6">
              {Object.entries(tierInfo).map(([tierKey, info]) => {
                const isCurrentTier = tierKey === loyaltyData.currentTier;
                const isUnlocked =
                  ["member", "genius1", "genius2"].includes(tierKey) &&
                  (["member", "genius1"].includes(loyaltyData.currentTier) ||
                    tierKey === loyaltyData.currentTier ||
                    (loyaltyData.currentTier === "genius2" &&
                      tierKey !== "genius3") ||
                    loyaltyData.currentTier === "genius3");

                return (
                  <div
                    key={tierKey}
                    className={`p-6 rounded-2xl border-2 transition-all duration-200 ${
                      isCurrentTier
                        ? `border-blue-300 ${info.bgColor} shadow-lg`
                        : isUnlocked
                        ? "border-green-200 bg-green-50"
                        : "border-gray-200 bg-gray-50"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div
                          className={`p-3 rounded-full mr-4 ${
                            isCurrentTier
                              ? `bg-gradient-to-r ${info.color} text-white`
                              : isUnlocked
                              ? "bg-green-100 text-green-600"
                              : "bg-gray-100 text-gray-400"
                          }`}
                        >
                          {info.icon}
                        </div>
                        <div>
                          <h3
                            className={`text-xl font-bold ${
                              isCurrentTier
                                ? info.textColor
                                : isUnlocked
                                ? "text-green-700"
                                : "text-gray-500"
                            }`}
                          >
                            {info.name}
                          </h3>
                          <p
                            className={`text-sm ${
                              isCurrentTier
                                ? "text-blue-600"
                                : isUnlocked
                                ? "text-green-600"
                                : "text-gray-400"
                            }`}
                          >
                            {info.requirement}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center">
                        {isCurrentTier && (
                          <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-semibold mr-4">
                            Current Level
                          </span>
                        )}
                        {isUnlocked && (
                          <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                            <svg
                              className="w-4 h-4 text-white"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path
                                fillRule="evenodd"
                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                clipRule="evenodd"
                              />
                            </svg>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Benefits for this tier */}
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <h4 className="font-semibold text-gray-700 mb-2">
                        Benefits at this level:
                      </h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {getBenefitsForTier(tierKey)
                          .slice(0, 4)
                          .map((benefit) => (
                            <div
                              key={benefit.id}
                              className="flex items-center text-sm text-gray-600"
                            >
                              <span className="w-1.5 h-1.5 bg-blue-400 rounded-full mr-2"></span>
                              {benefit.title}
                            </div>
                          ))}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {activeTab === "deals" && (
        <div className="space-y-6">
          {/* Exclusive Genius Deals */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-gray-900">
                Exclusive Genius Deals
              </h2>
              <button className="flex items-center text-blue-600 hover:text-blue-700 font-semibold">
                View All Deals
                <ChevronRightIcon className="w-5 h-5 ml-1" />
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {recentDeals.map((deal) => (
                <div
                  key={deal.id}
                  className="group cursor-pointer bg-gray-50 rounded-2xl overflow-hidden hover:shadow-lg transition-all duration-300"
                >
                  <div className="relative h-48 bg-gray-200">
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                    <div className="absolute top-4 left-4">
                      <span className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-3 py-1 text-sm font-bold rounded-full">
                        Genius {deal.discount} Off
                      </span>
                    </div>
                    <div className="absolute bottom-4 left-4 text-white">
                      <div className="flex items-center mb-2">
                        {Array.from({ length: 5 }, (_, i) => (
                          <StarSolidIcon
                            key={i}
                            className={`w-4 h-4 ${
                              i < Math.floor(deal.rating)
                                ? "text-yellow-400"
                                : "text-gray-300"
                            }`}
                          />
                        ))}
                        <span className="ml-2 text-sm font-semibold">
                          {deal.rating}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="p-4">
                    <h3 className="font-semibold text-gray-900 mb-1">
                      {deal.title}
                    </h3>
                    <p className="text-sm text-gray-600 mb-3">
                      {deal.location}
                    </p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <span className="text-lg font-bold text-blue-600">
                          ${deal.geniusPrice}
                        </span>
                        <span className="text-sm text-gray-500 line-through ml-2">
                          ${deal.originalPrice}
                        </span>
                      </div>
                      <span className="text-sm bg-green-100 text-green-700 px-2 py-1 rounded-full font-semibold">
                        Save ${deal.originalPrice - deal.geniusPrice}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
        <div className="bg-white rounded-2xl p-6 text-center shadow-lg">
          <div className="text-3xl font-bold text-blue-600 mb-2">
            {loyaltyData.completedBookings}
          </div>
          <div className="text-gray-600">Completed Bookings</div>
        </div>
        <div className="bg-white rounded-2xl p-6 text-center shadow-lg">
          <div className="text-3xl font-bold text-green-600 mb-2">
            {loyaltyData.pointsBalance.toLocaleString()}
          </div>
          <div className="text-gray-600">Reward Points</div>
        </div>
        <div className="bg-white rounded-2xl p-6 text-center shadow-lg">
          <div className="text-3xl font-bold text-purple-600 mb-2">
            ${loyaltyData.totalSavings}
          </div>
          <div className="text-gray-600">Total Saved</div>
        </div>
        <div className="bg-white rounded-2xl p-6 text-center shadow-lg">
          <div className="text-3xl font-bold text-yellow-600 mb-2">
            {Math.ceil(
              (loyaltyData.nextReward - loyaltyData.pointsBalance) / 100
            )}
          </div>
          <div className="text-gray-600">Bookings to Reward</div>
        </div>
      </div>
    </div>
  );
}
