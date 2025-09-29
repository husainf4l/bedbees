"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ChevronDownIcon,
  MagnifyingGlassIcon,
  QuestionMarkCircleIcon,
  ChatBubbleLeftRightIcon,
} from "@heroicons/react/24/outline";

const faqCategories = [
  {
    id: "general",
    name: "General",
    icon: QuestionMarkCircleIcon,
    faqs: [
      {
        question: "What is ShareTrip?",
        answer:
          "ShareTrip is a platform that connects travelers with local experts who share authentic experiences and adventures. Whether you're looking for cultural tours, adventure activities, or unique local experiences, our community of verified hosts offers unforgettable journeys.",
      },
      {
        question: "How does ShareTrip work?",
        answer:
          "Browse experiences from our curated collection, book directly with local hosts, and enjoy authentic adventures. Hosts share their passion and local knowledge to create memorable experiences for travelers.",
      },
      {
        question: "Is ShareTrip available in my country?",
        answer:
          "ShareTrip is currently available in the Middle East and Gulf region, including UAE, Saudi Arabia, Qatar, Kuwait, Bahrain, Oman, Turkey, Syria, Iraq, Yemen, Palestine, Jordan, Lebanon, and Egypt. We're expanding to more destinations soon!",
      },
      {
        question: "Do I need to create an account?",
        answer:
          "Yes, creating an account allows you to book experiences, save favorites, communicate with hosts, and manage your bookings. It's quick and free to sign up!",
      },
    ],
  },
  {
    id: "booking",
    name: "Booking & Payments",
    icon: QuestionMarkCircleIcon,
    faqs: [
      {
        question: "How do I book an experience?",
        answer:
          "Simply browse our experiences, select your preferred date and time, choose the number of participants, and complete the secure payment process. You'll receive instant confirmation and all the details you need.",
      },
      {
        question: "What payment methods do you accept?",
        answer:
          "We accept all major credit and debit cards (Visa, MasterCard, American Express), PayPal, and local payment methods including Apple Pay and Google Pay where available.",
      },
      {
        question: "Can I cancel or reschedule my booking?",
        answer:
          "Yes, you can cancel or reschedule most bookings up to 24 hours before the experience starts. Check the specific cancellation policy for each experience, as some adventure activities may have different terms.",
      },
      {
        question: "Do you offer refunds?",
        answer:
          "Refunds are processed according to each experience's cancellation policy. Full refunds are typically available for cancellations made 24+ hours before the experience. Contact our support team for assistance with refunds.",
      },
      {
        question: "What if the weather affects my experience?",
        answer:
          "Most outdoor experiences have rain-or-shine policies. If weather significantly impacts your experience, hosts will work with you to reschedule or provide alternatives. Desert safaris and beach activities may be weather-dependent.",
      },
    ],
  },
  {
    id: "hosting",
    name: "Hosting",
    icon: QuestionMarkCircleIcon,
    faqs: [
      {
        question: "How do I become a host?",
        answer:
          "Click 'Become a Host' in the navigation menu and complete our simple registration process. We'll verify your information and guide you through creating your first experience.",
      },
      {
        question: "What types of experiences can I host?",
        answer:
          "You can host any authentic experience you're passionate about! This includes cultural tours, adventure activities, cooking classes, art workshops, local explorations, and unique activities that showcase your community's culture and heritage.",
      },
      {
        question: "How much can I earn as a host?",
        answer:
          "Earnings vary based on your experience type, group size, and pricing. Most hosts earn between $50-300 per experience, depending on the activity and duration. You keep 80% of the booking price after platform fees.",
      },
      {
        question: "Do I need special qualifications to host?",
        answer:
          "For most experiences, passion and local knowledge are more important than formal qualifications. However, adventure activities may require specific certifications. We'll help you determine what's needed for your experience type.",
      },
      {
        question: "How do I get paid?",
        answer:
          "Payments are processed securely through our platform. Funds are typically available in your account 24-48 hours after the experience completes. You can withdraw earnings to your bank account or use them for future bookings.",
      },
    ],
  },
  {
    id: "safety",
    name: "Safety & Trust",
    icon: QuestionMarkCircleIcon,
    faqs: [
      {
        question: "How do you ensure safety?",
        answer:
          "All hosts undergo verification, and experiences follow our comprehensive safety guidelines. We require appropriate insurance coverage and provide emergency contact information for all bookings.",
      },
      {
        question: "What if something goes wrong during my experience?",
        answer:
          "Our 24/7 support team is available for any issues. Most problems can be resolved immediately with your host. For serious concerns, we provide backup plans and can arrange alternative experiences.",
      },
      {
        question: "Are hosts verified?",
        answer:
          "Yes, all hosts undergo identity verification, background checks, and experience validation. We also collect reviews and ratings to maintain quality standards.",
      },
      {
        question: "What insurance coverage do you provide?",
        answer:
          "We provide comprehensive insurance coverage for all experiences. This includes accident insurance, liability coverage, and emergency medical assistance. Hosts are also required to maintain appropriate insurance.",
      },
      {
        question: "What should I do in case of emergency?",
        answer:
          "Each booking includes emergency contact information for both the host and our 24/7 support team. Keep this information easily accessible during your experience.",
      },
    ],
  },
  {
    id: "technical",
    name: "Technical Support",
    icon: QuestionMarkCircleIcon,
    faqs: [
      {
        question: "I forgot my password. How can I reset it?",
        answer:
          "Click 'Forgot Password' on the login page and enter your email address. We'll send you a secure link to reset your password.",
      },
      {
        question: "How do I update my profile information?",
        answer:
          "Go to your Dashboard, click on 'Profile' in the sidebar, and update your information. Don't forget to save your changes.",
      },
      {
        question: "Can I book experiences on my mobile device?",
        answer:
          "Yes! Our website is fully responsive and works perfectly on all mobile devices. You can also download our mobile app for iOS and Android.",
      },
      {
        question: "How do I contact my host before the experience?",
        answer:
          "Once booked, you'll see a messaging system in your Dashboard. You can communicate directly with your host to ask questions or make arrangements.",
      },
      {
        question: "How do I leave a review?",
        answer:
          "After your experience completes, you'll receive an email with a link to leave a review. You can also access this from your booking history in the Dashboard.",
      },
    ],
  },
];

export default function FAQPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [expandedFaq, setExpandedFaq] = useState<{
    [key: string]: number | null;
  }>({});

  const filteredFaqs = faqCategories.flatMap((category) =>
    category.faqs
      .map((faq, index) => ({
        ...faq,
        categoryId: category.id,
        faqIndex: index,
      }))
      .filter(
        (faq) =>
          (selectedCategory === "all" || faq.categoryId === selectedCategory) &&
          (faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
            faq.answer.toLowerCase().includes(searchTerm.toLowerCase()))
      )
  );

  const toggleFaq = (categoryId: string, faqIndex: number) => {
    setExpandedFaq((prev) => ({
      ...prev,
      [categoryId]: prev[categoryId] === faqIndex ? null : faqIndex,
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Find quick answers to common questions
            </p>

            {/* Search Bar */}
            <div className="max-w-2xl mx-auto relative mb-8">
              <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search FAQs..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-12 pr-4 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
              />
            </div>

            {/* Category Filter */}
            <div className="flex flex-wrap justify-center gap-2">
              <button
                onClick={() => setSelectedCategory("all")}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                  selectedCategory === "all"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                All Categories
              </button>
              {faqCategories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    selectedCategory === category.id
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {category.name}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* FAQ List */}
        <div className="space-y-4">
          {filteredFaqs.map((faq) => (
            <div
              key={`${faq.categoryId}-${faq.faqIndex}`}
              className="bg-white rounded-lg shadow-sm border border-gray-200"
            >
              <button
                onClick={() => toggleFaq(faq.categoryId, faq.faqIndex)}
                className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span className="font-medium text-gray-900 pr-4">
                  {faq.question}
                </span>
                <ChevronDownIcon
                  className={`w-5 h-5 text-gray-500 transition-transform flex-shrink-0 ${
                    expandedFaq[faq.categoryId] === faq.faqIndex
                      ? "rotate-180"
                      : ""
                  }`}
                />
              </button>
              {expandedFaq[faq.categoryId] === faq.faqIndex && (
                <div className="px-6 pb-4">
                  <p className="text-gray-600 leading-relaxed">{faq.answer}</p>
                </div>
              )}
            </div>
          ))}
        </div>

        {filteredFaqs.length === 0 && (
          <div className="text-center py-12">
            <QuestionMarkCircleIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No FAQs found
            </h3>
            <p className="text-gray-600">
              Try adjusting your search terms or browse all categories.
            </p>
          </div>
        )}

        {/* Contact Support */}
        <div className="mt-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white text-center">
          <ChatBubbleLeftRightIcon className="w-16 h-16 mx-auto mb-6 text-blue-200" />
          <h2 className="text-3xl font-bold mb-4">Still have questions?</h2>
          <p className="text-xl mb-8 opacity-90">
            Our support team is here to help you
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/contact"
              className="bg-white text-blue-600 px-8 py-4 rounded-xl font-bold text-lg hover:bg-white/90 transition-all duration-200"
            >
              Contact Support
            </Link>
            <Link
              href="/help"
              className="border-2 border-white text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-white/10 transition-all duration-200"
            >
              Browse Help Center
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
