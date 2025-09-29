"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function ReviewsPage() {
  const router = useRouter();
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [showReplyForm, setShowReplyForm] = useState<string | null>(null);

  const reviews = [
    {
      id: "1",
      guestName: "Sarah Johnson",
      guestAvatar: "/api/placeholder/40/40",
      property: "Luxury Villa in Amman",
      rating: 5,
      date: "2024-01-15",
      comment:
        "Absolutely amazing stay! The villa was spotless and the host was incredibly helpful. The location is perfect for exploring Amman. Would definitely book again!",
      replied: true,
      reply:
        "Thank you so much for your kind words, Sarah! We're thrilled you enjoyed your stay. You're always welcome back!",
      replyDate: "2024-01-16",
    },
    {
      id: "2",
      guestName: "Ahmed Hassan",
      guestAvatar: "/api/placeholder/40/40",
      property: "Historic Amman Walking Tour",
      rating: 4,
      date: "2024-01-12",
      comment:
        "Great tour with lots of historical insights. Guide was knowledgeable and friendly. Only wish it was a bit longer!",
      replied: false,
    },
    {
      id: "3",
      guestName: "Emily Chen",
      guestAvatar: "/api/placeholder/40/40",
      property: "Desert Resort Experience",
      rating: 5,
      date: "2024-01-10",
      comment:
        "Unforgettable experience! The desert sunset was breathtaking and the camp setup was luxurious. Perfect for couples looking for a romantic getaway.",
      replied: true,
      reply:
        "We're so happy you had such a wonderful time, Emily! The desert sunsets are truly magical. Thank you for choosing us for your romantic getaway.",
      replyDate: "2024-01-11",
    },
    {
      id: "4",
      guestName: "David Smith",
      guestAvatar: "/api/placeholder/40/40",
      property: "Luxury Villa in Amman",
      rating: 3,
      date: "2024-01-08",
      comment:
        "Nice place but had some issues with the wifi and hot water took a while to come through. The host did try to help but these should be fixed.",
      replied: true,
      reply:
        "Thank you for your feedback, David. We've since upgraded our wifi and fixed the hot water system. We apologize for any inconvenience and hope to welcome you back for a better experience.",
      replyDate: "2024-01-09",
    },
    {
      id: "5",
      guestName: "Fatima Al-Zahra",
      guestAvatar: "/api/placeholder/40/40",
      property: "Historic Amman Walking Tour",
      rating: 5,
      date: "2024-01-05",
      comment:
        "Excellent tour! Learned so much about Amman's rich history. The guide was passionate and made everything come alive. Highly recommended!",
      replied: false,
    },
  ];

  const filteredReviews = reviews.filter((review) => {
    if (selectedFilter === "all") return true;
    if (selectedFilter === "pending") return !review.replied;
    if (selectedFilter === "replied") return review.replied;
    if (selectedFilter === "5stars") return review.rating === 5;
    if (selectedFilter === "4stars") return review.rating === 4;
    if (selectedFilter === "low") return review.rating <= 3;
    return true;
  });

  const renderStars = (rating: number) => {
    return [...Array(5)].map((_, index) => (
      <svg
        key={index}
        className={`w-4 h-4 ${
          index < rating ? "text-yellow-400" : "text-gray-300"
        }`}
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
      </svg>
    ));
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
              <span className="text-gray-500">Reviews</span>
            </li>
          </ol>
        </nav>

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Reviews</h1>
            <p className="text-gray-600">Manage guest feedback and responses</p>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-green-100">
                <svg
                  className="w-6 h-6 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">
                  Average Rating
                </p>
                <p className="text-2xl font-bold text-gray-900">4.6</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-blue-100">
                <svg
                  className="w-6 h-6 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">
                  Total Reviews
                </p>
                <p className="text-2xl font-bold text-gray-900">127</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-yellow-100">
                <svg
                  className="w-6 h-6 text-yellow-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">
                  Pending Replies
                </p>
                <p className="text-2xl font-bold text-gray-900">2</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-purple-100">
                <svg
                  className="w-6 h-6 text-purple-600"
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
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">
                  Response Rate
                </p>
                <p className="text-2xl font-bold text-gray-900">85%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedFilter("all")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedFilter === "all"
                  ? "bg-green-100 text-green-700 border border-green-200"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              All Reviews
            </button>
            <button
              onClick={() => setSelectedFilter("pending")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedFilter === "pending"
                  ? "bg-green-100 text-green-700 border border-green-200"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              Pending Reply
            </button>
            <button
              onClick={() => setSelectedFilter("replied")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedFilter === "replied"
                  ? "bg-green-100 text-green-700 border border-green-200"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              Replied
            </button>
            <button
              onClick={() => setSelectedFilter("5stars")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedFilter === "5stars"
                  ? "bg-green-100 text-green-700 border border-green-200"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              5 Stars
            </button>
            <button
              onClick={() => setSelectedFilter("4stars")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedFilter === "4stars"
                  ? "bg-green-100 text-green-700 border border-green-200"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              4 Stars
            </button>
            <button
              onClick={() => setSelectedFilter("low")}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedFilter === "low"
                  ? "bg-green-100 text-green-700 border border-green-200"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              3 Stars & Below
            </button>
          </div>
        </div>

        {/* Reviews List */}
        <div className="space-y-6">
          {filteredReviews.map((review) => (
            <div
              key={review.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
            >
              {/* Review Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <img
                    src={review.guestAvatar}
                    alt={review.guestName}
                    className="w-12 h-12 rounded-full mr-4"
                  />
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {review.guestName}
                    </h3>
                    <p className="text-sm text-gray-500">{review.property}</p>
                    <div className="flex items-center mt-1">
                      {renderStars(review.rating)}
                      <span className="ml-2 text-sm text-gray-500">
                        {review.date}
                      </span>
                    </div>
                  </div>
                </div>

                {!review.replied && (
                  <span className="bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                    Pending Reply
                  </span>
                )}
              </div>

              {/* Review Comment */}
              <div className="mb-4">
                <p className="text-gray-700">{review.comment}</p>
              </div>

              {/* Host Reply */}
              {review.replied && review.reply && (
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <div className="flex items-center mb-2">
                    <svg
                      className="w-5 h-5 text-gray-600 mr-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"
                      />
                    </svg>
                    <span className="text-sm font-medium text-gray-600">
                      Your reply
                    </span>
                    <span className="text-sm text-gray-500 ml-auto">
                      {review.replyDate}
                    </span>
                  </div>
                  <p className="text-gray-700">{review.reply}</p>
                </div>
              )}

              {/* Reply Form */}
              {showReplyForm === review.id && (
                <div className="border-t pt-4">
                  <textarea
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    rows={4}
                    placeholder="Write your reply to this review..."
                  />
                  <div className="flex justify-end space-x-2 mt-3">
                    <button
                      onClick={() => setShowReplyForm(null)}
                      className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => setShowReplyForm(null)}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      Send Reply
                    </button>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              {!review.replied && showReplyForm !== review.id && (
                <div className="flex justify-end">
                  <button
                    onClick={() => setShowReplyForm(review.id)}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    Reply
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>

        {filteredReviews.length === 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
            <svg
              className="w-12 h-12 mx-auto mb-4 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No reviews found
            </h3>
            <p className="text-gray-500">
              No reviews match your current filter selection.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
