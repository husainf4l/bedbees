"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState("basic");
  const [isEditing, setIsEditing] = useState(false);

  const [profile, setProfile] = useState({
    firstName: "Ahmed",
    lastName: "Al-Rashid",
    email: "ahmed.alrashid@example.com",
    phone: "+962 79 123 4567",
    dateOfBirth: "1985-06-15",
    gender: "male",
    nationality: "Jordanian",
    languages: ["Arabic", "English", "French"],
    bio: "Passionate host with 5+ years of experience in hospitality. I love sharing the beauty and culture of Jordan with travelers from around the world.",
    profileImage: "/api/placeholder/150/150",
    // Business Information
    businessName: "Jordan Heritage Hotels",
    businessType: "hotel",
    businessRegistrationNumber: "JOR-HTL-2019-001",
    taxId: "TAX-123456789",
    businessPhone: "+962 6 465 4321",
    businessEmail: "info@jordanheritagehotels.com",
    website: "www.jordanheritagehotels.com",
    establishedYear: "2019",
    numberOfProperties: 5,
    totalRooms: 120,
    businessLicense: "Active",
    touristicLicense: "Active",
  });

  const [address, setAddress] = useState({
    street: "123 Rainbow Street",
    city: "Amman",
    state: "Amman Governorate",
    country: "Jordan",
    postalCode: "11118",
  });

  const [verification, setVerification] = useState({
    email: true,
    phone: true,
    identity: true,
    address: false,
  });

  const [legalDocuments, setLegalDocuments] = useState({
    businessLicense: {
      fileName: "business_license_2024.pdf",
      uploadDate: "2024-01-15",
      status: "approved",
      expiryDate: "2025-01-15",
    },
    companyRegistration: {
      fileName: "company_registration_2019.pdf",
      uploadDate: "2024-01-05",
      status: "approved",
      expiryDate: "N/A",
    },
  });

  const handleSave = () => {
    // Here you would typically send the data to your backend
    console.log("Saving profile:", profile);
    setIsEditing(false);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "approved":
        return "bg-green-100 text-green-800";
      case "pending":
        return "bg-yellow-100 text-yellow-800";
      case "rejected":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getDocumentTitle = (type: string) => {
    const titles: { [key: string]: string } = {
      businessLicense: "Business License",
      companyRegistration: "Company Registration",
    };
    return titles[type] || type;
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
              <span className="text-gray-500">Profile</span>
            </li>
          </ol>
        </nav>

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Profile</h1>
            <p className="text-gray-600">
              Manage your account information and business documents
            </p>
          </div>

          <div className="mt-4 sm:mt-0">
            {isEditing ? (
              <div className="space-x-2">
                <button
                  onClick={() => setIsEditing(false)}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSave}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  Save Changes
                </button>
              </div>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Edit Profile
              </button>
            )}
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Profile Sidebar */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
              <div className="relative inline-block">
                <img
                  src={profile.profileImage}
                  alt="Profile"
                  className="w-32 h-32 rounded-full mx-auto mb-4"
                />
                {isEditing && (
                  <button className="absolute bottom-4 right-0 bg-green-600 text-white p-2 rounded-full hover:bg-green-700 transition-colors">
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
                        d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                      />
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                    </svg>
                  </button>
                )}
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {profile.firstName} {profile.lastName}
              </h3>
              <p className="text-gray-600 mb-2">{profile.businessName}</p>
              <p className="text-gray-500 text-sm mb-4">Host since 2019</p>

              {/* Verification Status */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Email</span>
                  {verification.email ? (
                    <span className="text-green-600 flex items-center">
                      <svg
                        className="w-4 h-4 mr-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      Verified
                    </span>
                  ) : (
                    <span className="text-red-600">Not verified</span>
                  )}
                </div>

                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Phone</span>
                  {verification.phone ? (
                    <span className="text-green-600 flex items-center">
                      <svg
                        className="w-4 h-4 mr-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      Verified
                    </span>
                  ) : (
                    <span className="text-red-600">Not verified</span>
                  )}
                </div>

                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Identity</span>
                  {verification.identity ? (
                    <span className="text-green-600 flex items-center">
                      <svg
                        className="w-4 h-4 mr-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      Verified
                    </span>
                  ) : (
                    <span className="text-red-600">Not verified</span>
                  )}
                </div>
              </div>
            </div>

            {/* Navigation Tabs */}
            <div className="mt-6 bg-white rounded-lg shadow-sm border border-gray-200">
              <nav className="flex flex-col">
                <button
                  onClick={() => setActiveTab("basic")}
                  className={`px-6 py-3 text-left border-b border-gray-200 ${
                    activeTab === "basic"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  Basic Information
                </button>
                <button
                  onClick={() => setActiveTab("business")}
                  className={`px-6 py-3 text-left border-b border-gray-200 ${
                    activeTab === "business"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  Business Information
                </button>
                <button
                  onClick={() => setActiveTab("address")}
                  className={`px-6 py-3 text-left border-b border-gray-200 ${
                    activeTab === "address"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  Address
                </button>
                <button
                  onClick={() => setActiveTab("documents")}
                  className={`px-6 py-3 text-left border-b border-gray-200 ${
                    activeTab === "documents"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  Business Documents
                </button>
                <button
                  onClick={() => setActiveTab("security")}
                  className={`px-6 py-3 text-left ${
                    activeTab === "security"
                      ? "bg-green-50 text-green-700 border-l-4 border-l-green-500"
                      : "text-gray-700 hover:bg-gray-50"
                  }`}
                >
                  Security
                </button>
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:w-3/4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200">
              {activeTab === "basic" && (
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">
                    Basic Information
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        First Name
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={profile.firstName}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              firstName: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.firstName}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Last Name
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={profile.lastName}
                          onChange={(e) =>
                            setProfile({ ...profile, lastName: e.target.value })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">{profile.lastName}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Email
                      </label>
                      <div className="flex items-center">
                        <p className="py-2 text-gray-900 mr-2">
                          {profile.email}
                        </p>
                        <svg
                          className="w-5 h-5 text-green-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                          />
                        </svg>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Phone
                      </label>
                      {isEditing ? (
                        <input
                          type="tel"
                          value={profile.phone}
                          onChange={(e) =>
                            setProfile({ ...profile, phone: e.target.value })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <div className="flex items-center">
                          <p className="py-2 text-gray-900 mr-2">
                            {profile.phone}
                          </p>
                          <svg
                            className="w-5 h-5 text-green-500"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                          </svg>
                        </div>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Date of Birth
                      </label>
                      {isEditing ? (
                        <input
                          type="date"
                          value={profile.dateOfBirth}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              dateOfBirth: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.dateOfBirth}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Nationality
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={profile.nationality}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              nationality: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.nationality}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="mt-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Bio
                    </label>
                    {isEditing ? (
                      <textarea
                        value={profile.bio}
                        onChange={(e) =>
                          setProfile({ ...profile, bio: e.target.value })
                        }
                        rows={4}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    ) : (
                      <p className="py-2 text-gray-900">{profile.bio}</p>
                    )}
                  </div>

                  <div className="mt-6">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Languages
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {profile.languages.map((language, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full"
                        >
                          {language}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "business" && (
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">
                    Business Information
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Business Name
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={profile.businessName}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              businessName: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.businessName}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Business Type
                      </label>
                      {isEditing ? (
                        <select
                          value={profile.businessType}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              businessType: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        >
                          <option value="hotel">Hotel</option>
                          <option value="resort">Resort</option>
                          <option value="guesthouse">Guesthouse</option>
                          <option value="apartment">Apartment</option>
                          <option value="tour_company">Tour Company</option>
                          <option value="individual">Individual Host</option>
                        </select>
                      ) : (
                        <p className="py-2 text-gray-900 capitalize">
                          {profile.businessType.replace("_", " ")}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Registration Number
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={profile.businessRegistrationNumber}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              businessRegistrationNumber: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.businessRegistrationNumber}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Tax ID
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={profile.taxId}
                          onChange={(e) =>
                            setProfile({ ...profile, taxId: e.target.value })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">{profile.taxId}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Business Phone
                      </label>
                      {isEditing ? (
                        <input
                          type="tel"
                          value={profile.businessPhone}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              businessPhone: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.businessPhone}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Business Email
                      </label>
                      {isEditing ? (
                        <input
                          type="email"
                          value={profile.businessEmail}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              businessEmail: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.businessEmail}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Website
                      </label>
                      {isEditing ? (
                        <input
                          type="url"
                          value={profile.website}
                          onChange={(e) =>
                            setProfile({ ...profile, website: e.target.value })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">{profile.website}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Established Year
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={profile.establishedYear}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              establishedYear: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.establishedYear}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Number of Properties
                      </label>
                      {isEditing ? (
                        <input
                          type="number"
                          value={profile.numberOfProperties}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              numberOfProperties: parseInt(e.target.value),
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.numberOfProperties}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Total Rooms/Units
                      </label>
                      {isEditing ? (
                        <input
                          type="number"
                          value={profile.totalRooms}
                          onChange={(e) =>
                            setProfile({
                              ...profile,
                              totalRooms: parseInt(e.target.value),
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {profile.totalRooms}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <h4 className="text-md font-medium text-gray-900 mb-4">
                      License Status
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Business License
                        </label>
                        <div className="flex items-center">
                          <span
                            className={`px-2 py-1 text-sm rounded-full ${
                              profile.businessLicense === "Active"
                                ? "bg-green-100 text-green-800"
                                : "bg-red-100 text-red-800"
                            }`}
                          >
                            {profile.businessLicense}
                          </span>
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Tourism License
                        </label>
                        <div className="flex items-center">
                          <span
                            className={`px-2 py-1 text-sm rounded-full ${
                              profile.touristicLicense === "Active"
                                ? "bg-green-100 text-green-800"
                                : "bg-red-100 text-red-800"
                            }`}
                          >
                            {profile.touristicLicense}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "address" && (
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">
                    Address Information
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Street Address
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={address.street}
                          onChange={(e) =>
                            setAddress({ ...address, street: e.target.value })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">{address.street}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        City
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={address.city}
                          onChange={(e) =>
                            setAddress({ ...address, city: e.target.value })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">{address.city}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        State/Province
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={address.state}
                          onChange={(e) =>
                            setAddress({ ...address, state: e.target.value })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">{address.state}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Country
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={address.country}
                          onChange={(e) =>
                            setAddress({ ...address, country: e.target.value })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">{address.country}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Postal Code
                      </label>
                      {isEditing ? (
                        <input
                          type="text"
                          value={address.postalCode}
                          onChange={(e) =>
                            setAddress({
                              ...address,
                              postalCode: e.target.value,
                            })
                          }
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        />
                      ) : (
                        <p className="py-2 text-gray-900">
                          {address.postalCode}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "documents" && (
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">
                    Business Documents
                  </h3>
                  <p className="text-gray-600 mb-6">
                    Upload and manage your legal business documents for
                    verification
                  </p>

                  <div className="space-y-6">
                    {Object.entries(legalDocuments).map(
                      ([docType, document]) => {
                        return (
                          <div
                            key={docType}
                            className="border border-gray-200 rounded-lg p-4"
                          >
                            <div className="flex items-center justify-between mb-3">
                              <h4 className="text-md font-medium text-gray-900">
                                {getDocumentTitle(docType)}
                              </h4>
                              <span
                                className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(
                                  document.status
                                )}`}
                              >
                                {document.status.charAt(0).toUpperCase() +
                                  document.status.slice(1)}
                              </span>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                              <div>
                                <span className="text-gray-500">File:</span>
                                <p className="font-medium">
                                  {document.fileName}
                                </p>
                              </div>
                              <div>
                                <span className="text-gray-500">Uploaded:</span>
                                <p className="font-medium">
                                  {document.uploadDate}
                                </p>
                              </div>
                              <div>
                                <span className="text-gray-500">Expires:</span>
                                <p className="font-medium">
                                  {document.expiryDate}
                                </p>
                              </div>
                            </div>

                            <div className="mt-4 flex items-center space-x-3">
                              <button className="flex items-center px-3 py-1 text-sm text-blue-600 hover:text-blue-800 transition-colors">
                                <svg
                                  className="w-4 h-4 mr-1"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                                  />
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                                  />
                                </svg>
                                View
                              </button>

                              <button className="flex items-center px-3 py-1 text-sm text-green-600 hover:text-green-800 transition-colors">
                                <svg
                                  className="w-4 h-4 mr-1"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                                  />
                                </svg>
                                Replace
                              </button>

                              <button className="flex items-center px-3 py-1 text-sm text-red-600 hover:text-red-800 transition-colors">
                                <svg
                                  className="w-4 h-4 mr-1"
                                  fill="none"
                                  stroke="currentColor"
                                  viewBox="0 0 24 24"
                                >
                                  <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                                  />
                                </svg>
                                Delete
                              </button>
                            </div>
                          </div>
                        );
                      }
                    )}

                    {/* Upload New Document */}
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                      <svg
                        className="mx-auto h-12 w-12 text-gray-400"
                        stroke="currentColor"
                        fill="none"
                        viewBox="0 0 48 48"
                      >
                        <path
                          d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                          strokeWidth={2}
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                      <div className="mt-4">
                        <p className="text-sm text-gray-600">
                          Upload a new document
                        </p>
                        <p className="text-xs text-gray-500 mt-2">
                          PDF, JPG, PNG up to 10MB
                        </p>
                      </div>
                      <div className="mt-6">
                        <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
                          Choose File
                        </button>
                      </div>
                    </div>

                    {/* Document Requirements */}
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <h4 className="font-medium text-blue-900 mb-2">
                        Required Documents for Hotel/Company Registration:
                      </h4>
                      <ul className="text-sm text-blue-800 space-y-1">
                        <li>
                          • Business License (Ministry of Industry & Trade)
                        </li>
                        <li>• Company Registration Documents</li>
                      </ul>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === "security" && (
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">
                    Security Settings
                  </h3>

                  <div className="space-y-6">
                    <div className="border-b border-gray-200 pb-6">
                      <h4 className="text-md font-medium text-gray-900 mb-3">
                        Password
                      </h4>
                      <p className="text-gray-600 mb-4">
                        Keep your account secure by using a strong password
                      </p>
                      <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                        Change Password
                      </button>
                    </div>

                    <div className="border-b border-gray-200 pb-6">
                      <h4 className="text-md font-medium text-gray-900 mb-3">
                        Two-Factor Authentication
                      </h4>
                      <p className="text-gray-600 mb-4">
                        Add an extra layer of security to your account
                      </p>
                      <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                        Enable 2FA
                      </button>
                    </div>

                    <div>
                      <h4 className="text-md font-medium text-gray-900 mb-3">
                        Login Activity
                      </h4>
                      <p className="text-gray-600 mb-4">
                        Review recent login activity on your account
                      </p>
                      <div className="bg-gray-50 rounded-lg p-4">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm text-gray-600">
                            Last login: Today at 2:30 PM
                          </span>
                          <span className="text-xs text-green-600">
                            Current session
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">
                            Location: Amman, Jordan
                          </span>
                          <span className="text-xs text-gray-500">
                            Chrome on Windows
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
