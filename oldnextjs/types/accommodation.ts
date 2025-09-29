export interface Accommodation {
  id: string;
  title: string;
  description: string;
  category: string;
  location: string;
  price: number;
  currency: string;
  bedrooms: number;
  bathrooms: number;
  maxGuests: number;
  images: string[];
  status: "active" | "draft" | "paused";
  createdAt: string;
  bookings: number;
}

export interface RoomType {
  id: string;
  name: string;
  description: string;
  maxGuests: number;
  basePrice: number;
  bedSetup?: string;
  view?: string;
  boardType?: string;
  ratePlans: RatePlan[];
  availability: AvailabilitySlot[];
  monthlyAvailability?: Record<string, MonthlyAvailability>;
  dailyAvailability?: Record<string, DailyAvailability>;
}

export interface RatePlan {
  id: string;
  name: string;
  description: string;
  priceAdjustment: number; // Percentage or fixed amount
  adjustmentType: "percentage" | "fixed";
  conditions: string[];
  minStay?: number;
  maxStay?: number;
  advanceBooking?: number;
  cancellationPolicy?: string;
}

export interface AvailabilitySlot {
  id: string;
  dateFrom: string;
  dateTo: string;
  isAvailable: boolean;
  price?: number;
  minStay?: number;
  maxStay?: number;
}

export interface MonthlyAvailability {
  month: number;
  year: number;
  isAvailable: boolean;
  price?: number;
  minStay?: number;
  maxStay?: number;
}

export interface DailyAvailability {
  date: string;
  isAvailable: boolean;
  price?: number;
  minStay?: number;
  maxStay?: number;
}

export interface AccommodationFormData {
  title: string;
  description: string;
  categoryId: string;
  city: string;
  country: string;
  address: string;
  latitude?: number;
  longitude?: number;
  basePrice: number;
  currency: string;
  maxGuests: number;
  bedrooms: number;
  bathrooms: number;
  amenities: string[];
  images: string[];
  isAvailable: boolean;
  roomTypes: RoomType[];
  // New fields
  starRating?: number;
  languagesSpoken?: string[];
  neighborhoodHighlights?: string[];
  roomSize?: number; // in m²
  checkInOutTimes?: {
    checkInTime?: string;
    checkOutTime?: string;
    earlyCheckIn?: boolean;
    lateCheckOut?: boolean;
    earlyCheckInFee?: number;
    lateCheckOutFee?: number;
  };
  cancellationPolicy?: string;
  safetyCompliance?: {
    smokeDetectors?: boolean;
    carbonMonoxideDetectors?: boolean;
    firstAidKit?: boolean;
    fireExtinguishers?: boolean;
    securityCameras?: boolean;
    emergencyContact?: string;
  };
}

export interface AccommodationCategory {
  id: string;
  name: string;
  type: string;
  title: string;
  subtitle: string;
  sectionTitle: string;
}

export interface AccommodationRegistrationFormProps {
  selectedCategory?: string;
  onSubmit?: (data: AccommodationFormData | Record<string, unknown>) => void;
  onCancel?: () => void;
  initialData?: Partial<AccommodationFormData>;
  isEditMode?: boolean;
  currentUser?: Record<string, unknown>;
}