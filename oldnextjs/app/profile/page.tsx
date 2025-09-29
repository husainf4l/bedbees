"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { useAuth } from "@/providers/AuthContext";
import {
  UserIcon,
  CameraIcon,
  PencilIcon,
  MapPinIcon,
  CalendarIcon,
  GlobeAltIcon,
  HeartIcon,
  ShieldCheckIcon,
  BellIcon,
  KeyIcon,
  CreditCardIcon,
  StarIcon,
} from "@heroicons/react/24/outline";
import {
  UserIcon as UserSolidIcon,
  HeartIcon as HeartSolidIcon,
  StarIcon as StarSolidIcon,
} from "@heroicons/react/24/solid";

interface UserProfile {
  id: string;
  name: string;
  email: string;
  phone?: string;
  image?: string;
  bio?: string;
  location?: string;
  joinDate: string;
  travelStyle?: string[];
  languages?: string[];
  emergencyContact?: {
    name: string;
    phone: string;
    relationship: string;
  };
  preferences: {
    currency: string;
    language: string;
    notifications: {
      email: boolean;
      sms: boolean;
      push: boolean;
    };
  };
  stats: {
    tripsCompleted: number;
    reviewsWritten: number;
    wishlistItems: number;
    totalSpent: number;
  };
}

const travelStyles = [
  "Adventure",
  "Cultural",
  "Relaxation",
  "Food & Wine",
  "Nature",
  "City Break",
  "Beach",
  "Mountain",
  "Luxury",
];

const languages = [
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
];

const currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"];

export default function ProfilePage() {
  const router = useRouter();
  const { user, logout, loading } = useAuth();
  const [activeTab, setActiveTab] = useState("personal");
  const [isEditing, setIsEditing] = useState(false);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [formData, setFormData] = useState<Partial<UserProfile>>({});

  // Mock profile data for demo
  const mockProfile: UserProfile = {
    id: "user-123",
    name: user?.name || "John Doe",
    email: user?.email || "john.doe@example.com",
    phone: "+1 (555) 123-4567",
    image: user?.image || undefined,
    bio: "Passionate traveler who loves exploring new cultures and creating unforgettable memories. Always seeking the next adventure!",
    location: "San Francisco, CA",
    joinDate: "2023-03-15",
    travelStyle: ["Adventure", "Cultural", "Nature"],
    languages: ["English", "Spanish"],
    emergencyContact: {
      name: "Jane Doe",
      phone: "+1 (555) 987-6543",
      relationship: "Sister",
    },
    preferences: {
      currency: "USD",
      language: "English",
      notifications: {
        email: true,
        sms: false,
        push: true,
      },
    },
    stats: {
      tripsCompleted: 24,
      reviewsWritten: 18,
      wishlistItems: 12,
      totalSpent: 15420,
    },
  };

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
      return;
    }

    // Load profile data
    setProfile(mockProfile);
    setFormData(mockProfile);
  }, [user, loading, router]);

  const handleSave = () => {
    // In a real app, this would save to the backend
    setProfile({ ...mockProfile, ...formData } as UserProfile);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setFormData(profile || {});
    setIsEditing(false);
  };

  const updateFormData = (field: string, value: unknown) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const updateNestedFormData = (
    parent: keyof UserProfile,
    field: string,
    value: any
  ) => {
    setFormData((prev) => ({
      ...prev,
      [parent]: {
        ...(prev[parent] as any),
        [field]: value,
      },
    }));
  };

  const getUserInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  if (!user || !profile) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Access Denied
          </h1>
          <p className="text-gray-600 mb-6">
            Please log in to view your profile.
          </p>
          <button
            onClick={() => router.push("/login")}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Log In
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>
            <div className="flex items-center space-x-4">
              {isEditing ? (
                <>
                  <button
                    onClick={handleSave}
                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                  >
                    Save Changes
                  </button>
                  <button
                    onClick={handleCancel}
                    className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                  >
                    Cancel
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setIsEditing(true)}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
                >
                  <PencilIcon className="w-4 h-4 mr-2" />
                  Edit Profile
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Profile Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="text-center">
                <div className="relative inline-block">
                  {profile.image ? (
                    <Image
                      src={profile.image}
                      alt={profile.name}
                      width={120}
                      height={120}
                      className="rounded-full mx-auto mb-4"
                    />
                  ) : (
                    <div className="w-30 h-30 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-white text-2xl font-bold">
                        {getUserInitials(profile.name)}
                      </span>
                    </div>
                  )}
                  {isEditing && (
                    <button className="absolute bottom-2 right-2 bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 transition-colors">
                      <CameraIcon className="w-4 h-4" />
                    </button>
                  )}
                </div>
                <h2 className="text-xl font-bold text-gray-900">
                  {profile.name}
                </h2>
                <p className="text-gray-600">{profile.email}</p>
                <p className="text-sm text-gray-500 mt-1">
                  Member since{" "}
                  {new Date(profile.joinDate).toLocaleDateString("en-US", {
                    month: "long",
                    year: "numeric",
                  })}
                </p>

                {/* Quick Stats */}
                <div className="mt-6 grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {profile.stats.tripsCompleted}
                    </div>
                    <div className="text-xs text-gray-600">Trips</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {profile.stats.reviewsWritten}
                    </div>
                    <div className="text-xs text-gray-600">Reviews</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {/* Tabs */}
            <div className="bg-white rounded-lg shadow-sm mb-6">
              <div className="border-b border-gray-200">
                <nav className="flex">
                  {[
                    { id: "personal", label: "Personal Info", icon: UserIcon },
                    {
                      id: "preferences",
                      label: "Preferences",
                      icon: HeartIcon,
                    },
                    {
                      id: "security",
                      label: "Security",
                      icon: ShieldCheckIcon,
                    },
                    {
                      id: "notifications",
                      label: "Notifications",
                      icon: BellIcon,
                    },
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex items-center px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                        activeTab === tab.id
                          ? "border-blue-500 text-blue-600"
                          : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                      }`}
                    >
                      <tab.icon className="w-4 h-4 mr-2" />
                      {tab.label}
                    </button>
                  ))}
                </nav>
              </div>

              <div className="p-6">
                {/* Personal Info Tab */}
                {activeTab === "personal" && (
                  <div className="space-y-6">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-4">
                        Personal Information
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Full Name
                          </label>
                          {isEditing ? (
                            <input
                              type="text"
                              value={formData.name || ""}
                              onChange={(e) =>
                                updateFormData("name", e.target.value)
                              }
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                          ) : (
                            <p className="text-gray-900">{profile.name}</p>
                          )}
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Email
                          </label>
                          {isEditing ? (
                            <input
                              type="email"
                              value={formData.email || ""}
                              onChange={(e) =>
                                updateFormData("email", e.target.value)
                              }
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                          ) : (
                            <p className="text-gray-900">{profile.email}</p>
                          )}
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Phone
                          </label>
                          {isEditing ? (
                            <input
                              type="tel"
                              value={formData.phone || ""}
                              onChange={(e) =>
                                updateFormData("phone", e.target.value)
                              }
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                          ) : (
                            <p className="text-gray-900">
                              {profile.phone || "Not provided"}
                            </p>
                          )}
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Location
                          </label>
                          {isEditing ? (
                            <input
                              type="text"
                              value={formData.location || ""}
                              onChange={(e) =>
                                updateFormData("location", e.target.value)
                              }
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                          ) : (
                            <p className="text-gray-900">
                              {profile.location || "Not provided"}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Bio
                      </label>
                      {isEditing ? (
                        <textarea
                          value={formData.bio || ""}
                          onChange={(e) =>
                            updateFormData("bio", e.target.value)
                          }
                          rows={4}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Tell us about yourself..."
                        />
                      ) : (
                        <p className="text-gray-900">
                          {profile.bio || "No bio provided"}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Travel Styles
                      </label>
                      {isEditing ? (
                        <div className="flex flex-wrap gap-2">
                          {travelStyles.map((style) => (
                            <button
                              key={style}
                              onClick={() => {
                                const currentStyles =
                                  formData.travelStyle || [];
                                const newStyles = currentStyles.includes(style)
                                  ? currentStyles.filter((s) => s !== style)
                                  : [...currentStyles, style];
                                updateFormData("travelStyle", newStyles);
                              }}
                              className={`px-3 py-1 rounded-full text-sm ${
                                (formData.travelStyle || []).includes(style)
                                  ? "bg-blue-100 text-blue-800"
                                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                              }`}
                            >
                              {style}
                            </button>
                          ))}
                        </div>
                      ) : (
                        <div className="flex flex-wrap gap-2">
                          {(profile.travelStyle || []).map((style) => (
                            <span
                              key={style}
                              className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                            >
                              {style}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Languages
                      </label>
                      {isEditing ? (
                        <div className="flex flex-wrap gap-2">
                          {languages.map((lang) => (
                            <button
                              key={lang}
                              onClick={() => {
                                const currentLangs = formData.languages || [];
                                const newLangs = currentLangs.includes(lang)
                                  ? currentLangs.filter((l) => l !== lang)
                                  : [...currentLangs, lang];
                                updateFormData("languages", newLangs);
                              }}
                              className={`px-3 py-1 rounded-full text-sm ${
                                (formData.languages || []).includes(lang)
                                  ? "bg-green-100 text-green-800"
                                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                              }`}
                            >
                              {lang}
                            </button>
                          ))}
                        </div>
                      ) : (
                        <div className="flex flex-wrap gap-2">
                          {(profile.languages || []).map((lang) => (
                            <span
                              key={lang}
                              className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
                            >
                              {lang}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Preferences Tab */}
                {activeTab === "preferences" && (
                  <div className="space-y-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                      Travel Preferences
                    </h3>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Preferred Currency
                        </label>
                        {isEditing ? (
                          <select
                            value={formData.preferences?.currency || "USD"}
                            onChange={(e) =>
                              updateNestedFormData(
                                "preferences",
                                "currency",
                                e.target.value
                              )
                            }
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          >
                            {currencies.map((currency) => (
                              <option key={currency} value={currency}>
                                {currency}
                              </option>
                            ))}
                          </select>
                        ) : (
                          <p className="text-gray-900">
                            {profile.preferences.currency}
                          </p>
                        )}
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Preferred Language
                        </label>
                        {isEditing ? (
                          <select
                            value={formData.preferences?.language || "English"}
                            onChange={(e) =>
                              updateNestedFormData(
                                "preferences",
                                "language",
                                e.target.value
                              )
                            }
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          >
                            {languages.map((lang) => (
                              <option key={lang} value={lang}>
                                {lang}
                              </option>
                            ))}
                          </select>
                        ) : (
                          <p className="text-gray-900">
                            {profile.preferences.language}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Security Tab */}
                {activeTab === "security" && (
                  <div className="space-y-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                      Account Security
                    </h3>

                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                        <div>
                          <h4 className="text-sm font-medium text-gray-900">
                            Password
                          </h4>
                          <p className="text-sm text-gray-600">
                            Last changed 3 months ago
                          </p>
                        </div>
                        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                          Change Password
                        </button>
                      </div>

                      <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                        <div>
                          <h4 className="text-sm font-medium text-gray-900">
                            Two-Factor Authentication
                          </h4>
                          <p className="text-sm text-gray-600">
                            Add an extra layer of security
                          </p>
                        </div>
                        <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                          Enable 2FA
                        </button>
                      </div>
                    </div>
                  </div>
                )}

                {/* Notifications Tab */}
                {activeTab === "notifications" && (
                  <div className="space-y-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">
                      Notification Preferences
                    </h3>

                    <div className="space-y-4">
                      {[
                        {
                          key: "email",
                          label: "Email Notifications",
                          description: "Receive updates via email",
                        },
                        {
                          key: "sms",
                          label: "SMS Notifications",
                          description: "Receive updates via text message",
                        },
                        {
                          key: "push",
                          label: "Push Notifications",
                          description: "Receive push notifications in browser",
                        },
                      ].map((notification) => (
                        <div
                          key={notification.key}
                          className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                        >
                          <div>
                            <h4 className="text-sm font-medium text-gray-900">
                              {notification.label}
                            </h4>
                            <p className="text-sm text-gray-600">
                              {notification.description}
                            </p>
                          </div>
                          {isEditing ? (
                            <div className="flex space-x-2">
                              <button
                                onClick={() =>
                                  updateNestedFormData(
                                    "preferences",
                                    `notifications.${notification.key}`,
                                    true
                                  )
                                }
                                className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
                                  formData.preferences?.notifications?.[
                                    notification.key as keyof typeof formData.preferences.notifications
                                  ]
                                    ? "bg-green-600 text-white"
                                    : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                                }`}
                              >
                                Enable
                              </button>
                              <button
                                onClick={() =>
                                  updateNestedFormData(
                                    "preferences",
                                    `notifications.${notification.key}`,
                                    false
                                  )
                                }
                                className={`px-3 py-1 text-xs font-medium rounded-md transition-colors ${
                                  !formData.preferences?.notifications?.[
                                    notification.key as keyof typeof formData.preferences.notifications
                                  ]
                                    ? "bg-red-600 text-white"
                                    : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                                }`}
                              >
                                Disable
                              </button>
                            </div>
                          ) : (
                            <span
                              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                profile.preferences.notifications[
                                  notification.key as keyof typeof profile.preferences.notifications
                                ]
                                  ? "bg-green-100 text-green-800"
                                  : "bg-gray-100 text-gray-800"
                              }`}
                            >
                              {profile.preferences.notifications[
                                notification.key as keyof typeof profile.preferences.notifications
                              ]
                                ? "Enabled"
                                : "Disabled"}
                            </span>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
