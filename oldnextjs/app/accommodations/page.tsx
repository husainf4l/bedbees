"use client";

import { useState, useEffect, use } from "react";
import AccommodationHeroSection from "@/components/ui/AccommodationHeroSection";
import AccommodationCard from "@/components/ui/AccommodationCard";
import AccommodationSearchBar from "@/components/ui/AccommodationSearchBar";
import { Apartment } from "@/types/common";
import { accommodationService } from "@/services/accommodation.service";

interface SearchData {
  destination: string;
  checkIn: string;
  checkOut: string;
  guests: {
    adults: number;
    children: number;
    rooms: number;
  };
}

export default function Accommodations({
  searchParams,
}: {
  searchParams: Promise<{ type?: string }>;
}) {
  const resolvedSearchParams = use(searchParams);
  const type = resolvedSearchParams?.type || "all";
  const [apartments, setApartments] = useState<Apartment[]>([]);
  const [loading, setLoading] = useState(true);
  const [categoryContent, setCategoryContent] = useState<{
    title: string;
    subtitle: string;
    image: string;
    sectionTitle: string;
    message: string;
  } | null>(null);

  useEffect(() => {
    const fetchAccommodations = async () => {
      try {
        setLoading(true);
        let data: Apartment[];

        if (type && type !== "all") {
          // Use category-specific endpoint when a type is specified
          data = await accommodationService.getAccommodationsByCategory(type);
        } else {
          // Use general endpoint for all accommodations
          data = await accommodationService.getAccommodations();
        }

        setApartments(data);
      } catch (error) {
        console.error("Failed to fetch accommodations:", error);
        setApartments([]);
      } finally {
        setLoading(false);
      }
    };

    const fetchCategoryContent = async () => {
      try {
        const content = await accommodationService.getCategoryContent(type);
        setCategoryContent(content);
      } catch (error) {
        console.error("Failed to fetch category content:", error);
      }
    };

    fetchAccommodations();
    fetchCategoryContent();
  }, [type]);

  const handleSearch = (searchData: SearchData) => {
    console.log("Search data:", searchData);
    // TODO: Implement search functionality
    // Filter apartments based on destination, dates, and guests
  };

  return (
    <div>
      {categoryContent ? (
        <AccommodationHeroSection
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

      {/* Search Bar Section */}
      <div className="relative -mt-24 z-10">
        <div className="max-w-6xl mx-auto px-6">
          <AccommodationSearchBar onSearch={handleSearch} />
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12 pt-20">
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
                Loading Accommodations...
              </h2>
              <p className="text-lg text-gray-600">
                Please wait while we load the content.
              </p>
            </>
          )}
        </div>

        {loading ? (
          <div className="text-center py-8">
            <p className="text-gray-600">Loading accommodations...</p>
          </div>
        ) : (
          <AccommodationCard apartments={apartments} />
        )}
      </div>
    </div>
  );
}
