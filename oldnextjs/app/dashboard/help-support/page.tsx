"use client";

import { useState } from "react";
import {
  QuestionMarkCircleIcon,
  ChatBubbleLeftRightIcon,
  PhoneIcon,
  EnvelopeIcon,
  DocumentTextIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  MagnifyingGlassIcon,
  BookOpenIcon,
  LifebuoyIcon,
  BugAntIcon,
  CreditCardIcon,
  MapPinIcon,
  UserGroupIcon,
} from "@heroicons/react/24/outline";

interface FAQ {
  id: string;
  question: string;
  answer: string;
  category: string;
}

interface SupportOption {
  id: string;
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  availability: string;
  responseTime: string;
  action: string;
}

const faqs: FAQ[] = [
  {
    id: "1",
    question: "How do I cancel my booking?",
    answer:
      "You can cancel your booking by visiting the 'My Bookings' section in your dashboard. Click on the booking you want to cancel and follow the cancellation process. Please note that cancellation policies vary by provider and timing.",
    category: "Bookings",
  },
  {
    id: "2",
    question: "What payment methods do you accept?",
    answer:
      "We accept all major credit cards (Visa, Mastercard, American Express), PayPal, and bank transfers. Payment is processed securely through our encrypted payment system.",
    category: "Payments",
  },
  {
    id: "3",
    question: "How do I contact the tour provider?",
    answer:
      "After booking, you'll receive the provider's contact information in your confirmation email. You can also find their details in your booking confirmation within the dashboard.",
    category: "Tours",
  },
  {
    id: "4",
    question: "Can I modify my booking dates?",
    answer:
      "Date modifications depend on the provider's policy and availability. Contact the provider directly or reach out to our support team for assistance with date changes.",
    category: "Bookings",
  },
  {
    id: "5",
    question: "What if my tour is cancelled due to weather?",
    answer:
      "If a tour is cancelled due to weather conditions, you'll receive a full refund or the option to reschedule. The provider will contact you directly about cancellations.",
    category: "Tours",
  },
  {
    id: "6",
    question: "How do I leave a review?",
    answer:
      "After completing your tour or stay, you'll receive an email invitation to leave a review. You can also access the review section through your booking history in the dashboard.",
    category: "Reviews",
  },
];

const supportOptions: SupportOption[] = [
  {
    id: "live-chat",
    title: "Live Chat",
    description: "Get instant help from our support team",
    icon: ChatBubbleLeftRightIcon,
    availability: "24/7",
    responseTime: "< 5 minutes",
    action: "Start Chat",
  },
  {
    id: "phone",
    title: "Phone Support",
    description: "Speak directly with a support representative",
    icon: PhoneIcon,
    availability: "9 AM - 9 PM",
    responseTime: "Immediate",
    action: "Call Now",
  },
  {
    id: "email",
    title: "Email Support",
    description: "Send us a detailed message about your issue",
    icon: EnvelopeIcon,
    availability: "24/7",
    responseTime: "< 24 hours",
    action: "Send Email",
  },
  {
    id: "help-center",
    title: "Help Center",
    description: "Browse our comprehensive knowledge base",
    icon: BookOpenIcon,
    availability: "Always available",
    responseTime: "Self-service",
    action: "Browse Articles",
  },
];

const categories = [
  { id: "all", name: "All Categories", icon: QuestionMarkCircleIcon },
  { id: "Bookings", name: "Bookings", icon: DocumentTextIcon },
  { id: "Payments", name: "Payments", icon: CreditCardIcon },
  { id: "Tours", name: "Tours", icon: MapPinIcon },
  { id: "Reviews", name: "Reviews", icon: UserGroupIcon },
];

export default function HelpSupport() {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedFAQ, setExpandedFAQ] = useState<string | null>(null);

  const filteredFAQs = faqs.filter((faq) => {
    const matchesCategory =
      selectedCategory === "all" || faq.category === selectedCategory;
    const matchesSearch =
      faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
      faq.answer.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="max-w-6xl mx-auto">
      {/* Apple-style Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-light text-gray-900 tracking-tight">
          Help & Support
        </h1>
        <p className="text-lg text-gray-500 mt-3 font-light">
          Get assistance and find answers to your questions
        </p>
      </div>

      {/* Support Options */}
      <div className="mb-12">
        <h2 className="text-2xl font-medium text-gray-900 mb-6">
          Contact Support
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {supportOptions.map((option) => {
            const IconComponent = option.icon;
            return (
              <div
                key={option.id}
                className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer"
              >
                <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center mb-4">
                  <IconComponent className="w-6 h-6 text-blue-600" />
                </div>

                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {option.title}
                </h3>
                <p className="text-gray-600 text-sm mb-4">
                  {option.description}
                </p>

                <div className="space-y-2 mb-4">
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <ClockIcon className="w-3 h-3" />
                    <span>Available: {option.availability}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <CheckCircleIcon className="w-3 h-3" />
                    <span>Response: {option.responseTime}</span>
                  </div>
                </div>

                <button className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-2xl font-medium transition-colors text-sm">
                  {option.action}
                </button>
              </div>
            );
          })}
        </div>
      </div>

      {/* Emergency Contact */}
      <div className="mb-12">
        <div className="bg-gradient-to-r from-red-50 to-orange-50 border border-red-200 rounded-3xl p-6">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 bg-red-100 rounded-2xl flex items-center justify-center flex-shrink-0">
              <ExclamationTriangleIcon className="w-6 h-6 text-red-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-medium text-red-900 mb-2">
                Emergency Support
              </h3>
              <p className="text-red-700 mb-4">
                If you&apos;re experiencing an emergency during your trip or
                need immediate assistance, contact our 24/7 emergency hotline.
              </p>
              <div className="flex items-center gap-4">
                <button className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-2xl font-medium transition-colors flex items-center gap-2">
                  <PhoneIcon className="w-4 h-4" />
                  Emergency Line: +962 6 123 4567
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* FAQ Section */}
      <div>
        <h2 className="text-2xl font-medium text-gray-900 mb-6">
          Frequently Asked Questions
        </h2>

        {/* Search and Filter */}
        <div className="mb-8 space-y-4">
          {/* Search Bar */}
          <div className="relative max-w-2xl">
            <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search frequently asked questions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-4 bg-white border border-gray-200 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 placeholder-gray-500"
            />
          </div>

          {/* Category Filters */}
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => {
              const IconComponent = category.icon;
              return (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-2xl font-medium transition-all duration-200 ${
                    selectedCategory === category.id
                      ? "bg-blue-500 text-white shadow-lg"
                      : "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50"
                  }`}
                >
                  <IconComponent className="w-4 h-4" />
                  {category.name}
                </button>
              );
            })}
          </div>
        </div>

        {/* FAQ List */}
        <div className="space-y-4">
          {filteredFAQs.map((faq) => (
            <div
              key={faq.id}
              className="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden"
            >
              <button
                onClick={() =>
                  setExpandedFAQ(expandedFAQ === faq.id ? null : faq.id)
                }
                className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <div className="flex-1">
                  <h3 className="text-lg font-medium text-gray-900 mb-1">
                    {faq.question}
                  </h3>
                  <span className="text-sm text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
                    {faq.category}
                  </span>
                </div>
                {expandedFAQ === faq.id ? (
                  <ChevronDownIcon className="w-5 h-5 text-gray-400" />
                ) : (
                  <ChevronRightIcon className="w-5 h-5 text-gray-400" />
                )}
              </button>

              {expandedFAQ === faq.id && (
                <div className="px-6 pb-6">
                  <div className="border-t border-gray-100 pt-4">
                    <p className="text-gray-600 leading-relaxed">
                      {faq.answer}
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* No Results */}
        {filteredFAQs.length === 0 && (
          <div className="text-center py-16">
            <QuestionMarkCircleIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">
              No FAQs found
            </h3>
            <p className="text-gray-500">
              Try adjusting your search or browse different categories.
            </p>
          </div>
        )}
      </div>

      {/* Additional Resources */}
      <div className="mt-12">
        <h2 className="text-2xl font-medium text-gray-900 mb-6">
          Additional Resources
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
            <LifebuoyIcon className="w-8 h-8 text-blue-600 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Travel Insurance
            </h3>
            <p className="text-gray-600 text-sm mb-4">
              Learn about travel insurance options and how to file claims.
            </p>
            <button className="text-blue-600 font-medium text-sm hover:text-blue-700">
              Learn More →
            </button>
          </div>

          <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
            <BugAntIcon className="w-8 h-8 text-green-600 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Report an Issue
            </h3>
            <p className="text-gray-600 text-sm mb-4">
              Found a bug or having technical difficulties? Let us know.
            </p>
            <button className="text-green-600 font-medium text-sm hover:text-green-700">
              Report Issue →
            </button>
          </div>

          <div className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6">
            <DocumentTextIcon className="w-8 h-8 text-purple-600 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              User Guide
            </h3>
            <p className="text-gray-600 text-sm mb-4">
              Complete guide to using our platform and booking services.
            </p>
            <button className="text-purple-600 font-medium text-sm hover:text-purple-700">
              View Guide →
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
