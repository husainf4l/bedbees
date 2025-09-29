"use client";

import React, { useState } from "react";
import Link from "next/link";
import { HeroMegaMenu, Category } from "./HeroMegaMenu";
import { cn } from "@/lib/utils";

interface TopNavProps {
  categories: Category[];
  activeId?: string;
  className?: string;
}

export const TopNav: React.FC<TopNavProps> = ({
  categories,
  activeId,
  className,
}) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <header
      className={cn(
        "relative bg-gradient-to-r from-blue-600 to-purple-700",
        className
      )}
    >
      {/* Background pattern overlay */}
      <div className="absolute inset-0 bg-black/10"></div>

      {/* Navigation bar */}
      <nav className="relative z-10 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-28">
            {/* Logo and Main Navigation - Stacked Layout */}
            <div className="flex flex-col items-start">
              {/* Logo */}
              <Link href="/" className="flex items-center gap-2 mb-2">
                <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
                  <svg
                    className="w-6 h-6 text-blue-600"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <span className="text-2xl font-bold text-white">ShareTrip</span>
              </Link>

              {/* Main Navigation Links - Below Logo */}
              <div className="hidden lg:flex items-center gap-6">
                <Link
                  href="/tours"
                  className="text-white/90 hover:text-white transition-colors text-sm font-medium"
                >
                  Experiences
                </Link>
                <Link
                  href="/accommodations"
                  className="text-white/90 hover:text-white transition-colors text-sm font-medium"
                >
                  Accommodations
                </Link>
                <Link
                  href="/destinations"
                  className="text-white/90 hover:text-white transition-colors text-sm font-medium"
                >
                  Destinations
                </Link>
              </div>
            </div>

            {/* Search Bar */}
            <div className="hidden md:flex flex-1 max-w-lg mx-8">
              <div className="relative w-full">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg
                    className="h-5 w-5 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                </div>
                <input
                  type="text"
                  placeholder="Search experiences..."
                  className="block w-full pl-10 pr-3 py-2 border border-transparent rounded-lg bg-white/10 backdrop-blur-sm text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/20 focus:border-transparent"
                />
              </div>
            </div>

            {/* Right Navigation */}
            <div className="flex items-center gap-4">
              {/* Mobile search button */}
              <button className="md:hidden p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors">
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
                <span className="sr-only">Search</span>
              </button>

              {/* Mobile menu button */}
              <button
                className="lg:hidden p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d={
                      isMobileMenuOpen
                        ? "M6 18L18 6M6 6l12 12"
                        : "M4 6h16M4 12h16M4 18h16"
                    }
                  />
                </svg>
                <span className="sr-only">Menu</span>
              </button>

              {/* Navigation Links */}
              <div className="hidden lg:flex items-center gap-6">
                <Link
                  href="/become-host"
                  className="text-white/90 hover:text-white transition-colors text-sm font-medium"
                >
                  Become a Host
                </Link>
                <Link
                  href="/help"
                  className="text-white/90 hover:text-white transition-colors text-sm font-medium"
                >
                  Help
                </Link>
              </div>

              {/* User Menu */}
              <div className="flex items-center gap-2">
                <button className="p-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors">
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                    />
                  </svg>
                  <span className="sr-only">User menu</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-white border-b border-gray-200">
          <div className="px-4 py-4 space-y-4">
            <Link
              href="/tours"
              className="block px-3 py-2 text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Experiences
            </Link>
            <Link
              href="/accommodations"
              className="block px-3 py-2 text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Accommodations
            </Link>
            <Link
              href="/destinations"
              className="block px-3 py-2 text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Destinations
            </Link>
            <div className="border-t border-gray-200 pt-4">
              <Link
                href="/become-host"
                className="block px-3 py-2 text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Become a Host
              </Link>
              <Link
                href="/help"
                className="block px-3 py-2 text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                Help
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* Hero Section */}
      <div className="relative z-10 pt-20 pb-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          {/* Hero Content */}
          <div className="mb-12">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
              Discover Amazing
              <br />
              <span className="bg-gradient-to-r from-yellow-400 to-pink-400 bg-clip-text text-transparent">
                Experiences
              </span>
            </h1>
            <p className="text-xl text-white/90 max-w-2xl mx-auto leading-relaxed">
              Book unforgettable activities, tours, and experiences around the
              world. From cultural adventures to outdoor thrills.
            </p>
          </div>

          {/* Hero Mega Menu */}
          <div className="flex justify-center">
            <HeroMegaMenu
              categories={categories}
              activeId={activeId}
              className="relative z-20"
            />
          </div>
        </div>
      </div>

      {/* Decorative Elements */}
      <div className="absolute top-20 left-10 w-20 h-20 bg-white/5 rounded-full blur-xl"></div>
      <div className="absolute top-32 right-20 w-32 h-32 bg-pink-400/20 rounded-full blur-2xl"></div>
      <div className="absolute bottom-20 left-1/4 w-16 h-16 bg-yellow-400/20 rounded-full blur-xl"></div>
    </header>
  );
};
