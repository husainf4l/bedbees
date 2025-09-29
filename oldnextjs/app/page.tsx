"use client";

import HeroSection from "@/components/ui/HeroSection";
import FiltersBar from "@/components/FiltersBar";
import DestinationStrip from "@/components/ui/DestinationStrip";
import DealsCarousel from "@/components/ui/DealsCarousel";
import TopAttractionsGrid from "@/components/ui/TopAttractionsGrid";
import TravelersChoiceBar from "@/components/ui/TravelersChoiceBar";
import FoodExperiencesGrid from "@/components/ui/FoodExperiencesGrid";
import AdventureToursGrid from "@/components/ui/AdventureToursGrid";
import WellnessRetreatGrid from "@/components/ui/WellnessRetreatGrid";
import HotelsDemo from "@/components/ui/HotelsDemo";
import GeniusLoyaltyProgram from "@/components/ui/GeniusLoyaltyProgram";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Left Sidebar - Filters */}
      <aside className="fixed left-0 top-0 h-full z-40">
        <FiltersBar />
      </aside>

      {/* Main Content */}
      <div className="ml-72 min-h-screen">
        {/* Hero Section - Full Width */}
        <HeroSection />

        {/* Content Sections */}
        <main className="relative">
          {/* Popular Destinations */}
          <section className="py-12 px-6">
            <DestinationStrip />
          </section>

          {/* Limited Time Deals */}
          <section className="py-12 px-6 bg-white">
            <DealsCarousel />
          </section>

          {/* Featured Hotels & Accommodations */}
          <section className="py-12 px-6">
            <HotelsDemo />
          </section>

          {/* Genius Loyalty Program */}
          <section className="py-6 px-6">
            <GeniusLoyaltyProgram />
          </section>

          {/* Top Attractions & Experiences */}
          <section className="py-12 px-6 bg-white">
            <TopAttractionsGrid />
          </section>

          {/* Award-Winning Excellence & Reviews */}
          <section className="py-12 px-6">
            <TravelersChoiceBar />
          </section>

          {/* Culinary Experiences */}
          <section className="py-12 px-6 bg-white">
            <FoodExperiencesGrid />
          </section>

          {/* Adventure Tours */}
          <section className="py-12 px-6">
            <AdventureToursGrid />
          </section>

          {/* Wellness & Spa Retreats */}
          <section className="py-12 px-6 bg-white">
            <WellnessRetreatGrid />
          </section>
        </main>
      </div>
    </div>
  );
}
