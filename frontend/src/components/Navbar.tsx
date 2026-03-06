"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";

export default function Navbar() {
  const pathname = usePathname();
  const isHome = pathname === "/";
  const { user, logout, isAuthenticated, loading } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);

  // Define links based on user role
  const getLinksForRole = () => {
    if (!user) {
      // Public links (not authenticated) - only show Home
      return [
        { href: "/", label: "Home" },
      ];
    }

    // Authenticated users see appropriate links based on role
    const baseLinks = [
      { href: "/", label: "Home" },
      { href: "/registry", label: "Registry" },
      { href: "/marketplace", label: "Marketplace" },
    ];

    if (user.role === "landowner") {
      return [
        ...baseLinks,
        { href: "/request-registration", label: "Register Land" },
      ];
    }

    if (user.role === "business") {
      return [
        ...baseLinks,
        { href: "/dashboard", label: "Dashboard" },
      ];
    }

    if (user.role === "admin") {
      return [
        ...baseLinks,
        { href: "/admin/requests", label: "Registrations" },
        { href: "/scan", label: "Scan Land" },
        { href: "/dashboard", label: "Dashboard" },
      ];
    }

    // Fallback for other roles
    return baseLinks;
  };

  const links = getLinksForRole();

  return (
    <nav
      className={`top-0 z-50 w-full transition-colors duration-300 ${
        isHome
          ? "fixed bg-black/20 backdrop-blur-md"
          : "sticky bg-white border-b border-gray-200"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div
                className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                  isHome
                    ? "bg-black/30 border border-white/20"
                    : "bg-terra-600"
                }`}
              >
                <span className="text-white font-bold text-sm">TF</span>
              </div>
              <span
                className={`text-xl font-bold ${
                  isHome ? "text-white drop-shadow" : "text-terra-800"
                }`}
              >
                TerraFoma
              </span>
            </Link>
          </div>
          <div className="flex items-center space-x-1">
            {/* Navigation Links */}
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isHome
                    ? pathname === link.href
                      ? "bg-black/30 text-white"
                      : "text-white/80 hover:bg-black/20 hover:text-white"
                    : pathname === link.href
                    ? "bg-terra-100 text-terra-700"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                }`}
              >
                {link.label}
              </Link>
            ))}

            {/* Auth Section */}
            {!loading && (
              <>
                {isAuthenticated && user ? (
                  <div className="relative ml-4">
                    <button
                      onClick={() => setShowUserMenu(!showUserMenu)}
                      className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        isHome
                          ? "text-white/90 hover:bg-black/20"
                          : "text-gray-700 hover:bg-gray-100"
                      }`}
                    >
                      <div
                        className={`w-8 h-8 rounded-full flex items-center justify-center ${
                          isHome
                            ? "bg-white/20 text-white"
                            : "bg-terra-100 text-terra-700"
                        }`}
                      >
                        {user.full_name.charAt(0).toUpperCase()}
                      </div>
                      <span>{user.full_name.split(" ")[0]}</span>
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
                          d="M19 9l-7 7-7-7"
                        />
                      </svg>
                    </button>

                    {showUserMenu && (
                      <div className="absolute right-0 mt-2 w-56 rounded-lg shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                        <div className="p-4 border-b">
                          <p className="text-sm font-medium text-gray-900">
                            {user.full_name}
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            {user.email}
                          </p>
                          <span className="inline-block mt-2 px-2 py-1 text-xs font-medium rounded-full bg-terra-100 text-terra-700">
                            {user.role === "landowner"
                              ? "🌳 Landowner"
                              : user.role === "admin"
                              ? "👑 Admin"
                              : "🏭 Business"}
                          </span>
                        </div>
                        <div className="p-2">
                          <button
                            onClick={() => {
                              setShowUserMenu(false);
                              logout();
                            }}
                            className="w-full text-left px-4 py-2 text-sm text-red-700 hover:bg-red-50 rounded-md transition-colors"
                          >
                            Sign out
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="ml-4 flex items-center space-x-2">
                    <Link
                      href="/login"
                      className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                        isHome
                          ? "text-white/90 hover:bg-black/20"
                          : "text-gray-700 hover:bg-gray-100"
                      }`}
                    >
                      Login
                    </Link>
                    <Link
                      href="/signup"
                      className={`px-4 py-2 rounded-md text-sm font-semibold transition-colors ${
                        isHome
                          ? "bg-white/90 text-terra-700 hover:bg-white"
                          : "bg-terra-600 text-white hover:bg-terra-700"
                      }`}
                    >
                      Sign up
                    </Link>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
