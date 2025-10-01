"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  ChevronRightIcon,
  MapPinIcon,
  StarIcon,
  ClockIcon,
  UsersIcon,
  GlobeAltIcon,
  CameraIcon,
} from "@heroicons/react/24/outline";
import { StarIcon as StarIconSolid } from "@heroicons/react/24/solid";

// Country data with detailed information
const countryData: Record<
  string,
  {
    name: string;
    fullName: string;
    capital: string;
    population: string;
    currency: string;
    language: string;
    description: string;
    highlights: string[];
    bestTimeToVisit: string;
    visaRequirements: string;
    flag: string;
    heroImage: string;
    destinations: Array<{
      id: string;
      name: string;
      description: string;
      imageUrl: string;
      rating: number;
      reviewCount: number;
      tours: number;
      category: string;
    }>;
    stats: {
      totalDestinations: number;
      totalTours: number;
      averageRating: number;
      popularActivities: string[];
    };
  }
> = {
  jordan: {
    name: "Jordan",
    fullName: "The Hashemite Kingdom of Jordan",
    capital: "Amman",
    population: "10.5 million",
    currency: "Jordanian Dinar (JOD)",
    language: "Arabic",
    description:
      "Jordan is a Middle Eastern country known for its ancient history, stunning desert landscapes, and warm hospitality. From the rose-red city of Petra to the serene waters of the Dead Sea, Jordan offers a perfect blend of archaeological wonders and natural beauty.",
    highlights: [
      "Petra - One of the Seven Wonders of the World",
      "Wadi Rum - Desert landscapes featured in Star Wars",
      "Dead Sea - The lowest point on Earth",
      "Jerash - Ancient Roman city",
      "Aqaba - Red Sea coastal city",
    ],
    bestTimeToVisit: "March to May, September to November",
    visaRequirements: "Visa on arrival for most nationalities",
    flag: "🇯🇴",
    heroImage: "/hero/chalets.webp",
    destinations: [
      {
        id: "1",
        name: "Petra",
        description: "Ancient Nabatean city carved into rose-red cliffs",
        imageUrl: "/hero/chalets.webp",
        rating: 4.8,
        reviewCount: 2450,
        tours: 450,
        category: "Historical",
      },
      {
        id: "2",
        name: "Wadi Rum",
        description: "Stunning desert valley with unique rock formations",
        imageUrl: "/hero/caravan.webp",
        rating: 4.7,
        reviewCount: 1890,
        tours: 320,
        category: "Adventure",
      },
      {
        id: "3",
        name: "Dead Sea",
        description: "Salt lake famous for its mineral-rich waters",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.5,
        reviewCount: 1650,
        tours: 280,
        category: "Wellness",
      },
    ],
    stats: {
      totalDestinations: 15,
      totalTours: 850,
      averageRating: 4.6,
      popularActivities: [
        "Historical Tours",
        "Desert Safaris",
        "Cultural Experiences",
        "Adventure Activities",
      ],
    },
  },
  uae: {
    name: "UAE",
    fullName: "United Arab Emirates",
    capital: "Abu Dhabi",
    population: "9.9 million",
    currency: "UAE Dirham (AED)",
    language: "Arabic",
    description:
      "The UAE is a federation of seven emirates, each offering unique experiences from futuristic skyscrapers in Dubai to cultural heritage in Abu Dhabi. Known for luxury, innovation, and hospitality.",
    highlights: [
      "Burj Khalifa - World's tallest building",
      "Palm Jumeirah - Man-made island",
      "Dubai Mall - World's largest shopping mall",
      "Desert Safari experiences",
      "Traditional souks and markets",
    ],
    bestTimeToVisit: "November to March",
    visaRequirements: "Visa on arrival for many nationalities",
    flag: "🇦🇪",
    heroImage: "/hero/hotel.webp",
    destinations: [
      {
        id: "1",
        name: "Dubai",
        description:
          "Modern metropolis with iconic skyscrapers and luxury shopping",
        imageUrl: "/hero/hotel.webp",
        rating: 4.6,
        reviewCount: 3200,
        tours: 800,
        category: "Modern",
      },
      {
        id: "2",
        name: "Abu Dhabi",
        description: "Cultural capital with stunning mosques and museums",
        imageUrl: "/hero/apartment.webp",
        rating: 4.5,
        reviewCount: 2100,
        tours: 450,
        category: "Cultural",
      },
      {
        id: "3",
        name: "Sharjah",
        description: "Cultural hub with heritage sites and museums",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.3,
        reviewCount: 1200,
        tours: 280,
        category: "Cultural",
      },
    ],
    stats: {
      totalDestinations: 12,
      totalTours: 1200,
      averageRating: 4.5,
      popularActivities: [
        "City Tours",
        "Desert Safaris",
        "Shopping",
        "Luxury Experiences",
      ],
    },
  },
  palestine: {
    name: "Palestine",
    fullName: "State of Palestine",
    capital: "Ramallah (Administrative), Jerusalem (Claimed)",
    population: "5.4 million",
    currency: "Israeli Shekel (ILS), Jordanian Dinar (JOD)",
    language: "Arabic",
    description:
      "Palestine offers a rich tapestry of history, culture, and resilience. From the ancient walls of Jerusalem to the vibrant streets of Bethlehem, discover the heart of the Holy Land.",
    highlights: [
      "Jerusalem - Holy city for three major religions",
      "Bethlehem - Birthplace of Jesus Christ",
      "Hebron - Ancient city with rich history",
      "Nablus - Known for traditional soap and food",
      "Gaza - Coastal city with Mediterranean charm",
    ],
    bestTimeToVisit: "March to May, September to November",
    visaRequirements: "Complex visa situation - check current requirements",
    flag: "🇵🇸",
    heroImage: "/hero/travelhero.webp",
    destinations: [
      {
        id: "1",
        name: "Jerusalem",
        description:
          "Holy city with religious significance for Judaism, Christianity, and Islam",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.7,
        reviewCount: 2100,
        tours: 380,
        category: "Historical",
      },
      {
        id: "2",
        name: "Bethlehem",
        description:
          "Ancient city known for its religious heritage and olive wood crafts",
        imageUrl: "/hero/caravan.webp",
        rating: 4.4,
        reviewCount: 1450,
        tours: 220,
        category: "Cultural",
      },
      {
        id: "3",
        name: "Ramallah",
        description: "Cultural and political center with modern amenities",
        imageUrl: "/hero/caravan.webp",
        rating: 4.1,
        reviewCount: 520,
        tours: 90,
        category: "Cultural",
      },
    ],
    stats: {
      totalDestinations: 8,
      totalTours: 450,
      averageRating: 4.2,
      popularActivities: [
        "Religious Tours",
        "Historical Sites",
        "Cultural Experiences",
        "Market Visits",
      ],
    },
  },
  "saudi-arabia": {
    name: "Saudi Arabia",
    fullName: "Kingdom of Saudi Arabia",
    capital: "Riyadh",
    population: "35.9 million",
    currency: "Saudi Riyal (SAR)",
    language: "Arabic",
    description:
      "Saudi Arabia, the birthplace of Islam, offers a unique blend of ancient Islamic heritage and modern development. From the holy cities of Mecca and Medina to the Red Sea coast, discover the Kingdom's diverse landscapes.",
    highlights: [
      "Mecca - Holiest city in Islam",
      "Medina - Second holiest city in Islam",
      "Riyadh - Modern capital city",
      "Red Sea coastal areas",
      "Desert landscapes and oases",
    ],
    bestTimeToVisit: "October to April",
    visaRequirements: "eVisa available for many nationalities",
    flag: "🇸🇦",
    heroImage: "/hero/caravan.webp",
    destinations: [
      {
        id: "1",
        name: "Mecca",
        description: "Holiest city in Islam, home to the Kaaba",
        imageUrl: "/hero/caravan.webp",
        rating: 4.9,
        reviewCount: 1800,
        tours: 200,
        category: "Religious",
      },
      {
        id: "2",
        name: "Riyadh",
        description:
          "Modern capital with traditional souks and contemporary architecture",
        imageUrl: "/hero/caravan.webp",
        rating: 4.3,
        reviewCount: 1680,
        tours: 420,
        category: "Cultural",
      },
      {
        id: "3",
        name: "Medina",
        description: "Second holiest city in Islam with Prophet's Mosque",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.8,
        reviewCount: 1500,
        tours: 180,
        category: "Religious",
      },
    ],
    stats: {
      totalDestinations: 18,
      totalTours: 950,
      averageRating: 4.4,
      popularActivities: [
        "Religious Pilgrimage",
        "Cultural Tours",
        "Desert Activities",
        "Modern Attractions",
      ],
    },
  },
  qatar: {
    name: "Qatar",
    fullName: "State of Qatar",
    capital: "Doha",
    population: "2.9 million",
    currency: "Qatari Riyal (QAR)",
    language: "Arabic",
    description:
      "Qatar is a small but wealthy nation known for its modern architecture, cultural heritage, and hospitality. From the futuristic skyline of Doha to traditional desert experiences, Qatar offers a perfect blend of tradition and innovation.",
    highlights: [
      "Doha - Modern capital with stunning architecture",
      "Museum of Islamic Art - World-class museum",
      "Souq Waqif - Traditional market",
      "Desert experiences",
      "Luxury shopping and dining",
    ],
    bestTimeToVisit: "November to March",
    visaRequirements: "Visa on arrival for many nationalities",
    flag: "🇶🇦",
    heroImage: "/hero/apartment.webp",
    destinations: [
      {
        id: "1",
        name: "Doha",
        description:
          "Modern capital blending Islamic architecture with contemporary design",
        imageUrl: "/hero/apartment.webp",
        rating: 4.4,
        reviewCount: 1420,
        tours: 280,
        category: "Cultural",
      },
      {
        id: "2",
        name: "Al Wakrah",
        description:
          "Coastal city with traditional souks and modern developments",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.2,
        reviewCount: 680,
        tours: 120,
        category: "Cultural",
      },
      {
        id: "3",
        name: "Al Khor",
        description: "Charming coastal town with beautiful beaches and coral reefs",
        imageUrl: "/hero/caravan.webp",
        rating: 4.1,
        reviewCount: 450,
        tours: 85,
        category: "Adventure",
      },
    ],
    stats: {
      totalDestinations: 6,
      totalTours: 350,
      averageRating: 4.3,
      popularActivities: [
        "Museum Tours",
        "Cultural Experiences",
        "Desert Activities",
        "Shopping",
      ],
    },
  },
  kuwait: {
    name: "Kuwait",
    fullName: "State of Kuwait",
    capital: "Kuwait City",
    population: "4.3 million",
    currency: "Kuwait Dinar (KWD)",
    language: "Arabic",
    description:
      "Kuwait is a modern Gulf state with a rich maritime heritage and impressive skyline. Known for its hospitality and blend of traditional culture with contemporary development.",
    highlights: [
      "Kuwait City - Modern capital with impressive towers",
      "Kuwait Towers - Iconic water towers",
      "Souq Mubarakiya - Traditional market",
      "Liberation Tower - Modern architecture",
      "Marina Bay and coastal areas",
    ],
    bestTimeToVisit: "November to March",
    visaRequirements: "Visa on arrival for many nationalities",
    flag: "🇰🇼",
    heroImage: "/hero/travelhero.webp",
    destinations: [
      {
        id: "1",
        name: "Kuwait City",
        description:
          "Modern capital with traditional souks and contemporary architecture",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.2,
        reviewCount: 920,
        tours: 190,
        category: "Modern",
      },
      {
        id: "2",
        name: "Kuwait Towers",
        description: "Iconic water towers symbolizing Kuwait's modern identity",
        imageUrl: "/hero/apartment.webp",
        rating: 4.0,
        reviewCount: 650,
        tours: 95,
        category: "Modern",
      },
      {
        id: "3",
        name: "Failaka Island",
        description: "Historical island with ancient ruins and beautiful beaches",
        imageUrl: "/hero/caravan.webp",
        rating: 3.9,
        reviewCount: 380,
        tours: 65,
        category: "Historical",
      },
    ],
    stats: {
      totalDestinations: 4,
      totalTours: 220,
      averageRating: 4.1,
      popularActivities: [
        "City Tours",
        "Museum Visits",
        "Market Exploration",
        "Cultural Experiences",
      ],
    },
  },
  bahrain: {
    name: "Bahrain",
    fullName: "Kingdom of Bahrain",
    capital: "Manama",
    population: "1.8 million",
    currency: "Bahrain Dinar (BHD)",
    language: "Arabic",
    description:
      "Bahrain, the smallest Arab country, is an island nation known for its ancient forts, modern development, and strategic location in the Persian Gulf. A perfect blend of ancient forts and contemporary lifestyle.",
    highlights: [
      "Bahrain Fort - Ancient Portuguese fort",
      "Bab Al Bahrain - Historic gate",
      "Gold Souq - Traditional market",
      "Formula 1 circuit",
      "Pearl diving heritage",
    ],
    bestTimeToVisit: "November to March",
    visaRequirements: "Visa on arrival for many nationalities",
    flag: "🇧🇭",
    heroImage: "/hero/apartment.webp",
    destinations: [
      {
        id: "1",
        name: "Manama",
        description:
          "Vibrant capital with ancient forts and modern attractions",
        imageUrl: "/hero/apartment.webp",
        rating: 4.1,
        reviewCount: 1100,
        tours: 150,
        category: "Cultural",
      },
      {
        id: "2",
        name: "Muharraq",
        description: "Historical city with traditional architecture and cultural sites",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.0,
        reviewCount: 580,
        tours: 85,
        category: "Historical",
      },
      {
        id: "3",
        name: "Riffa",
        description: "Royal city with palaces and traditional Bahraini culture",
        imageUrl: "/hero/caravan.webp",
        rating: 3.9,
        reviewCount: 420,
        tours: 65,
        category: "Cultural",
      },
    ],
    stats: {
      totalDestinations: 3,
      totalTours: 180,
      averageRating: 4.0,
      popularActivities: [
        "Historical Tours",
        "Market Visits",
        "Cultural Experiences",
        "Modern Attractions",
      ],
    },
  },
  oman: {
    name: "Oman",
    fullName: "Sultanate of Oman",
    capital: "Muscat",
    population: "5.2 million",
    currency: "Omani Rial (OMR)",
    language: "Arabic",
    description:
      "Oman is known for its stunning natural beauty, rich maritime history, and warm hospitality. From the rugged mountains to pristine beaches, Oman offers diverse landscapes and cultural experiences.",
    highlights: [
      "Muscat - Elegant capital city",
      "Sultan Qaboos Grand Mosque",
      "Mutrah Souq - Traditional market",
      "Al Alam Palace",
      "Coastal and mountain landscapes",
    ],
    bestTimeToVisit: "October to April",
    visaRequirements: "Visa on arrival for many nationalities",
    flag: "🇴🇲",
    heroImage: "/hero/hotel.webp",
    destinations: [
      {
        id: "1",
        name: "Muscat",
        description:
          "Elegant capital with stunning mosques and traditional souks",
        imageUrl: "/hero/hotel.webp",
        rating: 4.5,
        reviewCount: 980,
        tours: 220,
        category: "Cultural",
      },
      {
        id: "2",
        name: "Nizwa",
        description: "Ancient inland city with historic forts and traditional markets",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.3,
        reviewCount: 720,
        tours: 140,
        category: "Historical",
      },
      {
        id: "3",
        name: "Salalah",
        description: "Southern coastal city known for frankincense and monsoon rains",
        imageUrl: "/hero/caravan.webp",
        rating: 4.4,
        reviewCount: 650,
        tours: 110,
        category: "Adventure",
      },
    ],
    stats: {
      totalDestinations: 8,
      totalTours: 280,
      averageRating: 4.4,
      popularActivities: [
        "Historical Tours",
        "Market Visits",
        "Coastal Activities",
        "Cultural Experiences",
      ],
    },
  },
  turkey: {
    name: "Turkey",
    fullName: "Republic of Turkey",
    capital: "Ankara",
    population: "85.3 million",
    currency: "Turkish Lira (TRY)",
    language: "Turkish",
    description:
      "Turkey bridges Europe and Asia, offering a fascinating mix of Eastern and Western cultures. From the historic streets of Istanbul to the stunning landscapes of Cappadocia, Turkey is a treasure trove of experiences.",
    highlights: [
      "Istanbul - City of two continents",
      "Cappadocia - Unique rock formations",
      "Ephesus - Ancient Greek city",
      "Pamukkale - Natural thermal pools",
      "Mediterranean and Aegean coasts",
    ],
    bestTimeToVisit: "April to June, September to November",
    visaRequirements: "eVisa available for many nationalities",
    flag: "🇹🇷",
    heroImage: "/hero/travelhero.webp",
    destinations: [
      {
        id: "1",
        name: "Istanbul",
        description:
          "Historic city bridging Europe and Asia with rich cultural heritage",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.6,
        reviewCount: 3800,
        tours: 950,
        category: "Historical",
      },
      {
        id: "2",
        name: "Cappadocia",
        description: "Surreal landscape with cave dwellings and hot air balloon rides",
        imageUrl: "/hero/caravan.webp",
        rating: 4.7,
        reviewCount: 2900,
        tours: 680,
        category: "Adventure",
      },
      {
        id: "3",
        name: "Antalya",
        description: "Beautiful coastal city with ancient ruins and Mediterranean beaches",
        imageUrl: "/hero/apartment.webp",
        rating: 4.4,
        reviewCount: 2100,
        tours: 420,
        category: "Adventure",
      },
    ],
    stats: {
      totalDestinations: 25,
      totalTours: 1200,
      averageRating: 4.5,
      popularActivities: [
        "Historical Tours",
        "Cultural Experiences",
        "Adventure Activities",
        "Beach Holidays",
      ],
    },
  },
  syria: {
    name: "Syria",
    fullName: "Syrian Arab Republic",
    capital: "Damascus",
    population: "21.3 million",
    currency: "Syrian Pound (SYP)",
    language: "Arabic",
    description:
      "Syria, known as the cradle of civilization, boasts one of the world's oldest continuously inhabited cities. Despite challenges, it offers rich archaeological sites and cultural heritage.",
    highlights: [
      "Damascus - World's oldest continuously inhabited city",
      "Aleppo - Historic UNESCO site",
      "Palmyra - Ancient desert city",
      "Crac des Chevaliers - Medieval castle",
      "Coastal cities and mountains",
    ],
    bestTimeToVisit: "March to May, October to November",
    visaRequirements: "Complex visa situation - check current requirements",
    flag: "🇸🇾",
    heroImage: "/hero/treehouses.webp",
    destinations: [
      {
        id: "1",
        name: "Damascus",
        description: "Ancient city with Umayyad Mosque and vibrant souks",
        imageUrl: "/hero/treehouses.webp",
        rating: 4.0,
        reviewCount: 650,
        tours: 120,
        category: "Historical",
      },
      {
        id: "2",
        name: "Aleppo",
        description: "Historic city with ancient citadel and traditional markets",
        imageUrl: "/hero/caravan.webp",
        rating: 3.9,
        reviewCount: 480,
        tours: 95,
        category: "Historical",
      },
      {
        id: "3",
        name: "Homs",
        description: "Ancient city on the Orontes River with rich archaeological sites",
        imageUrl: "/hero/travelhero.webp",
        rating: 3.8,
        reviewCount: 320,
        tours: 70,
        category: "Historical",
      },
    ],
    stats: {
      totalDestinations: 12,
      totalTours: 180,
      averageRating: 3.8,
      popularActivities: [
        "Historical Tours",
        "Cultural Experiences",
        "Market Visits",
        "Archaeological Sites",
      ],
    },
  },
  iraq: {
    name: "Iraq",
    fullName: "Republic of Iraq",
    capital: "Baghdad",
    population: "42.7 million",
    currency: "Iraqi Dinar (IQD)",
    language: "Arabic, Kurdish",
    description:
      "Iraq, the land between two rivers, is home to some of the world's most ancient civilizations. From the fertile plains of Mesopotamia to the rugged mountains of Kurdistan, Iraq offers a rich tapestry of history and culture.",
    highlights: [
      "Baghdad - Historic capital city",
      "Babylon - Ancient Mesopotamian city",
      "Uruk - Birthplace of writing",
      "Ziggurat of Ur",
      "Kurdish mountains and plains",
    ],
    bestTimeToVisit: "October to April",
    visaRequirements: "Visa required - check current requirements",
    flag: "🇮🇶",
    heroImage: "/hero/motels.webp",
    destinations: [
      {
        id: "1",
        name: "Baghdad",
        description: "Historic capital with ancient mosques and museums",
        imageUrl: "/hero/motels.webp",
        rating: 3.8,
        reviewCount: 420,
        tours: 140,
        category: "Historical",
      },
      {
        id: "2",
        name: "Erbil",
        description: "Ancient city in Kurdistan with citadel and modern developments",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.0,
        reviewCount: 580,
        tours: 110,
        category: "Cultural",
      },
      {
        id: "3",
        name: "Babylon",
        description: "Ancient Mesopotamian city with legendary hanging gardens",
        imageUrl: "/hero/caravan.webp",
        rating: 4.1,
        reviewCount: 720,
        tours: 95,
        category: "Historical",
      },
    ],
    stats: {
      totalDestinations: 15,
      totalTours: 220,
      averageRating: 3.7,
      popularActivities: [
        "Historical Tours",
        "Cultural Experiences",
        "Market Visits",
        "Educational Tours",
      ],
    },
  },
  yemen: {
    name: "Yemen",
    fullName: "Republic of Yemen",
    capital: "Sana'a",
    population: "31.2 million",
    currency: "Yemeni Rial (YER)",
    language: "Arabic",
    description:
      "Yemen, the land of the Queen of Sheba, offers ancient cities, stunning coastlines, and rich cultural heritage. Known for its unique architecture and strategic location at the crossroads of civilizations.",
    highlights: [
      "Sana'a - Ancient capital city",
      "Zabid - Historic coastal city",
      "Shibam - Mud brick city",
      "Socotra - Unique island ecosystem",
      "Aden - Historic port city",
    ],
    bestTimeToVisit: "November to February",
    visaRequirements: "Visa required - check current requirements",
    flag: "🇾🇪",
    heroImage: "/hero/hostels.webp",
    destinations: [
      {
        id: "1",
        name: "Sana'a",
        description:
          "Ancient capital with unique architecture and rich cultural heritage",
        imageUrl: "/hero/hostels.webp",
        rating: 3.9,
        reviewCount: 380,
        tours: 80,
        category: "Historical",
      },
      {
        id: "2",
        name: "Aden",
        description: "Historic port city with colonial architecture and coastal beauty",
        imageUrl: "/hero/travelhero.webp",
        rating: 3.8,
        reviewCount: 290,
        tours: 65,
        category: "Historical",
      },
      {
        id: "3",
        name: "Shibam",
        description: "Ancient mud-brick city known as the 'Manhattan of the Desert'",
        imageUrl: "/hero/caravan.webp",
        rating: 4.0,
        reviewCount: 420,
        tours: 75,
        category: "Historical",
      },
    ],
    stats: {
      totalDestinations: 10,
      totalTours: 120,
      averageRating: 3.8,
      popularActivities: [
        "Historical Tours",
        "Cultural Experiences",
        "Architectural Walks",
        "Market Exploration",
      ],
    },
  },
  lebanon: {
    name: "Lebanon",
    fullName: "Lebanese Republic",
    capital: "Beirut",
    population: "5.3 million",
    currency: "Lebanese Pound (LBP)",
    language: "Arabic",
    description:
      "Lebanon, the 'Switzerland of the East', offers stunning Mediterranean landscapes, ancient ruins, and vibrant cultural scenes. From the bustling streets of Beirut to the serene cedars of the mountains.",
    highlights: [
      "Beirut - Vibrant capital city",
      "Baalbek - Ancient Roman temples",
      "Byblos - World's oldest continuously inhabited city",
      "Cedar forests",
      "Mediterranean coastline",
    ],
    bestTimeToVisit: "April to June, September to November",
    visaRequirements: "Visa on arrival for many nationalities",
    flag: "🇱🇧",
    heroImage: "/hero/travelhero.webp",
    destinations: [
      {
        id: "1",
        name: "Beirut",
        description:
          "Vibrant capital with Mediterranean charm and rich cultural heritage",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.2,
        reviewCount: 1350,
        tours: 350,
        category: "Cultural",
      },
      {
        id: "2",
        name: "Baalbek",
        description: "Ancient city with massive Roman temple ruins",
        imageUrl: "/hero/caravan.webp",
        rating: 4.4,
        reviewCount: 890,
        tours: 180,
        category: "Historical",
      },
      {
        id: "3",
        name: "Byblos",
        description: "Ancient Phoenician city with Mediterranean beaches",
        imageUrl: "/hero/apartment.webp",
        rating: 4.1,
        reviewCount: 720,
        tours: 140,
        category: "Historical",
      },
    ],
    stats: {
      totalDestinations: 8,
      totalTours: 420,
      averageRating: 4.1,
      popularActivities: [
        "City Tours",
        "Historical Sites",
        "Beach Activities",
        "Cultural Experiences",
      ],
    },
  },
  egypt: {
    name: "Egypt",
    fullName: "Arab Republic of Egypt",
    capital: "Cairo",
    population: "109.3 million",
    currency: "Egyptian Pound (EGP)",
    language: "Arabic",
    description:
      "Egypt, the gift of the Nile, is home to one of the world's greatest civilizations. From the pyramids of Giza to the temples of Luxor, Egypt offers unparalleled historical and cultural experiences.",
    highlights: [
      "Pyramids of Giza - Ancient wonders",
      "Valley of the Kings - Royal tombs",
      "Nile River cruises",
      "Alexandria - Historic coastal city",
      "Red Sea resorts",
    ],
    bestTimeToVisit: "October to April",
    visaRequirements: "Visa on arrival for many nationalities",
    flag: "🇪🇬",
    heroImage: "/hero/travelhero.webp",
    destinations: [
      {
        id: "1",
        name: "Cairo",
        description:
          "Historic capital with pyramids, museums, and vibrant culture",
        imageUrl: "/hero/travelhero.webp",
        rating: 4.4,
        reviewCount: 2800,
        tours: 600,
        category: "Historical",
      },
      {
        id: "2",
        name: "Luxor",
        description: "Ancient city with Karnak Temple and Valley of the Kings",
        imageUrl: "/hero/caravan.webp",
        rating: 4.6,
        reviewCount: 2100,
        tours: 450,
        category: "Historical",
      },
      {
        id: "3",
        name: "Alexandria",
        description: "Mediterranean coastal city with Greek and Roman history",
        imageUrl: "/hero/apartment.webp",
        rating: 4.2,
        reviewCount: 1600,
        tours: 320,
        category: "Historical",
      },
    ],
    stats: {
      totalDestinations: 20,
      totalTours: 850,
      averageRating: 4.3,
      popularActivities: [
        "Historical Tours",
        "Nile Cruises",
        "Desert Adventures",
        "Cultural Experiences",
      ],
    },
  },
};

export default function CountryPage() {
  const params = useParams();
  const countrySlug = params.country as string;
  const country = countryData[countrySlug];

  const [selectedCategory, setSelectedCategory] = useState("All");

  if (!country) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <GlobeAltIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Country Not Found
          </h1>
          <p className="text-gray-600 mb-6">
            The country you&apos;re looking for doesn&apos;t exist in our
            database.
          </p>
          <Link
            href="/destinations"
            className="bg-orange-600 text-white px-6 py-3 rounded-lg hover:bg-orange-700 transition-colors"
          >
            Explore All Destinations
          </Link>
        </div>
      </div>
    );
  }

  const filteredDestinations =
    selectedCategory === "All"
      ? country.destinations
      : country.destinations.filter(
          (dest) => dest.category === selectedCategory
        );

  const categories = [
    "All",
    ...Array.from(new Set(country.destinations.map((dest) => dest.category))),
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-sm sticky top-0 z-40 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link href="/destinations" className="text-gray-600 hover:text-orange-600 transition-colors">
                ← Back to Destinations
              </Link>
              <div className="flex items-center space-x-6">
                <button
                  onClick={() => document.getElementById('overview')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-700 hover:text-orange-600 font-medium transition-colors"
                >
                  Overview
                </button>
                <button
                  onClick={() => document.getElementById('destinations')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-700 hover:text-orange-600 font-medium transition-colors"
                >
                  Destinations
                </button>
                <button
                  onClick={() => document.getElementById('highlights')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-700 hover:text-orange-600 font-medium transition-colors"
                >
                  Highlights
                </button>
                <button
                  onClick={() => document.getElementById('tours')?.scrollIntoView({ behavior: 'smooth' })}
                  className="text-gray-700 hover:text-orange-600 font-medium transition-colors"
                >
                  Tours
                </button>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-2xl">{country.flag}</span>
              <span className="font-semibold text-gray-900">{country.name}</span>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section
        id="overview"
        className="relative bg-gradient-to-r from-orange-600 to-red-600 text-white py-24 min-h-[60vh] bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url('${country.heroImage}')` }}
      >
        <div className="absolute inset-0 bg-black/50"></div>
        <div className="relative max-w-7xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center mb-4">
            <span className="text-6xl mr-4">{country.flag}</span>
            <h1 className="text-5xl font-bold">{country.name}</h1>
          </div>
          <p className="text-xl mb-8 max-w-3xl mx-auto">
            {country.description}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-sm opacity-90">Capital</div>
              <div className="font-semibold">{country.capital}</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-sm opacity-90">Population</div>
              <div className="font-semibold">{country.population}</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-sm opacity-90">Currency</div>
              <div className="font-semibold">{country.currency}</div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white border-b">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">
                {country.stats.totalDestinations}
              </div>
              <div className="text-gray-600">Destinations</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">
                {country.stats.totalTours}
              </div>
              <div className="text-gray-600">Tours Available</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">
                {country.stats.averageRating}
              </div>
              <div className="text-gray-600">Average Rating</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">
                {country.flag}
              </div>
              <div className="text-gray-600">Country</div>
            </div>
          </div>
        </div>
      </section>

      {/* Country Info Section */}
      <section id="highlights" className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          <div className="mb-8">
            <div className="relative h-64 rounded-2xl overflow-hidden mb-8">
              <Image
                src={country.heroImage}
                alt={`${country.name} highlights`}
                fill
                className="object-cover"
              />
              <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                <div className="text-center text-white">
                  <h2 className="text-4xl font-bold mb-2">Discover {country.name}</h2>
                  <p className="text-xl opacity-90">Explore the highlights and hidden gems</p>
                </div>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">
                About {country.name}
              </h2>
              <div className="space-y-4 text-gray-600">
                <p>
                  <strong>Official Name:</strong> {country.fullName}
                </p>
                <p>
                  <strong>Capital:</strong> {country.capital}
                </p>
                <p>
                  <strong>Population:</strong> {country.population}
                </p>
                <p>
                  <strong>Language:</strong> {country.language}
                </p>
                <p>
                  <strong>Currency:</strong> {country.currency}
                </p>
              </div>

              <div className="mt-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Best Time to Visit
                </h3>
                <p className="text-gray-600">{country.bestTimeToVisit}</p>
              </div>

              <div className="mt-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Visa Requirements
                </h3>
                <p className="text-gray-600">{country.visaRequirements}</p>
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">
                Highlights
              </h3>
              <div className="space-y-3">
                {country.highlights.map((highlight, index) => (
                  <div key={index} className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-gray-600">{highlight}</p>
                  </div>
                ))}
              </div>

              <div className="mt-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Popular Activities
                </h3>
                <div className="flex flex-wrap gap-2">
                  {country.stats.popularActivities.map((activity, index) => (
                    <span
                      key={index}
                      className="bg-orange-100 text-orange-700 px-3 py-1 text-sm rounded-full"
                    >
                      {activity}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Destinations Section */}
      <section id="destinations" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="mb-8">
            <div className="relative h-64 rounded-2xl overflow-hidden mb-8">
              <Image
                src={country.destinations[0]?.imageUrl || country.heroImage}
                alt={`${country.name} destinations`}
                fill
                className="object-cover"
              />
              <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                <div className="text-center text-white">
                  <h2 className="text-4xl font-bold mb-2">Explore Destinations</h2>
                  <p className="text-xl opacity-90">Amazing places to visit in {country.name}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Explore {country.name}
            </h2>
            <p className="text-lg text-gray-600 mb-6">
              Discover amazing destinations and experiences in {country.name}
            </p>

            {/* Category Filter */}
            <div className="flex gap-2 flex-wrap">
              {categories.map((category) => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    selectedCategory === category
                      ? "bg-orange-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredDestinations.map((destination) => (
              <div
                key={destination.id}
                className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 group border"
              >
                {/* Image */}
                <div className="relative h-64 overflow-hidden">
                  <Image
                    src={destination.imageUrl}
                    alt={destination.name}
                    fill
                    className="object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  <div className="absolute top-4 left-4">
                    <span className="bg-orange-500 text-white px-3 py-1 text-sm font-semibold rounded-full">
                      {destination.category}
                    </span>
                  </div>
                  <div className="absolute top-4 right-4">
                    <div className="flex items-center bg-white/90 backdrop-blur-sm rounded-lg px-2 py-1">
                      <StarIconSolid className="w-4 h-4 text-yellow-400" />
                      <span className="text-sm font-semibold ml-1">
                        {destination.rating}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="p-6">
                  <div className="mb-3">
                    <h3 className="text-2xl font-bold text-gray-900 mb-1 group-hover:text-orange-600 transition-colors">
                      {destination.name}
                    </h3>
                    <div className="flex items-center text-gray-600 mb-2">
                      <MapPinIcon className="w-4 h-4 mr-1" />
                      <span>{country.name}</span>
                    </div>
                    <p className="text-gray-600 text-sm line-clamp-2">
                      {destination.description}
                    </p>
                  </div>

                  {/* Stats */}
                  <div className="flex items-center justify-between text-sm text-gray-600 mb-4">
                    <div className="flex items-center">
                      <StarIcon className="w-4 h-4 mr-1" />
                      <span>{destination.reviewCount} reviews</span>
                    </div>
                    <div className="flex items-center">
                      <CameraIcon className="w-4 h-4 mr-1" />
                      <span>{destination.tours} tours</span>
                    </div>
                  </div>

                  {/* CTA */}
                  <Link
                    href={`/tours?destination=${destination.name
                      .toLowerCase()
                      .replace(/\s+/g, "-")}`}
                    className="w-full bg-orange-600 text-white px-4 py-3 rounded-lg hover:bg-orange-700 transition-colors flex items-center justify-center font-medium group-hover:translate-y-0.5"
                  >
                    Explore Tours
                    <ChevronRightIcon className="w-4 h-4 ml-2" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section id="tours" className="py-16 bg-gradient-to-r from-orange-600 to-red-600 text-white">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <div className="relative h-64 rounded-2xl overflow-hidden mb-8">
            <Image
              src={country.heroImage}
              alt={`${country.name} tours`}
              fill
              className="object-cover"
            />
            <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
              <div className="text-center text-white">
                <h2 className="text-4xl font-bold mb-2">Available Tours</h2>
                <p className="text-xl opacity-90">Book your perfect experience in {country.name}</p>
              </div>
            </div>
          </div>
          <h2 className="text-4xl font-bold mb-6">
            Ready to Explore {country.name}?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Discover amazing experiences and create unforgettable memories in{" "}
            {country.name}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href={`/tours?country=${countrySlug}`}
              className="bg-white text-orange-600 px-8 py-4 rounded-xl font-bold text-lg hover:bg-gray-100 transition-all duration-200 hover:shadow-lg"
            >
              View All Tours
            </Link>
            <Link
              href="/destinations"
              className="border-2 border-white text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-white/10 transition-all duration-200"
            >
              Explore Other Countries
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
