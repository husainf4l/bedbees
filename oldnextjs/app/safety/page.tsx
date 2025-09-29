"use client";

import React from "react";
import {
  ShieldCheckIcon,
  ExclamationTriangleIcon,
  HeartIcon,
  UserGroupIcon,
} from "@heroicons/react/24/outline";
import { CheckCircleIcon } from "@heroicons/react/24/solid";

const safetyGuidelines = [
  {
    icon: ShieldCheckIcon,
    title: "Host Verification",
    description:
      "All hosts undergo thorough background checks and identity verification before they can list experiences on our platform.",
    details: [
      "Government ID verification",
      "Address confirmation",
      "Background check screening",
      "Experience validation",
      "Regular quality assessments",
    ],
  },
  {
    icon: UserGroupIcon,
    title: "Community Standards",
    description:
      "We maintain high standards for all experiences and participants to ensure everyone has a positive and safe experience.",
    details: [
      "Respectful communication required",
      "Zero tolerance for harassment",
      "Cultural sensitivity training",
      "Regular community feedback",
      "Quality assurance reviews",
    ],
  },
  {
    icon: HeartIcon,
    title: "Health & Safety",
    description:
      "Your health and safety are our top priorities. All experiences follow comprehensive safety protocols.",
    details: [
      "Emergency contact information provided",
      "First aid kits available for outdoor activities",
      "Weather-appropriate planning",
      "Health condition considerations",
      "COVID-19 safety measures",
    ],
  },
  {
    icon: ExclamationTriangleIcon,
    title: "Emergency Preparedness",
    description:
      "We're prepared for emergencies and have protocols in place to handle any situation that may arise.",
    details: [
      "24/7 emergency support line",
      "Local emergency service coordination",
      "Medical evacuation arrangements",
      "Travel insurance partnerships",
      "Crisis management team",
    ],
  },
];

const travelerTips = [
  {
    title: "Before Your Experience",
    tips: [
      "Review the experience description and requirements carefully",
      "Check weather conditions and dress appropriately",
      "Inform someone about your plans and expected return time",
      "Save emergency contact numbers in your phone",
      "Review cancellation and refund policies",
    ],
  },
  {
    title: "During Your Experience",
    tips: [
      "Stay with your group and follow your host's instructions",
      "Communicate openly if you have any concerns or special needs",
      "Take photos responsibly and respect privacy",
      "Stay hydrated and take breaks as needed",
      "Keep valuables secure and minimal",
    ],
  },
  {
    title: "General Safety Tips",
    tips: [
      "Trust your instincts - if something feels off, speak up",
      "Respect local customs and cultural norms",
      "Keep your booking confirmation and itinerary handy",
      "Use reputable transportation to and from experiences",
      "Share your location with trusted contacts when appropriate",
    ],
  },
];

const emergencyContacts = [
  {
    region: "UAE",
    police: "999",
    ambulance: "998",
    fire: "997",
    touristPolice: "+971 800 243",
    ourSupport: "+971 4 123 4567",
  },
  {
    region: "Saudi Arabia",
    police: "999",
    ambulance: "997",
    fire: "998",
    touristPolice: "1909",
    ourSupport: "+966 11 123 4567",
  },
  {
    region: "Qatar",
    police: "999",
    ambulance: "199",
    fire: "199",
    touristPolice: "+974 4020 1333",
    ourSupport: "+974 4412 3456",
  },
];

export default function SafetyPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Safety Guidelines
            </h1>
            <p className="text-xl text-gray-600">
              Your safety and security are our highest priorities
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Safety Overview */}
        <div className="mb-16">
          <div className="bg-gradient-to-r from-green-600 to-blue-600 rounded-2xl p-8 text-white text-center">
            <ShieldCheckIcon className="w-20 h-20 mx-auto mb-6 text-green-200" />
            <h2 className="text-3xl font-bold mb-4">Safe Adventures Await</h2>
            <p className="text-xl opacity-90 mb-6">
              Every experience on ShareTrip follows rigorous safety standards
              and protocols
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <div className="flex items-center space-x-2">
                <CheckCircleIcon className="w-5 h-5" />
                <span>Verified Hosts</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircleIcon className="w-5 h-5" />
                <span>24/7 Support</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircleIcon className="w-5 h-5" />
                <span>Insurance Coverage</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircleIcon className="w-5 h-5" />
                <span>Emergency Ready</span>
              </div>
            </div>
          </div>
        </div>

        {/* Safety Guidelines Grid */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            Our Safety Commitments
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {safetyGuidelines.map((guideline, index) => (
              <div
                key={index}
                className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                      <guideline.icon className="w-6 h-6 text-blue-600" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">
                      {guideline.title}
                    </h3>
                    <p className="text-gray-600 mb-4">
                      {guideline.description}
                    </p>
                    <ul className="space-y-2">
                      {guideline.details.map((detail, idx) => (
                        <li key={idx} className="flex items-start space-x-2">
                          <CheckCircleIcon className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                          <span className="text-sm text-gray-600">
                            {detail}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Traveler Tips */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            Traveler Safety Tips
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {travelerTips.map((section, index) => (
              <div
                key={index}
                className="bg-white rounded-xl p-6 shadow-sm border border-gray-200"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  {section.title}
                </h3>
                <ul className="space-y-3">
                  {section.tips.map((tip, idx) => (
                    <li key={idx} className="flex items-start space-x-2">
                      <div className="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0 mt-2"></div>
                      <span className="text-sm text-gray-600">{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Emergency Contacts */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            Emergency Contacts
          </h2>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                      Region
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                      Police
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                      Ambulance
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                      Fire
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                      Tourist Police
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                      Our Support
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {emergencyContacts.map((contact, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="px-6 py-4 text-sm font-medium text-gray-900">
                        {contact.region}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {contact.police}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {contact.ambulance}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {contact.fire}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {contact.touristPolice}
                      </td>
                      <td className="px-6 py-4 text-sm text-blue-600 font-medium">
                        {contact.ourSupport}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Report Safety Concern */}
        <div className="bg-gradient-to-r from-red-600 to-orange-600 rounded-2xl p-8 text-white text-center">
          <ExclamationTriangleIcon className="w-16 h-16 mx-auto mb-6 text-red-200" />
          <h2 className="text-3xl font-bold mb-4">Report a Safety Concern</h2>
          <p className="text-xl mb-8 opacity-90">
            If you encounter any safety issues or have concerns about an
            experience, please let us know immediately.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/contact?category=safety"
              className="bg-white text-red-600 px-8 py-4 rounded-xl font-bold text-lg hover:bg-gray-100 transition-all duration-200"
            >
              Report Issue
            </a>
            <a
              href="tel:+97141234567"
              className="border-2 border-white text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-white/10 transition-all duration-200"
            >
              Emergency: +971 4 123 4567
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
