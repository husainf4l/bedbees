"use client";

import { useState, useEffect, use } from "react";
import TourHeroSection from "@/components/ui/TourHeroSection";
import TourCard from "@/components/ui/TourCard";
import ExperienceSearchBar from "@/components/ui/ExperienceSearchBar";
import { Tour } from "@/types/tour";
import { tourService } from "@/services/tour.service";

export default function ToursPage({
  searchParams,
}: {
  searchParams: Promise<{ type?: string }>;
}) {
  const resolvedSearchParams = use(searchParams);
  const type = resolvedSearchParams?.type || "all";
  const [tours, setTours] = useState<Tour[]>([]);
  const [loading, setLoading] = useState(true);
  const [categoryContent, setCategoryContent] = useState<{
    title: string;
    subtitle: string;
    image: string;
    sectionTitle: string;
    message: string;
  } | null>(null);

  useEffect(() => {
    const fetchTours = async () => {
      try {
        setLoading(true);
        let data: Tour[];

        if (type && type !== "all") {
          // Use category-specific endpoint when a type is specified
          data = await tourService.getToursByCategory(type);
        } else {
          // Use general endpoint for all tours
          data = await tourService.getTours();
        }

        setTours(data);
      } catch (error) {
        console.error("Failed to fetch tours:", error);
        setTours([]);
      } finally {
        setLoading(false);
      }
    };

    const fetchCategoryContent = async () => {
      try {
        const content = await tourService.getCategoryContent(type);
        setCategoryContent(content);
      } catch (error) {
        console.warn(
          "Using fallback category content due to API error:",
          error
        );
        // Set fallback content if API fails
        setCategoryContent({
          title: "Discover Amazing Tours & Experiences",
          subtitle:
            "Join unique experiences with local guides and fellow travelers",
          image: "/hero/travelhero.webp",
          sectionTitle: "All Tours & Experiences",
          message: "Explore our curated collection of tours and experiences...",
        });
      }
    };

    fetchTours();
    fetchCategoryContent();
  }, [type]);

  return (
    <div>
      {categoryContent ? (
        <TourHeroSection
          image={categoryContent.image}
          title={categoryContent.title}
          subtitle={categoryContent.subtitle}
        />
      ) : (
        <div className="h-96 bg-gray-200 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading...</p>
          </div>
        </div>
      )}

      {/* Experience Search Bar Section */}
      <div className="relative -mt-20 z-10 max-w-6xl mx-auto px-6">
        <ExperienceSearchBar
          onSearch={(searchData) => {
            console.log("Experience search:", searchData);
            // Here you can implement search filtering logic
          }}
        />
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="text-center mb-8">
          {categoryContent ? (
            <>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                {categoryContent.sectionTitle}
              </h2>
              <p className="text-lg text-gray-600">{categoryContent.message}</p>
            </>
          ) : (
            <>
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Loading Tours & Experiences...
              </h2>
              <p className="text-lg text-gray-600">
                Please wait while we load the content.
              </p>
            </>
          )}
        </div>

        {loading ? (
          <div className="text-center py-8">
            <p className="text-gray-600">Loading tours...</p>
          </div>
        ) : (
          <TourCard tours={tours} />
        )}
      </div>
    </div>
  );
}
