"use client";

import React from "react";
import { TopNav } from "@/components/TopNav";
import { Category } from "@/components/HeroMegaMenu";

// Sample data for the mega menu
const sampleCategories: Category[] = [
  {
    id: "for-you",
    label: "For you",
    items: [
      {
        href: "/experiences/trending",
        title: "Trending Now",
        img: "/hero/travelhero.webp",
        alt: "Trending experiences"
      },
      {
        href: "/experiences/popular",
        title: "Most Popular",
        img: "/hero/hero1.webp",
        alt: "Popular experiences"
      },
      {
        href: "/experiences/new",
        title: "New Experiences",
        img: "/hero/apartment.webp",
        alt: "New experiences"
      },
      {
        href: "/experiences/deals",
        title: "Special Deals",
        img: "/hero/hotel.webp",
        alt: "Special deal experiences"
      },
      {
        href: "/experiences/local-favorites",
        title: "Local Favorites",
        img: "/hero/villa.webp",
        alt: "Local favorite experiences"
      },
      {
        href: "/experiences/weekend",
        title: "Weekend Getaways",
        img: "/hero/resort.webp",
        alt: "Weekend getaway experiences"
      },
      {
        href: "/experiences/romantic",
        title: "Romantic Experiences",
        img: "/hero/chalets.webp",
        alt: "Romantic experiences"
      },
      {
        href: "/experiences/family",
        title: "Family Fun",
        img: "/hero/treehouses.webp",
        alt: "Family-friendly experiences"
      }
    ]
  },
  {
    id: "culture",
    label: "Culture",
    items: [
      {
        href: "/culture/museums",
        title: "Museums & Galleries",
        img: "/hero/apartment.webp",
        alt: "Museums and galleries"
      },
      {
        href: "/culture/historical",
        title: "Historical Sites",
        img: "/hero/villa.webp",
        alt: "Historical sites"
      },
      {
        href: "/culture/architecture",
        title: "Architecture Tours",
        img: "/hero/hotel.webp",
        alt: "Architecture tours"
      },
      {
        href: "/culture/art",
        title: "Art Experiences",
        img: "/hero/resort.webp",
        alt: "Art experiences"
      },
      {
        href: "/culture/festivals",
        title: "Local Festivals",
        img: "/hero/chalets.webp",
        alt: "Local festivals"
      },
      {
        href: "/culture/traditions",
        title: "Cultural Traditions",
        img: "/hero/motels.webp",
        alt: "Cultural traditions"
      },
      {
        href: "/culture/workshops",
        title: "Cultural Workshops",
        img: "/hero/treehouses.webp",
        alt: "Cultural workshops"
      },
      {
        href: "/culture/heritage",
        title: "Heritage Sites",
        img: "/hero/hostels.webp",
        alt: "Heritage sites"
      }
    ]
  },
  {
    id: "food",
    label: "Food",
    items: [
      {
        href: "/food/cooking-classes",
        title: "Cooking Classes",
        img: "/hero/villa.webp",
        alt: "Cooking classes"
      },
      {
        href: "/food/food-tours",
        title: "Food Tours",
        img: "/hero/hotel.webp",
        alt: "Food tours"
      },
      {
        href: "/food/wine-tasting",
        title: "Wine Tasting",
        img: "/hero/resort.webp",
        alt: "Wine tasting experiences"
      },
      {
        href: "/food/street-food",
        title: "Street Food Adventures",
        img: "/hero/apartment.webp",
        alt: "Street food adventures"
      },
      {
        href: "/food/markets",
        title: "Local Markets",
        img: "/hero/chalets.webp",
        alt: "Local market tours"
      },
      {
        href: "/food/fine-dining",
        title: "Fine Dining",
        img: "/hero/motels.webp",
        alt: "Fine dining experiences"
      },
      {
        href: "/food/brewery",
        title: "Brewery Tours",
        img: "/hero/treehouses.webp",
        alt: "Brewery tours"
      },
      {
        href: "/food/desserts",
        title: "Dessert Experiences",
        img: "/hero/hostels.webp",
        alt: "Dessert experiences"
      }
    ]
  },
  {
    id: "nature",
    label: "Nature",
    items: [
      {
        href: "/nature/hiking",
        title: "Hiking Adventures",
        img: "/hero/treehouses.webp",
        alt: "Hiking adventures"
      },
      {
        href: "/nature/wildlife",
        title: "Wildlife Watching",
        img: "/hero/resort.webp",
        alt: "Wildlife watching"
      },
      {
        href: "/nature/beaches",
        title: "Beach Experiences",
        img: "/hero/villa.webp",
        alt: "Beach experiences"
      },
      {
        href: "/nature/mountains",
        title: "Mountain Adventures",
        img: "/hero/chalets.webp",
        alt: "Mountain adventures"
      },
      {
        href: "/nature/gardens",
        title: "Gardens & Parks",
        img: "/hero/apartment.webp",
        alt: "Gardens and parks"
      },
      {
        href: "/nature/water-sports",
        title: "Water Sports",
        img: "/hero/hotel.webp",
        alt: "Water sports"
      },
      {
        href: "/nature/eco-tours",
        title: "Eco Tours",
        img: "/hero/motels.webp",
        alt: "Eco tours"
      },
      {
        href: "/nature/camping",
        title: "Camping Experiences",
        img: "/hero/hostels.webp",
        alt: "Camping experiences"
      }
    ]
  },
  {
    id: "adventure",
    label: "Adventure",
    items: [
      {
        href: "/adventure/extreme-sports",
        title: "Extreme Sports",
        img: "/hero/treehouses.webp",
        alt: "Extreme sports"
      },
      {
        href: "/adventure/skydiving",
        title: "Skydiving",
        img: "/hero/resort.webp",
        alt: "Skydiving experiences"
      },
      {
        href: "/adventure/rock-climbing",
        title: "Rock Climbing",
        img: "/hero/chalets.webp",
        alt: "Rock climbing"
      },
      {
        href: "/adventure/bungee",
        title: "Bungee Jumping",
        img: "/hero/villa.webp",
        alt: "Bungee jumping"
      },
      {
        href: "/adventure/zip-lining",
        title: "Zip Lining",
        img: "/hero/hotel.webp",
        alt: "Zip lining"
      },
      {
        href: "/adventure/rafting",
        title: "White Water Rafting",
        img: "/hero/apartment.webp",
        alt: "White water rafting"
      },
      {
        href: "/adventure/paragliding",
        title: "Paragliding",
        img: "/hero/motels.webp",
        alt: "Paragliding"
      },
      {
        href: "/adventure/caving",
        title: "Cave Exploration",
        img: "/hero/hostels.webp",
        alt: "Cave exploration"
      }
    ]
  }
];

export default function HeroMegaMenuDemo() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation with Hero Mega Menu */}
      <TopNav
        categories={sampleCategories}
        activeId="for-you"
        className="mb-0"
      />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Hero Mega Menu Demo
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            This demo showcases a GetYourGuide-style hero mega menu with pills, hover intent,
            keyboard navigation, and mobile-responsive design.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {[
            {
              title: "Hover Intent",
              description: "Pills open mega menu panels with 150ms hover delay for better UX",
              icon: "🎯"
            },
            {
              title: "Keyboard Navigation",
              description: "Full keyboard support with arrow keys, Enter, Space, and Escape",
              icon: "⌨️"
            },
            {
              title: "Mobile Responsive",
              description: "Horizontal scroll pills with slide-down drawer for mobile",
              icon: "📱"
            },
            {
              title: "Accessibility",
              description: "ARIA compliant with proper roles, labels, and focus management",
              icon: "♿"
            },
            {
              title: "Animations",
              description: "Smooth framer-motion animations with reduced motion support",
              icon: "✨"
            },
            {
              title: "SSR Safe",
              description: "No hydration mismatches, fully compatible with Next.js App Router",
              icon: "⚡"
            }
          ].map((feature) => (
            <div
              key={feature.title}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
            >
              <div className="text-3xl mb-4">{feature.icon}</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 rounded-2xl p-8 border border-blue-100">
          <h3 className="text-xl font-semibold text-blue-900 mb-4">
            How to Use
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-blue-800 mb-2">Desktop</h4>
              <ul className="text-blue-700 space-y-1 text-sm">
                <li>• Hover over pills to open mega menu</li>
                <li>• Use arrow keys to navigate between pills</li>
                <li>• Press Enter/Space to toggle menu</li>
                <li>• Press Escape to close menu</li>
                <li>• Click outside to close</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-blue-800 mb-2">Mobile</h4>
              <ul className="text-blue-700 space-y-1 text-sm">
                <li>• Scroll horizontally through pills</li>
                <li>• Tap pills to open slide-down drawer</li>
                <li>• Tap category headers to expand</li>
                <li>• Tap outside or close button to dismiss</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Sample Content */}
        <div className="mt-16">
          <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            Featured Experiences
          </h3>
          <div className="grid md:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100">
                <div className="aspect-[4/3] bg-gradient-to-br from-blue-400 to-purple-500"></div>
                <div className="p-6">
                  <h4 className="font-semibold text-gray-900 mb-2">
                    Sample Experience {i}
                  </h4>
                  <p className="text-gray-600 text-sm">
                    This is a sample experience card to demonstrate the layout below the hero section.
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}