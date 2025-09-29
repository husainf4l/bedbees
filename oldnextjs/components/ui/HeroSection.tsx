"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";
import Link from "next/link";
import { cn } from "@/lib/utils";

// Types for mega menu
export interface NavItem {
  href: string;
  title: string;
  img: string;
  alt: string;
}

export interface Category {
  id: string;
  label: string;
  items: NavItem[];
}

interface HeroSectionProps {
  categories?: Category[];
  activeId?: string;
}

// Sample categories data
const defaultCategories: Category[] = [
  {
    id: "for-you",
    label: "For you",
    items: [
      {
        href: "/experiences/trending",
        title: "Trending Now",
        img: "/hero/travelhero.webp",
        alt: "Trending experiences",
      },
      {
        href: "/experiences/popular",
        title: "Most Popular",
        img: "/hero/hero1.webp",
        alt: "Popular experiences",
      },
      {
        href: "/experiences/new",
        title: "New Experiences",
        img: "/hero/apartment.webp",
        alt: "New experiences",
      },
      {
        href: "/experiences/deals",
        title: "Special Deals",
        img: "/hero/hotel.webp",
        alt: "Special deal experiences",
      },
      {
        href: "/experiences/local-favorites",
        title: "Local Favorites",
        img: "/hero/villa.webp",
        alt: "Local favorite experiences",
      },
      {
        href: "/experiences/weekend",
        title: "Weekend Getaways",
        img: "/hero/resort.webp",
        alt: "Weekend getaway experiences",
      },
    ],
  },
  {
    id: "culture",
    label: "Culture",
    items: [
      {
        href: "/culture",
        title: "All Cultural Experiences",
        img: "/hero/apartment.webp",
        alt: "All cultural experiences",
      },
      {
        href: "/culture#museums",
        title: "Museums & Galleries",
        img: "/hero/apartment.webp",
        alt: "Museums and galleries",
      },
      {
        href: "/culture#historical",
        title: "Historical Sites",
        img: "/hero/villa.webp",
        alt: "Historical sites",
      },
      {
        href: "/culture#architecture",
        title: "Architecture Tours",
        img: "/hero/hotel.webp",
        alt: "Architecture tours",
      },
      {
        href: "/culture#art",
        title: "Art Experiences",
        img: "/hero/resort.webp",
        alt: "Art experiences",
      },
      {
        href: "/culture#festivals",
        title: "Local Festivals",
        img: "/hero/chalets.webp",
        alt: "Local festivals",
      },
    ],
  },
  {
    id: "food",
    label: "Food",
    items: [
      {
        href: "/food",
        title: "All Food Experiences",
        img: "/hero/villa.webp",
        alt: "All food experiences",
      },
      {
        href: "/food#cooking",
        title: "Cooking Classes",
        img: "/hero/villa.webp",
        alt: "Cooking classes",
      },
      {
        href: "/food#tours",
        title: "Food Tours",
        img: "/hero/hotel.webp",
        alt: "Food tours",
      },
      {
        href: "/food#wine",
        title: "Wine Tasting",
        img: "/hero/resort.webp",
        alt: "Wine tasting experiences",
      },
      {
        href: "/food#street-food",
        title: "Street Food Adventures",
        img: "/hero/apartment.webp",
        alt: "Street food adventures",
      },
      {
        href: "/food#markets",
        title: "Local Markets",
        img: "/hero/chalets.webp",
        alt: "Local market tours",
      },
    ],
  },
  {
    id: "nature",
    label: "Nature",
    items: [
      {
        href: "/nature",
        title: "All Nature Experiences",
        img: "/hero/treehouses.webp",
        alt: "All nature experiences",
      },
      {
        href: "/nature#hiking",
        title: "Hiking Adventures",
        img: "/hero/treehouses.webp",
        alt: "Hiking adventures",
      },
      {
        href: "/nature#wildlife",
        title: "Wildlife Watching",
        img: "/hero/resort.webp",
        alt: "Wildlife watching",
      },
      {
        href: "/nature#beaches",
        title: "Beach Experiences",
        img: "/hero/villa.webp",
        alt: "Beach experiences",
      },
      {
        href: "/nature#mountains",
        title: "Mountain Adventures",
        img: "/hero/chalets.webp",
        alt: "Mountain adventures",
      },
      {
        href: "/nature#water-sports",
        title: "Water Sports",
        img: "/hero/hotel.webp",
        alt: "Water sports",
      },
    ],
  },
  {
    id: "adventure",
    label: "Adventure",
    items: [
      {
        href: "/adventure",
        title: "All Adventure Experiences",
        img: "/hero/resort.webp",
        alt: "All adventure experiences",
      },
      {
        href: "/adventure#extreme",
        title: "Extreme Sports",
        img: "/hero/treehouses.webp",
        alt: "Extreme sports",
      },
      {
        href: "/adventure#skydiving",
        title: "Skydiving",
        img: "/hero/resort.webp",
        alt: "Skydiving experiences",
      },
      {
        href: "/adventure#climbing",
        title: "Rock Climbing",
        img: "/hero/chalets.webp",
        alt: "Rock climbing",
      },
      {
        href: "/adventure#bungee",
        title: "Bungee Jumping",
        img: "/hero/villa.webp",
        alt: "Bungee jumping",
      },
      {
        href: "/adventure#rafting",
        title: "White Water Rafting",
        img: "/hero/apartment.webp",
        alt: "White water rafting",
      },
    ],
  },
  {
    id: "accommodations",
    label: "Accommodations",
    items: [
      {
        href: "/accommodations",
        title: "All Accommodations",
        img: "/hero/hotel.webp",
        alt: "All accommodations",
      },
      {
        href: "/accommodations#hotels",
        title: "Hotels & Resorts",
        img: "/hero/hotel.webp",
        alt: "Hotels and resorts",
      },
      {
        href: "/accommodations#villas",
        title: "Villas & Houses",
        img: "/hero/villa.webp",
        alt: "Villas and houses",
      },
      {
        href: "/accommodations#apartments",
        title: "Apartments",
        img: "/hero/apartment.webp",
        alt: "Apartments",
      },
      {
        href: "/accommodations#unique",
        title: "Unique Stays",
        img: "/hero/treehouses.webp",
        alt: "Unique accommodations",
      },
      {
        href: "/accommodations#luxury",
        title: "Luxury Properties",
        img: "/hero/resort.webp",
        alt: "Luxury properties",
      },
    ],
  },
];

// Hook for managing hover intent with delay
function useHoverIntent(delay = 150) {
  const [isHovered, setIsHovered] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  const onMouseEnter = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    timeoutRef.current = setTimeout(() => {
      setIsHovered(true);
    }, delay);
  };

  const onMouseLeave = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    timeoutRef.current = setTimeout(() => {
      setIsHovered(false);
    }, delay);
  };

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return { isHovered, onMouseEnter, onMouseLeave };
}

// Individual pill component
const CategoryPill: React.FC<{
  category: Category;
  isActive: boolean;
  isOpen: boolean;
  onClick: () => void;
  onKeyDown: (e: React.KeyboardEvent) => void;
  onMouseEnter: () => void;
  onMouseLeave: () => void;
}> = ({
  category,
  isActive,
  isOpen,
  onClick,
  onKeyDown,
  onMouseEnter,
  onMouseLeave,
}) => {
  return (
    <button
      role="menuitem"
      aria-expanded={isOpen}
      aria-controls={`mega-menu-${category.id}`}
      className={cn(
        "relative inline-flex items-center justify-center px-6 py-3 text-sm font-medium transition-all duration-200 rounded-full",
        "border border-transparent shadow-sm",
        "hover:shadow-md hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
        isOpen || isActive
          ? "bg-white text-gray-900 border-gray-200 shadow-md"
          : "bg-white/90 text-gray-700 hover:bg-white hover:text-gray-900"
      )}
      onClick={onClick}
      onKeyDown={onKeyDown}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      tabIndex={0}
    >
      {category.label}
      {(isActive || isOpen) && (
        <motion.div
          layoutId="active-indicator"
          className="absolute -bottom-2 left-1/2 w-2 h-2 bg-blue-500 rounded-full"
          style={{ x: "-50%" }}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          exit={{ scale: 0 }}
          transition={{ duration: 0.2 }}
        />
      )}
    </button>
  );
};

// Mega menu panel component
const MegaMenuPanel: React.FC<{
  category: Category;
  isOpen: boolean;
  onClose: () => void;
  onMouseEnter: () => void;
  onMouseLeave: () => void;
}> = ({ category, isOpen, onClose, onMouseEnter, onMouseLeave }) => {
  const panelRef = useRef<HTMLDivElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      onClose();
    }
  };

  useEffect(() => {
    if (isOpen && panelRef.current) {
      const firstItem = panelRef.current.querySelector(
        '[role="menuitem"]'
      ) as HTMLElement;
      if (firstItem) {
        firstItem.focus();
      }
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        ref={panelRef}
        id={`mega-menu-${category.id}`}
        role="menu"
        aria-label={`${category.label} menu`}
        className="absolute left-1/2 top-full mt-4 bg-white rounded-2xl shadow-xl ring-1 ring-black/5 p-8 z-[9999] w-full max-w-4xl"
        style={{
          x: "-50%",
        }}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        onKeyDown={handleKeyDown}
        initial={{ opacity: 0, y: -10, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: -10, scale: 0.95 }}
        transition={{
          duration: 0.2,
          ease: [0.16, 1, 0.3, 1],
        }}
      >
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {category.label}
          </h3>
          <p className="text-sm text-gray-600">
            Discover amazing {category.label.toLowerCase()} experiences
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4 max-h-80 overflow-y-auto">
          {category.items.map((item, index) => (
            <Link
              key={`${item.href}-${index}`}
              href={item.href}
              role="menuitem"
              className="group flex items-center gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-inset"
              tabIndex={0}
            >
              <div className="relative w-10 h-10 rounded-full overflow-hidden bg-gray-100 flex-shrink-0">
                <Image
                  src={item.img}
                  alt={item.alt}
                  width={40}
                  height={40}
                  className="object-cover w-full h-full"
                  sizes="(min-width: 1024px) 40px, 40px"
                  placeholder="empty"
                  loading="lazy"
                />
              </div>

              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-medium text-gray-900 group-hover:text-blue-600 transition-colors truncate">
                  {item.title}
                </h4>
                <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                  Explore {item.title.toLowerCase()} experiences
                </p>
              </div>

              <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                <svg
                  className="w-4 h-4 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </div>
            </Link>
          ))}
        </div>

        <div className="mt-6 pt-6 border-t border-gray-100">
          <Link
            href={`/categories/${category.id}`}
            className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-500 transition-colors"
          >
            View all {category.label.toLowerCase()} experiences
            <svg
              className="ml-1 w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </Link>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

// Mobile drawer component
const MobileDrawer: React.FC<{
  categories: Category[];
  activeId?: string;
  isOpen: boolean;
  onClose: () => void;
}> = ({ categories, activeId, isOpen, onClose }) => {
  const [expandedCategory, setExpandedCategory] = useState<string | null>(
    activeId || null
  );

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }

    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-[9999] bg-black/50 lg:hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div
          className="absolute top-0 left-0 right-0 bg-white shadow-xl max-h-[80vh] overflow-y-auto"
          initial={{ y: "-100%" }}
          animate={{ y: 0 }}
          exit={{ y: "-100%" }}
          transition={{ type: "spring", damping: 25, stiffness: 200 }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                Categories
              </h2>
              <button
                onClick={onClose}
                className="p-2 rounded-full hover:bg-gray-100 transition-colors"
                aria-label="Close menu"
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
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <div className="space-y-4">
              {categories.map((category) => (
                <div
                  key={category.id}
                  className="border-b border-gray-100 pb-4 last:border-b-0"
                >
                  <button
                    className="flex items-center justify-between w-full py-2 text-left"
                    onClick={() =>
                      setExpandedCategory(
                        expandedCategory === category.id ? null : category.id
                      )
                    }
                  >
                    <span className="font-medium text-gray-900">
                      {category.label}
                    </span>
                    <motion.svg
                      className="w-5 h-5 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      animate={{
                        rotate: expandedCategory === category.id ? 180 : 0,
                      }}
                      transition={{ duration: 0.2 }}
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                      />
                    </motion.svg>
                  </button>

                  <AnimatePresence>
                    {expandedCategory === category.id && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="overflow-hidden"
                      >
                        <div className="pt-3 space-y-2">
                          {category.items.map((item, index) => (
                            <Link
                              key={`${item.href}-${index}`}
                              href={item.href}
                              className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-50 transition-colors"
                              onClick={onClose}
                            >
                              <div className="relative w-8 h-8 rounded-full overflow-hidden bg-gray-100 flex-shrink-0">
                                <Image
                                  src={item.img}
                                  alt={item.alt}
                                  width={32}
                                  height={32}
                                  className="object-cover w-full h-full"
                                  sizes="32px"
                                  placeholder="empty"
                                  loading="lazy"
                                />
                              </div>
                              <span className="text-sm text-gray-700">
                                {item.title}
                              </span>
                            </Link>
                          ))}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

// Main HeroSection component with integrated mega menu
export default function HeroSection({
  categories = defaultCategories,
  activeId,
}: HeroSectionProps) {
  const [openCategory, setOpenCategory] = useState<string | null>(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  // Hover intent for desktop
  const {
    isHovered: isMenuHovered,
    onMouseEnter: onMenuEnter,
    onMouseLeave: onMenuLeave,
  } = useHoverIntent(100);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setOpenCategory(null);
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setOpenCategory(null);
        setIsMobileMenuOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleEscape);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEscape);
    };
  }, []);

  // Close menu when not hovered (desktop only)
  useEffect(() => {
    if (!isMenuHovered && window.innerWidth >= 1024) {
      const timer = setTimeout(() => {
        setOpenCategory(null);
      }, 150);

      return () => clearTimeout(timer);
    }
  }, [isMenuHovered]);

  // Keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent, categoryId: string) => {
    const currentIndex = categories.findIndex((cat) => cat.id === categoryId);

    switch (e.key) {
      case "ArrowLeft":
        e.preventDefault();
        const prevIndex =
          currentIndex > 0 ? currentIndex - 1 : categories.length - 1;
        setFocusedIndex(prevIndex);
        setOpenCategory(categories[prevIndex].id);
        break;
      case "ArrowRight":
        e.preventDefault();
        const nextIndex =
          currentIndex < categories.length - 1 ? currentIndex + 1 : 0;
        setFocusedIndex(nextIndex);
        setOpenCategory(categories[nextIndex].id);
        break;
      case "Enter":
      case " ":
        e.preventDefault();
        setOpenCategory(openCategory === categoryId ? null : categoryId);
        break;
      case "Escape":
        e.preventDefault();
        setOpenCategory(null);
        break;
    }
  };

  const handleCategoryClick = (categoryId: string) => {
    if (window.innerWidth < 1024) {
      setIsMobileMenuOpen(true);
    } else {
      setOpenCategory(openCategory === categoryId ? null : categoryId);
    }
  };

  return (
    <>
      <section className="relative h-[70vh] flex items-start justify-center pt-48">
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: "url('/hero/travelhero.webp')",
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-br from-black/40 via-purple-900/20 to-blue-900/30"></div>
        </div>

        <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-6">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 animate-fade-up text-white">
            Journeys that stay forever
          </h1>
          <p className="text-xl md:text-2xl mb-8 opacity-90 animate-fade-up text-amber-50">
            Find your travel crew. Share tours. Save more.
          </p>

          {/* Hero Mega Menu */}
          <div
            ref={containerRef}
            className="relative animate-fade-up"
            role="menubar"
            aria-label="Category navigation"
          >
            {/* Desktop Pills */}
            <div className="hidden lg:flex items-center justify-center gap-4">
              {categories.map((category) => (
                <CategoryPill
                  key={category.id}
                  category={category}
                  isActive={activeId === category.id}
                  isOpen={openCategory === category.id}
                  onClick={() => handleCategoryClick(category.id)}
                  onKeyDown={(e) => handleKeyDown(e, category.id)}
                  onMouseEnter={() => {
                    onMenuEnter();
                    setOpenCategory(category.id);
                  }}
                  onMouseLeave={onMenuLeave}
                />
              ))}
            </div>

            {/* Mobile Horizontal Scroll Pills */}
            <div className="lg:hidden">
              <div className="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-hide">
                {categories.map((category) => (
                  <button
                    key={category.id}
                    className={cn(
                      "flex-shrink-0 px-4 py-2 text-sm font-medium rounded-full transition-colors",
                      "border border-white/30",
                      activeId === category.id
                        ? "bg-white text-gray-900 border-white"
                        : "bg-white/10 text-white hover:bg-white/20"
                    )}
                    onClick={() => handleCategoryClick(category.id)}
                  >
                    {category.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Desktop Mega Menu Panel */}
            {openCategory && (
              <MegaMenuPanel
                category={categories.find((cat) => cat.id === openCategory)!}
                isOpen={openCategory !== null}
                onClose={() => setOpenCategory(null)}
                onMouseEnter={onMenuEnter}
                onMouseLeave={onMenuLeave}
              />
            )}
          </div>
        </div>
      </section>

      {/* Mobile Drawer */}
      <MobileDrawer
        categories={categories}
        activeId={activeId}
        isOpen={isMobileMenuOpen}
        onClose={() => setIsMobileMenuOpen(false)}
      />

      {/* Global styles for scrollbar hiding */}
      <style jsx global>{`
        .scrollbar-hide {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
        .scrollbar-hide::-webkit-scrollbar {
          display: none;
        }
      `}</style>
    </>
  );
}
