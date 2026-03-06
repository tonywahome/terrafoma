"use client";

import { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import ProtectedRoute from "@/components/ProtectedRoute";

function RequestRegistrationContent() {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    landLocation: "",
    landSize: "",
    landType: "forest",
    additionalInfo: "",
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002"}/api/registration/request`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            owner_name: user?.full_name,
            owner_email: user?.email,
            land_location: formData.landLocation,
            land_size: formData.landSize,
            land_type: formData.landType,
            additional_info: formData.additionalInfo,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to submit request");
      }

      setSuccess(true);
      setFormData({
        landLocation: "",
        landSize: "",
        landType: "forest",
        additionalInfo: "",
      });
    } catch (err: any) {
      setError(err.message || "Failed to submit request. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-terra-50 to-green-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-block p-4 bg-terra-100 rounded-full mb-4">
            <span className="text-4xl">🌳</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Register Your Land for Carbon Credits
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Submit your land details and our admin team will scan your property
            using AI satellite analysis. You'll receive a certificate upon
            verification.
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {success ? (
            <div className="text-center py-12">
              <div className="inline-block p-6 bg-green-100 rounded-full mb-6">
                <svg
                  className="w-16 h-16 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-3">
                Request Submitted Successfully!
              </h2>
              <p className="text-gray-600 mb-6 max-w-md mx-auto">
                Your land registration request has been sent to our admin team
                at <strong>mangamhizha@gmail.com</strong>. They will scan your
                land and contact you with the results.
              </p>
              <button
                onClick={() => setSuccess(false)}
                className="bg-terra-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-terra-700 transition"
              >
                Submit Another Request
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                  {error}
                </div>
              )}

              {/* Owner Info (readonly) */}
              <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h3 className="text-sm font-semibold text-gray-700 mb-3">
                  Your Information
                </h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">
                      Name
                    </label>
                    <p className="text-sm font-medium">{user?.full_name}</p>
                  </div>
                  <div>
                    <label className="block text-xs text-gray-600 mb-1">
                      Email
                    </label>
                    <p className="text-sm font-medium">{user?.email}</p>
                  </div>
                </div>
              </div>

              {/* Land Location */}
              <div>
                <label
                  htmlFor="landLocation"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Land Location <span className="text-red-500">*</span>
                </label>
                <input
                  id="landLocation"
                  type="text"
                  required
                  value={formData.landLocation}
                  onChange={(e) =>
                    setFormData({ ...formData, landLocation: e.target.value })
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-terra-500 focus:border-transparent"
                  placeholder="e.g., Nyeri County, Kenya or GPS coordinates"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Provide county, region, or GPS coordinates of your land
                </p>
              </div>

              {/* Land Size */}
              <div>
                <label
                  htmlFor="landSize"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Land Size (hectares) <span className="text-red-500">*</span>
                </label>
                <input
                  id="landSize"
                  type="number"
                  step="0.01"
                  required
                  value={formData.landSize}
                  onChange={(e) =>
                    setFormData({ ...formData, landSize: e.target.value })
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-terra-500 focus:border-transparent"
                  placeholder="e.g., 25.5"
                />
              </div>

              {/* Land Type */}
              <div>
                <label
                  htmlFor="landType"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Land Type <span className="text-red-500">*</span>
                </label>
                <select
                  id="landType"
                  value={formData.landType}
                  onChange={(e) =>
                    setFormData({ ...formData, landType: e.target.value })
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-terra-500 focus:border-transparent"
                >
                  <option value="forest">Forest</option>
                  <option value="grassland">Grassland</option>
                  <option value="cropland">Cropland</option>
                  <option value="wetland">Wetland</option>
                  <option value="agroforestry">Agroforestry</option>
                </select>
              </div>

              {/* Additional Info */}
              <div>
                <label
                  htmlFor="additionalInfo"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Additional Information (Optional)
                </label>
                <textarea
                  id="additionalInfo"
                  rows={4}
                  value={formData.additionalInfo}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      additionalInfo: e.target.value,
                    })
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-terra-500 focus:border-transparent"
                  placeholder="Any additional details about your land, conservation efforts, or questions..."
                />
              </div>

              {/* Submit Button */}
              <div className="pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-terra-600 to-terra-700 text-white py-4 rounded-lg font-semibold hover:from-terra-700 hover:to-terra-800 disabled:opacity-50 transition-all shadow-lg"
                >
                  {loading ? "Submitting Request..." : "Submit Registration Request"}
                </button>
              </div>

              {/* Info Box */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-start">
                  <svg
                    className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <div className="text-sm text-blue-800">
                    <p className="font-semibold mb-1">What happens next?</p>
                    <ul className="space-y-1 text-blue-700">
                      <li>• Admin receives your request via email</li>
                      <li>
                        • Your land is scanned using AI satellite imagery
                      </li>
                      <li>• Carbon credit potential is calculated</li>
                      <li>
                        • You receive a certificate and listing in marketplace
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </form>
          )}
        </div>

        {/* Contact Info */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>
            Questions? Contact our admin team at{" "}
            <a
              href="mailto:mangamhizha@gmail.com"
              className="text-terra-600 hover:text-terra-700 font-medium"
            >
              mangamhizha@gmail.com
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default function RequestRegistrationPage() {
  return (
    <ProtectedRoute allowedRoles={["landowner"]}>
      <RequestRegistrationContent />
    </ProtectedRoute>
  );
}
