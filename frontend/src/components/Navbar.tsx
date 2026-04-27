"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { useState, useEffect } from "react";

export default function Navbar() {
  const pathname = usePathname();
  const isHome = pathname === "/";
  const { user, logout, isAuthenticated, loading } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    if (!isHome) return;
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [isHome]);

  // Close menu on outside click
  useEffect(() => {
    if (!showUserMenu) return;
    const close = () => setShowUserMenu(false);
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, [showUserMenu]);

  const getLinks = () => {
    if (!user) return [{ href: "/", label: "Home" }];

    const base = [
      { href: "/", label: "Home" },
      { href: "/registry", label: "Registry" },
      { href: "/marketplace", label: "Marketplace" },
    ];

    if (user.role === "landowner")
      return [...base, { href: "/landowner", label: "Dashboard" }, { href: "/request-registration", label: "Register site" }];
    if (user.role === "business")
      return [...base, { href: "/dashboard", label: "Dashboard" }];
    if (user.role === "admin")
      return [...base, { href: "/admin/requests", label: "Registrations" }, { href: "/scan", label: "Scan" }, { href: "/admin/dashboard", label: "Console" }];

    return base;
  };

  const links = getLinks();

  const navBg = isHome
    ? scrolled
      ? "bg-terra-900/90 backdrop-blur-md shadow-lg"
      : "bg-transparent"
    : "bg-[var(--color-surface)] border-b border-[var(--color-border)]";

  const linkBase = isHome
    ? "text-white/80 hover:text-white hover:bg-white/10"
    : "text-secondary hover:text-primary hover:bg-terra-50";

  const linkActive = isHome
    ? "bg-white/15 text-white"
    : "bg-terra-100 text-terra-700 font-semibold";

  return (
    <nav className={`top-0 z-50 w-full transition-all duration-300 ${isHome ? "fixed" : "sticky"} ${navBg}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">

          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center transition-colors ${
              isHome ? "bg-white/15 border border-white/20 group-hover:bg-white/25" : "bg-terra-700 group-hover:bg-terra-800"
            }`}>
              <span className="text-white font-bold text-sm tracking-tight">TF</span>
            </div>
            <span className={`text-lg font-bold tracking-tight transition-colors ${
              isHome ? "text-white drop-shadow" : "text-terra-800"
            }`}>
              TerraFoma
            </span>
          </Link>

          {/* Links */}
          <div className="hidden md:flex items-center gap-0.5">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                  pathname === link.href ? linkActive : linkBase
                }`}
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Auth section */}
          {!loading && (
            <div className="flex items-center gap-2">
              {isAuthenticated && user ? (
                <div className="relative" onMouseDown={(e) => e.stopPropagation()}>
                  <button
                    onClick={() => setShowUserMenu((v) => !v)}
                    className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-sm font-medium transition-all ${
                      isHome
                        ? "text-white/90 hover:bg-white/10 border border-white/20"
                        : "text-secondary hover:bg-terra-50 border border-[var(--color-border)]"
                    }`}
                  >
                    <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
                      isHome ? "bg-white/20 text-white" : "bg-terra-700 text-white"
                    }`}>
                      {user.full_name.charAt(0).toUpperCase()}
                    </div>
                    <span className="hidden sm:block">{user.full_name.split(" ")[0]}</span>
                    <svg className={`w-3.5 h-3.5 transition-transform ${showUserMenu ? "rotate-180" : ""}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {showUserMenu && (
                    <div className="absolute right-0 mt-2 w-60 rounded-2xl shadow-xl bg-[var(--color-surface)] ring-1 ring-[var(--color-border)] overflow-hidden animate-scale-in">
                      <div className="px-4 py-3 bg-terra-50 border-b border-[var(--color-border)]">
                        <p className="text-sm font-semibold text-primary">{user.full_name}</p>
                        <p className="text-xs text-muted mt-0.5">{user.email}</p>
                        <span className="inline-block mt-2 px-2.5 py-0.5 text-xs font-medium rounded-full bg-terra-100 text-terra-700 border border-terra-200">
                          {user.role === "landowner" ? "Project operator" : user.role === "admin" ? "Platform admin" : "Credit buyer"}
                        </span>
                      </div>
                      <div className="p-2">
                        <button
                          onClick={() => { setShowUserMenu(false); logout(); }}
                          className="w-full text-left px-3 py-2 text-sm text-risk-high hover:bg-red-50 rounded-lg transition-colors font-medium"
                        >
                          Sign out
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Link
                    href="/login"
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      isHome ? "text-white/90 hover:bg-white/10" : "text-secondary hover:bg-terra-50"
                    }`}
                  >
                    Sign in
                  </Link>
                  <Link
                    href="/signup"
                    className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all shadow-sm ${
                      isHome
                        ? "bg-white text-terra-800 hover:bg-terra-50"
                        : "bg-terra-700 text-white hover:bg-terra-800"
                    }`}
                  >
                    Get access
                  </Link>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
