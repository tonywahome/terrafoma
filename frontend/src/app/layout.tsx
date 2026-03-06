import type { Metadata } from "next";
import "./globals.css";
import "mapbox-gl/dist/mapbox-gl.css";
import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
import Navbar from "@/components/Navbar";
import { AuthProvider } from "@/contexts/AuthContext";

export const metadata: Metadata = {
  title: "TerraFoma - AI Carbon Credit Verification",
  description:
    "Empowering local economies through transparent, AI-verified natural capital",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen">
        <AuthProvider>
          <Navbar />
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
