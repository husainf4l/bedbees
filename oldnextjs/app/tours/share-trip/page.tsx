"use client";

import { useState, useEffect } from "react";
import TourHeroSection from "@/components/ui/TourHeroSection";
import TourCard from "@/components/ui/TourCard";
import ExperienceSearchBar from "@/components/ui/ExperienceSearchBar";
import { Tour } from "@/types/tour";
import { tourService } from "@/services/tour.service";

export default function ShareTripToursPage() {
  const [tours, setTours] = useState<Tour[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTours = async () => {
      try {
        setLoading(true);
        const data = await tourService.getToursByCategory("share_trip");
        setTours(data);
      } catch (error) {
        console.error("Failed to fetch share trip tours:", error);
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
        image="/hero/travelhero.webp"
        title="Join Fellow Travelers on Share Trips"
        subtitle="Meet like-minded travelers and explore together"
      />

      {/* Experience Search Bar Section */}
      <div className="relative -mt-20 z-10 max-w-6xl mx-auto px-6">
        <ExperienceSearchBar
          onSearch={(searchData) => {
            console.log("Experience search:", searchData);
            // Filter for share_trip category
            window.location.href = `/tours?search=${encodeURIComponent(
              JSON.stringify({ ...searchData, category: "share_trip" })
            )}`;
          }}
        />
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Share Trip Experiences
          </h2>
          <p className="text-lg text-gray-600">
            Connect with fellow travelers and share unforgettable experiences.
            Our share trips bring together small groups of like-minded
            adventurers for authentic local experiences.
          </p>
        </div>

        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading share trip tours...</p>
          </div>
        ) : tours.length > 0 ? (
          <TourCard tours={tours} />
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">
              No share trip tours available at the moment.
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
