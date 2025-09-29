"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/providers/AuthContext";
import ListPropertyCategories from "@/components/ui/ListPropertyCategories";
import AccommodationRegistrationForm from "@/components/ui/AccommodationRegistrationForm";
import TourRegistrationForm from "@/components/ui/TourRegistrationForm";

type ViewState = "categories" | "accommodation-form" | "tour-form";

export default function HostDashboard() {
  const router = useRouter();
  const { user } = useAuth();
  const [currentView, setCurrentView] = useState<ViewState>("categories");
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [selectedSubcategory, setSelectedSubcategory] = useState<string>("");

  // Debug: Check authentication status
  useEffect(() => {
    console.log("HostDashboard - User:", user);
    console.log("HostDashboard - Token:", localStorage.getItem("accessToken"));

    // Redirect to login if not authenticated
    if (!user && !localStorage.getItem("accessToken")) {
      console.log("No user or token found, redirecting to login");
      router.push("/login");
    }
  }, [user, router]);

  const handleCategorySelect = (category: string, subcategory?: string) => {
    console.log("Selected category:", category, "subcategory:", subcategory);

    setSelectedCategory(category);
    setSelectedSubcategory(subcategory || "");

    // Navigate to appropriate form based on category
    if (category === "accommodations") {
      setCurrentView("accommodation-form");
    } else if (category === "tours" && subcategory) {
      setCurrentView("tour-form");
    }
  };

  const handleFormSubmit = (response: unknown) => {
    console.log("Form submitted with response:", response);

    // If response has an ID, navigate to the accommodations list in host dashboard
    if (response && (response.id || response.data?.id)) {
      const accommodationId = response.id || response.data?.id;
      console.log("Accommodation created successfully:", accommodationId);
      // Navigate to host dashboard accommodations list instead of individual accommodation
      router.push(`/hostdashboard/accommodations`);
    } else {
      console.warn("No valid ID in response:", response);
      // Fallback: navigate back to dashboard
      console.log("No ID in response, navigating to dashboard");
      setCurrentView("categories");
    }
  };

  const handleFormCancel = () => {
    setCurrentView("categories");
    setSelectedCategory("");
    setSelectedSubcategory("");
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case "accommodation-form":
        return (
          <AccommodationRegistrationForm
            selectedCategory={selectedSubcategory}
            onSubmit={handleFormSubmit}
            onCancel={handleFormCancel}
            currentUser={user}
          />
        );

      case "tour-form":
        return (
          <TourRegistrationForm
            selectedCategory={selectedSubcategory}
            onSubmit={handleFormSubmit}
            onCancel={handleFormCancel}
            currentUser={user}
          />
        );

      case "categories":
      default:
        return (
          <ListPropertyCategories onCategorySelect={handleCategorySelect} />
        );
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Host Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Manage your tours and accommodations
        </p>
      </div>

      {/* Breadcrumb */}
      {currentView !== "categories" && (
        <div className="mb-6">
          <nav className="flex" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-4">
              <li>
                <button
                  onClick={() => setCurrentView("categories")}
                  className="text-gray-400 hover:text-gray-500 transition-colors"
                >
                  Categories
                </button>
              </li>
              <li>
                <svg
                  className="flex-shrink-0 h-5 w-5 text-gray-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
              </li>
              <li>
                <span className="text-gray-500">
                  {selectedCategory === "accommodations"
                    ? "Accommodation"
                    : "My Tour"}{" "}
                  Registration
                </span>
              </li>
              {selectedSubcategory && (
                <>
                  <li>
                    <svg
                      className="flex-shrink-0 h-5 w-5 text-gray-400"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </li>
                  <li>
                    <span className="text-gray-900 font-medium capitalize">
                      {selectedSubcategory.replace("-", " ")}
                    </span>
                  </li>
                </>
              )}
            </ol>
          </nav>
        </div>
      )}

      {renderCurrentView()}
    </div>
  );
}
