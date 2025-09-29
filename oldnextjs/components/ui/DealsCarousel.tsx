"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  ClockIcon,
  FireIcon,
} from "@heroicons/react/24/outline";

interface Deal {
  id: string;
  title: string;
  description: string;
  imageUrl: string;
  originalPrice: number;
  discountedPrice: number;
  discountPercentage: number;
  location: string;
  validUntil: string;
  isFlashSale?: boolean;
  isLimitedTime?: boolean;
  dealType: "early_bird" | "last_minute" | "seasonal" | "flash_sale";
}

const deals: Deal[] = [
  {
    id: "1",
    title: "Petra Archaeological Wonder Tour",
    description:
      "Skip-the-line access with expert guide. Explore the ancient city and Treasury.",
    imageUrl: "/hero/chalets.webp",
    originalPrice: 120,
    discountedPrice: 85,
    discountPercentage: 29,
    location: "Petra, Jordan",
    validUntil: "2025-10-15",
    dealType: "early_bird",
  },
  {
    id: "2",
    title: "Dubai Desert Safari & BBQ Dinner",
    description:
      "Dune bashing, camel riding, and traditional entertainment with buffet dinner.",
    imageUrl: "/hero/hotel.webp",
    originalPrice: 95,
    discountedPrice: 59,
    discountPercentage: 38,
    location: "Dubai, UAE",
    validUntil: "2025-09-25",
    isFlashSale: true,
    dealType: "flash_sale",
  },
  {
    id: "3",
    title: "Wadi Rum Stargazing Experience",
    description:
      "Overnight desert camping with traditional Bedouin dinner under the stars.",
    imageUrl: "/hero/apartment.webp",
    originalPrice: 150,
    discountedPrice: 110,
    discountPercentage: 27,
    location: "Wadi Rum, Jordan",
    validUntil: "2025-11-30",
    dealType: "seasonal",
  },
  {
    id: "4",
    title: "Pyramids & Egyptian Museum Tour",
    description:
      "Full-day guided tour with lunch. Visit Giza Pyramids, Sphinx, and museum.",
    imageUrl: "/hero/villa.webp",
    originalPrice: 80,
    discountedPrice: 55,
    discountPercentage: 31,
    location: "Cairo, Egypt",
    validUntil: "2025-10-01",
    isLimitedTime: true,
    dealType: "last_minute",
  },
  {
    id: "5",
    title: "Lebanese Food & Wine Tour",
    description:
      "Taste authentic Lebanese cuisine and local wines in historic Beirut.",
    imageUrl: "/hero/resort.webp",
    originalPrice: 75,
    discountedPrice: 52,
    discountPercentage: 31,
    location: "Beirut, Lebanon",
    validUntil: "2025-12-15",
    dealType: "seasonal",
  },
  {
    id: "6",
    title: "Dead Sea Floating & Spa Day",
    description:
      "Relax in mineral-rich waters and enjoy luxury spa treatments.",
    imageUrl: "/hero/treehouses.webp",
    originalPrice: 110,
    discountedPrice: 78,
    discountPercentage: 29,
    location: "Dead Sea, Jordan",
    validUntil: "2025-10-20",
    dealType: "early_bird",
  },
];

export default function DealsCarousel() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAutoPlaying, setIsAutoPlaying] = useState(true);

  // Auto-advance carousel
  useEffect(() => {
    if (!isAutoPlaying) return;

    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) =>
        prevIndex === deals.length - 1 ? 0 : prevIndex + 1
      );
    }, 5000);

    return () => clearInterval(interval);
  }, [isAutoPlaying]);

  const goToNext = () => {
    setCurrentIndex((prevIndex) =>
      prevIndex === deals.length - 1 ? 0 : prevIndex + 1
    );
  };

  const goToPrevious = () => {
    setCurrentIndex((prevIndex) =>
      prevIndex === 0 ? deals.length - 1 : prevIndex - 1
    );
  };

  const goToSlide = (index: number) => {
    setCurrentIndex(index);
  };

  const getDealBadgeStyle = (dealType: string, isFlashSale?: boolean) => {
    if (isFlashSale) {
      return "bg-red-500 text-white animate-pulse";
    }

    switch (dealType) {
      case "early_bird":
        return "bg-green-500 text-white";
      case "last_minute":
        return "bg-orange-500 text-white";
      case "seasonal":
        return "bg-blue-500 text-white";
      case "flash_sale":
        return "bg-red-500 text-white animate-pulse";
      default:
        return "bg-purple-500 text-white";
    }
  };

  const getDealBadgeText = (dealType: string, isFlashSale?: boolean) => {
    if (isFlashSale) return "Flash Sale";

    switch (dealType) {
      case "early_bird":
        return "Early Bird";
      case "last_minute":
        return "Last Minute";
      case "seasonal":
        return "Seasonal Deal";
      case "flash_sale":
        return "Flash Sale";
      default:
        return "Special Deal";
    }
  };

  const isExpiringSoon = (validUntil: string) => {
    const today = new Date();
    const expiryDate = new Date(validUntil);
    const daysUntilExpiry = Math.ceil(
      (expiryDate.getTime() - today.getTime()) / (1000 * 3600 * 24)
    );
    return daysUntilExpiry <= 7;
  };

  return (
    <section className="py-16 bg-gradient-to-br from-orange-50 to-yellow-50">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <FireIcon className="w-8 h-8 text-orange-500 mr-3" />
            <h2 className="text-3xl font-bold text-gray-900">
              Limited Time Deals
            </h2>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Don&apos;t miss out on these incredible savings! Book now and save
            up to 40% on popular experiences.
          </p>
        </div>

        {/* Carousel Container */}
        <div
          className="relative"
          onMouseEnter={() => setIsAutoPlaying(false)}
          onMouseLeave={() => setIsAutoPlaying(true)}
        >
          {/* Main Carousel */}
          <div className="overflow-hidden rounded-3xl">
            <div
              className="flex transition-transform duration-500 ease-in-out"
              style={{ transform: `translateX(-${currentIndex * 100}%)` }}
            >
              {deals.map((deal) => (
                <div key={deal.id} className="w-full flex-shrink-0">
                  <div className="relative h-96 bg-white rounded-3xl shadow-xl overflow-hidden">
                    <div className="flex h-full">
                      {/* Image Section */}
                      <div className="relative w-1/2 overflow-hidden">
                        <Image
                          src={deal.imageUrl}
                          alt={deal.title}
                          fill
                          className="object-cover"
                        />
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent to-black/20" />

                        {/* Deal Badge */}
                        <div className="absolute top-4 left-4">
                          <span
                            className={`px-4 py-2 text-sm font-bold rounded-full shadow-lg ${getDealBadgeStyle(
                              deal.dealType,
                              deal.isFlashSale
                            )}`}
                          >
                            {getDealBadgeText(deal.dealType, deal.isFlashSale)}
                          </span>
                        </div>

                        {/* Discount Badge */}
                        <div className="absolute top-4 right-4">
                          <div className="bg-red-500 text-white px-4 py-2 rounded-full font-bold text-lg shadow-lg">
                            -{deal.discountPercentage}%
                          </div>
                        </div>
                      </div>

                      {/* Content Section */}
                      <div className="w-1/2 p-8 flex flex-col justify-center">
                        <div className="mb-6">
                          <h3 className="text-2xl font-bold text-gray-900 mb-3">
                            {deal.title}
                          </h3>
                          <p className="text-gray-600 mb-4 leading-relaxed">
                            {deal.description}
                          </p>
                          <p className="text-orange-600 font-semibold">
                            📍 {deal.location}
                          </p>
                        </div>

                        {/* Pricing */}
                        <div className="mb-6">
                          <div className="flex items-center mb-2">
                            <span className="text-3xl font-bold text-green-600">
                              ${deal.discountedPrice}
                            </span>
                            <span className="text-lg text-gray-500 line-through ml-3">
                              ${deal.originalPrice}
                            </span>
                            <span className="text-sm bg-green-100 text-green-800 px-2 py-1 rounded-full ml-3 font-semibold">
                              Save ${deal.originalPrice - deal.discountedPrice}
                            </span>
                          </div>
                          <p className="text-sm text-gray-500">per person</p>
                        </div>

                        {/* Expiry Warning */}
                        {isExpiringSoon(deal.validUntil) && (
                          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                            <div className="flex items-center text-red-700">
                              <ClockIcon className="w-4 h-4 mr-2" />
                              <span className="text-sm font-semibold">
                                Expires soon:{" "}
                                {new Date(deal.validUntil).toLocaleDateString()}
                              </span>
                            </div>
                          </div>
                        )}

                        {/* CTA Button */}
                        <button className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-200 hover:shadow-lg hover:scale-105">
                          Book Now & Save
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Navigation Arrows */}
          <button
            onClick={goToPrevious}
            className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/90 hover:bg-white text-gray-800 p-3 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 z-10"
          >
            <ChevronLeftIcon className="w-6 h-6" />
          </button>
          <button
            onClick={goToNext}
            className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/90 hover:bg-white text-gray-800 p-3 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 z-10"
          >
            <ChevronRightIcon className="w-6 h-6" />
          </button>

          {/* Dot Indicators */}
          <div className="flex justify-center mt-8 space-x-2">
            {deals.map((_, index) => (
              <button
                key={index}
                onClick={() => goToSlide(index)}
                className={`w-3 h-3 rounded-full transition-all duration-200 ${
                  index === currentIndex
                    ? "bg-orange-600 scale-125"
                    : "bg-gray-300 hover:bg-gray-400"
                }`}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
