"use client";

import { useState, useEffect } from "react";
import { accommodationService } from "@/services/accommodation.service";
import PhotoUpload from "@/components/ui/PhotoUpload";
import {
  RoomType,
  RatePlan,
  AvailabilitySlot,
  MonthlyAvailability,
  DailyAvailability,
  AccommodationFormData,
  AccommodationCategory,
  AccommodationRegistrationFormProps,
} from "@/types/accommodation";

export default function AccommodationRegistrationForm({
  selectedCategory,
  onSubmit,
  onCancel,
  initialData,
  isEditMode = false,
  currentUser,
}: AccommodationRegistrationFormProps) {
  const [formData, setFormData] = useState<AccommodationFormData>(() => {
    if (initialData && isEditMode) {
      return {
        title: initialData.title || "",
        description: initialData.description || "",
        categoryId: initialData.categoryId || "default",
        city: initialData.city || "",
        country: initialData.country || "",
        address: initialData.address || "",
        latitude: initialData.latitude,
        longitude: initialData.longitude,
        basePrice: initialData.basePrice || 100,
        currency: initialData.currency || "USD",
        maxGuests: initialData.maxGuests || 2,
        bedrooms: initialData.bedrooms || 1,
        bathrooms: initialData.bathrooms || 1,
        amenities: initialData.amenities || [],
        images: initialData.images || [],
        isAvailable: initialData.isAvailable !== false,
        roomTypes: initialData.roomTypes || [],
        starRating: initialData.starRating,
        languagesSpoken: initialData.languagesSpoken || [],
        neighborhoodHighlights: initialData.neighborhoodHighlights || [],
        roomSize: initialData.roomSize,
        checkInOutTimes: initialData.checkInOutTimes || {
          checkInTime: "15:00",
          checkOutTime: "11:00",
          earlyCheckIn: false,
          lateCheckOut: false,
          earlyCheckInFee: 0,
          lateCheckOutFee: 0,
        },
        cancellationPolicy: initialData.cancellationPolicy,
        safetyCompliance: initialData.safetyCompliance || {},
      };
    }

    return {
      title: "",
      description: "",
      categoryId: selectedCategory || "default",
      city: "",
      country: "",
      address: "",
      basePrice: 100,
      currency: "USD",
      maxGuests: 2,
      bedrooms: 1,
      bathrooms: 1,
      amenities: [],
      images: [],
      isAvailable: true,
      roomTypes: [
        {
          id: "1",
          name: "Standard Room",
          description: "",
          maxGuests: 1,
          basePrice: 0,
          ratePlans: [],
          availability: [],
        },
      ],
      // Initialize new fields
      starRating: undefined,
      languagesSpoken: [],
      neighborhoodHighlights: [],
      roomSize: undefined,
      checkInOutTimes: {
        checkInTime: "15:00",
        checkOutTime: "11:00",
        earlyCheckIn: false,
        lateCheckOut: false,
        earlyCheckInFee: 0,
        lateCheckOutFee: 0,
      },
      cancellationPolicy: "Standard",
      safetyCompliance: {
        smokeDetectors: false,
        carbonMonoxideDetectors: false,
        firstAidKit: false,
        fireExtinguishers: false,
        securityCameras: false,
        emergencyContact: "",
      },
    };
  });

  const [categories, setCategories] = useState<AccommodationCategory[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [step, setStep] = useState(1);
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth());
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [selectedRoomType, setSelectedRoomType] = useState<string>("");
  const [selectedStandardRoomType, setSelectedStandardRoomType] =
    useState<string>("");
  const [dayEditModal, setDayEditModal] = useState<{
    isOpen: boolean;
    date: string;
    roomTypeId: string;
    availability: DailyAvailability;
  } | null>(null);

  // Standard room types
  const standardRoomTypes = [
    "Standard / Classic",
    "Superior",
    "Deluxe",
    "Premium / Executive",
    "Club / Concierge Floor",
    "Suite (general)",
    "Junior Suite",
    "One-Bedroom Suite",
    "Two-Bedroom Suite",
    "Presidential / Royal Suite",
    "Bunk Bed / Family Bunk",
  ];

  // Comprehensive amenities list organized by categories
  const amenitiesCategories = {
    "Internet & Technology": [
      "Free WiFi",
      "High-Speed Internet",
      "WiFi in Common Areas",
      "Computer/Laptop Access",
      "Smart TV",
      "Cable TV",
      "Streaming Services",
      "Gaming Console",
      "Sound System",
      "Bluetooth Speaker",
    ],
    "Kitchen & Dining": [
      "Full Kitchen",
      "Kitchenette",
      "Microwave",
      "Refrigerator",
      "Dishwasher",
      "Coffee Maker",
      "Tea Making Facilities",
      "Toaster",
      "Dining Table",
      "Bar/Counter Seating",
      "Barbecue Grill",
      "Outdoor Dining Area",
    ],
    "Comfort & Climate": [
      "Air Conditioning",
      "Central Heating",
      "Ceiling Fan",
      "Fireplace",
      "Humidifier",
      "Space Heater",
      "Temperature Control",
      "Blackout Curtains",
      "Extra Blankets",
      "Pillows & Linens",
    ],
    "Bathroom & Personal Care": [
      "Private Bathroom",
      "Shared Bathroom",
      "Bathtub",
      "Walk-in Shower",
      "Rainfall Shower",
      "Hairdryer",
      "Towels Provided",
      "Toiletries",
      "Hot Water",
      "Bidet",
      "Bathrobes",
      "Slippers",
    ],
    "Outdoor & Recreation": [
      "Swimming Pool",
      "Hot Tub/Jacuzzi",
      "Sauna",
      "Garden",
      "Terrace",
      "Balcony",
      "Patio",
      "Beach Access",
      "Sea View",
      "Mountain View",
      "City View",
      "Pool View",
      "Garden View",
      "Waterfront",
      "Tennis Court",
      "Golf Course Access",
      "Hiking Trails",
      "Bicycle Rental",
      "Kayak Rental",
      "Fishing",
    ],
    "Transportation & Parking": [
      "Free Parking",
      "Private Parking",
      "Garage Parking",
      "Street Parking",
      "Valet Parking",
      "Electric Vehicle Charging",
      "Airport Shuttle",
      "Public Transit Access",
      "Car Rental",
      "Bike Storage",
    ],
    "Safety & Security": [
      "Security System",
      "Smoke Detector",
      "Carbon Monoxide Detector",
      "Fire Extinguisher",
      "First Aid Kit",
      "Safe/Lock Box",
      "Security Cameras",
      "Gated Community",
      "24/7 Security",
      "Key Card Access",
      "Keyless Entry",
    ],
    "Services & Facilities": [
      "Concierge Service",
      "Front Desk (24-hour)",
      "Room Service",
      "Housekeeping",
      "Daily Cleaning",
      "Laundry Service",
      "Dry Cleaning",
      "Washing Machine",
      "Dryer",
      "Iron & Ironing Board",
      "Luggage Storage",
      "Package Receiving",
      "Mail Service",
      "Wake-up Service",
      "Currency Exchange",
    ],
    "Business & Work": [
      "Dedicated Workspace",
      "Office Chair",
      "Desk",
      "Business Center",
      "Meeting Rooms",
      "Printer/Scanner",
      "Fax Machine",
      "Conference Call Facilities",
      "High-Speed Internet for Work",
      "Quiet Space",
    ],
    "Entertainment & Leisure": [
      "Fitness Center/Gym",
      "Spa Services",
      "Massage Services",
      "Library",
      "Game Room",
      "Playground",
      "Kids' Club",
      "Entertainment Staff",
      "Live Music",
      "Pool Table",
      "Ping Pong Table",
      "Board Games",
      "Books & Magazines",
    ],
    "Food & Beverage": [
      "Restaurant",
      "Bar/Lounge",
      "Breakfast Included",
      "Continental Breakfast",
      "Room Service",
      "Mini Bar",
      "Coffee Shop",
      "Snack Bar",
      "Wine Cellar",
      "Cooking Classes",
      "BBQ Facilities",
    ],
    "Accessibility & Special Needs": [
      "Wheelchair Accessible",
      "Accessible Bathroom",
      "Elevator Access",
      "Grab Rails",
      "Accessible Parking",
      "Visual Aids",
      "Hearing Loop",
      "Braille",
      "Service Animals Allowed",
      "Mobility Equipment Rental",
    ],
    "Pet & Family Friendly": [
      "Pet Friendly",
      "Pet Beds",
      "Pet Food Bowls",
      "Dog Park",
      "Pet Sitting",
      "Crib Available",
      "High Chair",
      "Baby Bath",
      "Child Safety Gates",
      "Toys",
      "Family Rooms",
      "Connecting Rooms",
    ],
    "Special Policies": [
      "Smoking Allowed",
      "Non-Smoking",
      "Adults Only",
      "Parties/Events Allowed",
      "Long-term Stays Welcome",
      "Self Check-in",
      "Late Check-in",
      "Flexible Cancellation",
      "Eco-Friendly",
      "Solar Power",
      "Recycling Program",
    ],
  };

  // Comprehensive neighborhood highlights list organized by categories
  const neighborhoodHighlightsCategories = {
    "Transportation & Access": [
      "Walking Distance to Metro",
      "Close to Bus Stop",
      "Near Train Station",
      "Airport Shuttle Available",
      "Car Rental Nearby",
      "Bike Rental Available",
      "Taxi Stand Nearby",
      "Public Parking Available",
      "Valet Parking",
      "Electric Vehicle Charging",
      "Highway Access",
      "Ferry Terminal Nearby",
    ],
    "Attractions & Landmarks": [
      "Near City Center",
      "Historic District",
      "Museum District",
      "Art Gallery Area",
      "Theater District",
      "Shopping District",
      "Business District",
      "University Area",
      "Hospital Nearby",
      "Library Access",
      "Cultural Center",
      "Religious Sites",
      "Parks & Gardens",
      "Botanical Gardens",
      "Zoo or Aquarium",
      "Sports Stadium",
      "Concert Venue",
      "Convention Center",
    ],
    "Nature & Outdoors": [
      "Beach Access",
      "Lake Access",
      "River Access",
      "Mountain Views",
      "Ocean Views",
      "Forest Nearby",
      "National Park Access",
      "Hiking Trails",
      "Cycling Paths",
      "Scenic Views",
      "Waterfront Location",
      "Golf Course Nearby",
      "Ski Resort Access",
      "Camping Area",
      "Fishing Spot",
      "Marina Access",
    ],
    "Shopping & Dining": [
      "Shopping Mall Nearby",
      "Local Markets",
      "Supermarket Access",
      "Farmers Market",
      "Restaurants Nearby",
      "Cafes & Coffee Shops",
      "Nightlife District",
      "Food Court",
      "Grocery Store",
      "Pharmacy Access",
      "Banking Services",
      "ATM Available",
      "Post Office",
      "Laundromat",
    ],
    "Entertainment & Leisure": [
      "Movie Theater",
      "Bowling Alley",
      "Arcade or Gaming",
      "Casino Nearby",
      "Nightclub Access",
      "Live Music Venue",
      "Comedy Club",
      "Sports Bar",
      "Fitness Center Nearby",
      "Yoga Studio",
      "Dance Studio",
      "Art Classes",
      "Cooking School",
      "Wine Tasting",
    ],
    "Services & Amenities": [
      "Hospital Access",
      "Emergency Services",
      "Police Station",
      "Fire Station",
      "Medical Clinic",
      "Dentist Office",
      "Veterinarian",
      "Pet Services",
      "Childcare Center",
      "School Access",
      "Community Center",
      "Religious Services",
      "Laundry Services",
      "Dry Cleaning",
      "Car Wash",
      "Gas Station",
    ],
    "Recreational Facilities": [
      "Public Pool",
      "Tennis Courts",
      "Basketball Court",
      "Soccer Field",
      "Golf Course",
      "Bowling",
      "Mini Golf",
      "Ice Skating",
      "Rock Climbing",
      "Horseback Riding",
      "Boat Rental",
      "Kayaking",
      "Surfing Lessons",
      "Diving Center",
      "Spa & Wellness",
      "Massage Therapy",
    ],
    "Educational & Cultural": [
      "University Campus",
      "College Area",
      "Library",
      "Museum",
      "Art Gallery",
      "Historical Society",
      "Science Center",
      "Planetarium",
      "Aquarium",
      "Botanical Garden",
      "Arboretum",
      "Cultural Festival Site",
      "Film Festival Venue",
      "Music Festival Grounds",
      "Theater Company",
      "Opera House",
    ],
  };

  // Flatten all amenities for backward compatibility
  const commonAmenities = Object.values(amenitiesCategories).flat();

  useEffect(() => {
    fetchCategories();
  }, []);

  // Set default categoryId if not set
  useEffect(() => {
    if (!formData.categoryId) {
      setFormData((prev) => ({ ...prev, categoryId: "default" }));
    }
  }, []);

  const fetchCategories = async () => {
    try {
      const categoriesData = await accommodationService.getCategories();
      setCategories(categoriesData);
    } catch (error) {
      console.error("Failed to fetch categories:", error);
      setError("Failed to load accommodation categories");
    }
  };

  const handleInputChange = (
    field: keyof AccommodationFormData,
    value: string | number | boolean | string[] | undefined
  ) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleAmenityToggle = (amenity: string) => {
    setFormData((prev) => ({
      ...prev,
      amenities: prev.amenities.includes(amenity)
        ? prev.amenities.filter((a) => a !== amenity)
        : [...prev.amenities, amenity],
    }));
  };

  const handleImagesChange = (images: string[]) => {
    setFormData((prev) => ({
      ...prev,
      images,
    }));
  };

  // Room type handlers
  const addRoomType = () => {
    const newRoomType: RoomType = {
      id: Date.now().toString(),
      name: selectedStandardRoomType || "",
      description: "",
      maxGuests: 1,
      basePrice: 0,
      ratePlans: [],
      availability: [],
    };
    setFormData((prev) => ({
      ...prev,
      roomTypes: [...prev.roomTypes, newRoomType],
    }));
    setSelectedStandardRoomType(""); // Reset selection
  };

  const removeRoomType = (roomTypeId: string) => {
    setFormData((prev) => ({
      ...prev,
      roomTypes: prev.roomTypes.filter((rt) => rt.id !== roomTypeId),
    }));
  };

  const updateRoomType = (
    roomTypeId: string,
    field: keyof RoomType,
    value: unknown
  ) => {
    setFormData((prev) => ({
      ...prev,
      roomTypes: prev.roomTypes.map((rt) =>
        rt.id === roomTypeId ? { ...rt, [field]: value } : rt
      ),
    }));
  };

  const addRatePlan = (roomTypeId: string) => {
    const newRatePlan: RatePlan = {
      id: Date.now().toString(),
      name: "",
      description: "",
      priceAdjustment: 0,
      adjustmentType: "percentage",
      conditions: [],
      minStay: 1,
      cancellationPolicy: "Standard",
    };
    setFormData((prev) => ({
      ...prev,
      roomTypes: prev.roomTypes.map((rt) =>
        rt.id === roomTypeId
          ? { ...rt, ratePlans: [...rt.ratePlans, newRatePlan] }
          : rt
      ),
    }));
  };

  const removeRatePlan = (roomTypeId: string, ratePlanId: string) => {
    setFormData((prev) => ({
      ...prev,
      roomTypes: prev.roomTypes.map((rt) =>
        rt.id === roomTypeId
          ? {
              ...rt,
              ratePlans: rt.ratePlans.filter((rp) => rp.id !== ratePlanId),
            }
          : rt
      ),
    }));
  };

  const updateRatePlan = (
    roomTypeId: string,
    ratePlanId: string,
    field: keyof RatePlan,
    value: unknown
  ) => {
    setFormData((prev) => ({
      ...prev,
      roomTypes: prev.roomTypes.map((rt) =>
        rt.id === roomTypeId
          ? {
              ...rt,
              ratePlans: rt.ratePlans.map((rp) =>
                rp.id === ratePlanId ? { ...rp, [field]: value } : rp
              ),
            }
          : rt
      ),
    }));
  };

  const addAvailabilitySlot = (roomTypeId: string) => {
    const today = new Date().toISOString().split("T")[0];
    const tomorrow = new Date(Date.now() + 24 * 60 * 60 * 1000)
      .toISOString()
      .split("T")[0];

    const newSlot: AvailabilitySlot = {
      id: Date.now().toString(),
      dateFrom: today,
      dateTo: tomorrow,
      isAvailable: true,
      minStay: 1,
    };

    setFormData((prev) => ({
      ...prev,
      roomTypes: prev.roomTypes.map((rt) =>
        rt.id === roomTypeId
          ? { ...rt, availability: [...rt.availability, newSlot] }
          : rt
      ),
    }));
  };

  const removeAvailabilitySlot = (roomTypeId: string, slotId: string) => {
    setFormData((prev) => ({
      ...prev,
      roomTypes: prev.roomTypes.map((rt) =>
        rt.id === roomTypeId
          ? {
              ...rt,
              availability: rt.availability.filter(
                (slot) => slot.id !== slotId
              ),
            }
          : rt
      ),
    }));
  };

  const updateAvailabilitySlot = (
    roomTypeId: string,
    slotId: string,
    field: keyof AvailabilitySlot,
    value: unknown
  ) => {
    setFormData((prev) => ({
      ...prev,
      roomTypes: prev.roomTypes.map((rt) =>
        rt.id === roomTypeId
          ? {
              ...rt,
              availability: rt.availability.map((slot) =>
                slot.id === slotId ? { ...slot, [field]: value } : slot
              ),
            }
          : rt
      ),
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    console.log("Form submit triggered", {
      step,
      formData,
      eventType: e.type,
      target: e.target,
    });

    // Only allow submission on the final step
    if (step !== 6) {
      console.log("Form submission blocked - not on final step");
      return;
    }

    // Prevent double submission
    if (loading) {
      console.log("Form submission blocked - already loading");
      return;
    }

    console.log("Form submission allowed - proceeding with submission");
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      // Validate required fields
      if (!formData.title || !formData.description) {
        throw new Error("Please fill in all required fields");
      }

      if (formData.basePrice <= 0) {
        throw new Error("Base price must be greater than 0");
      }

      // Ensure categoryId has a default value and include hostId
      const submissionData = {
        ...formData,
        categoryId: formData.categoryId || "default",
        hostId: currentUser?.id || "default-host", // Include current user's ID as hostId
      };

      // Submit to API
      const response = await accommodationService.createAccommodation(
        submissionData
      );

      console.log("Accommodation created successfully:", response);

      // Show success message
      setSuccess("Accommodation created successfully! Redirecting...");

      // Clear success message after 2 seconds and call onSubmit with response (includes ID)
      setTimeout(() => {
        setSuccess("");
        onSubmit?.(response); // Pass the response which includes the ID
      }, 2000);
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : "Failed to create accommodation"
      );
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => {
    console.log("nextStep called, current step:", step);
    setStep(step + 1);
  };
  const prevStep = () => {
    console.log("prevStep called, current step:", step);
    setStep(step - 1);
  };

  // Step 1: Basic Information
  const renderBasicInfo = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Basic Information
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Property Title *
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => handleInputChange("title", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="e.g., Modern Studio Apartment in City Center"
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
            placeholder="Describe your accommodation in detail..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Category *
          </label>
          <select
            value={formData.categoryId}
            onChange={(e) => handleInputChange("categoryId", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            <option value="">Select a category</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.sectionTitle}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Star Rating
          </label>
          <select
            value={formData.starRating || ""}
            onChange={(e) =>
              handleInputChange(
                "starRating",
                e.target.value ? parseInt(e.target.value) : undefined
              )
            }
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
          >
            <option value="">Not rated</option>
            <option value="1">⭐ 1 Star</option>
            <option value="2">⭐⭐ 2 Stars</option>
            <option value="3">⭐⭐⭐ 3 Stars</option>
            <option value="4">⭐⭐⭐⭐ 4 Stars</option>
            <option value="5">⭐⭐⭐⭐⭐ 5 Stars</option>
          </select>
        </div>
      </div>
    </div>
  );

  // Step 2: Location
  const renderLocation = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Location Details
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
            placeholder="e.g., Limassol"
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
            placeholder="e.g., Cyprus"
          />
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Address *
          </label>
          <input
            type="text"
            value={formData.address}
            onChange={(e) => handleInputChange("address", e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            placeholder="e.g., 123 Main Street, Central Limassol"
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
            placeholder="e.g., 34.7071"
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
            placeholder="e.g., 33.0226"
          />
        </div>
      </div>
    </div>
  );

  // Step 3: Property Details
  const renderPropertyDetails = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Property Details
        </h3>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-6">
          Property Amenities
        </label>
        <div className="space-y-8">
          {Object.entries(amenitiesCategories).map(([category, amenities]) => (
            <div
              key={category}
              className="bg-gray-50 p-6 rounded-lg border border-gray-200"
            >
              <h4 className="text-md font-semibold text-gray-900 mb-4 flex items-center">
                <span className="inline-block w-3 h-3 bg-green-500 rounded-full mr-3"></span>
                {category}
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                {amenities.map((amenity) => (
                  <label
                    key={amenity}
                    className="flex items-center space-x-2 cursor-pointer p-2 rounded hover:bg-white transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={formData.amenities.includes(amenity)}
                      onChange={() => handleAmenityToggle(amenity)}
                      className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                    />
                    <span className="text-sm text-gray-700">{amenity}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Selected Amenities Summary */}
        {formData.amenities.length > 0 && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <h4 className="text-sm font-semibold text-green-800 mb-2">
              Selected Amenities ({formData.amenities.length})
            </h4>
            <div className="flex flex-wrap gap-2">
              {formData.amenities.map((amenity) => (
                <span
                  key={amenity}
                  className="inline-flex items-center px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full"
                >
                  {amenity}
                  <button
                    type="button"
                    onClick={() => handleAmenityToggle(amenity)}
                    className="ml-1 text-green-600 hover:text-green-800"
                  >
                    <svg
                      className="w-3 h-3"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </button>
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Languages Spoken */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Languages Spoken
        </label>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {[
            "English",
            "Spanish",
            "French",
            "German",
            "Italian",
            "Portuguese",
            "Chinese",
            "Japanese",
            "Korean",
            "Arabic",
            "Russian",
            "Hindi",
            "Dutch",
            "Swedish",
            "Turkish",
            "Greek",
            "Hebrew",
            "Thai",
            "Vietnamese",
            "Indonesian",
            "Malay",
            "Swahili",
            "Afrikaans",
            "Danish",
            "Norwegian",
            "Finnish",
            "Polish",
            "Czech",
            "Hungarian",
            "Romanian",
            "Bulgarian",
            "Croatian",
            "Serbian",
            "Slovenian",
            "Slovak",
            "Ukrainian",
            "Persian",
            "Urdu",
            "Bengali",
            "Tamil",
            "Telugu",
            "Marathi",
            "Gujarati",
            "Punjabi",
            "Filipino",
            "Burmese",
            "Khmer",
            "Lao",
            "Mongolian",
            "Nepali",
            "Sinhala",
            "Amharic",
            "Zulu",
            "Xhosa",
            "Hausa",
            "Yoruba",
            "Igbo",
          ].map((language) => (
            <label
              key={language}
              className="flex items-center space-x-2 cursor-pointer p-2 rounded hover:bg-gray-50 transition-colors"
            >
              <input
                type="checkbox"
                checked={formData.languagesSpoken?.includes(language) || false}
                onChange={() => {
                  const current = formData.languagesSpoken || [];
                  const updated = current.includes(language)
                    ? current.filter((l) => l !== language)
                    : [...current, language];
                  handleInputChange("languagesSpoken", updated);
                }}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <span className="text-sm text-gray-700">{language}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Neighborhood Highlights */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
        <h4 className="text-md font-semibold text-gray-900 mb-4">
          Neighborhood Highlights
        </h4>
        <p className="text-sm text-gray-600 mb-4">
          Select all that apply to highlight what makes your location special
        </p>

        {Object.entries(neighborhoodHighlightsCategories).map(
          ([category, highlights]) => (
            <div key={category} className="mb-6">
              <h5 className="text-sm font-medium text-gray-800 mb-3">
                {category}
              </h5>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {highlights.map((highlight) => (
                  <label
                    key={highlight}
                    className="flex items-center space-x-2 cursor-pointer p-2 rounded hover:bg-gray-50 transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={
                        formData.neighborhoodHighlights?.includes(highlight) ||
                        false
                      }
                      onChange={() => {
                        const current = formData.neighborhoodHighlights || [];
                        const updated = current.includes(highlight)
                          ? current.filter((h) => h !== highlight)
                          : [...current, highlight];
                        handleInputChange("neighborhoodHighlights", updated);
                      }}
                      className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                    />
                    <span className="text-sm text-gray-700">{highlight}</span>
                  </label>
                ))}
              </div>
            </div>
          )
        )}

        {/* Selected Neighborhood Highlights Summary */}
        {formData.neighborhoodHighlights &&
          formData.neighborhoodHighlights.length > 0 && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <h5 className="text-sm font-medium text-green-800 mb-2">
                Selected Neighborhood Highlights (
                {formData.neighborhoodHighlights.length})
              </h5>
              <div className="flex flex-wrap gap-2">
                {formData.neighborhoodHighlights.map((highlight) => (
                  <span
                    key={highlight}
                    className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                  >
                    {highlight}
                    <button
                      type="button"
                      onClick={() => {
                        const updated =
                          formData.neighborhoodHighlights?.filter(
                            (h) => h !== highlight
                          ) || [];
                        handleInputChange("neighborhoodHighlights", updated);
                      }}
                      className="ml-1 inline-flex items-center justify-center w-4 h-4 rounded-full text-green-400 hover:bg-green-200 hover:text-green-500"
                    >
                      <span className="sr-only">Remove {highlight}</span>×
                    </button>
                  </span>
                ))}
              </div>
            </div>
          )}
      </div>
    </div>
  );

  // Step 4: Room Types & Rate Plans
  const renderRoomTypes = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Room Types & Rate Plans
        </h3>
        <p className="text-gray-600">
          Define different room types and their pricing plans
        </p>
      </div>

      <div className="space-y-6">
        {formData.roomTypes.map((roomType, index) => (
          <div
            key={roomType.id}
            className="bg-gray-50 p-6 rounded-lg border border-gray-200"
          >
            <div className="flex justify-between items-center mb-4">
              <h4 className="font-semibold text-gray-900">
                Room Type {index + 1}
              </h4>
              {formData.roomTypes.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeRoomType(roomType.id)}
                  className="text-red-600 hover:bg-red-50 p-2 rounded-lg transition-colors"
                >
                  Remove
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Room Name *
                </label>
                <input
                  type="text"
                  value={roomType.name}
                  onChange={(e) =>
                    updateRoomType(roomType.id, "name", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="e.g., Standard Room, Deluxe Suite"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Guests *
                </label>
                <input
                  type="number"
                  value={roomType.maxGuests || 1}
                  onChange={(e) =>
                    updateRoomType(
                      roomType.id,
                      "maxGuests",
                      parseInt(e.target.value) || 1
                    )
                  }
                  min="1"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Room Size (m²)
                </label>
                <input
                  type="number"
                  value={formData.roomSize || ""}
                  onChange={(e) => {
                    setFormData((prev) => ({
                      ...prev,
                      roomSize: e.target.value
                        ? parseFloat(e.target.value)
                        : undefined,
                    }));
                  }}
                  min="0"
                  step="0.1"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="e.g., 25.5"
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Room Description
                </label>
                <textarea
                  value={roomType.description}
                  onChange={(e) =>
                    updateRoomType(roomType.id, "description", e.target.value)
                  }
                  rows={2}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="Describe this room type..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Base Price (per night) *
                </label>
                <div className="relative">
                  <input
                    type="number"
                    value={(roomType.basePrice || 0) / 100}
                    onChange={(e) =>
                      updateRoomType(
                        roomType.id,
                        "basePrice",
                        parseFloat(e.target.value) * 100
                      )
                    }
                    min="0"
                    step="0.01"
                    className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="0.00"
                  />
                  <span className="absolute left-3 top-3 text-gray-500">$</span>
                </div>
              </div>
            </div>

            {/* Room Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Room Type
                </label>
                <select
                  value={roomType.name || ""}
                  onChange={(e) =>
                    updateRoomType(roomType.id, "name", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="">Select room type</option>
                  {standardRoomTypes.map((type) => (
                    <option key={type} value={type}>
                      {type}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Bed Type
                </label>
                <select
                  value={roomType.bedSetup || ""}
                  onChange={(e) =>
                    updateRoomType(roomType.id, "bedSetup", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="">Select bed type</option>
                  <option value="King Bed">King Bed</option>
                  <option value="Queen Bed">Queen Bed</option>
                  <option value="Double Bed">Double Bed</option>
                  <option value="Twin Beds">Twin Beds</option>
                  <option value="Single Bed">Single Bed</option>
                  <option value="Bunk Beds">Bunk Beds</option>
                  <option value="Sofa Bed">Sofa Bed</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Room View
                </label>
                <select
                  value={roomType.view || ""}
                  onChange={(e) =>
                    updateRoomType(roomType.id, "view", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="">Select view</option>
                  <option value="Ocean View">Ocean View</option>
                  <option value="Sea View">Sea View</option>
                  <option value="Mountain View">Mountain View</option>
                  <option value="City View">City View</option>
                  <option value="Garden View">Garden View</option>
                  <option value="Pool View">Pool View</option>
                  <option value="No View">No View</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Board Type
                </label>
                <select
                  value={roomType.boardType || ""}
                  onChange={(e) =>
                    updateRoomType(roomType.id, "boardType", e.target.value)
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="">Select board type</option>
                  <option value="Room Only">Room Only</option>
                  <option value="Breakfast Included">Breakfast Included</option>
                  <option value="Half Board">Half Board</option>
                  <option value="Full Board">Full Board</option>
                  <option value="All Inclusive">All Inclusive</option>
                </select>
              </div>
            </div>

            {/* Rate Plans */}
            <div className="mt-6">
              <div className="flex justify-between items-center mb-4">
                <h5 className="font-medium text-gray-900">Rate Plans</h5>
                <button
                  type="button"
                  onClick={() => addRatePlan(roomType.id)}
                  className="text-sm text-green-600 hover:bg-green-50 px-3 py-2 rounded-lg transition-colors"
                >
                  + Add Rate Plan
                </button>
              </div>

              {roomType.ratePlans.map((ratePlan, ratePlanIndex) => (
                <div
                  key={ratePlan.id}
                  className="bg-white p-4 rounded-lg border border-gray-200 mb-3"
                >
                  <div className="flex justify-between items-center mb-3">
                    <span className="font-medium text-sm">
                      Rate Plan {ratePlanIndex + 1}
                    </span>
                    <button
                      type="button"
                      onClick={() => removeRatePlan(roomType.id, ratePlan.id)}
                      className="text-red-600 text-sm hover:bg-red-50 px-2 py-1 rounded transition-colors"
                    >
                      Remove
                    </button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Plan Name
                      </label>
                      <input
                        type="text"
                        value={ratePlan.name}
                        onChange={(e) =>
                          updateRatePlan(
                            roomType.id,
                            ratePlan.id,
                            "name",
                            e.target.value
                          )
                        }
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-green-500 focus:border-transparent"
                        placeholder="e.g., Early Bird, Last Minute"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Price Adjustment
                      </label>
                      <div className="flex gap-2">
                        <input
                          type="number"
                          value={ratePlan.priceAdjustment}
                          onChange={(e) =>
                            updateRatePlan(
                              roomType.id,
                              ratePlan.id,
                              "priceAdjustment",
                              parseFloat(e.target.value)
                            )
                          }
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-green-500 focus:border-transparent"
                          placeholder="0"
                        />
                        <select
                          value={ratePlan.adjustmentType}
                          onChange={(e) =>
                            updateRatePlan(
                              roomType.id,
                              ratePlan.id,
                              "adjustmentType",
                              e.target.value as "percentage" | "fixed"
                            )
                          }
                          className="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-green-500 focus:border-transparent"
                        >
                          <option value="percentage">%</option>
                          <option value="fixed">$</option>
                        </select>
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Min Stay (nights)
                      </label>
                      <input
                        type="number"
                        value={ratePlan.minStay || 1}
                        onChange={(e) =>
                          updateRatePlan(
                            roomType.id,
                            ratePlan.id,
                            "minStay",
                            parseInt(e.target.value) || 1
                          )
                        }
                        min="1"
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Cancellation Policy
                      </label>
                      <select
                        value={ratePlan.cancellationPolicy || "Standard"}
                        onChange={(e) =>
                          updateRatePlan(
                            roomType.id,
                            ratePlan.id,
                            "cancellationPolicy",
                            e.target.value
                          )
                        }
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-green-500 focus:border-transparent"
                      >
                        <option value="Standard">Standard</option>
                        <option value="Flexible">Flexible</option>
                        <option value="Moderate">Moderate</option>
                        <option value="Strict">Strict</option>
                        <option value="Non-refundable">Non-refundable</option>
                      </select>
                    </div>

                    <div className="md:col-span-2">
                      <label className="block text-xs font-medium text-gray-700 mb-1">
                        Description
                      </label>
                      <textarea
                        value={ratePlan.description}
                        onChange={(e) =>
                          updateRatePlan(
                            roomType.id,
                            ratePlan.id,
                            "description",
                            e.target.value
                          )
                        }
                        rows={2}
                        className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-green-500 focus:border-transparent"
                        placeholder="Describe the conditions for this rate..."
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}

        <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h4 className="font-medium text-gray-900 mb-3">Add New Room Type</h4>
          <div className="flex gap-3">
            <div className="flex-1">
              <select
                value={selectedStandardRoomType}
                onChange={(e) => setSelectedStandardRoomType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                <option value="">Select Room Type</option>
                {standardRoomTypes.map((roomType) => (
                  <option key={roomType} value={roomType}>
                    {roomType}
                  </option>
                ))}
              </select>
            </div>
            <button
              type="button"
              onClick={addRoomType}
              disabled={!selectedStandardRoomType}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              <svg
                className="w-4 h-4"
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
              Add Room Type
            </button>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            Choose from standard room types or customize the name after adding
          </p>
        </div>
      </div>
    </div>
  );

  // Step 5: Rates & Availability
  const renderRatesAvailability = () => {
    const months = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];

    const getDaysInMonth = (month: number, year: number) => {
      return new Date(year, month + 1, 0).getDate();
    };

    const getFirstDayOfMonth = (month: number, year: number) => {
      return new Date(year, month, 1).getDay();
    };

    const renderCalendar = (roomType: RoomType) => {
      const daysInMonth = getDaysInMonth(selectedMonth, selectedYear);
      const firstDay = getFirstDayOfMonth(selectedMonth, selectedYear);
      const days = [];

      // Add empty cells for days before the first day of the month
      for (let i = 0; i < firstDay; i++) {
        days.push(<div key={`empty-${i}`} className="h-20"></div>);
      }

      // Add cells for each day of the month
      for (let day = 1; day <= daysInMonth; day++) {
        const dateKey = `${selectedYear}-${String(selectedMonth + 1).padStart(
          2,
          "0"
        )}-${String(day).padStart(2, "0")}`;
        const dayAvailability = roomType.dailyAvailability?.[dateKey];
        const isAvailable = dayAvailability?.isAvailable ?? true;
        const specialPrice = dayAvailability?.price;
        const minStay = dayAvailability?.minStay;
        const maxStay = dayAvailability?.maxStay;

        days.push(
          <div
            key={day}
            className={`h-20 border border-gray-200 p-1 cursor-pointer hover:bg-gray-50 ${
              isAvailable ? "bg-green-50" : "bg-red-50"
            }`}
            onClick={() => {
              setDayEditModal({
                isOpen: true,
                date: dateKey,
                roomTypeId: roomType.id,
                availability: {
                  date: dateKey,
                  isAvailable: isAvailable,
                  price: specialPrice,
                  minStay: minStay,
                  maxStay: maxStay,
                },
              });
            }}
          >
            <div className="text-xs font-medium text-gray-900 mb-1">{day}</div>
            <div className="text-xs">
              {specialPrice ? (
                <div className="text-green-600 font-semibold">
                  ${(specialPrice / 100).toFixed(0)}
                </div>
              ) : (
                <div className="text-gray-400">Base</div>
              )}
            </div>
            {minStay && (
              <div className="text-xs text-blue-600">Min: {minStay}</div>
            )}
            {!isAvailable && (
              <div className="text-xs text-red-600 font-medium">Blocked</div>
            )}
          </div>
        );
      }

      return days;
    };

    return (
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Rates & Availability
          </h3>
          <p className="text-gray-600">
            Set daily availability and pricing for each room type using the
            calendar below
          </p>
        </div>

        {/* Month/Year/Room Type Selector */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-4">
            <select
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              {months.map((month, index) => (
                <option key={month} value={index}>
                  {month}
                </option>
              ))}
            </select>
            <select
              value={selectedYear}
              onChange={(e) => setSelectedYear(parseInt(e.target.value))}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value={2024}>2024</option>
              <option value={2025}>2025</option>
              <option value={2026}>2026</option>
            </select>
            <select
              value={selectedRoomType}
              onChange={(e) => setSelectedRoomType(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="">All Room Types</option>
              {formData.roomTypes.map((roomType, index) => (
                <option key={roomType.id} value={roomType.id}>
                  {roomType.name || `Room Type ${index + 1}`}
                </option>
              ))}
            </select>
          </div>
          <div className="text-sm text-gray-600">
            Click days to set custom pricing, availability, and stay
            restrictions • Green = Available, Red = Blocked
          </div>
        </div>

        {/* Calendar Legend */}
        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <h4 className="text-sm font-medium text-gray-900 mb-2">
            Calendar Legend
          </h4>
          <div className="flex flex-wrap gap-4 text-xs">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-green-50 border border-gray-200 rounded"></div>
              <span>Available (base price)</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-green-50 border border-gray-200 rounded relative">
                <span className="absolute inset-0 flex items-center justify-center text-green-600 font-semibold text-xs">
                  $
                </span>
              </div>
              <span>Custom price set</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-red-50 border border-gray-200 rounded"></div>
              <span>Blocked/unavailable</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-blue-600">Min: 2</span>
              <span>Minimum stay required</span>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          {formData.roomTypes
            .filter(
              (roomType) =>
                !selectedRoomType || roomType.id === selectedRoomType
            )
            .map((roomType, index) => (
              <div
                key={roomType.id}
                className="bg-gray-50 p-6 rounded-lg border border-gray-200"
              >
                <div className="flex justify-between items-center mb-4">
                  <h4 className="font-semibold text-gray-900">
                    {roomType.name || `Room Type ${index + 1}`}
                  </h4>
                  <div className="flex items-center space-x-4">
                    <div className="text-sm text-gray-600">
                      Base Price:
                      <input
                        type="number"
                        value={
                          roomType.basePrice
                            ? (roomType.basePrice / 100).toFixed(2)
                            : ""
                        }
                        onChange={(e) => {
                          const newPrice = e.target.value
                            ? parseFloat(e.target.value) * 100
                            : 0;
                          updateRoomType(roomType.id, "basePrice", newPrice);
                        }}
                        className="ml-2 w-20 px-2 py-1 text-sm border border-gray-300 rounded focus:ring-1 focus:ring-green-500 focus:border-transparent"
                        placeholder="0.00"
                        min="0"
                        step="0.01"
                      />
                    </div>
                    <div className="text-sm text-gray-600">
                      Max Guests: {roomType.maxGuests}
                    </div>
                  </div>
                </div>

                {/* Calendar Grid */}
                <div className="bg-white rounded-lg border border-gray-200 p-4">
                  {/* Bulk Operations */}
                  <div className="mb-4 flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => {
                        const currentAvailability =
                          roomType.dailyAvailability || {};
                        const daysInMonth = getDaysInMonth(
                          selectedMonth,
                          selectedYear
                        );
                        const updatedAvailability = { ...currentAvailability };

                        for (let day = 1; day <= daysInMonth; day++) {
                          const dateKey = `${selectedYear}-${String(
                            selectedMonth + 1
                          ).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
                          updatedAvailability[dateKey] = {
                            date: dateKey,
                            isAvailable: true,
                            price: undefined, // Clear special pricing
                            minStay: undefined,
                            maxStay: undefined,
                          };
                        }

                        updateRoomType(
                          roomType.id,
                          "dailyAvailability",
                          updatedAvailability
                        );
                      }}
                      className="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
                    >
                      Clear All Pricing
                    </button>

                    <button
                      type="button"
                      onClick={() => {
                        const currentAvailability =
                          roomType.dailyAvailability || {};
                        const daysInMonth = getDaysInMonth(
                          selectedMonth,
                          selectedYear
                        );
                        const updatedAvailability = { ...currentAvailability };

                        for (let day = 1; day <= daysInMonth; day++) {
                          const dateKey = `${selectedYear}-${String(
                            selectedMonth + 1
                          ).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
                          updatedAvailability[dateKey] = {
                            date: dateKey,
                            isAvailable: false,
                            price: undefined,
                            minStay: undefined,
                            maxStay: undefined,
                          };
                        }

                        updateRoomType(
                          roomType.id,
                          "dailyAvailability",
                          updatedAvailability
                        );
                      }}
                      className="px-3 py-1 text-sm bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
                    >
                      Block Entire Month
                    </button>

                    <button
                      type="button"
                      onClick={() => {
                        const currentAvailability =
                          roomType.dailyAvailability || {};
                        const daysInMonth = getDaysInMonth(
                          selectedMonth,
                          selectedYear
                        );
                        const updatedAvailability = { ...currentAvailability };

                        for (let day = 1; day <= daysInMonth; day++) {
                          const dateKey = `${selectedYear}-${String(
                            selectedMonth + 1
                          ).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
                          const date = new Date(
                            selectedYear,
                            selectedMonth,
                            day
                          );
                          if (date.getDay() === 0 || date.getDay() === 6) {
                            // Weekend
                            updatedAvailability[dateKey] = {
                              date: dateKey,
                              isAvailable: true,
                              price: roomType.basePrice * 1.2, // 20% weekend surcharge
                              minStay: undefined,
                              maxStay: undefined,
                            };
                          }
                        }

                        updateRoomType(
                          roomType.id,
                          "dailyAvailability",
                          updatedAvailability
                        );
                      }}
                      className="px-3 py-1 text-sm bg-green-600 hover:bg-green-700 text-white rounded transition-colors"
                    >
                      Weekend Surcharge (+20%)
                    </button>
                  </div>

                  {/* Day Headers */}
                  <div className="grid grid-cols-7 gap-1 mb-2">
                    {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map(
                      (day) => (
                        <div
                          key={day}
                          className="h-8 flex items-center justify-center text-sm font-medium text-gray-700"
                        >
                          {day}
                        </div>
                      )
                    )}
                  </div>

                  {/* Calendar Days */}
                  <div className="grid grid-cols-7 gap-1">
                    {renderCalendar(roomType)}
                  </div>
                </div>

                {/* Day Edit Modal */}
                {dayEditModal && dayEditModal.roomTypeId === roomType.id && (
                  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">
                        Edit{" "}
                        {new Date(dayEditModal.date).toLocaleDateString(
                          "en-US",
                          {
                            weekday: "long",
                            year: "numeric",
                            month: "long",
                            day: "numeric",
                          }
                        )}
                      </h3>

                      <div className="space-y-4">
                        <div>
                          <label className="flex items-center space-x-2 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={dayEditModal.availability.isAvailable}
                              onChange={(e) =>
                                setDayEditModal((prev) =>
                                  prev
                                    ? {
                                        ...prev,
                                        availability: {
                                          ...prev.availability,
                                          isAvailable: e.target.checked,
                                        },
                                      }
                                    : null
                                )
                              }
                              className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                            />
                            <span className="text-sm font-medium text-gray-700">
                              Available
                            </span>
                          </label>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Price (leave empty for base price)
                          </label>
                          <div className="relative">
                            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                              $
                            </span>
                            <input
                              type="number"
                              value={
                                dayEditModal.availability.price
                                  ? (
                                      dayEditModal.availability.price / 100
                                    ).toFixed(2)
                                  : ""
                              }
                              onChange={(e) =>
                                setDayEditModal((prev) =>
                                  prev
                                    ? {
                                        ...prev,
                                        availability: {
                                          ...prev.availability,
                                          price: e.target.value
                                            ? parseFloat(e.target.value) * 100
                                            : undefined,
                                        },
                                      }
                                    : null
                                )
                              }
                              className="w-full pl-8 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                              placeholder="Base price"
                              min="0"
                              step="0.01"
                            />
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Min Stay (nights)
                            </label>
                            <input
                              type="number"
                              value={dayEditModal.availability.minStay || ""}
                              onChange={(e) =>
                                setDayEditModal((prev) =>
                                  prev
                                    ? {
                                        ...prev,
                                        availability: {
                                          ...prev.availability,
                                          minStay: e.target.value
                                            ? parseInt(e.target.value)
                                            : undefined,
                                        },
                                      }
                                    : null
                                )
                              }
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                              placeholder="1"
                              min="1"
                            />
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Max Stay (nights)
                            </label>
                            <input
                              type="number"
                              value={dayEditModal.availability.maxStay || ""}
                              onChange={(e) =>
                                setDayEditModal((prev) =>
                                  prev
                                    ? {
                                        ...prev,
                                        availability: {
                                          ...prev.availability,
                                          maxStay: e.target.value
                                            ? parseInt(e.target.value)
                                            : undefined,
                                        },
                                      }
                                    : null
                                )
                              }
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                              placeholder="30"
                              min="1"
                            />
                          </div>
                        </div>
                      </div>

                      <div className="flex justify-end space-x-3 mt-6">
                        <button
                          type="button"
                          onClick={() => setDayEditModal(null)}
                          className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                        >
                          Cancel
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            if (dayEditModal) {
                              const currentAvailability =
                                roomType.dailyAvailability || {};
                              updateRoomType(roomType.id, "dailyAvailability", {
                                ...currentAvailability,
                                [dayEditModal.date]: dayEditModal.availability,
                              });
                              setDayEditModal(null);
                            }
                          }}
                          className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                        >
                          Save Changes
                        </button>
                      </div>
                    </div>
                  </div>
                )}

                {/* Room Type Settings */}
                <div className="mt-4 bg-white rounded-lg border border-gray-200 p-4">
                  <h5 className="font-medium text-gray-900 mb-3">
                    Room Type Settings
                  </h5>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Room Name
                      </label>
                      <input
                        type="text"
                        value={roomType.name}
                        onChange={(e) =>
                          updateRoomType(roomType.id, "name", e.target.value)
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        placeholder="e.g., Deluxe Suite"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Max Guests
                      </label>
                      <input
                        type="number"
                        value={roomType.maxGuests || 1}
                        onChange={(e) =>
                          updateRoomType(
                            roomType.id,
                            "maxGuests",
                            parseInt(e.target.value)
                          )
                        }
                        min="1"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Description
                      </label>
                      <input
                        type="text"
                        value={roomType.description}
                        onChange={(e) =>
                          updateRoomType(
                            roomType.id,
                            "description",
                            e.target.value
                          )
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        placeholder="Brief description"
                      />
                    </div>
                  </div>
                </div>
              </div>
            ))}
        </div>

        {/* Check-in/out Times & Policies */}
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            Check-in/out Times & Policies
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Check-in Time
              </label>
              <input
                type="time"
                value={formData.checkInOutTimes?.checkInTime || "15:00"}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    checkInOutTimes: {
                      ...prev.checkInOutTimes,
                      checkInTime: e.target.value,
                    },
                  }));
                }}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Check-out Time
              </label>
              <input
                type="time"
                value={formData.checkInOutTimes?.checkOutTime || "11:00"}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    checkInOutTimes: {
                      ...prev.checkInOutTimes,
                      checkOutTime: e.target.value,
                    },
                  }));
                }}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Early Check-in Fee ($)
              </label>
              <input
                type="number"
                value={formData.checkInOutTimes?.earlyCheckInFee || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    checkInOutTimes: {
                      ...prev.checkInOutTimes,
                      earlyCheckInFee: e.target.value
                        ? parseFloat(e.target.value)
                        : 0,
                    },
                  }));
                }}
                min="0"
                step="0.01"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="0.00"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Late Check-out Fee ($)
              </label>
              <input
                type="number"
                value={formData.checkInOutTimes?.lateCheckOutFee || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    checkInOutTimes: {
                      ...prev.checkInOutTimes,
                      lateCheckOutFee: e.target.value
                        ? parseFloat(e.target.value)
                        : 0,
                    },
                  }));
                }}
                min="0"
                step="0.01"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="0.00"
              />
            </div>
          </div>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="earlyCheckIn"
                checked={formData.checkInOutTimes?.earlyCheckIn || false}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    checkInOutTimes: {
                      ...prev.checkInOutTimes,
                      earlyCheckIn: e.target.checked,
                    },
                  }));
                }}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <label
                htmlFor="earlyCheckIn"
                className="ml-2 text-sm text-gray-700"
              >
                Allow early check-in (additional fee may apply)
              </label>
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                id="lateCheckOut"
                checked={formData.checkInOutTimes?.lateCheckOut || false}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    checkInOutTimes: {
                      ...prev.checkInOutTimes,
                      lateCheckOut: e.target.checked,
                    },
                  }));
                }}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <label
                htmlFor="lateCheckOut"
                className="ml-2 text-sm text-gray-700"
              >
                Allow late check-out (additional fee may apply)
              </label>
            </div>
          </div>
        </div>

        {/* Cancellation Policy */}
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            Cancellation Policy
          </h4>
          <div>
            <select
              value={formData.cancellationPolicy || "Standard"}
              onChange={(e) => {
                setFormData((prev) => ({
                  ...prev,
                  cancellationPolicy: e.target.value,
                }));
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="Flexible">
                Flexible - Free cancellation up to 24 hours
              </option>
              <option value="Moderate">
                Moderate - Free cancellation up to 5 days
              </option>
              <option value="Standard">
                Standard - Free cancellation up to 7 days
              </option>
              <option value="Strict">
                Strict - 50% refund up to 7 days, no refund after
              </option>
              <option value="Non-refundable">
                Non-refundable - No refunds
              </option>
            </select>
          </div>
        </div>

        {/* Safety & Compliance */}
        <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
          <h4 className="text-md font-semibold text-gray-900 mb-4">
            Safety & Compliance
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-3">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="smokeDetectors"
                  checked={formData.safetyCompliance?.smokeDetectors || false}
                  onChange={(e) => {
                    setFormData((prev) => ({
                      ...prev,
                      safetyCompliance: {
                        ...prev.safetyCompliance,
                        smokeDetectors: e.target.checked,
                      },
                    }));
                  }}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label
                  htmlFor="smokeDetectors"
                  className="ml-2 text-sm text-gray-700"
                >
                  Smoke detectors
                </label>
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="carbonMonoxide"
                  checked={
                    formData.safetyCompliance?.carbonMonoxideDetectors || false
                  }
                  onChange={(e) => {
                    setFormData((prev) => ({
                      ...prev,
                      safetyCompliance: {
                        ...prev.safetyCompliance,
                        carbonMonoxideDetectors: e.target.checked,
                      },
                    }));
                  }}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label
                  htmlFor="carbonMonoxide"
                  className="ml-2 text-sm text-gray-700"
                >
                  Carbon monoxide detectors
                </label>
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="firstAidKit"
                  checked={formData.safetyCompliance?.firstAidKit || false}
                  onChange={(e) => {
                    setFormData((prev) => ({
                      ...prev,
                      safetyCompliance: {
                        ...prev.safetyCompliance,
                        firstAidKit: e.target.checked,
                      },
                    }));
                  }}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label
                  htmlFor="firstAidKit"
                  className="ml-2 text-sm text-gray-700"
                >
                  First aid kit
                </label>
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="fireExtinguishers"
                  checked={
                    formData.safetyCompliance?.fireExtinguishers || false
                  }
                  onChange={(e) => {
                    setFormData((prev) => ({
                      ...prev,
                      safetyCompliance: {
                        ...prev.safetyCompliance,
                        fireExtinguishers: e.target.checked,
                      },
                    }));
                  }}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label
                  htmlFor="fireExtinguishers"
                  className="ml-2 text-sm text-gray-700"
                >
                  Fire extinguishers
                </label>
              </div>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="securityCameras"
                  checked={formData.safetyCompliance?.securityCameras || false}
                  onChange={(e) => {
                    setFormData((prev) => ({
                      ...prev,
                      safetyCompliance: {
                        ...prev.safetyCompliance,
                        securityCameras: e.target.checked,
                      },
                    }));
                  }}
                  className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label
                  htmlFor="securityCameras"
                  className="ml-2 text-sm text-gray-700"
                >
                  Security cameras on property
                </label>
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Emergency Contact
              </label>
              <input
                type="text"
                value={formData.safetyCompliance?.emergencyContact || ""}
                onChange={(e) => {
                  setFormData((prev) => ({
                    ...prev,
                    safetyCompliance: {
                      ...prev.safetyCompliance,
                      emergencyContact: e.target.value,
                    },
                  }));
                }}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Phone number or emergency contact info"
              />
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Step 6: Images
  const renderImages = () => (
    <div>
      {/* Temporarily disabled PhotoUpload to test */}
      {/* <PhotoUpload
        images={formData.images}
        onImagesChange={handleImagesChange}
        maxImages={15}
        maxSizeInMB={5}
        title="Upload Property Photos"
        subtitle="Add high-quality photos of your property. The first photo will be used as the cover image."
        acceptedFormats={[".jpg", ".jpeg", ".png", ".webp"]}
      /> */}
      <div className="text-center p-8 border-2 border-dashed border-gray-300 rounded-lg">
        <p className="text-gray-500">
          Photo upload temporarily disabled for testing
        </p>
        <p className="text-sm text-gray-400 mt-2">
          If form stops submitting, the issue is in PhotoUpload component
        </p>
      </div>
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            List Your Accommodation
          </h2>
          <p className="text-gray-600">Step {step} of 6</p>
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
            {Math.round((step / 6) * 100)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-green-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${(step / 6) * 100}%` }}
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

      <form
        method="post"
        action="javascript:void(0)"
        onSubmit={(e) => {
          e.preventDefault();
          console.log("Form onSubmit called", {
            step,
            loading,
            event: e,
            eventType: e.type,
            target: e.target,
            currentTarget: e.currentTarget,
            isTrusted: e.isTrusted,
            timeStamp: e.timeStamp,
          });
          handleSubmit(e);
        }}
        onKeyDown={(e) => {
          // Prevent form submission on Enter key
          if (e.key === "Enter" && step !== 6) {
            e.preventDefault();
            console.log("Enter key prevented on step", step);
          }
        }}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => e.preventDefault()}
      >
        {step === 1 && renderBasicInfo()}
        {step === 2 && renderLocation()}
        {step === 3 && renderPropertyDetails()}
        {step === 4 && renderRoomTypes()}
        {step === 5 && renderRatesAvailability()}
        {/* Step 6 PhotoUpload moved outside form */}

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

          <div className="flex gap-4">
            {step < 6 ? (
              <button
                type="button"
                onClick={nextStep}
                className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
              >
                Next
              </button>
            ) : (
              <button
                type="button" // Changed to button to prevent form submission
                disabled={false} // Enabled for production
                className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                onClick={() => {
                  console.log("Create button clicked");
                  handleSubmit({ preventDefault: () => {} } as React.FormEvent<HTMLFormElement>);
                }}
              >
                Create Accommodation (Test)
              </button>
            )}
          </div>
        </div>
      </form>

      {/* PhotoUpload outside the form to prevent any interference */}
      {step === 6 && (
        <div className="mt-8">
          <PhotoUpload
            images={formData.images}
            onImagesChange={handleImagesChange}
            maxImages={15}
            maxSizeInMB={5}
            title="Upload Property Photos"
            subtitle="Add high-quality photos of your property. The first photo will be used as the cover image."
            acceptedFormats={[".jpg", ".jpeg", ".png", ".webp"]}
          />
        </div>
      )}
    </div>
  );
}
