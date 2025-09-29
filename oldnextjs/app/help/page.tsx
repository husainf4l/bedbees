"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ChevronDownIcon,
  MagnifyingGlassIcon,
  QuestionMarkCircleIcon,
  ChatBubbleLeftRightIcon,
  ShieldCheckIcon,
  ClockIcon,
  UserGroupIcon,
  CreditCardIcon,
  TruckIcon,
  ExclamationTriangleIcon,
} from "@heroicons/react/24/outline";
import { StarIcon } from "@heroicons/react/24/solid";

const faqs = [
  {
    question: "How do I book an experience?",
    answer:
      "Browse our experiences, select your preferred date and time, and complete the booking process. You'll receive a confirmation email with all the details.",
    category: "booking",
  },
  {
    question: "Can I cancel or reschedule my booking?",
    answer:
      "Yes, you can cancel or reschedule up to 24 hours before your experience starts. Check the specific cancellation policy for each experience.",
    category: "booking",
  },
  {
    question: "What payment methods do you accept?",
    answer:
      "We accept all major credit cards, PayPal, and local payment methods in your region.",
    category: "payment",
  },
  {
    question: "How do I become a host?",
    answer:
      "Click on 'Become a Host' in the navigation menu and follow the registration process. We'll guide you through creating your first experience.",
    category: "hosting",
  },
  {
    question: "What should I do if I have a problem with my booking?",
    answer:
      "Contact our support team through the chat widget or email us at support@raheva.com. We'll help resolve any issues.",
    category: "support",
  },
  {
    question: "Are the experiences insured?",
    answer:
      "All our experiences are covered by comprehensive insurance. Hosts are also required to have appropriate insurance coverage.",
    category: "safety",
  },
];

const categories = [
  {
    title: "Getting Started",
    icon: QuestionMarkCircleIcon,
    description: "New to ShareTrip? Start here",
    articles: [
      "How ShareTrip works",
      "Creating your account",
      "Finding your first experience",
    ],
  },
  {
    title: "Booking & Payments",
    icon: CreditCardIcon,
    description: "Everything about booking and paying",
    articles: [
      "How to book an experience",
      "Payment methods",
      "Refunds and cancellations",
      "Booking modifications",
    ],
  },
  {
    title: "Hosting",
    icon: UserGroupIcon,
    description: "Share your experiences with travelers",
    articles: [
      "Becoming a host",
      "Creating your first experience",
      "Managing bookings",
      "Getting paid",
    ],
  },
  {
    title: "Safety & Trust",
    icon: ShieldCheckIcon,
    description: "Your safety is our priority",
    articles: [
      "Safety guidelines",
      "Trust & verification",
      "Insurance coverage",
      "Emergency contacts",
    ],
  },
  {
    title: "Travel Tips",
    icon: TruckIcon,
    description: "Make the most of your travels",
    articles: [
      "Packing essentials",
      "Local customs",
      "Transportation tips",
      "Cultural etiquette",
    ],
  },
  {
    title: "Account & Settings",
    icon: ExclamationTriangleIcon,
    description: "Manage your account",
    articles: [
      "Profile settings",
      "Privacy controls",
      "Notification preferences",
      "Account security",
    ],
  },
];

export default function HelpCenterPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null);

  const filteredFaqs = faqs.filter(
    (faq) =>
      faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      faq.answer.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Help Center
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Find answers to your questions and get the help you need
            </p>

            {/* Search Bar */}
            <div className="max-w-2xl mx-auto relative">
              <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search for help..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-12 pr-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Quick Help Categories */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            Browse by Category
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {categories.map((category, index) => (
              <div
                key={index}
                className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer group"
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-200 transition-colors">
                      <category.icon className="w-6 h-6 text-blue-600" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {category.title}
                    </h3>
                    <p className="text-gray-600 mb-4">{category.description}</p>
                    <ul className="space-y-1">
                      {category.articles.slice(0, 3).map((article, idx) => (
                        <li
                          key={idx}
                          className="text-sm text-gray-500 flex items-center"
                        >
                          <span className="w-1.5 h-1.5 bg-gray-300 rounded-full mr-2"></span>
                          {article}
                        </li>
                      ))}
                      {category.articles.length > 3 && (
                        <li className="text-sm text-blue-600 font-medium">
                          +{category.articles.length - 3} more articles
                        </li>
                      )}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Popular FAQs */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            Frequently Asked Questions
          </h2>
          <div className="max-w-3xl mx-auto space-y-4">
            {filteredFaqs.map((faq, index) => (
              <div
                key={index}
                className="bg-white rounded-lg shadow-sm border border-gray-200"
              >
                <button
                  onClick={() =>
                    setExpandedFaq(expandedFaq === index ? null : index)
                  }
                  className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
                >
                  <span className="font-medium text-gray-900">
                    {faq.question}
                  </span>
                  <ChevronDownIcon
                    className={`w-5 h-5 text-gray-500 transition-transform ${
                      expandedFaq === index ? "rotate-180" : ""
                    }`}
                  />
                </button>
                {expandedFaq === index && (
                  <div className="px-6 pb-4">
                    <p className="text-gray-600 leading-relaxed">
                      {faq.answer}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Contact Support */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white text-center">
          <ChatBubbleLeftRightIcon className="w-16 h-16 mx-auto mb-6 text-blue-200" />
          <h2 className="text-3xl font-bold mb-4">Still need help?</h2>
          <p className="text-xl mb-8 opacity-90">
            Our support team is here to help you 24/7
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/contact"
              className="bg-white text-blue-600 px-8 py-4 rounded-xl font-bold text-lg hover:bg-gray-100 transition-all duration-200 hover:shadow-lg"
            >
              Contact Support
            </Link>
            <button className="border-2 border-white text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-white/10 transition-all duration-200">
              Live Chat
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
