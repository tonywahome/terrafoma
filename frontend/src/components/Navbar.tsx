"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Home" },
  { href: "/scan", label: "Scan" },
  { href: "/registry", label: "Registry" },
  { href: "/marketplace", label: "Marketplace" },
  { href: "/dashboard", label: "Dashboard" },
];

export default function Navbar() {
  const pathname = usePathname();
  const isHome = pathname === "/";

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
          </div>
        </div>
      </div>
    </nav>
  );
}
