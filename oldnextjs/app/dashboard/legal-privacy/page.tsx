"use client";

import { useState } from "react";
import {
  ShieldCheckIcon,
  DocumentTextIcon,
  EyeIcon,
  LockClosedIcon,
  GlobeAltIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  CogIcon,
  ClockIcon,
  EnvelopeIcon,
  ChatBubbleLeftIcon,
} from "@heroicons/react/24/outline";

interface PrivacySetting {
  id: string;
  title: string;
  description: string;
  enabled: boolean;
  category: string;
}

interface LegalDocument {
  id: string;
  title: string;
  description: string;
  lastUpdated: string;
  version: string;
  icon: React.ComponentType<{ className?: string }>;
}

const privacySettings: PrivacySetting[] = [
  {
    id: "email-marketing",
    title: "Email Marketing",
    description:
      "Receive promotional emails about new tours and special offers",
    enabled: true,
    category: "Communications",
  },
  {
    id: "sms-notifications",
    title: "SMS Notifications",
    description: "Get text messages about booking confirmations and updates",
    enabled: false,
    category: "Communications",
  },
  {
    id: "push-notifications",
    title: "Push Notifications",
    description: "Receive notifications on your device about important updates",
    enabled: true,
    category: "Communications",
  },
  {
    id: "profile-visibility",
    title: "Profile Visibility",
    description: "Allow other users to see your profile and reviews",
    enabled: false,
    category: "Privacy",
  },
  {
    id: "data-analytics",
    title: "Data Analytics",
    description: "Help us improve our service by sharing usage analytics",
    enabled: true,
    category: "Privacy",
  },
  {
    id: "location-sharing",
    title: "Location Sharing",
    description: "Share your location for personalized recommendations",
    enabled: false,
    category: "Privacy",
  },
];

const legalDocuments: LegalDocument[] = [
  {
    id: "privacy-policy",
    title: "Privacy Policy",
    description: "How we collect, use, and protect your personal information",
    lastUpdated: "December 1, 2024",
    version: "v2.1",
    icon: ShieldCheckIcon,
  },
  {
    id: "terms-of-service",
    title: "Terms of Service",
    description: "The rules and regulations for using our platform",
    lastUpdated: "November 15, 2024",
    version: "v3.0",
    icon: DocumentTextIcon,
  },
  {
    id: "cookie-policy",
    title: "Cookie Policy",
    description: "Information about cookies and tracking technologies we use",
    lastUpdated: "October 20, 2024",
    version: "v1.5",
    icon: GlobeAltIcon,
  },
  {
    id: "refund-policy",
    title: "Refund Policy",
    description:
      "Guidelines for cancellations, refunds, and dispute resolution",
    lastUpdated: "November 30, 2024",
    version: "v2.0",
    icon: ExclamationTriangleIcon,
  },
];

export default function LegalPrivacy() {
  const [settings, setSettings] = useState<PrivacySetting[]>(privacySettings);
  const [selectedCategory, setSelectedCategory] = useState("all");

  const toggleSetting = (settingId: string) => {
    setSettings((prev) =>
      prev.map((setting) =>
        setting.id === settingId
          ? { ...setting, enabled: !setting.enabled }
          : setting
      )
    );
  };

  const filteredSettings = settings.filter(
    (setting) =>
      selectedCategory === "all" || setting.category === selectedCategory
  );

  const categories = [
    { id: "all", name: "All Settings" },
    { id: "Communications", name: "Communications" },
    { id: "Privacy", name: "Privacy" },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Apple-style Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-light text-gray-900 tracking-tight">
          Legal & Privacy
        </h1>
        <p className="text-lg text-gray-500 mt-3 font-light">
          Manage your privacy settings and access legal documents
        </p>
      </div>

      {/* Privacy Settings */}
      <div className="mb-12">
        <h2 className="text-2xl font-medium text-gray-900 mb-6">
          Privacy Settings
        </h2>

        {/* Category Filter */}
        <div className="mb-6">
          <div className="flex space-x-1 bg-gray-100 rounded-2xl p-1 w-fit">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-6 py-2 rounded-xl font-medium transition-all duration-200 ${
                  selectedCategory === category.id
                    ? "bg-white text-blue-600 shadow-sm"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>

        {/* Settings List */}
        <div className="space-y-4">
          {filteredSettings.map((setting) => (
            <div
              key={setting.id}
              className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <div
                      className={`w-8 h-8 rounded-2xl flex items-center justify-center ${
                        setting.category === "Communications"
                          ? "bg-blue-100"
                          : "bg-purple-100"
                      }`}
                    >
                      {setting.category === "Communications" ? (
                        <ChatBubbleLeftIcon
                          className={`w-4 h-4 ${
                            setting.category === "Communications"
                              ? "text-blue-600"
                              : "text-purple-600"
                          }`}
                        />
                      ) : (
                        <LockClosedIcon className="w-4 h-4 text-purple-600" />
                      )}
                    </div>
                    <h3 className="text-lg font-medium text-gray-900">
                      {setting.title}
                    </h3>
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        setting.category === "Communications"
                          ? "bg-blue-100 text-blue-700"
                          : "bg-purple-100 text-purple-700"
                      }`}
                    >
                      {setting.category}
                    </span>
                  </div>
                  <p className="text-gray-600 text-sm">{setting.description}</p>
                </div>

                <div className="ml-6">
                  <button
                    onClick={() => toggleSetting(setting.id)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                      setting.enabled ? "bg-blue-600" : "bg-gray-200"
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200 ${
                        setting.enabled ? "translate-x-6" : "translate-x-1"
                      }`}
                    />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Data Management */}
      <div className="mb-12">
        <h2 className="text-2xl font-medium text-gray-900 mb-6">
          Data Management
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
            <div className="w-12 h-12 bg-green-100 rounded-2xl flex items-center justify-center mb-4">
              <CheckCircleIcon className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Download Your Data
            </h3>
            <p className="text-gray-600 text-sm mb-4">
              Request a copy of all your personal data stored in our system
            </p>
            <button className="w-full bg-green-500 hover:bg-green-600 text-white py-2 rounded-2xl font-medium transition-colors text-sm">
              Request Download
            </button>
          </div>

          <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
            <div className="w-12 h-12 bg-yellow-100 rounded-2xl flex items-center justify-center mb-4">
              <ExclamationTriangleIcon className="w-6 h-6 text-yellow-600" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Delete Account
            </h3>
            <p className="text-gray-600 text-sm mb-4">
              Permanently delete your account and all associated data
            </p>
            <button className="w-full bg-yellow-500 hover:bg-yellow-600 text-white py-2 rounded-2xl font-medium transition-colors text-sm">
              Delete Account
            </button>
          </div>

          <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
            <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center mb-4">
              <CogIcon className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Privacy Controls
            </h3>
            <p className="text-gray-600 text-sm mb-4">
              Manage advanced privacy settings and data sharing preferences
            </p>
            <button className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-2xl font-medium transition-colors text-sm">
              Advanced Settings
            </button>
          </div>
        </div>
      </div>

      {/* Legal Documents */}
      <div className="mb-12">
        <h2 className="text-2xl font-medium text-gray-900 mb-6">
          Legal Documents
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {legalDocuments.map((document) => {
            const IconComponent = document.icon;
            return (
              <div
                key={document.id}
                className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer"
              >
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-gray-100 rounded-2xl flex items-center justify-center flex-shrink-0">
                    <IconComponent className="w-6 h-6 text-gray-600" />
                  </div>

                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-lg font-medium text-gray-900">
                        {document.title}
                      </h3>
                      <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                        {document.version}
                      </span>
                    </div>

                    <p className="text-gray-600 text-sm mb-3">
                      {document.description}
                    </p>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <ClockIcon className="w-3 h-3" />
                        <span>Updated: {document.lastUpdated}</span>
                      </div>

                      <button className="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium text-sm">
                        <EyeIcon className="w-4 h-4" />
                        View Document
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Security Information */}
      <div className="mb-12">
        <h2 className="text-2xl font-medium text-gray-900 mb-6">
          Security & Compliance
        </h2>
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-3xl p-6">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <ShieldCheckIcon className="w-6 h-6 text-blue-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-medium text-blue-900 mb-2">
                Data Protection & Security
              </h3>
              <p className="text-blue-700 mb-4">
                We are committed to protecting your privacy and ensuring the
                security of your personal information. Our platform complies
                with international data protection standards including GDPR and
                other relevant privacy regulations.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center gap-2">
                  <CheckCircleIcon className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-blue-800">
                    SSL Encrypted Data Transfer
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircleIcon className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-blue-800">GDPR Compliant</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircleIcon className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-blue-800">
                    Regular Security Audits
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircleIcon className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-blue-800">
                    Data Backup & Recovery
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Contact Information */}
      <div>
        <h2 className="text-2xl font-medium text-gray-900 mb-6">
          Privacy Questions?
        </h2>
        <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
          <div className="text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <EnvelopeIcon className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Need Help with Privacy Settings?
            </h3>
            <p className="text-gray-600 mb-6">
              If you have questions about your privacy settings or need
              assistance with data management, our privacy team is here to help.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-3 rounded-2xl font-medium transition-colors flex items-center gap-2">
                <EnvelopeIcon className="w-4 h-4" />
                Contact Privacy Team
              </button>
              <button className="border border-gray-200 text-gray-700 px-6 py-3 rounded-2xl font-medium hover:bg-gray-50 transition-colors">
                Privacy FAQ
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
