import { ReactNode } from "react";

export interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
}

export interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export interface SearchFilters {
  destination: string;
  checkIn: string;
  checkOut: string;
  guests: number;
}

export interface AccommodationHeroSectionProps {
  image: string;
  title?: string;
  subtitle?: string;
}

export interface Apartment {
  id: string;
  title: string;
  description: string;
  categoryId: string;
  hostId: string;
  city: string;
  country: string;
  address: string;
  latitude: number;
  longitude: number;
  basePrice: number;
  currency: string;
  maxGuests: number;
  bedrooms: number;
  bathrooms: number;
  amenities: string[];
  images: string[];
  isAvailable: boolean;
  status: string;
  createdAt: string;
  updatedAt: string;
  rating?: number;
  reviewCount?: number;
  host: {
    id: string;
    name: string;
    email: string;
    image: string | null;
  };
  category: {
    id: string;
    type: string;
    title: string;
    subtitle: string;
    image: string;
    sectionTitle: string;
    message: string;
    createdAt: string;
    updatedAt: string;
  };
}

export interface AccommodationCardProps {
  apartments: Apartment[];
}
