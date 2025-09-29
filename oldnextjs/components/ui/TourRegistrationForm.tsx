"use client";

import { useState, useEffect } from "react";
import {
  CreateTourDto,
  TourCategory as TourCategoryEnum,
  CancellationPolicy,
} from "@/types/tour";
import { tourService } from "@/services/tour.service";
import PhotoUpload from "@/components/ui/PhotoUpload";

interface TourSchedule {
  id: string;
  date: string;
  time: string;
  isRecurring: boolean;
  recurringDays?: string[];
  maxBookings: number;
  currentBookings: number;
}

interface TourItineraryItem {
  id: string;
  title: string;
  description: string;
  duration: number;
  location?: string;
  order: number;
}

interface TourFormData extends CreateTourDto {
  highlights: string[];
  whatsIncluded: string[];
  whatsExcluded: string[];
  requirements: string[];
  itinerary: TourItineraryItem[];
  images: string[];
  schedules: TourSchedule[];
  difficulty: string;
  paymentOptions: string[];

  // Tour Experience
  guided?: boolean;
  licensedGuide?: boolean;

  // Age & Participation
  ageRestrictions?: {
    minAge?: number;
    maxAge?: number;
    childPolicy?: string;
  };

  // Tour Details
  endPoint?: string;
  whatToBring?: string[];
  notAllowed?: string[];
  importantInfo?: string[];

  // Pricing Enhancements
  groupDiscount?: {
    enabled?: boolean;
    percentage?: number;
    minGroupSize?: number;
  };
  taxesFees?: {
    included?: string[];
    excluded?: string[];
    notes?: string;
  };

  // Availability & Scheduling
  operatingDays?: string[]; // ['monday', 'tuesday', etc.]
  timeSlots?: string[]; // ['09:00', '14:00', etc.]
  cutOffTime?: number; // hours before start
  capacity?: {
    minGroupSize?: number;
    maxGroupSize?: number;
    perSlot?: number;
  };
  seasonality?: {
    activeFrom?: string;
    activeTo?: string;
  };

  // Safety & Compliance
  operatorLicense?: {
    number?: string;
    issuingAuthority?: string;
    issueDate?: string;
    expiryDate?: string;
  };
  permits?: {
    type: string;
    number: string;
    issueDate: string;
    expiryDate: string;
  }[];
  insurance?: {
    provider?: string;
    policyNumber?: string;
    coverageAmount?: number;
    expiryDate?: string;
    coverageTypes?: string[];
  };

  // Policies
  leadTime?: number; // minimum hours before booking
  noShowPolicy?: string;
}

interface TourRegistrationFormProps {
  selectedCategory?: string;
  onSubmit?: (data: TourFormData | Record<string, unknown>) => void;
  onCancel?: () => void;
  currentUser?: Record<string, unknown>;
}

export default function TourRegistrationForm({
  selectedCategory,
  onSubmit,
  onCancel,
  currentUser,
}: TourRegistrationFormProps) {
  const [formData, setFormData] = useState<TourFormData>({
    title: "",
    city: "",
    country: "",
    category: TourCategoryEnum.SHARE_TRIP,
    description: "",
    startTimes: [],
    basePrice: 0,
    currency: "USD",
    minGroup: 1,
    maxGroup: 10,
    durationMins: 120,
    language: "English",
    languages: ["English"],
    isPayWhatYouWant: false,
    status: "active",
    travelStyles: [],
    accessibility: [],
    startWindow: "morning",
    instantBook: true,
    cancellationPolicy: CancellationPolicy.STANDARD,
    meetingPoint: "",
    tags: [],
    searchKeywords: [],
    highlights: [""],
    whatsIncluded: [""],
    whatsExcluded: [""],
    requirements: [""],
    itinerary: [
      {
        id: "1",
        title: "",
        description: "",
        duration: 30,
        order: 1,
      },
    ],
    images: [],
    schedules: [
      {
        id: "1",
        date: new Date().toISOString().split("T")[0],
        time: "09:00",
        isRecurring: false,
        maxBookings: 10,
        currentBookings: 0,
      },
    ],
    difficulty: "Easy",
    paymentOptions: [],

    // Tour Experience
    guided: true,
    licensedGuide: false,

    // Age & Participation
    ageRestrictions: {
      minAge: 0,
      maxAge: 99,
      childPolicy: "",
    },

    // Tour Details
    endPoint: "",
    whatToBring: [],
    notAllowed: [],
    importantInfo: [],

    // Pricing Enhancements
    groupDiscount: {
      enabled: false,
      percentage: 0,
      minGroupSize: 2,
    },
    taxesFees: {
      included: [],
      excluded: [],
      notes: "",
    },

    // Availability & Scheduling
    operatingDays: [
      "monday",
      "tuesday",
      "wednesday",
      "thursday",
      "friday",
      "saturday",
      "sunday",
    ],
    timeSlots: ["09:00", "14:00"],
    cutOffTime: 24,
    capacity: {
      minGroupSize: 1,
      maxGroupSize: 10,
      perSlot: 10,
    },
    seasonality: {
      activeFrom: "",
      activeTo: "",
    },

    // Safety & Compliance
    operatorLicense: {
      number: "",
      issuingAuthority: "",
      issueDate: "",
      expiryDate: "",
    },
    permits: [],
    insurance: {
      provider: "",
      policyNumber: "",
      coverageAmount: 0,
      expiryDate: "",
      coverageTypes: [],
    },

    // Policies
    leadTime: 24,
    noShowPolicy: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [step, setStep] = useState(1);

  // Tour categories
  const tourCategories = [
    {
      id: "sightseeing",
      name: "Tours & Sightseeing",
      description: "Discover iconic landmarks and attractions",
    },
    {
      id: "culture",
      name: "Cultural Experiences",
      description: "Immerse in local culture and traditions",
    },
    {
      id: "adventure",
      name: "Adventure & Outdoor",
      description: "Thrilling outdoor activities and adventures",
    },
    {
      id: "food",
      name: "Food Tours",
      description: "Culinary adventures and local cuisine",
    },
    {
      id: "walking",
      name: "Walking Tours",
      description: "Explore on foot at a comfortable pace",
    },
    {
      id: "share",
      name: "Share Tours",
      description: "Join group experiences with other travelers",
    },
    {
      id: "private",
      name: "Private Tours",
      description: "Exclusive personalized experiences",
    },
  ];

  // Common travel styles
  const travelStyleOptions = [
    "Photography",
    "History",
    "Architecture",
    "Nature",
    "Local Life",
    "Family Friendly",
    "Romance",
    "Adventure",
    "Relaxed",
    "Fast Paced",
    "Educational",
    "Entertainment",
    "Spiritual",
    "Shopping",
    "Nightlife",
    "Culinary",
    "Wine Tasting",
    "Beach & Coast",
    "Mountains",
    "Urban Exploration",
    "Wildlife",
    "Art & Museums",
    "Music & Festivals",
    "Sports & Recreation",
    "Wellness & Spa",
    "Luxury",
    "Budget-Friendly",
    "Eco-Tourism",
    "Cultural Immersion",
    "Solo Traveler",
    "Group Travel",
    "Business Travel",
    "Backpacking",
    "Glamping",
    "Road Trip",
    "Cruise",
    "Desert",
    "Forest",
    "City Break",
    "Weekend Getaway",
    "Extended Stay",
    "Off the Beaten Path",
    "Popular Attractions",
    "Local Markets",
    "Street Food",
    "Fine Dining",
    "Nighttime Tours",
    "Sunrise Tours",
    "Seasonal",
    "Holiday Special",
  ];

  // Accessibility options
  const accessibilityOptions = [
    "Wheelchair Accessible",
    "Mobility Aid Friendly",
    "Visual Impairment Friendly",
    "Hearing Impairment Friendly",
    "Accessible Restrooms",
    "Elevator Access",
    "Assistance Available",
    "Service Animals Welcome",
    "Senior Friendly",
    "Family Friendly",
    "Audio Descriptions Available",
    "Sign Language Interpreter",
  ];

  // Language options
  const languageOptions = [
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Arabic",
    "Chinese (Mandarin)",
    "Chinese (Cantonese)",
    "Japanese",
    "Korean",
    "Russian",
    "Dutch",
    "Hindi",
    "Bengali",
    "Urdu",
    "Indonesian",
    "Malay",
    "Thai",
    "Vietnamese",
    "Filipino/Tagalog",
    "Turkish",
    "Hebrew",
    "Greek",
    "Polish",
    "Czech",
    "Hungarian",
    "Romanian",
    "Bulgarian",
    "Croatian",
    "Serbian",
    "Slovak",
    "Slovenian",
    "Estonian",
    "Latvian",
    "Lithuanian",
    "Finnish",
    "Swedish",
    "Norwegian",
    "Danish",
    "Icelandic",
    "Ukrainian",
    "Belarusian",
    "Georgian",
    "Armenian",
    "Azerbaijani",
    "Kazakh",
    "Uzbek",
    "Kyrgyz",
    "Tajik",
    "Mongolian",
    "Tibetan",
    "Burmese",
    "Khmer",
    "Lao",
    "Nepali",
    "Sinhala",
    "Tamil",
    "Telugu",
    "Kannada",
    "Malayalam",
    "Marathi",
    "Gujarati",
    "Punjabi",
    "Persian (Farsi)",
    "Kurdish",
    "Pashto",
    "Dari",
    "Amharic",
    "Tigrinya",
    "Oromo",
    "Somali",
    "Swahili",
    "Yoruba",
    "Igbo",
    "Hausa",
    "Zulu",
    "Afrikaans",
    "Xhosa",
    "Catalan",
    "Basque",
    "Galician",
    "Welsh",
    "Irish Gaelic",
    "Scottish Gaelic",
    "Maltese",
    "Albanian",
    "Macedonian",
    "Bosnian",
    "Montenegrin",
    "Moldovan",
  ];

  useEffect(() => {
    if (selectedCategory) {
      // Map the selected category to TourCategory enum
      const categoryMap: Record<string, TourCategoryEnum> = {
        share: TourCategoryEnum.SHARE_TRIP,
        private: TourCategoryEnum.PRIVATE,
        sightseeing: TourCategoryEnum.GROUP,
        culture: TourCategoryEnum.GROUP,
        adventure: TourCategoryEnum.GROUP,
        food: TourCategoryEnum.GROUP,
        walking: TourCategoryEnum.GROUP,
      };

      setFormData((prev) => ({
        ...prev,
        category: categoryMap[selectedCategory] || TourCategoryEnum.SHARE_TRIP,
      }));
    }
  }, [selectedCategory]);

  const handleInputChange = (
    field: string,
    value: string | number | boolean | string[] | undefined
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleArrayFieldAdd = (field: keyof TourFormData) => {
    setFormData((prev) => ({
      ...prev,
      [field]: [...(prev[field] as string[]), ""],
    }));
  };

  const handleArrayFieldRemove = (field: keyof TourFormData, index: number) => {
    setFormData((prev) => ({
      ...prev,
      [field]: (prev[field] as string[]).filter((_, i) => i !== index),
    }));
  };

  const handleArrayFieldUpdate = (
    fieldName: string,
    index: number,
    value: string
  ) => {
    setFormData((prev) => ({
      ...prev,
      [fieldName]: (prev[fieldName as keyof TourFormData] as string[]).map(
        (item, i) => (i === index ? value : item)
      ),
    }));
  };

  const handleItineraryAdd = () => {
    const newItem: TourItineraryItem = {
      id: Date.now().toString(),
      title: "",
      description: "",
      duration: 30,
      order: formData.itinerary.length + 1,
    };
    setFormData((prev) => ({
      ...prev,
      itinerary: [...prev.itinerary, newItem],
    }));
  };

  const handleItineraryRemove = (id: string) => {
    setFormData((prev) => ({
      ...prev,
      itinerary: prev.itinerary.filter((item) => item.id !== id),
    }));
  };

  const handleItineraryUpdate = (
    id: string,
    field: string,
    value: string | number
  ) => {
    setFormData((prev) => ({
      ...prev,
      itinerary: prev.itinerary.map((item) =>
        item.id === id ? { ...item, [field]: value } : item
      ),
    }));
  };

  const handleScheduleAdd = () => {
    const newSchedule: TourSchedule = {
      id: Date.now().toString(),
      date: new Date().toISOString().split("T")[0],
      time: "09:00",
      isRecurring: false,
      maxBookings: formData.maxGroup,
      currentBookings: 0,
    };
    setFormData((prev) => ({
      ...prev,
      schedules: [...prev.schedules, newSchedule],
    }));
  };

  const handleScheduleRemove = (id: string) => {
    setFormData((prev) => ({
      ...prev,
      schedules: prev.schedules.filter((schedule) => schedule.id !== id),
    }));
  };

  const handleScheduleUpdate = (
    id: string,
    field: keyof TourSchedule,
    value: string | number | boolean | string[]
  ) => {
    setFormData((prev) => ({
      ...prev,
      schedules: prev.schedules.map((schedule) =>
        schedule.id === id ? { ...schedule, [field]: value } : schedule
      ),
    }));
  };

  const handleImagesChange = (images: string[]) => {
    setFormData((prev) => ({
      ...prev,
      images,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      // Validate required fields
      if (!formData.title || !formData.description || !formData.city) {
        throw new Error("Please fill in all required fields");
      }

      if (formData.basePrice <= 0) {
        throw new Error("Base price must be greater than 0");
      }

      // Convert schedules to startTimes
      const startTimes = formData.schedules.map((schedule) =>
        new Date(`${schedule.date}T${schedule.time}`).toISOString()
      );

      const submitData: TourFormData = {
        ...formData,
        startTimes,
        highlights: formData.highlights.filter((h) => h.trim()),
        whatsIncluded: formData.whatsIncluded.filter((i) => i.trim()),
        whatsExcluded: formData.whatsExcluded.filter((e) => e.trim()),
        requirements: formData.requirements.filter((r) => r.trim()),
        tags: [...(formData.tags || []), selectedCategory || ""].filter((t) =>
          t.trim()
        ),
        searchKeywords: (formData.searchKeywords || []).filter((k) => k.trim()),
      };

      // Submit to API
      const tourData = {
        title: submitData.title,
        description: submitData.description,
        city: submitData.city,
        country: submitData.country,
        category: submitData.category || "general",
        basePrice: submitData.basePrice,
        currency: submitData.currency,
        maxParticipants: submitData.maxGroup || 10,
        duration: submitData.durationMins || 60,
        difficulty: submitData.difficulty,
        highlights: submitData.highlights,
        whatsIncluded: submitData.whatsIncluded,
        whatsExcluded: submitData.whatsExcluded,
        requirements: submitData.requirements,
        itinerary: submitData.itinerary,
        images: submitData.images,
        latitude: submitData.latitude,
        longitude: submitData.longitude,
        guideId: currentUser?.id || "default-guide", // Include current user's ID as guideId
      };

      const response = await tourService.createTour(tourData);

      console.log("Tour created successfully:", response);

      // Show success message
      setSuccess("Tour created successfully! Redirecting...");

      // Clear success message after 2 seconds and call onSubmit
      setTimeout(() => {
        setSuccess("");
        onSubmit?.(submitData);
      }, 2000);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to create tour");
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  // Step 1: Basic Information
  const renderBasicInfo = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Basic Tour Information
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tour Title *
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => handleInputChange("title", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="e.g., Historic Walking Tour of Old City"
          />
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description *
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => handleInputChange("description", e.target.value)}
            rows={4}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="Describe your tour in detail..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tour Category *
          </label>
          <select
            value={selectedCategory}
            disabled
            className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-600"
          >
            {tourCategories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Difficulty Level
          </label>
          <select
            value={formData.difficulty}
            onChange={(e) => handleInputChange("difficulty", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            <option value="Easy">Easy</option>
            <option value="Moderate">Moderate</option>
            <option value="Challenging">Challenging</option>
            <option value="Strenuous">Strenuous</option>
          </select>
        </div>
      </div>

      {/* Tour Experience */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h4 className="text-md font-semibold text-gray-900 mb-4">
          Tour Experience
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Guided Tour?
            </label>
            <div className="flex items-center space-x-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="guided"
                  checked={formData.guided === true}
                  onChange={() => handleInputChange("guided", true)}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-700">Yes</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="guided"
                  checked={formData.guided === false}
                  onChange={() => handleInputChange("guided", false)}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-700">No</span>
              </label>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Licensed Guide?
            </label>
            <div className="flex items-center space-x-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="licensedGuide"
                  checked={formData.licensedGuide === true}
                  onChange={() => handleInputChange("licensedGuide", true)}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-700">Yes</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="licensedGuide"
                  checked={formData.licensedGuide === false}
                  onChange={() => handleInputChange("licensedGuide", false)}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300"
                />
                <span className="ml-2 text-sm text-gray-700">No</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Step 2: Location & Meeting Details
  const renderLocationDetails = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Location & Meeting Details
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            City *
          </label>
          <input
            type="text"
            value={formData.city}
            onChange={(e) => handleInputChange("city", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="e.g., Amman"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Country *
          </label>
          <input
            type="text"
            value={formData.country}
            onChange={(e) => handleInputChange("country", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="e.g., Jordan"
          />
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Meeting Point *
          </label>
          <input
            type="text"
            value={formData.meetingPoint}
            onChange={(e) => handleInputChange("meetingPoint", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="e.g., Roman Theatre entrance, Amman"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Latitude (Optional)
          </label>
          <input
            type="number"
            value={formData.latitude || ""}
            onChange={(e) =>
              handleInputChange(
                "latitude",
                e.target.value ? parseFloat(e.target.value) : 0
              )
            }
            step="any"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="e.g., 31.9539"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Longitude (Optional)
          </label>
          <input
            type="number"
            value={formData.longitude || ""}
            onChange={(e) =>
              handleInputChange(
                "longitude",
                e.target.value ? parseFloat(e.target.value) : 0
              )
            }
            step="any"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="e.g., 35.9106"
          />
        </div>
      </div>
    </div>
  );

  // Step 3: Pricing & Group Details
  const renderPricingDetails = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Pricing & Group Details
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Base Price (per person) *
          </label>
          <div className="relative">
            <input
              type="number"
              value={formData.basePrice / 100}
              onChange={(e) =>
                handleInputChange("basePrice", parseFloat(e.target.value) * 100)
              }
              min="0"
              step="0.01"
              className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="0.00"
            />
            <span className="absolute left-3 top-3 text-gray-500">$</span>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Currency
          </label>
          <select
            value={formData.currency}
            onChange={(e) => handleInputChange("currency", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
            <option value="JOD">JOD</option>
            <option value="GBP">GBP</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Minimum Group Size *
          </label>
          <input
            type="number"
            value={formData.minGroup}
            onChange={(e) =>
              handleInputChange("minGroup", parseInt(e.target.value))
            }
            min="1"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Maximum Group Size *
          </label>
          <input
            type="number"
            value={formData.maxGroup}
            onChange={(e) =>
              handleInputChange("maxGroup", parseInt(e.target.value))
            }
            min="1"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Duration (minutes) *
          </label>
          <input
            type="number"
            value={formData.durationMins}
            onChange={(e) =>
              handleInputChange("durationMins", parseInt(e.target.value))
            }
            min="15"
            step="15"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Cancellation Policy
          </label>
          <select
            value={formData.cancellationPolicy}
            onChange={(e) =>
              handleInputChange("cancellationPolicy", e.target.value)
            }
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            <option value={CancellationPolicy.FLEXIBLE}>
              Flexible - Free cancellation
            </option>
            <option value={CancellationPolicy.STANDARD}>
              Standard - 24h notice required
            </option>
            <option value={CancellationPolicy.STRICT}>
              Strict - 72h notice required
            </option>
          </select>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={formData.isPayWhatYouWant}
            onChange={(e) =>
              handleInputChange("isPayWhatYouWant", e.target.checked)
            }
            className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
          />
          <span className="ml-2 text-sm text-gray-700">
            Pay What You Want Tour
          </span>
        </label>

        <label className="flex items-center">
          <input
            type="checkbox"
            checked={formData.instantBook}
            onChange={(e) => handleInputChange("instantBook", e.target.checked)}
            className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
          />
          <span className="ml-2 text-sm text-gray-700">Instant Booking</span>
        </label>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-4">
          Payment Options
        </label>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {["Pay on Arrival", "Full Payment Upfront"].map((option) => (
            <label
              key={option}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                checked={formData.paymentOptions?.includes(option)}
                onChange={(e) => {
                  const currentOptions = formData.paymentOptions || [];
                  if (e.target.checked) {
                    handleInputChange("paymentOptions", [
                      ...currentOptions,
                      option,
                    ]);
                  } else {
                    handleInputChange(
                      "paymentOptions",
                      currentOptions.filter((o) => o !== option)
                    );
                  }
                }}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <span className="text-sm text-gray-700">{option}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Group Discount */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h4 className="text-md font-semibold text-gray-900 mb-4">
          Group Discount
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="flex items-center mb-2">
              <input
                type="checkbox"
                checked={formData.groupDiscount?.enabled || false}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    groupDiscount: {
                      ...prev.groupDiscount,
                      enabled: e.target.checked,
                    },
                  }));
                }}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded mr-2"
              />
              <span className="text-sm font-medium text-gray-700">
                Enable Group Discount
              </span>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Discount Percentage
            </label>
            <input
              type="number"
              value={formData.groupDiscount?.percentage || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  groupDiscount: {
                    ...prev.groupDiscount,
                    percentage: e.target.value ? parseFloat(e.target.value) : 0,
                  },
                }));
              }}
              min="0"
              max="100"
              step="0.1"
              disabled={!formData.groupDiscount?.enabled}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="10"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Minimum Group Size
            </label>
            <input
              type="number"
              value={formData.groupDiscount?.minGroupSize || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  groupDiscount: {
                    ...prev.groupDiscount,
                    minGroupSize: e.target.value ? parseInt(e.target.value) : 2,
                  },
                }));
              }}
              min="2"
              disabled={!formData.groupDiscount?.enabled}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="2"
            />
          </div>
        </div>
      </div>

      {/* Taxes & Fees */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h4 className="text-md font-semibold text-gray-900 mb-4">
          Taxes & Fees
        </h4>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Included in Price
            </label>
            {formData.taxesFees?.included?.map((item, index) => (
              <div key={index} className="flex gap-3 mb-3">
                <input
                  type="text"
                  value={item}
                  onChange={(e) => {
                    const updated = [...(formData.taxesFees?.included || [])];
                    updated[index] = e.target.value;
                    setFormData((prev) => ({
                      ...prev,
                      taxesFees: {
                        ...prev.taxesFees,
                        included: updated,
                      },
                    }));
                  }}
                  placeholder="e.g., All taxes, Service fees"
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <button
                  type="button"
                  onClick={() => {
                    const updated = (formData.taxesFees?.included || []).filter(
                      (_, i) => i !== index
                    );
                    setFormData((prev) => ({
                      ...prev,
                      taxesFees: {
                        ...prev.taxesFees,
                        included: updated,
                      },
                    }));
                  }}
                  className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  Remove
                </button>
              </div>
            )) || []}
            <button
              type="button"
              onClick={() => {
                const updated = [...(formData.taxesFees?.included || []), ""];
                setFormData((prev) => ({
                  ...prev,
                  taxesFees: {
                    ...prev.taxesFees,
                    included: updated,
                  },
                }));
              }}
              className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
            >
              + Add Included Item
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Excluded from Price
            </label>
            {formData.taxesFees?.excluded?.map((item, index) => (
              <div key={index} className="flex gap-3 mb-3">
                <input
                  type="text"
                  value={item}
                  onChange={(e) => {
                    const updated = [...(formData.taxesFees?.excluded || [])];
                    updated[index] = e.target.value;
                    setFormData((prev) => ({
                      ...prev,
                      taxesFees: {
                        ...prev.taxesFees,
                        excluded: updated,
                      },
                    }));
                  }}
                  placeholder="e.g., Gratuities, Transportation"
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <button
                  type="button"
                  onClick={() => {
                    const updated = (formData.taxesFees?.excluded || []).filter(
                      (_, i) => i !== index
                    );
                    setFormData((prev) => ({
                      ...prev,
                      taxesFees: {
                        ...prev.taxesFees,
                        excluded: updated,
                      },
                    }));
                  }}
                  className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  Remove
                </button>
              </div>
            )) || []}
            <button
              type="button"
              onClick={() => {
                const updated = [...(formData.taxesFees?.excluded || []), ""];
                setFormData((prev) => ({
                  ...prev,
                  taxesFees: {
                    ...prev.taxesFees,
                    excluded: updated,
                  },
                }));
              }}
              className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
            >
              + Add Excluded Item
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Notes
            </label>
            <textarea
              value={formData.taxesFees?.notes || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  taxesFees: {
                    ...prev.taxesFees,
                    notes: e.target.value,
                  },
                }));
              }}
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Any additional information about taxes and fees..."
            />
          </div>
        </div>
      </div>
    </div>
  );

  // Step 4: Language & Preferences
  const renderLanguagePreferences = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Language & Tour Preferences
        </h3>
      </div>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Primary Language *
          </label>
          <select
            value={formData.language}
            onChange={(e) => handleInputChange("language", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            {languageOptions.map((lang) => (
              <option key={lang} value={lang}>
                {lang}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            Additional Languages (Optional)
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {languageOptions
              .filter((lang) => lang !== formData.language)
              .map((lang) => (
                <label
                  key={lang}
                  className="flex items-center space-x-2 cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={formData.languages?.includes(lang)}
                    onChange={(e) => {
                      const currentLangs = formData.languages || [
                        formData.language,
                      ];
                      if (e.target.checked) {
                        handleInputChange("languages", [...currentLangs, lang]);
                      } else {
                        handleInputChange(
                          "languages",
                          currentLangs.filter((l) => l !== lang)
                        );
                      }
                    }}
                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  />
                  <span className="text-sm text-gray-700">{lang}</span>
                </label>
              ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            Travel Styles
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {travelStyleOptions.map((style) => (
              <label
                key={style}
                className="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={formData.travelStyles?.includes(style)}
                  onChange={(e) => {
                    const currentStyles = formData.travelStyles || [];
                    if (e.target.checked) {
                      handleInputChange("travelStyles", [
                        ...currentStyles,
                        style,
                      ]);
                    } else {
                      handleInputChange(
                        "travelStyles",
                        currentStyles.filter((s) => s !== style)
                      );
                    }
                  }}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <span className="text-sm text-gray-700">{style}</span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            Accessibility Features
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {accessibilityOptions.map((option) => (
              <label
                key={option}
                className="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={formData.accessibility?.includes(option)}
                  onChange={(e) => {
                    const currentAccessibility = formData.accessibility || [];
                    if (e.target.checked) {
                      handleInputChange("accessibility", [
                        ...currentAccessibility,
                        option,
                      ]);
                    } else {
                      handleInputChange(
                        "accessibility",
                        currentAccessibility.filter((a) => a !== option)
                      );
                    }
                  }}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <span className="text-sm text-gray-700">{option}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  // Step 5: Tour Highlights & Details
  const renderHighlightsDetails = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Tour Highlights & Details
        </h3>
      </div>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            Tour Highlights
          </label>
          {formData.highlights.map((highlight, index) => (
            <div key={index} className="flex gap-3 mb-3">
              <input
                type="text"
                value={highlight}
                onChange={(e) =>
                  handleArrayFieldUpdate("highlights", index, e.target.value)
                }
                placeholder="e.g., Visit the iconic Roman Theatre"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              {formData.highlights.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleArrayFieldRemove("highlights", index)}
                  className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => handleArrayFieldAdd("highlights")}
            className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
          >
            + Add Highlight
          </button>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            What&apos;s Included
          </label>
          {formData.whatsIncluded.map((item, index) => (
            <div key={index} className="flex gap-3 mb-3">
              <input
                type="text"
                value={item}
                onChange={(e) =>
                  handleArrayFieldUpdate("whatsIncluded", index, e.target.value)
                }
                placeholder="e.g., Professional guide, Entry tickets"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              {formData.whatsIncluded.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleArrayFieldRemove("whatsIncluded", index)}
                  className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => handleArrayFieldAdd("whatsIncluded")}
            className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
          >
            + Add Item
          </button>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            What&apos;s Not Included
          </label>
          {formData.whatsExcluded.map((item, index) => (
            <div key={index} className="flex gap-3 mb-3">
              <input
                type="text"
                value={item}
                onChange={(e) =>
                  handleArrayFieldUpdate("whatsExcluded", index, e.target.value)
                }
                placeholder="e.g., Transportation, Meals"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              {formData.whatsExcluded.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleArrayFieldRemove("whatsExcluded", index)}
                  className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => handleArrayFieldAdd("whatsExcluded")}
            className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
          >
            + Add Item
          </button>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            Requirements & Recommendations
          </label>
          {formData.requirements.map((req, index) => (
            <div key={index} className="flex gap-3 mb-3">
              <input
                type="text"
                value={req}
                onChange={(e) =>
                  handleArrayFieldUpdate("requirements", index, e.target.value)
                }
                placeholder="e.g., Comfortable walking shoes, Basic fitness level"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              {formData.requirements.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleArrayFieldRemove("requirements", index)}
                  className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <button
            type="button"
            onClick={() => handleArrayFieldAdd("requirements")}
            className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
          >
            + Add Requirement
          </button>
        </div>

        {/* Age Restrictions */}
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            Age Restrictions & Participation
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Minimum Age
              </label>
              <input
                type="number"
                value={formData.ageRestrictions?.minAge || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    ageRestrictions: {
                      ...prev.ageRestrictions,
                      minAge: e.target.value ? parseInt(e.target.value) : 0,
                    },
                  }));
                }}
                min="0"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Maximum Age
              </label>
              <input
                type="number"
                value={formData.ageRestrictions?.maxAge || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    ageRestrictions: {
                      ...prev.ageRestrictions,
                      maxAge: e.target.value ? parseInt(e.target.value) : 99,
                    },
                  }));
                }}
                min="0"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="99"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Child Policy
              </label>
              <input
                type="text"
                value={formData.ageRestrictions?.childPolicy || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    ageRestrictions: {
                      ...prev.ageRestrictions,
                      childPolicy: e.target.value,
                    },
                  }));
                }}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="e.g., Children under 12 welcome with adult"
              />
            </div>
          </div>
        </div>

        {/* Tour Logistics */}
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            Tour Logistics
          </h4>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                End Point (Optional)
              </label>
              <input
                type="text"
                value={formData.endPoint || ""}
                onChange={(e) => handleInputChange("endPoint", e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Where does the tour end? (if different from start)"
              />
            </div>
          </div>
        </div>

        {/* What to Bring */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            What to Bring
          </label>
          {formData.whatToBring?.map((item, index) => (
            <div key={index} className="flex gap-3 mb-3">
              <input
                type="text"
                value={item}
                onChange={(e) => {
                  const updated = [...(formData.whatToBring || [])];
                  updated[index] = e.target.value;
                  handleInputChange("whatToBring", updated);
                }}
                placeholder="e.g., Comfortable walking shoes, Water bottle"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => {
                  const updated = (formData.whatToBring || []).filter(
                    (_, i) => i !== index
                  );
                  handleInputChange("whatToBring", updated);
                }}
                className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              >
                Remove
              </button>
            </div>
          )) || []}
          <button
            type="button"
            onClick={() => {
              const updated = [...(formData.whatToBring || []), ""];
              handleInputChange("whatToBring", updated);
            }}
            className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
          >
            + Add Item
          </button>
        </div>

        {/* Not Allowed */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            Not Allowed
          </label>
          {formData.notAllowed?.map((item, index) => (
            <div key={index} className="flex gap-3 mb-3">
              <input
                type="text"
                value={item}
                onChange={(e) => {
                  const updated = [...(formData.notAllowed || [])];
                  updated[index] = e.target.value;
                  handleInputChange("notAllowed", updated);
                }}
                placeholder="e.g., Pets, Outside food/drinks"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => {
                  const updated = (formData.notAllowed || []).filter(
                    (_, i) => i !== index
                  );
                  handleInputChange("notAllowed", updated);
                }}
                className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              >
                Remove
              </button>
            </div>
          )) || []}
          <button
            type="button"
            onClick={() => {
              const updated = [...(formData.notAllowed || []), ""];
              handleInputChange("notAllowed", updated);
            }}
            className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
          >
            + Add Item
          </button>
        </div>

        {/* Important Info */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-4">
            Important Information
          </label>
          {formData.importantInfo?.map((info, index) => (
            <div key={index} className="flex gap-3 mb-3">
              <input
                type="text"
                value={info}
                onChange={(e) => {
                  const updated = [...(formData.importantInfo || [])];
                  updated[index] = e.target.value;
                  handleInputChange("importantInfo", updated);
                }}
                placeholder="e.g., Health/fitness requirements, Dress code"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => {
                  const updated = (formData.importantInfo || []).filter(
                    (_, i) => i !== index
                  );
                  handleInputChange("importantInfo", updated);
                }}
                className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              >
                Remove
              </button>
            </div>
          )) || []}
          <button
            type="button"
            onClick={() => {
              const updated = [...(formData.importantInfo || []), ""];
              handleInputChange("importantInfo", updated);
            }}
            className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
          >
            + Add Info
          </button>
        </div>
      </div>
    </div>
  );

  // Step 6: Safety & Compliance
  const renderSafetyCompliance = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          Safety & Compliance
        </h3>
        <p className="text-gray-600">
          Provide your licensing, permits, and insurance information
        </p>
      </div>

      {/* Operator License */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h4 className="text-md font-semibold text-gray-900 mb-4">
          Operator License
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              License Number
            </label>
            <input
              type="text"
              value={formData.operatorLicense?.number || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  operatorLicense: {
                    ...prev.operatorLicense,
                    number: e.target.value,
                  },
                }));
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Enter license number"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Issuing Authority
            </label>
            <input
              type="text"
              value={formData.operatorLicense?.issuingAuthority || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  operatorLicense: {
                    ...prev.operatorLicense,
                    issuingAuthority: e.target.value,
                  },
                }));
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="e.g., Ministry of Tourism"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Issue Date
            </label>
            <input
              type="date"
              value={formData.operatorLicense?.issueDate || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  operatorLicense: {
                    ...prev.operatorLicense,
                    issueDate: e.target.value,
                  },
                }));
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Expiry Date
            </label>
            <input
              type="date"
              value={formData.operatorLicense?.expiryDate || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  operatorLicense: {
                    ...prev.operatorLicense,
                    expiryDate: e.target.value,
                  },
                }));
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Permits */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h4 className="text-md font-semibold text-gray-900 mb-4">
          Permits & Certifications
        </h4>
        <div className="space-y-4">
          {formData.permits?.map((permit, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Permit Type
                  </label>
                  <input
                    type="text"
                    value={permit.type}
                    onChange={(e) => {
                      const updated = [...(formData.permits || [])];
                      updated[index] = { ...permit, type: e.target.value };
                      setFormData((prev) => ({
                        ...prev,
                        permits: updated,
                      }));
                    }}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="e.g., Environmental Permit"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Permit Number
                  </label>
                  <input
                    type="text"
                    value={permit.number}
                    onChange={(e) => {
                      const updated = [...(formData.permits || [])];
                      updated[index] = { ...permit, number: e.target.value };
                      setFormData((prev) => ({
                        ...prev,
                        permits: updated,
                      }));
                    }}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Enter permit number"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Issue Date
                  </label>
                  <input
                    type="date"
                    value={permit.issueDate}
                    onChange={(e) => {
                      const updated = [...(formData.permits || [])];
                      updated[index] = { ...permit, issueDate: e.target.value };
                      setFormData((prev) => ({
                        ...prev,
                        permits: updated,
                      }));
                    }}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Expiry Date
                  </label>
                  <input
                    type="date"
                    value={permit.expiryDate}
                    onChange={(e) => {
                      const updated = [...(formData.permits || [])];
                      updated[index] = {
                        ...permit,
                        expiryDate: e.target.value,
                      };
                      setFormData((prev) => ({
                        ...prev,
                        permits: updated,
                      }));
                    }}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                </div>
              </div>

              <button
                type="button"
                onClick={() => {
                  const updated = (formData.permits || []).filter(
                    (_, i) => i !== index
                  );
                  setFormData((prev) => ({
                    ...prev,
                    permits: updated,
                  }));
                }}
                className="mt-4 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              >
                Remove Permit
              </button>
            </div>
          )) || []}

          <button
            type="button"
            onClick={() => {
              const updated = [
                ...(formData.permits || []),
                { type: "", number: "", issueDate: "", expiryDate: "" },
              ];
              setFormData((prev) => ({
                ...prev,
                permits: updated,
              }));
            }}
            className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
          >
            + Add Permit
          </button>
        </div>
      </div>

      {/* Insurance Details */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h4 className="text-md font-semibold text-gray-900 mb-4">
          Insurance Information
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Insurance Provider
            </label>
            <input
              type="text"
              value={formData.insurance?.provider || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  insurance: {
                    ...prev.insurance,
                    provider: e.target.value,
                  },
                }));
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Insurance company name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Policy Number
            </label>
            <input
              type="text"
              value={formData.insurance?.policyNumber || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  insurance: {
                    ...prev.insurance,
                    policyNumber: e.target.value,
                  },
                }));
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Enter policy number"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Coverage Amount
            </label>
            <input
              type="number"
              value={formData.insurance?.coverageAmount || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  insurance: {
                    ...prev.insurance,
                    coverageAmount: e.target.value
                      ? parseInt(e.target.value)
                      : 0,
                  },
                }));
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Coverage amount"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Expiry Date
            </label>
            <input
              type="date"
              value={formData.insurance?.expiryDate || ""}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  insurance: {
                    ...prev.insurance,
                    expiryDate: e.target.value,
                  },
                }));
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
        </div>

        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Coverage Types
          </label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {[
              "Liability",
              "Property",
              "Accident",
              "Medical",
              "Cancellation",
              "Emergency",
            ].map((type) => (
              <label
                key={type}
                className="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={
                    formData.insurance?.coverageTypes?.includes(type) || false
                  }
                  onChange={(e) => {
                    const current = formData.insurance?.coverageTypes || [];
                    const updated = e.target.checked
                      ? [...current, type]
                      : current.filter((t) => t !== type);
                    setFormData((prev) => ({
                      ...prev,
                      insurance: {
                        ...prev.insurance,
                        coverageTypes: updated,
                      },
                    }));
                  }}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <span className="text-sm text-gray-700">{type}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  // Step 7: Policies
  const renderPolicies = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">Tour Policies</h3>
        <p className="text-gray-600">
          Set your booking and cancellation policies
        </p>
      </div>

      {/* Lead Time */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h4 className="text-md font-semibold text-gray-900 mb-4">
          Booking Requirements
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Minimum Lead Time (hours)
            </label>
            <input
              type="number"
              value={formData.leadTime || ""}
              onChange={(e) =>
                handleInputChange("leadTime", parseInt(e.target.value))
              }
              min="0"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="24"
            />
            <p className="text-xs text-gray-500 mt-1">
              Minimum hours required between booking and tour start
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cancellation Policy
            </label>
            <select
              value={formData.cancellationPolicy || ""}
              onChange={(e) =>
                handleInputChange("cancellationPolicy", e.target.value)
              }
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="">Select policy</option>
              <option value="flexible">
                Flexible - Free cancellation up to 24 hours
              </option>
              <option value="moderate">
                Moderate - Free cancellation up to 7 days
              </option>
              <option value="strict">Strict - No refunds</option>
              <option value="custom">Custom policy</option>
            </select>
          </div>
        </div>
      </div>

      {/* No-show Policy */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h4 className="text-md font-semibold text-gray-900 mb-4">
          No-Show Policy
        </h4>
        <textarea
          value={formData.noShowPolicy || ""}
          onChange={(e) => handleInputChange("noShowPolicy", e.target.value)}
          rows={3}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          placeholder="Describe your policy for no-shows (e.g., full charge applies)"
        />
      </div>
    </div>
  );

  // Step 9: Tour Itinerary
  const renderItinerary = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Tour Itinerary
        </h3>
        <p className="text-gray-600">
          Break down your tour into steps and activities
        </p>
      </div>

      <div className="space-y-4">
        {formData.itinerary.map((item, index) => (
          <div
            key={item.id}
            className="bg-gray-50 p-6 rounded-lg border border-gray-200"
          >
            <div className="flex justify-between items-center mb-4">
              <h4 className="font-semibold text-gray-900">Step {index + 1}</h4>
              {formData.itinerary.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleItineraryRemove(item.id)}
                  className="text-red-600 hover:bg-red-50 p-2 rounded-lg transition-colors"
                >
                  Remove
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Activity Title *
                </label>
                <input
                  type="text"
                  value={item.title}
                  onChange={(e) =>
                    handleItineraryUpdate(item.id, "title", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="e.g., Explore the Roman Theatre"
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={item.description}
                  onChange={(e) =>
                    handleItineraryUpdate(
                      item.id,
                      "description",
                      e.target.value
                    )
                  }
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="Describe what happens in this part of the tour..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Duration (minutes)
                </label>
                <input
                  type="number"
                  value={item.duration}
                  onChange={(e) =>
                    handleItineraryUpdate(
                      item.id,
                      "duration",
                      parseInt(e.target.value)
                    )
                  }
                  min="5"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location (Optional)
                </label>
                <input
                  type="text"
                  value={item.location || ""}
                  onChange={(e) =>
                    handleItineraryUpdate(item.id, "location", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="e.g., Downtown Amman"
                />
              </div>
            </div>
          </div>
        ))}

        <button
          type="button"
          onClick={handleItineraryAdd}
          className="flex items-center gap-2 px-4 py-3 text-green-600 hover:bg-green-50 border-2 border-dashed border-green-200 rounded-lg transition-colors w-full justify-center"
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
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          Add Itinerary Step
        </button>
      </div>
    </div>
  );

  // Step 7: Schedule & Availability
  const renderScheduleAvailability = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Schedule & Availability
        </h3>
        <p className="text-gray-600">Set when your tour is available</p>
      </div>

      <div className="space-y-4">
        {formData.schedules.map((schedule, index) => (
          <div
            key={schedule.id}
            className="bg-gray-50 p-6 rounded-lg border border-gray-200"
          >
            <div className="flex justify-between items-center mb-4">
              <h4 className="font-semibold text-gray-900">
                Schedule {index + 1}
              </h4>
              {formData.schedules.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleScheduleRemove(schedule.id)}
                  className="text-red-600 hover:bg-red-50 p-2 rounded-lg transition-colors"
                >
                  Remove
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Date *
                </label>
                <input
                  type="date"
                  value={schedule.date}
                  onChange={(e) =>
                    handleScheduleUpdate(schedule.id, "date", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Start Time *
                </label>
                <input
                  type="time"
                  value={schedule.time}
                  onChange={(e) =>
                    handleScheduleUpdate(schedule.id, "time", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Bookings
                </label>
                <input
                  type="number"
                  value={schedule.maxBookings}
                  onChange={(e) =>
                    handleScheduleUpdate(
                      schedule.id,
                      "maxBookings",
                      parseInt(e.target.value)
                    )
                  }
                  min="1"
                  max={formData.maxGroup}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div className="md:col-span-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={schedule.isRecurring}
                    onChange={(e) =>
                      handleScheduleUpdate(
                        schedule.id,
                        "isRecurring",
                        e.target.checked
                      )
                    }
                    className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">
                    Recurring Schedule
                  </span>
                </label>
              </div>

              {schedule.isRecurring && (
                <div className="md:col-span-3">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Recurring Days
                  </label>
                  <div className="flex gap-2 flex-wrap">
                    {[
                      "Sunday",
                      "Monday",
                      "Tuesday",
                      "Wednesday",
                      "Thursday",
                      "Friday",
                      "Saturday",
                    ].map((day) => (
                      <label key={day} className="flex items-center">
                        <input
                          type="checkbox"
                          checked={
                            schedule.recurringDays?.includes(day) || false
                          }
                          onChange={(e) => {
                            const currentDays = schedule.recurringDays || [];
                            const newDays = e.target.checked
                              ? [...currentDays, day]
                              : currentDays.filter((d) => d !== day);
                            handleScheduleUpdate(
                              schedule.id,
                              "recurringDays",
                              newDays
                            );
                          }}
                          className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                        />
                        <span className="ml-1 text-sm text-gray-700">
                          {day.slice(0, 3)}
                        </span>
                      </label>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Operating Days */}
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            Operating Days
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-3">
            {[
              "monday",
              "tuesday",
              "wednesday",
              "thursday",
              "friday",
              "saturday",
              "sunday",
            ].map((day) => (
              <label
                key={day}
                className="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={formData.operatingDays?.includes(day) || false}
                  onChange={(e) => {
                    const current = formData.operatingDays || [];
                    const updated = e.target.checked
                      ? [...current, day]
                      : current.filter((d) => d !== day);
                    handleInputChange("operatingDays", updated);
                  }}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <span className="text-sm text-gray-700 capitalize">{day}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Time Slots */}
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            Available Time Slots
          </h4>
          <div className="space-y-3">
            {formData.timeSlots?.map((slot, index) => (
              <div key={index} className="flex gap-3">
                <input
                  type="time"
                  value={slot}
                  onChange={(e) => {
                    const updated = [...(formData.timeSlots || [])];
                    updated[index] = e.target.value;
                    handleInputChange("timeSlots", updated);
                  }}
                  className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <button
                  type="button"
                  onClick={() => {
                    const updated = (formData.timeSlots || []).filter(
                      (_, i) => i !== index
                    );
                    handleInputChange("timeSlots", updated);
                  }}
                  className="px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  Remove
                </button>
              </div>
            )) || []}
            <button
              type="button"
              onClick={() => {
                const updated = [...(formData.timeSlots || []), "09:00"];
                handleInputChange("timeSlots", updated);
              }}
              className="text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors text-sm"
            >
              + Add Time Slot
            </button>
          </div>
        </div>

        {/* Capacity & Cut-off Time */}
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            Capacity & Booking Settings
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Min Group Size
              </label>
              <input
                type="number"
                value={formData.capacity?.minGroupSize || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    capacity: {
                      ...prev.capacity,
                      minGroupSize: e.target.value
                        ? parseInt(e.target.value)
                        : 1,
                    },
                  }));
                }}
                min="1"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="1"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Group Size
              </label>
              <input
                type="number"
                value={formData.capacity?.maxGroupSize || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    capacity: {
                      ...prev.capacity,
                      maxGroupSize: e.target.value
                        ? parseInt(e.target.value)
                        : 10,
                    },
                  }));
                }}
                min="1"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="10"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Per Slot Capacity
              </label>
              <input
                type="number"
                value={formData.capacity?.perSlot || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    capacity: {
                      ...prev.capacity,
                      perSlot: e.target.value ? parseInt(e.target.value) : 10,
                    },
                  }));
                }}
                min="1"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="10"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cut-off Time (hours)
              </label>
              <input
                type="number"
                value={formData.cutOffTime || ""}
                onChange={(e) =>
                  handleInputChange("cutOffTime", parseInt(e.target.value))
                }
                min="0"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="24"
              />
            </div>
          </div>
        </div>

        {/* Seasonality */}
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            Seasonality
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Active From
              </label>
              <input
                type="date"
                value={formData.seasonality?.activeFrom || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    seasonality: {
                      ...prev.seasonality,
                      activeFrom: e.target.value,
                    },
                  }));
                }}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Active To
              </label>
              <input
                type="date"
                value={formData.seasonality?.activeTo || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    seasonality: {
                      ...prev.seasonality,
                      activeTo: e.target.value,
                    },
                  }));
                }}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        <button
          type="button"
          onClick={handleScheduleAdd}
          className="flex items-center gap-2 px-4 py-3 text-green-600 hover:bg-green-50 border-2 border-dashed border-green-200 rounded-lg transition-colors w-full justify-center"
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
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          Add Schedule
        </button>
      </div>
    </div>
  );

  // Step 8: Images
  const renderImages = () => (
    <PhotoUpload
      images={formData.images}
      onImagesChange={handleImagesChange}
      maxImages={10}
      maxSizeInMB={5}
      title="Upload Tour Photos"
      subtitle="Add photos to showcase your tour experience. The first photo will be used as the cover image."
      acceptedFormats={[".jpg", ".jpeg", ".png", ".webp"]}
    />
  );

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Create Your Tour Experience
          </h2>
          <p className="text-gray-600">Step {step} of 10</p>
        </div>
        {onCancel && (
          <button
            onClick={onCancel}
            className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
          >
            Cancel
          </button>
        )}
      </div>

      {/* Progress bar */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-gray-600">Progress</span>
          <span className="text-sm text-gray-600">
            {Math.round((step / 10) * 100)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-green-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${(step / 10) * 100}%` }}
          ></div>
        </div>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {success && (
        <div className="mb-6 bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {step === 1 && renderBasicInfo()}
        {step === 2 && renderLocationDetails()}
        {step === 3 && renderPricingDetails()}
        {step === 4 && renderLanguagePreferences()}
        {step === 5 && renderHighlightsDetails()}
        {step === 6 && renderSafetyCompliance()}
        {step === 7 && renderPolicies()}
        {step === 8 && renderItinerary()}
        {step === 9 && renderScheduleAvailability()}
        {step === 10 && renderImages()}

        {/* Navigation buttons */}
        <div className="flex justify-between mt-8 pt-6 border-t border-gray-200">
          <button
            type="button"
            onClick={prevStep}
            disabled={step === 1}
            className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Previous
          </button>

          {step < 10 ? (
            <button
              type="button"
              onClick={nextStep}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
            >
              Next
            </button>
          ) : (
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Creating Tour..." : "Create Tour"}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
