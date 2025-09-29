"use client";

import { useState, useEffect } from "react";
import TourHeroSection from "@/components/ui/TourHeroSection";
import TourCard from "@/components/ui/TourCard";
import ExperienceSearchBar from "@/components/ui/ExperienceSearchBar";
import { Tour } from "@/types/tour";
import { tourService } from "@/services/tour.service";

export default function GroupToursPage() {
  const [tours, setTours] = useState<Tour[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTours = async () => {
      try {
        setLoading(true);
        const data = await tourService.getToursByCategory("group");
        setTours(data);
      } catch (error) {
        console.error("Failed to fetch group tours:", error);
        setTours([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTours();
  }, []);

  return (
    <div>
      <TourHeroSection
        image="/hero/apartment.webp"
        title="Join Organized Group Tours"
        subtitle="Explore with expert guides and fellow adventurers"
      />

      {/* Experience Search Bar Section */}
      <div className="relative -mt-20 z-10 max-w-6xl mx-auto px-6">
        <ExperienceSearchBar
          onSearch={(searchData) => {
            console.log("Experience search:", searchData);
            // Filter for group category
            window.location.href = `/tours?search=${encodeURIComponent(
              JSON.stringify({ ...searchData, category: "group" })
            )}`;
          }}
        />
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Group Adventures
          </h2>
          <p className="text-lg text-gray-600">
            Discover amazing places with our expertly guided group tours. Join
            fellow travelers for structured experiences with professional guides
            and comprehensive itineraries.
          </p>
        </div>

        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading group tours...</p>
          </div>
        ) : tours.length > 0 ? (
          <TourCard tours={tours} />
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">
              No group tours available at the moment.
            </p>
            <p className="text-gray-500 mt-2">
              Check back soon for new experiences!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
