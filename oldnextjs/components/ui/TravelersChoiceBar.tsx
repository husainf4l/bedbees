"use client";

import React from "react";
import {
  TrophyIcon,
  HeartIcon,
  StarIcon,
  CheckBadgeIcon,
  ShieldCheckIcon,
  GlobeAltIcon,
} from "@heroicons/react/24/outline";
import {
  StarIcon as StarSolidIcon,
  HeartIcon as HeartSolidIcon,
} from "@heroicons/react/24/solid";

interface Award {
  id: string;
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  gradient: string;
  year: string;
  description: string;
  metric?: string;
}

const awards: Award[] = [
  {
    id: "1",
    title: "Travelers' Choice",
    subtitle: "Best Travel Company 2025",
    icon: <TrophyIcon className="w-8 h-8" />,
    gradient: "from-yellow-400 via-yellow-500 to-orange-500",
    year: "2025",
    description: "Awarded based on traveler reviews and ratings",
    metric: "4.8/5 rating",
  },
  {
    id: "2",
    title: "Loved by Guests",
    subtitle: "98% Customer Satisfaction",
    icon: <HeartSolidIcon className="w-8 h-8" />,
    gradient: "from-pink-400 via-red-400 to-red-500",
    year: "2025",
    description: "Based on 50,000+ verified reviews",
    metric: "98% satisfaction",
  },
  {
    id: "3",
    title: "Excellence Award",
    subtitle: "Outstanding Service",
    icon: <StarSolidIcon className="w-8 h-8" />,
    gradient: "from-blue-400 via-purple-400 to-purple-500",
    year: "2025",
    description: "Consistent 5-star service delivery",
    metric: "5-star service",
  },
  {
    id: "4",
    title: "Verified Partner",
    subtitle: "Trusted & Secure",
    icon: <CheckBadgeIcon className="w-8 h-8" />,
    gradient: "from-green-400 via-emerald-400 to-teal-500",
    year: "2025",
    description: "Verified business with secure booking",
    metric: "100% secure",
  },
  {
    id: "5",
    title: "Safety First",
    subtitle: "COVID-Safe Certified",
    icon: <ShieldCheckIcon className="w-8 h-8" />,
    gradient: "from-cyan-400 via-blue-400 to-indigo-500",
    year: "2025",
    description: "Enhanced safety protocols verified",
    metric: "Safety certified",
  },
  {
    id: "6",
    title: "Global Recognition",
    subtitle: "Best Middle East Tours",
    icon: <GlobeAltIcon className="w-8 h-8" />,
    gradient: "from-orange-400 via-red-400 to-pink-500",
    year: "2025",
    description: "Leading tour operator in the region",
    metric: "#1 in region",
  },
];

const testimonialStats = [
  { label: "Happy Travelers", value: "250K+" },
  { label: "Countries Covered", value: "15+" },
  { label: "Tour Experiences", value: "5K+" },
  { label: "Years of Excellence", value: "12+" },
];

const recentReviews = [
  {
    name: "Sarah M.",
    location: "New York, USA",
    rating: 5,
    comment:
      "Absolutely incredible experience! The Petra tour exceeded all expectations.",
    avatar: "🇺🇸",
  },
  {
    name: "Ahmed K.",
    location: "London, UK",
    rating: 5,
    comment: "Professional guides and seamless booking. Highly recommend!",
    avatar: "🇬🇧",
  },
  {
    name: "Maria L.",
    location: "Barcelona, Spain",
    rating: 5,
    comment: "Amazing value for money. Every detail was perfectly planned.",
    avatar: "🇪🇸",
  },
];

export default function TravelersChoiceBar() {
  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <StarSolidIcon
        key={i}
        className={`w-4 h-4 ${
          i < rating ? "text-yellow-400" : "text-gray-300"
        }`}
      />
    ));
  };

  return (
    <section className="py-16 bg-gradient-to-br from-gray-50 via-white to-gray-50">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center mb-4">
            <TrophyIcon className="w-12 h-12 text-yellow-500 mr-4" />
            <div>
              <h2 className="text-3xl font-bold text-gray-900">
                Award-Winning Excellence
              </h2>
              <p className="text-lg text-gray-600 mt-2">
                Recognized globally for outstanding travel experiences
              </p>
            </div>
          </div>
        </div>

        {/* Awards Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-16">
          {awards.map((award) => (
            <div
              key={award.id}
              className="group relative bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 text-center"
            >
              {/* Background Gradient */}
              <div
                className={`absolute inset-0 bg-gradient-to-br ${award.gradient} opacity-0 group-hover:opacity-10 rounded-2xl transition-opacity duration-300`}
              />

              {/* Icon */}
              <div
                className={`inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br ${award.gradient} rounded-full text-white mb-4 group-hover:scale-110 transition-transform duration-300`}
              >
                {award.icon}
              </div>

              {/* Content */}
              <div className="relative z-10">
                <h3 className="text-sm font-bold text-gray-900 mb-1">
                  {award.title}
                </h3>
                <p className="text-xs text-gray-600 mb-2">{award.subtitle}</p>
                <div className="text-xs text-gray-500 mb-2">{award.year}</div>
                {award.metric && (
                  <div
                    className={`inline-block px-2 py-1 bg-gradient-to-r ${award.gradient} text-white text-xs font-semibold rounded-full`}
                  >
                    {award.metric}
                  </div>
                )}
              </div>

              {/* Hover Effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-white/0 to-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl" />
            </div>
          ))}
        </div>

        {/* Stats Row */}
        <div className="bg-white rounded-3xl shadow-xl p-8 mb-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {testimonialStats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl font-bold bg-gradient-to-r from-orange-500 to-pink-500 bg-clip-text text-transparent mb-2">
                  {stat.value}
                </div>
                <div className="text-gray-600 font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Reviews Section */}
        <div className="bg-gradient-to-r from-orange-50 to-yellow-50 rounded-3xl p-8">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              What Our Travelers Say
            </h3>
            <p className="text-gray-600">
              Real experiences from verified travelers
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {recentReviews.map((review, index) => (
              <div
                key={index}
                className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow duration-300"
              >
                {/* Stars */}
                <div className="flex items-center mb-4">
                  {renderStars(review.rating)}
                </div>

                {/* Comment */}
                <p className="text-gray-700 mb-4 italic leading-relaxed">
                  &ldquo;{review.comment}&rdquo;
                </p>

                {/* Reviewer */}
                <div className="flex items-center">
                  <div className="text-2xl mr-3">{review.avatar}</div>
                  <div>
                    <div className="font-semibold text-gray-900">
                      {review.name}
                    </div>
                    <div className="text-sm text-gray-500">
                      {review.location}
                    </div>
                  </div>
                </div>

                {/* Verified Badge */}
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <div className="flex items-center text-sm text-green-600">
                    <CheckBadgeIcon className="w-4 h-4 mr-2" />
                    Verified Review
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Trust Indicators */}
          <div className="mt-8 pt-8 border-t border-orange-200">
            <div className="flex flex-wrap items-center justify-center gap-8 text-sm text-gray-600">
              <div className="flex items-center">
                <ShieldCheckIcon className="w-5 h-5 mr-2 text-green-500" />
                SSL Secured Booking
              </div>
              <div className="flex items-center">
                <CheckBadgeIcon className="w-5 h-5 mr-2 text-blue-500" />
                Verified Business
              </div>
              <div className="flex items-center">
                <HeartSolidIcon className="w-5 h-5 mr-2 text-red-500" />
                24/7 Customer Support
              </div>
              <div className="flex items-center">
                <TrophyIcon className="w-5 h-5 mr-2 text-yellow-500" />
                Award Winner 2025
              </div>
            </div>
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-12">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Join 250,000+ Happy Travelers
          </h3>
          <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
            Experience the difference that award-winning service makes. Book
            with confidence and create memories that last a lifetime.
          </p>
          <button className="bg-gradient-to-r from-orange-600 to-pink-600 hover:from-orange-700 hover:to-pink-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-200 hover:shadow-lg hover:scale-105">
            Start Your Journey Today
          </button>
        </div>
      </div>
    </section>
  );
}
