"use client";

import Link from "next/link";
import {
  MapPinIcon,
  PhoneIcon,
  EnvelopeIcon,
} from "@heroicons/react/24/outline";
import Logo from "./Logo";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main Footer Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Logo variant="white" size="lg" />
            </div>
            <p className="text-gray-300 text-sm leading-relaxed">
              Discover and share unforgettable experiences around the world.
              Connect with local experts and create memories that last a
              lifetime.
            </p>
            <div className="flex space-x-4">
              <a
                href="#"
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="Facebook"
              >
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                </svg>
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="Instagram"
              >
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M12.017 0C8.396 0 7.996.014 6.79.067 5.584.12 4.652.287 3.846.548c-.827.275-1.529.647-2.23 1.348C.887 2.597.515 3.299.24 4.126.12 4.932-.014 5.864-.067 7.07c-.053 1.206-.067 1.606-.067 5.217s.014 3.991.067 5.197c.053 1.206.14 2.138.367 2.944.275.827.647 1.529 1.348 2.23.701.701 1.403 1.073 2.23 1.348.796.261 1.728.428 2.934.481 1.206.053 1.606.067 5.217.067s3.991-.014 5.197-.067c1.206-.053 2.138-.22 2.944-.481.827-.275 1.529-.647 2.23-1.348.701-.701 1.073-1.403 1.348-2.23.227-.806.314-1.738.367-2.944.053-1.206.067-1.606.067-5.217s-.014-3.991-.067-5.197c-.053-1.206-.22-2.138-.481-2.944-.275-.827-.647-1.529-1.348-2.23-.701-.701-1.403-1.073-2.23-1.348-.806-.261-1.738-.428-2.944-.481C15.991.014 15.591 0 12.017 0zm0 1.802c3.532 0 3.932.014 5.318.067 1.306.053 2.028.22 2.51.367.979.294 1.677.686 2.434 1.443.757.757 1.149 1.455 1.443 2.434.147.482.314 1.204.367 2.51.053 1.386.067 1.786.067 5.318s-.014 3.932-.067 5.318c-.053 1.306-.22 2.028-.367 2.51-.294.979-.686 1.677-1.443 2.434-.757.757-1.455 1.149-2.434 1.443-.482.147-1.204.314-2.51.367-1.386.053-1.786.067-5.318.067s-3.932-.014-5.318-.067c-1.306-.053-2.028-.22-2.51-.367-.979-.294-1.677-.686-2.434-1.443-.757-.757-1.149-1.455-1.443-2.434-.147-.482-.314-1.204-.367-2.51C1.85 15.949 1.836 15.549 1.836 12.017s.014-3.932.067-5.318c.053-1.306.22-2.028.367-2.51.294-.979.686-1.677 1.443-2.434.757-.757 1.455-1.149 2.434-1.443.482-.147 1.204-.314 2.51-.367C8.085 1.816 8.485 1.802 12.017 1.802zm0 3.293c-3.662 0-6.622 2.96-6.622 6.622s2.96 6.622 6.622 6.622 6.622-2.96 6.622-6.622-2.96-6.622-6.622-6.622zm0 10.857c-2.355 0-4.265-1.91-4.265-4.265s1.91-4.265 4.265-4.265 4.265 1.91 4.265 4.265-1.91 4.265-4.265 4.265zm6.815-10.857c0 .829-.671 1.5-1.5 1.5s-1.5-.671-1.5-1.5.671-1.5 1.5-1.5 1.5.671 1.5 1.5z" />
                </svg>
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="Twitter"
              >
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
                </svg>
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="YouTube"
              >
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/tours"
                  className="text-gray-300 hover:text-white transition-colors text-sm"
                >
                  Browse Experiences
                </Link>
              </li>
              <li>
                <Link
                  href="/hostregister"
                  className="text-gray-300 hover:text-white transition-colors text-sm"
                >
                  Become a Host
                </Link>
              </li>
              <li>
                <Link
                  href="/share-tours"
                  className="text-gray-300 hover:text-white transition-colors text-sm"
                >
                  Share Your Tour
                </Link>
              </li>
              <li>
                <Link
                  href="/dashboard"
                  className="text-gray-300 hover:text-white transition-colors text-sm"
                >
                  Dashboard
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Support</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/help"
                  className="text-gray-300 hover:text-white transition-colors text-sm"
                >
                  Help Center
                </Link>
              </li>
              <li>
                <Link
                  href="/contact"
                  className="text-gray-300 hover:text-white transition-colors text-sm"
                >
                  Contact Us
                </Link>
              </li>
              <li>
                <Link
                  href="/faq"
                  className="text-gray-300 hover:text-white transition-colors text-sm"
                >
                  FAQ
                </Link>
              </li>
              <li>
                <Link
                  href="/safety"
                  className="text-gray-300 hover:text-white transition-colors text-sm"
                >
                  Safety Guidelines
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact & Newsletter */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Stay Connected</h3>

            {/* Contact Info */}
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <MapPinIcon className="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-gray-300">
                  <p>123 Travel Street</p>
                  <p>Adventure City, AC 12345</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <PhoneIcon className="w-5 h-5 text-gray-400 flex-shrink-0" />
                <span className="text-sm text-gray-300">+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-3">
                <EnvelopeIcon className="w-5 h-5 text-gray-400 flex-shrink-0" />
                <span className="text-sm text-gray-300">hello@raheva.com</span>
              </div>
            </div>

            {/* Newsletter Signup */}
            <div className="space-y-3">
              <p className="text-sm text-gray-300">
                Subscribe to our newsletter for the latest experiences and
                travel tips.
              </p>
              <div className="flex space-x-2">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-md text-white placeholder-gray-400 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-md transition-colors">
                  Subscribe
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            {/* Copyright */}
            <div className="text-sm text-gray-400">
              © {currentYear} Raheva. All rights reserved.
            </div>

            {/* Legal Links */}
            <div className="flex flex-wrap justify-center md:justify-end space-x-6">
              <Link
                href="/privacy"
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Privacy Policy
              </Link>
              <Link
                href="/terms"
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Terms of Service
              </Link>
              <Link
                href="/cookies"
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Cookie Policy
              </Link>
              <Link
                href="/accessibility"
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Accessibility
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
