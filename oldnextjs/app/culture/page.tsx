"use client";

import React from "react";
import Header from "@/components/ui/Header";
import { motion } from "framer-motion";

const cultureExperiences = [
  {
    id: 1,
    title: "Historic City Walking Tour",
    location: "Old Town District",
    price: "$25",
    rating: 4.8,
    reviews: 342,
    image: "/hero/apartment.webp",
    duration: "3 hours",
    category: "Historical Sites",
  },
  {
    id: 2,
    title: "Art Gallery & Museum Pass",
    location: "Cultural Quarter",
    price: "$40",
    rating: 4.9,
    reviews: 578,
    image: "/hero/villa.webp",
    duration: "Full day",
    category: "Museums & Galleries",
  },
  {
    id: 3,
    title: "Traditional Craft Workshop",
    location: "Artisan Village",
    price: "$35",
    rating: 4.7,
    reviews: 234,
    image: "/hero/hotel.webp",
    duration: "2 hours",
    category: "Cultural Workshops",
  },
  {
    id: 4,
    title: "Architecture Discovery Tour",
    location: "Downtown",
    price: "$30",
    rating: 4.8,
    reviews: 456,
    image: "/hero/resort.webp",
    duration: "2.5 hours",
    category: "Architecture Tours",
  },
  {
    id: 5,
    title: "Local Festival Experience",
    location: "City Center",
    price: "$20",
    rating: 4.9,
    reviews: 123,
    image: "/hero/chalets.webp",
    duration: "4 hours",
    category: "Local Festivals",
  },
  {
    id: 6,
    title: "Heritage Site Guided Tour",
    location: "UNESCO Site",
    price: "$45",
    rating: 4.8,
    reviews: 289,
    image: "/hero/motels.webp",
    duration: "3.5 hours",
    category: "Heritage Sites",
  },
];

const categories = [
  "All Categories",
  "Museums & Galleries",
  "Historical Sites",
  "Architecture Tours",
  "Cultural Workshops",
  "Local Festivals",
  "Heritage Sites",
];

export default function CulturePage() {
  const [selectedCategory, setSelectedCategory] =
    React.useState("All Categories");

  const filteredExperiences =
    selectedCategory === "All Categories"
      ? cultureExperiences
      : cultureExperiences.filter((exp) => exp.category === selectedCategory);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="relative h-[40vh] flex items-center justify-center">
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: "url('/hero/apartment.webp')" }}
        >
          <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-purple-900/30 to-blue-900/40"></div>
        </div>

        <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-6">
          <motion.h1
            className="text-4xl md:text-5xl font-bold mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Cultural Experiences
          </motion.h1>
          <motion.p
            className="text-xl opacity-90"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Discover rich traditions, heritage sites, and immersive cultural
            activities
          </motion.p>
        </div>
      </section>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Category Filter */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-3">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  selectedCategory === category
                    ? "bg-blue-600 text-white"
                    : "bg-white text-gray-700 hover:bg-gray-100 border border-gray-200"
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Results Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            {filteredExperiences.length} Cultural Experiences
          </h2>
          <p className="text-gray-600 mt-1">
            {selectedCategory === "All Categories"
              ? "All categories"
              : selectedCategory}
          </p>
        </div>

        {/* Experience Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredExperiences.map((experience) => (
            <motion.div
              key={experience.id}
              className="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="aspect-[4/3] relative">
                <img
                  src={experience.image}
                  alt={experience.title}
                  className="w-full h-full object-cover"
                />
                <div className="absolute top-3 right-3 bg-white px-2 py-1 rounded-lg text-sm font-medium">
                  {experience.price}
                </div>
              </div>

              <div className="p-6">
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-2">
                  <span>{experience.category}</span>
                  <span>•</span>
                  <span>{experience.duration}</span>
                </div>

                <h3 className="font-semibold text-gray-900 mb-2">
                  {experience.title}
                </h3>

                <p className="text-gray-600 text-sm mb-3">
                  {experience.location}
                </p>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1">
                    <span className="text-yellow-400">★</span>
                    <span className="font-medium">{experience.rating}</span>
                    <span className="text-gray-500 text-sm">
                      ({experience.reviews})
                    </span>
                  </div>

                  <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors">
                    Book Now
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </main>
    </div>
  );
}
