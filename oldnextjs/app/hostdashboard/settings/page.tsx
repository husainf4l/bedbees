"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/providers/AuthContext";

export default function SettingsPage() {
  const router = useRouter();
  const { logout } = useAuth();
  const [activeTab, setActiveTab] = useState("general");

  const [generalSettings, setGeneralSettings] = useState({
    language: "en",
    timezone: "Asia/Amman",
    currency: "JOD",
    dateFormat: "DD/MM/YYYY",
    emailNotifications: true,
    pushNotifications: true,
    smsNotifications: false,
  });

  const [bookingSettings, setBookingSettings] = useState({
    instantBook: true,
    requireGuestProfile: true,
    allowPets: false,
    smokingAllowed: false,
    checkInTime: "15:00",
    checkOutTime: "11:00",
    minAdvanceBooking: 1,
    maxAdvanceBooking: 365,
    cancellationPolicy: "flexible",
  });

  const [pricingSettings, setPricingSettings] = useState({
    baseCurrency: "JOD",
    smartPricing: true,
    weekendSurcharge: 20,
    cleaningFee: 15,
    securityDeposit: 100,
    taxRate: 16,
  });

  const [notificationSettings, setNotificationSettings] = useState({
    newBooking: { email: true, push: true, sms: false },
    cancellation: { email: true, push: true, sms: true },
    review: { email: true, push: false, sms: false },
    message: { email: false, push: true, sms: false },
    payout: { email: true, push: true, sms: false },
    maintenance: { email: true, push: false, sms: false },
  });

  const handleSaveSettings = (section: string) => {
    // Here you would typically send the settings to your backend
    console.log(`Saving ${section} settings`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Breadcrumb */}
        <nav className="flex mb-6" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-4">
            <li>
              <button
                onClick={() => router.push("/hostdashboard")}
                className="text-gray-400 hover:text-gray-500 transition-colors"
              >
                Host Dashboard
              </button>
            </li>
            <li>
              <svg
                className="flex-shrink-0 h-5 w-5 text-gray-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            </li>
            <li>
              <span className="text-gray-500">Settings</span>
            </li>
          </ol>
        </nav>

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
            <p className="text-gray-600">
              Manage your account preferences and configurations
            </p>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Settings Navigation */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              <nav className="flex flex-col">
                <button
                  onClick={() => setActiveTab("general")}
                  className={`px-6 py-3 text-left border-b border-gray-200 flex items-center ${
                    activeTab === "general"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  <svg
                    className="w-5 h-5 mr-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                  General
                </button>

                <button
                  onClick={() => setActiveTab("booking")}
                  className={`px-6 py-3 text-left border-b border-gray-200 flex items-center ${
                    activeTab === "booking"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  <svg
                    className="w-5 h-5 mr-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 7V3a4 4 0 118 0v4m-4 8a4 4 0 11-8 0v1h16v-1a4 4 0 11-8 0z"
                    />
                  </svg>
                  Booking
                </button>

                <button
                  onClick={() => setActiveTab("pricing")}
                  className={`px-6 py-3 text-left border-b border-gray-200 flex items-center ${
                    activeTab === "pricing"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  <svg
                    className="w-5 h-5 mr-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"
                    />
                  </svg>
                  Pricing
                </button>

                <button
                  onClick={() => setActiveTab("notifications")}
                  className={`px-6 py-3 text-left border-b border-gray-200 flex items-center ${
                    activeTab === "notifications"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  <svg
                    className="w-5 h-5 mr-3"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M15 17h5l-5 5v-5zM4 19h10v-1a6 6 0 00-6-6H6a6 6 0 00-6 6v1zM12 9a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                  Notifications
                </button>

                <button
                  onClick={() => setActiveTab("account")}
                  className={`px-6 py-3 text-left flex items-center ${
                    activeTab === "account"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  <svg
                    className="w-5 h-5 mr-3"
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
                  Account
                </button>
              </nav>
            </div>
          </div>

          {/* Settings Content */}
          <div className="lg:w-3/4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              {activeTab === "general" && (
                <div className="p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-lg font-semibold text-gray-900">
                      General Settings
                    </h3>
                    <button
                      onClick={() => handleSaveSettings("general")}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      Save Changes
                    </button>
                  </div>

                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Language
                        </label>
                        <select
                          value={generalSettings.language}
                          onChange={(e) =>
                            setGeneralSettings({
                              ...generalSettings,
                              language: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        >
                          <option value="en">English</option>
                          <option value="ar">Arabic</option>
                          <option value="fr">French</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Timezone
                        </label>
                        <select
                          value={generalSettings.timezone}
                          onChange={(e) =>
                            setGeneralSettings({
                              ...generalSettings,
                              timezone: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        >
                          <option value="Asia/Amman">Asia/Amman (GMT+3)</option>
                          <option value="UTC">UTC (GMT+0)</option>
                          <option value="America/New_York">
                            America/New_York (GMT-5)
                          </option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Currency
                        </label>
                        <select
                          value={generalSettings.currency}
                          onChange={(e) =>
                            setGeneralSettings({
                              ...generalSettings,
                              currency: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        >
                          <option value="JOD">Jordanian Dinar (JOD)</option>
                          <option value="USD">US Dollar (USD)</option>
                          <option value="EUR">Euro (EUR)</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Date Format
                        </label>
                        <select
                          value={generalSettings.dateFormat}
                          onChange={(e) =>
                            setGeneralSettings({
                              ...generalSettings,
                              dateFormat: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        >
                          <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                          <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                          <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                        </select>
                      </div>
                    </div>

                    <div className="border-t pt-6">
                      <h4 className="text-md font-medium text-gray-900 mb-4">
                        Quick Notifications
                      </h4>
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <span className="text-gray-700">
                            Email Notifications
                          </span>
                          <button
                            onClick={() =>
                              setGeneralSettings({
                                ...generalSettings,
                                emailNotifications:
                                  !generalSettings.emailNotifications,
                              })
                            }
                            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                              generalSettings.emailNotifications
                                ? "bg-green-600"
                                : "bg-gray-200"
                            }`}
                          >
                            <span
                              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                generalSettings.emailNotifications
                                  ? "translate-x-6"
                                  : "translate-x-1"
                              }`}
                            />
                          </button>
                        </div>

                        <div className="flex items-center justify-between">
                          <span className="text-gray-700">
                            Push Notifications
                          </span>
                          <button
                            onClick={() =>
                              setGeneralSettings({
                                ...generalSettings,
                                pushNotifications:
                                  !generalSettings.pushNotifications,
                              })
                            }
                            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                              generalSettings.pushNotifications
                                ? "bg-green-600"
                                : "bg-gray-200"
                            }`}
                          >
                            <span
                              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                generalSettings.pushNotifications
                                  ? "translate-x-6"
                                  : "translate-x-1"
                              }`}
                            />
                          </button>
                        </div>

                        <div className="flex items-center justify-between">
                          <span className="text-gray-700">
                            SMS Notifications
                          </span>
                          <button
                            onClick={() =>
                              setGeneralSettings({
                                ...generalSettings,
                                smsNotifications:
                                  !generalSettings.smsNotifications,
                              })
                            }
                            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                              generalSettings.smsNotifications
                                ? "bg-green-600"
                                : "bg-gray-200"
                            }`}
                          >
                            <span
                              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                generalSettings.smsNotifications
                                  ? "translate-x-6"
                                  : "translate-x-1"
                              }`}
                            />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "booking" && (
                <div className="p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Booking Settings
                    </h3>
                    <button
                      onClick={() => handleSaveSettings("booking")}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      Save Changes
                    </button>
                  </div>

                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Check-in Time
                        </label>
                        <input
                          type="time"
                          value={bookingSettings.checkInTime}
                          onChange={(e) =>
                            setBookingSettings({
                              ...bookingSettings,
                              checkInTime: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Check-out Time
                        </label>
                        <input
                          type="time"
                          value={bookingSettings.checkOutTime}
                          onChange={(e) =>
                            setBookingSettings({
                              ...bookingSettings,
                              checkOutTime: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Min Advance Booking (days)
                        </label>
                        <input
                          type="number"
                          value={bookingSettings.minAdvanceBooking}
                          onChange={(e) =>
                            setBookingSettings({
                              ...bookingSettings,
                              minAdvanceBooking: parseInt(e.target.value),
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Max Advance Booking (days)
                        </label>
                        <input
                          type="number"
                          value={bookingSettings.maxAdvanceBooking}
                          onChange={(e) =>
                            setBookingSettings({
                              ...bookingSettings,
                              maxAdvanceBooking: parseInt(e.target.value),
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Cancellation Policy
                      </label>
                      <select
                        value={bookingSettings.cancellationPolicy}
                        onChange={(e) =>
                          setBookingSettings({
                            ...bookingSettings,
                            cancellationPolicy: e.target.value,
                          })
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      >
                        <option value="flexible">Flexible</option>
                        <option value="moderate">Moderate</option>
                        <option value="strict">Strict</option>
                      </select>
                    </div>

                    <div className="border-t pt-6">
                      <h4 className="text-md font-medium text-gray-900 mb-4">
                        Booking Options
                      </h4>
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <div>
                            <span className="text-gray-700 font-medium">
                              Instant Book
                            </span>
                            <p className="text-sm text-gray-500">
                              Guests can book without waiting for approval
                            </p>
                          </div>
                          <button
                            onClick={() =>
                              setBookingSettings({
                                ...bookingSettings,
                                instantBook: !bookingSettings.instantBook,
                              })
                            }
                            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                              bookingSettings.instantBook
                                ? "bg-green-600"
                                : "bg-gray-200"
                            }`}
                          >
                            <span
                              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                bookingSettings.instantBook
                                  ? "translate-x-6"
                                  : "translate-x-1"
                              }`}
                            />
                          </button>
                        </div>

                        <div className="flex items-center justify-between">
                          <div>
                            <span className="text-gray-700 font-medium">
                              Require Guest Profile
                            </span>
                            <p className="text-sm text-gray-500">
                              Guests must have a complete profile to book
                            </p>
                          </div>
                          <button
                            onClick={() =>
                              setBookingSettings({
                                ...bookingSettings,
                                requireGuestProfile:
                                  !bookingSettings.requireGuestProfile,
                              })
                            }
                            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                              bookingSettings.requireGuestProfile
                                ? "bg-green-600"
                                : "bg-gray-200"
                            }`}
                          >
                            <span
                              className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                bookingSettings.requireGuestProfile
                                  ? "translate-x-6"
                                  : "translate-x-1"
                              }`}
                            />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "pricing" && (
                <div className="p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Pricing Settings
                    </h3>
                    <button
                      onClick={() => handleSaveSettings("pricing")}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      Save Changes
                    </button>
                  </div>

                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Weekend Surcharge (%)
                        </label>
                        <input
                          type="number"
                          value={pricingSettings.weekendSurcharge}
                          onChange={(e) =>
                            setPricingSettings({
                              ...pricingSettings,
                              weekendSurcharge: parseInt(e.target.value),
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Cleaning Fee (JOD)
                        </label>
                        <input
                          type="number"
                          value={pricingSettings.cleaningFee}
                          onChange={(e) =>
                            setPricingSettings({
                              ...pricingSettings,
                              cleaningFee: parseInt(e.target.value),
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Security Deposit (JOD)
                        </label>
                        <input
                          type="number"
                          value={pricingSettings.securityDeposit}
                          onChange={(e) =>
                            setPricingSettings({
                              ...pricingSettings,
                              securityDeposit: parseInt(e.target.value),
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Tax Rate (%)
                        </label>
                        <input
                          type="number"
                          step="0.1"
                          value={pricingSettings.taxRate}
                          onChange={(e) =>
                            setPricingSettings({
                              ...pricingSettings,
                              taxRate: parseFloat(e.target.value),
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      </div>
                    </div>

                    <div className="border-t pt-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <span className="text-gray-700 font-medium">
                            Smart Pricing
                          </span>
                          <p className="text-sm text-gray-500">
                            Automatically adjust prices based on demand
                          </p>
                        </div>
                        <button
                          onClick={() =>
                            setPricingSettings({
                              ...pricingSettings,
                              smartPricing: !pricingSettings.smartPricing,
                            })
                          }
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            pricingSettings.smartPricing
                              ? "bg-green-600"
                              : "bg-gray-200"
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              pricingSettings.smartPricing
                                ? "translate-x-6"
                                : "translate-x-1"
                            }`}
                          />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "notifications" && (
                <div className="p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Notification Settings
                    </h3>
                    <button
                      onClick={() => handleSaveSettings("notifications")}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      Save Changes
                    </button>
                  </div>

                  <div className="space-y-6">
                    <div className="overflow-x-auto">
                      <table className="min-w-full">
                        <thead>
                          <tr className="border-b border-gray-200">
                            <th className="text-left py-3 font-medium text-gray-900">
                              Event
                            </th>
                            <th className="text-center py-3 font-medium text-gray-900">
                              Email
                            </th>
                            <th className="text-center py-3 font-medium text-gray-900">
                              Push
                            </th>
                            <th className="text-center py-3 font-medium text-gray-900">
                              SMS
                            </th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-200">
                          {Object.entries(notificationSettings).map(
                            ([key, settings]) => (
                              <tr key={key}>
                                <td className="py-4">
                                  <div className="capitalize font-medium text-gray-900">
                                    {key.replace(/([A-Z])/g, " $1")}
                                  </div>
                                </td>
                                <td className="py-4 text-center">
                                  <button
                                    onClick={() =>
                                      setNotificationSettings({
                                        ...notificationSettings,
                                        [key]: {
                                          ...settings,
                                          email: !settings.email,
                                        },
                                      })
                                    }
                                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                                      settings.email
                                        ? "bg-green-600"
                                        : "bg-gray-200"
                                    }`}
                                  >
                                    <span
                                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                        settings.email
                                          ? "translate-x-6"
                                          : "translate-x-1"
                                      }`}
                                    />
                                  </button>
                                </td>
                                <td className="py-4 text-center">
                                  <button
                                    onClick={() =>
                                      setNotificationSettings({
                                        ...notificationSettings,
                                        [key]: {
                                          ...settings,
                                          push: !settings.push,
                                        },
                                      })
                                    }
                                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                                      settings.push
                                        ? "bg-green-600"
                                        : "bg-gray-200"
                                    }`}
                                  >
                                    <span
                                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                        settings.push
                                          ? "translate-x-6"
                                          : "translate-x-1"
                                      }`}
                                    />
                                  </button>
                                </td>
                                <td className="py-4 text-center">
                                  <button
                                    onClick={() =>
                                      setNotificationSettings({
                                        ...notificationSettings,
                                        [key]: {
                                          ...settings,
                                          sms: !settings.sms,
                                        },
                                      })
                                    }
                                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                                      settings.sms
                                        ? "bg-green-600"
                                        : "bg-gray-200"
                                    }`}
                                  >
                                    <span
                                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                        settings.sms
                                          ? "translate-x-6"
                                          : "translate-x-1"
                                      }`}
                                    />
                                  </button>
                                </td>
                              </tr>
                            )
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "account" && (
                <div className="p-6">
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      Account Settings
                    </h3>
                    <p className="text-gray-600">
                      Manage your account and security settings
                    </p>
                  </div>

                  <div className="space-y-6">
                    {/* Logout Section */}
                    <div className="border border-red-200 rounded-lg p-6 bg-red-50">
                      <div className="flex items-start">
                        <div className="flex-shrink-0">
                          <svg
                            className="w-6 h-6 text-red-600"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                            />
                          </svg>
                        </div>
                        <div className="ml-4 flex-1">
                          <h4 className="text-lg font-medium text-red-900 mb-2">
                            Sign Out
                          </h4>
                          <p className="text-red-700 mb-4">
                            You will be signed out of your account and
                            redirected to the login page.
                          </p>
                          <button
                            onClick={() => {
                              if (
                                confirm("Are you sure you want to sign out?")
                              ) {
                                logout();
                                router.push("/login");
                              }
                            }}
                            className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium flex items-center gap-2"
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
                                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                              />
                            </svg>
                            Sign Out
                          </button>
                        </div>
                      </div>
                    </div>

                    {/* Account Info Section */}
                    <div className="border border-gray-200 rounded-lg p-6">
                      <h4 className="text-lg font-medium text-gray-900 mb-4">
                        Account Information
                      </h4>
                      <div className="space-y-4">
                        <div className="flex justify-between items-center py-3 border-b border-gray-200">
                          <span className="text-gray-600">Account Type</span>
                          <span className="font-medium text-gray-900">
                            Host Account
                          </span>
                        </div>
                        <div className="flex justify-between items-center py-3 border-b border-gray-200">
                          <span className="text-gray-600">Member Since</span>
                          <span className="font-medium text-gray-900">
                            January 2024
                          </span>
                        </div>
                        <div className="flex justify-between items-center py-3">
                          <span className="text-gray-600">Account Status</span>
                          <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                            Active
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
