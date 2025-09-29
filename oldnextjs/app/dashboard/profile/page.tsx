"use client";

import { useState } from "react";
import Image from "next/image";
import { useAuth } from "@/providers/AuthContext";
import {
  UserIcon,
  EnvelopeIcon,
  PhoneIcon,
  MapPinIcon,
  CalendarIcon,
  CameraIcon,
  PencilIcon,
} from "@heroicons/react/24/outline";

interface ProfileData {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  dateOfBirth: string;
  address: string;
  city: string;
  country: string;
  bio: string;
  profileImage: string;
}

export default function Profile() {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [profileData, setProfileData] = useState<ProfileData>({
    firstName: user?.name?.split(" ")[0] || "",
    lastName: user?.name?.split(" ")[1] || "",
    email: user?.email || "",
    phone: "",
    dateOfBirth: "",
    address: "",
    city: "",
    country: "",
    bio: "",
    profileImage: user?.image || "",
  });

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setProfileData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSave = () => {
    // Here you would typically save to your backend
    console.log("Saving profile data:", profileData);
    setIsEditing(false);
    // Show success message
  };

  const handleCancel = () => {
    // Reset to original data
    setProfileData({
      firstName: user?.name?.split(" ")[0] || "",
      lastName: user?.name?.split(" ")[1] || "",
      email: user?.email || "",
      phone: "",
      dateOfBirth: "",
      address: "",
      city: "",
      country: "",
      bio: "",
      profileImage: user?.image || "",
    });
    setIsEditing(false);
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Apple-style Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-light text-gray-900 tracking-tight">
          Profile
        </h1>
        <p className="text-lg text-gray-500 mt-3 font-light">
          Manage your personal information and account settings
        </p>
      </div>

      <div className="space-y-8">
        {/* Profile Header Card */}
        <div className="rounded-3xl shadow-lg border border-gray-100 overflow-hidden backdrop-blur-xl bg-white/80">
          <div className="p-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-2xl font-medium text-gray-900">
                Personal Information
              </h2>
              {!isEditing ? (
                <button
                  onClick={() => setIsEditing(true)}
                  className="flex items-center gap-2 px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-full transition-all duration-200 hover:shadow-lg hover:scale-105 active:scale-95 font-medium"
                >
                  <PencilIcon className="w-4 h-4" />
                  Edit Profile
                </button>
              ) : (
                <div className="flex gap-3">
                  <button
                    onClick={handleCancel}
                    className="px-6 py-3 border border-gray-200 text-gray-700 rounded-full hover:bg-gray-50 transition-all duration-200 font-medium hover:scale-105 active:scale-95"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSave}
                    className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-full transition-all duration-200 hover:shadow-lg hover:scale-105 active:scale-95 font-medium"
                  >
                    Save Changes
                  </button>
                </div>
              )}
            </div>

            <div className="flex items-start gap-8">
              {/* Apple-style Profile Image */}
              <div className="flex-shrink-0">
                <div className="relative group">
                  {profileData.profileImage ? (
                    <Image
                      src={profileData.profileImage}
                      alt="Profile"
                      width={128}
                      height={128}
                      className="w-32 h-32 rounded-3xl object-cover shadow-lg ring-4 ring-white/50"
                    />
                  ) : (
                    <div className="w-32 h-32 rounded-3xl bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center shadow-lg ring-4 ring-white/50">
                      <UserIcon className="w-16 h-16 text-gray-400" />
                    </div>
                  )}
                  {isEditing && (
                    <button className="absolute bottom-2 right-2 bg-blue-500 hover:bg-blue-600 text-white p-3 rounded-full transition-all duration-200 shadow-lg hover:scale-110 active:scale-95">
                      <CameraIcon className="w-5 h-5" />
                    </button>
                  )}
                </div>
              </div>

              {/* Apple-style Form Fields */}
              <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-2">
                    First Name
                  </label>
                  {isEditing ? (
                    <input
                      type="text"
                      name="firstName"
                      value={profileData.firstName}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-gray-50 border-0 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all duration-200 text-gray-900 placeholder-gray-400"
                    />
                  ) : (
                    <div className="px-4 py-3 bg-gray-50 rounded-2xl text-gray-900 min-h-[48px] flex items-center">
                      {profileData.firstName || (
                        <span className="text-gray-400">Not set</span>
                      )}
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-2">
                    Last Name
                  </label>
                  {isEditing ? (
                    <input
                      type="text"
                      name="lastName"
                      value={profileData.lastName}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-gray-50 border-0 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all duration-200 text-gray-900 placeholder-gray-400"
                    />
                  ) : (
                    <div className="px-4 py-3 bg-gray-50 rounded-2xl text-gray-900 min-h-[48px] flex items-center">
                      {profileData.lastName || (
                        <span className="text-gray-400">Not set</span>
                      )}
                    </div>
                  )}
                </div>

                <div className="lg:col-span-2">
                  <label className="block text-sm font-medium text-gray-600 mb-2">
                    Email Address
                  </label>
                  <div className="relative">
                    <EnvelopeIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    {isEditing ? (
                      <input
                        type="email"
                        name="email"
                        value={profileData.email}
                        onChange={handleInputChange}
                        className="w-full pl-12 pr-4 py-3 bg-gray-50 border-0 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all duration-200 text-gray-900 placeholder-gray-400"
                      />
                    ) : (
                      <div className="pl-12 pr-4 py-3 bg-gray-50 rounded-2xl text-gray-900 min-h-[48px] flex items-center">
                        {profileData.email || (
                          <span className="text-gray-400">Not set</span>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-2">
                    Phone Number
                  </label>
                  <div className="relative">
                    <PhoneIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    {isEditing ? (
                      <input
                        type="tel"
                        name="phone"
                        value={profileData.phone}
                        onChange={handleInputChange}
                        placeholder="+1 (555) 123-4567"
                        className="w-full pl-12 pr-4 py-3 bg-gray-50 border-0 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all duration-200 text-gray-900 placeholder-gray-400"
                      />
                    ) : (
                      <div className="pl-12 pr-4 py-3 bg-gray-50 rounded-2xl text-gray-900 min-h-[48px] flex items-center">
                        {profileData.phone || (
                          <span className="text-gray-400">Not set</span>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-600 mb-2">
                    Date of Birth
                  </label>
                  <div className="relative">
                    <CalendarIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    {isEditing ? (
                      <input
                        type="date"
                        name="dateOfBirth"
                        value={profileData.dateOfBirth}
                        onChange={handleInputChange}
                        className="w-full pl-12 pr-4 py-3 bg-gray-50 border-0 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all duration-200 text-gray-900"
                      />
                    ) : (
                      <div className="pl-12 pr-4 py-3 bg-gray-50 rounded-2xl text-gray-900 min-h-[48px] flex items-center">
                        {profileData.dateOfBirth || (
                          <span className="text-gray-400">Not set</span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Address Information Card */}
        <div className="rounded-3xl shadow-lg border border-gray-100 overflow-hidden backdrop-blur-xl bg-white/80">
          <div className="p-8">
            <h3 className="text-2xl font-medium text-gray-900 mb-6 flex items-center gap-3">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <MapPinIcon className="w-4 h-4 text-blue-600" />
              </div>
              Address Information
            </h3>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="lg:col-span-2">
                <label className="block text-sm font-medium text-gray-600 mb-2">
                  Street Address
                </label>
                {isEditing ? (
                  <input
                    type="text"
                    name="address"
                    value={profileData.address}
                    onChange={handleInputChange}
                    placeholder="123 Main Street"
                    className="w-full px-4 py-3 bg-gray-50 border-0 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all duration-200 text-gray-900 placeholder-gray-400"
                  />
                ) : (
                  <div className="px-4 py-3 bg-gray-50 rounded-2xl text-gray-900 min-h-[48px] flex items-center">
                    {profileData.address || (
                      <span className="text-gray-400">Not set</span>
                    )}
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-600 mb-2">
                  City
                </label>
                {isEditing ? (
                  <input
                    type="text"
                    name="city"
                    value={profileData.city}
                    onChange={handleInputChange}
                    placeholder="New York"
                    className="w-full px-4 py-3 bg-gray-50 border-0 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all duration-200 text-gray-900 placeholder-gray-400"
                  />
                ) : (
                  <div className="px-4 py-3 bg-gray-50 rounded-2xl text-gray-900 min-h-[48px] flex items-center">
                    {profileData.city || (
                      <span className="text-gray-400">Not set</span>
                    )}
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-600 mb-2">
                  Country
                </label>
                {isEditing ? (
                  <input
                    type="text"
                    name="country"
                    value={profileData.country}
                    onChange={handleInputChange}
                    placeholder="United States"
                    className="w-full px-4 py-3 bg-gray-50 border-0 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all duration-200 text-gray-900 placeholder-gray-400"
                  />
                ) : (
                  <div className="px-4 py-3 bg-gray-50 rounded-2xl text-gray-900 min-h-[48px] flex items-center">
                    {profileData.country || (
                      <span className="text-gray-400">Not set</span>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Bio Section Card */}
        <div className="rounded-3xl shadow-lg border border-gray-100 overflow-hidden backdrop-blur-xl bg-white/80">
          <div className="p-8">
            <h3 className="text-2xl font-medium text-gray-900 mb-6">
              About Me
            </h3>
            <div>
              <label className="block text-sm font-medium text-gray-600 mb-2">
                Bio
              </label>
              {isEditing ? (
                <textarea
                  name="bio"
                  value={profileData.bio}
                  onChange={handleInputChange}
                  rows={4}
                  placeholder="Tell us about yourself..."
                  className="w-full px-4 py-3 bg-gray-50 border-0 rounded-2xl focus:bg-white focus:ring-2 focus:ring-blue-500 transition-all duration-200 text-gray-900 placeholder-gray-400 resize-none"
                />
              ) : (
                <div className="px-4 py-3 bg-gray-50 rounded-2xl text-gray-900 min-h-[120px] flex items-start">
                  {profileData.bio || (
                    <span className="text-gray-400">No bio added yet</span>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
