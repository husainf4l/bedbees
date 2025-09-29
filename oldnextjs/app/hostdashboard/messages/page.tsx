"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function MessagesPage() {
  const router = useRouter();
  const [selectedConversation, setSelectedConversation] = useState("1");
  const [newMessage, setNewMessage] = useState("");

  const conversations = [
    {
      id: "1",
      guestName: "Sarah Johnson",
      guestAvatar: "/api/placeholder/40/40",
      property: "Luxury Villa in Amman",
      lastMessage: "Thank you for the amazing stay! Everything was perfect.",
      timestamp: "2 hours ago",
      unread: 0,
      status: "active",
    },
    {
      id: "2",
      guestName: "Ahmed Hassan",
      guestAvatar: "/api/placeholder/40/40",
      property: "Historic Amman Walking Tour",
      lastMessage: "What time should we meet for the tour tomorrow?",
      timestamp: "5 hours ago",
      unread: 2,
      status: "active",
    },
    {
      id: "3",
      guestName: "Emily Chen",
      guestAvatar: "/api/placeholder/40/40",
      property: "Desert Resort Experience",
      lastMessage: "Is there WiFi available at the desert camp?",
      timestamp: "1 day ago",
      unread: 1,
      status: "active",
    },
    {
      id: "4",
      guestName: "David Smith",
      guestAvatar: "/api/placeholder/40/40",
      property: "Luxury Villa in Amman",
      lastMessage: "The checkout process was smooth. Thanks!",
      timestamp: "2 days ago",
      unread: 0,
      status: "archived",
    },
    {
      id: "5",
      guestName: "Fatima Al-Zahra",
      guestAvatar: "/api/placeholder/40/40",
      property: "Historic Amman Walking Tour",
      lastMessage: "Looking forward to the tour next week!",
      timestamp: "3 days ago",
      unread: 0,
      status: "active",
    },
  ];

  const messages = {
    "1": [
      {
        id: "1",
        sender: "guest",
        content:
          "Hi! I just booked your villa for next weekend. Could you please provide the check-in instructions?",
        timestamp: "2024-01-14 10:30 AM",
        type: "text",
      },
      {
        id: "2",
        sender: "host",
        content:
          "Hello Sarah! Thank you for booking with us. I'll send you the detailed check-in instructions via email. The villa address is 123 Rainbow Street, Amman. Check-in is from 3:00 PM onwards.",
        timestamp: "2024-01-14 11:15 AM",
        type: "text",
      },
      {
        id: "3",
        sender: "guest",
        content: "Perfect! Is parking available?",
        timestamp: "2024-01-14 11:20 AM",
        type: "text",
      },
      {
        id: "4",
        sender: "host",
        content:
          "Yes, there are 2 free parking spaces available right in front of the villa. I'll include a parking map in the check-in instructions.",
        timestamp: "2024-01-14 11:25 AM",
        type: "text",
      },
      {
        id: "5",
        sender: "guest",
        content: "Thank you for the amazing stay! Everything was perfect.",
        timestamp: "2024-01-15 12:00 PM",
        type: "text",
      },
    ],
    "2": [
      {
        id: "1",
        sender: "guest",
        content:
          "Hi! I booked the Historic Amman Walking Tour for tomorrow. What time should we meet?",
        timestamp: "2024-01-14 08:00 AM",
        type: "text",
      },
      {
        id: "2",
        sender: "host",
        content:
          "Hello Ahmed! The tour starts at 9:00 AM. We'll meet at the Roman Theatre entrance. I'll be wearing a blue ShareTrip shirt and holding a small flag.",
        timestamp: "2024-01-14 08:30 AM",
        type: "text",
      },
      {
        id: "3",
        sender: "guest",
        content: "What time should we meet for the tour tomorrow?",
        timestamp: "2024-01-14 06:00 PM",
        type: "text",
      },
    ],
  };

  const currentConversation = conversations.find(
    (c) => c.id === selectedConversation
  );
  const currentMessages =
    messages[selectedConversation as keyof typeof messages] || [];

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      // Here you would typically send the message to your backend
      console.log("Sending message:", newMessage);
      setNewMessage("");
    }
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
              <span className="text-gray-500">Messages</span>
            </li>
          </ol>
        </nav>

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Messages</h1>
            <p className="text-gray-600">Communicate with your guests</p>
          </div>
        </div>

        {/* Messages Interface */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 h-[600px] flex">
          {/* Conversations List */}
          <div className="w-1/3 border-r border-gray-200 flex flex-col">
            <div className="p-4 border-b border-gray-200">
              <div className="relative">
                <svg
                  className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
                <input
                  type="text"
                  placeholder="Search conversations..."
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
            </div>

            <div className="flex-1 overflow-y-auto">
              {conversations.map((conversation) => (
                <div
                  key={conversation.id}
                  onClick={() => setSelectedConversation(conversation.id)}
                  className={`p-4 cursor-pointer border-b border-gray-100 hover:bg-gray-50 transition-colors ${
                    selectedConversation === conversation.id
                      ? "bg-green-50 border-l-4 border-l-green-500"
                      : ""
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className="relative">
                      <img
                        src={conversation.guestAvatar}
                        alt={conversation.guestName}
                        className="w-10 h-10 rounded-full"
                      />
                      {conversation.unread > 0 && (
                        <div className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                          {conversation.unread}
                        </div>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {conversation.guestName}
                        </p>
                        <p className="text-xs text-gray-500">
                          {conversation.timestamp}
                        </p>
                      </div>
                      <p className="text-xs text-gray-500 truncate">
                        {conversation.property}
                      </p>
                      <p className="text-sm text-gray-600 truncate mt-1">
                        {conversation.lastMessage}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Chat Area */}
          <div className="flex-1 flex flex-col">
            {currentConversation ? (
              <>
                {/* Chat Header */}
                <div className="p-4 border-b border-gray-200 bg-gray-50">
                  <div className="flex items-center space-x-3">
                    <img
                      src={currentConversation.guestAvatar}
                      alt={currentConversation.guestName}
                      className="w-10 h-10 rounded-full"
                    />
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">
                        {currentConversation.guestName}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {currentConversation.property}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                  {currentMessages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${
                        message.sender === "host"
                          ? "justify-end"
                          : "justify-start"
                      }`}
                    >
                      <div
                        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                          message.sender === "host"
                            ? "bg-green-600 text-white"
                            : "bg-gray-200 text-gray-900"
                        }`}
                      >
                        <p className="text-sm">{message.content}</p>
                        <p
                          className={`text-xs mt-1 ${
                            message.sender === "host"
                              ? "text-green-100"
                              : "text-gray-500"
                          }`}
                        >
                          {message.timestamp}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Message Input */}
                <div className="p-4 border-t border-gray-200">
                  <div className="flex space-x-2">
                    <div className="flex-1 relative">
                      <input
                        type="text"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyPress={(e) =>
                          e.key === "Enter" && handleSendMessage()
                        }
                        placeholder="Type your message..."
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      />
                    </div>
                    <button
                      onClick={handleSendMessage}
                      disabled={!newMessage.trim()}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                    >
                      <svg
                        className="w-5 h-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                        />
                      </svg>
                    </button>
                  </div>

                  {/* Quick Responses */}
                  <div className="mt-2 flex flex-wrap gap-2">
                    <button
                      onClick={() =>
                        setNewMessage(
                          "Thank you for your message! I'll get back to you shortly."
                        )
                      }
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
                    >
                      Quick reply
                    </button>
                    <button
                      onClick={() =>
                        setNewMessage(
                          "Check-in is at 3:00 PM. I'll send detailed instructions soon."
                        )
                      }
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
                    >
                      Check-in info
                    </button>
                    <button
                      onClick={() =>
                        setNewMessage(
                          "Thank you for choosing us! We hope you have a wonderful stay."
                        )
                      }
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
                    >
                      Welcome message
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <div className="text-center">
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
                    Select a conversation
                  </h3>
                  <p className="text-gray-500">
                    Choose a conversation from the list to start messaging
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Message Statistics */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-6">
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
                  Total Conversations
                </p>
                <p className="text-2xl font-bold text-gray-900">24</p>
              </div>
            </div>
          </div>

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
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">
                  Response Rate
                </p>
                <p className="text-2xl font-bold text-gray-900">98%</p>
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
                  Avg Response Time
                </p>
                <p className="text-2xl font-bold text-gray-900">2.5h</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <div className="p-2 rounded-lg bg-red-100">
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
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.866-.833-2.464 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z"
                  />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">
                  Unread Messages
                </p>
                <p className="text-2xl font-bold text-gray-900">3</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
