"use client";

import React from "react";
import Header from "@/components/ui/Header";
import { motion } from "framer-motion";

const natureExperiences = [
  {
    id: 1,
    title: "Mountain Hiking Adventure",
    location: "Alpine Trails",
    price: "$55",
    rating: 4.8,
    reviews: 512,
    image: "/hero/chalets.webp",
    duration: "6 hours",
    category: "Hiking Adventures",
  },
  {
    id: 2,
    title: "Wildlife Safari Experience",
    location: "National Park",
    price: "$75",
    rating: 4.9,
    reviews: 378,
    image: "/hero/resort.webp",
    duration: "4 hours",
    category: "Wildlife Watching",
  },
  {
    id: 3,
    title: "Beach & Coastal Exploration",
    location: "Coastal Reserve",
    price: "$40",
    rating: 4.7,
    reviews: 423,
    image: "/hero/villa.webp",
    duration: "3 hours",
    category: "Beach Experiences",
  },
  {
    id: 4,
    title: "Botanical Garden Tour",
    location: "City Gardens",
    price: "$25",
    rating: 4.6,
    reviews: 234,
    image: "/hero/apartment.webp",
    duration: "2 hours",
    category: "Gardens & Parks",
  },
  {
    id: 5,
    title: "Kayaking & Water Sports",
    location: "Lake District",
    price: "$65",
    rating: 4.8,
    reviews: 345,
    image: "/hero/hotel.webp",
    duration: "3.5 hours",
    category: "Water Sports",
  },
  {
    id: 6,
    title: "Eco-Tourism Adventure",
    location: "Conservation Area",
    price: "$80",
    rating: 4.9,
    reviews: 156,
    image: "/hero/treehouses.webp",
    duration: "5 hours",
    category: "Eco Tours",
  },
];

const categories = [
  "All Categories",
  "Hiking Adventures",
  "Wildlife Watching",
  "Beach Experiences",
  "Mountain Adventures",
  "Gardens & Parks",
  "Water Sports",
  "Eco Tours",
  "Camping Experiences",
];

export default function NaturePage() {
  const [selectedCategory, setSelectedCategory] =
    React.useState("All Categories");

  const filteredExperiences =
    selectedCategory === "All Categories"
      ? natureExperiences
      : natureExperiences.filter((exp) => exp.category === selectedCategory);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="relative h-[40vh] flex items-center justify-center">
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: "url('/hero/treehouses.webp')" }}
        >
          <div className="absolute inset-0 bg-gradient-to-br from-black/60 via-green-900/30 to-blue-900/40"></div>
        </div>

        <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-6">
          <motion.h1
            className="text-4xl md:text-5xl font-bold mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Nature Experiences
          </motion.h1>
          <motion.p
            className="text-xl opacity-90"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Connect with nature through wildlife, hiking, and outdoor adventures
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
                    ? "bg-green-600 text-white"
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
            {filteredExperiences.length} Nature Experiences
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

                  <button className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors">
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
