"use client";

import { usePathname } from "next/navigation";
import { useAuth } from "@/providers/AuthContext";
import Header from "./Header";
import Footer from "./Footer";

interface ConditionalLayoutProps {
  children: React.ReactNode;
}

export default function ConditionalLayout({
  children,
}: ConditionalLayoutProps) {
  const pathname = usePathname();
  const { loading } = useAuth();
  const isDashboard =
    pathname?.startsWith("/dashboard") ||
    pathname?.startsWith("/hostdashboard");

  // Show loading state if auth is still loading and we're not on a public page
  if (
    loading &&
    !pathname?.startsWith("/login") &&
    !pathname?.startsWith("/signup")
  ) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (isDashboard) {
    // Dashboard pages: no header/footer, full height
    return <main className="h-screen">{children}</main>;
  }

  // Regular pages: with header and footer
  return (
    <>
      <Header />
      <main className="min-h-screen">{children}</main>
      <Footer />
    </>
  );
}
