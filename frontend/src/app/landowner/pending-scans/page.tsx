"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { useAuth } from "@/contexts/AuthContext";

interface PendingScan {
  credit_id: string;
  scan_id: string;
  plot_id: string;
  plot_name: string;
  scan_date: string;
  quantity_tco2e: number;
  price_per_tonne: number;
  total_value: number;
  integrity_score: number;
  risk_score: number;
  biomass: number;
  ndvi: number;
  evi: number;
  carbon_density: number;
  status: string;
}

export default function PendingScansPage() {
  const router = useRouter();
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [pendingScans, setPendingScans] = useState<PendingScan[]>([]);
  const [selectedScan, setSelectedScan] = useState<PendingScan | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [rejectionReason, setRejectionReason] = useState("");
  const [showRejectModal, setShowRejectModal] = useState(false);

  useEffect(() => {
    if (!authLoading) {
      if (!isAuthenticated || !user) {
        router.push("/login");
        return;
      }
      loadPendingScans();
    }
  }, [authLoading, isAuthenticated, user]);

  const loadPendingScans = async () => {
    if (!user?.id) {
      return;
    }

    try {
      const response = await api.getPendingScans(user.id) as { pending_scans: PendingScan[] };
      setPendingScans(response.pending_scans || []);
    } catch (error) {
      console.error("Error loading pending scans:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (creditId: string) => {
    if (!confirm("Are you sure you want to approve this listing? Your land will be listed on the marketplace.")) {
      return;
    }

    setProcessing(true);
    try {
      await api.approveListing(creditId, true);
      alert("✅ Listing approved! Your carbon credit is now on the marketplace.");
      loadPendingScans(); // Refresh list
      setSelectedScan(null);
    } catch (error) {
      console.error("Error approving listing:", error);
      alert("Failed to approve listing. Please try again.");
    } finally {
      setProcessing(false);
    }
  };

  const handleReject = async () => {
    if (!selectedScan) return;

    setProcessing(true);
    try {
      await api.approveListing(selectedScan.credit_id, false, rejectionReason);
      alert("Listing rejected.");
      loadPendingScans(); // Refresh list
      setSelectedScan(null);
      setShowRejectModal(false);
      setRejectionReason("");
    } catch (error) {
      console.error("Error rejecting listing:", error);
      alert("Failed to reject listing. Please try again.");
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8 flex items-center justify-center">
        <div className="text-gray-600">Loading pending scans...</div>
      </div>
    );
  }

  if (pendingScans.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Pending Land Scans</h1>
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <p className="text-gray-600 mb-4">No pending scans to review.</p>
            <p className="text-sm text-gray-500">
              When admin scans your registered land, you'll see the results here for approval.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Alert Banner */}
        <div className="bg-blue-600 text-white rounded-lg p-6 mb-6 shadow-lg">
          <div className="flex items-center space-x-3">
            <div className="text-3xl">📊</div>
            <div className="flex-1">
              <h2 className="text-xl font-bold mb-1">Land Scan Results Ready</h2>
              <p className="text-blue-100">
                Review your land scan results below. Approve to list your carbon credits on the marketplace and start earning.
              </p>
            </div>
          </div>
        </div>

        <h1 className="text-3xl font-bold text-gray-900 mb-2">Pending Land Scans</h1>
        <p className="text-gray-600 mb-8">
          Review your land scan results and approve to list on the marketplace
        </p>

        <div className="grid gap-6">
          {pendingScans.map((scan) => (
            <div
              key={scan.credit_id}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
            >
              <div className="p-6">
                {/* Header */}
                <div className="flex items-start justify-between mb-6">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900 mb-1">
                      {scan.plot_name}
                    </h2>
                    <p className="text-sm text-gray-500">
                      Scanned: {new Date(scan.scan_date).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      ⏳ Awaiting Approval
                    </span>
                  </div>
                </div>

                {/* Main Results */}
                <div className="grid md:grid-cols-2 gap-6 mb-6">
                  {/* Carbon Stock */}
                  <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-6 border-2 border-green-200">
                    <div className="text-5xl font-bold text-green-700 mb-2">
                      {scan.quantity_tco2e.toFixed(1)}
                    </div>
                    <div className="text-gray-700 text-sm font-medium">tCO2e</div>
                    <div className="text-xs text-gray-600 mt-1">Total Carbon Stock</div>
                  </div>

                  {/* Integrity Score */}
                  <div className={`rounded-lg p-6 border-2 ${
                    scan.integrity_score >= 70
                      ? "bg-green-50 border-green-200"
                      : scan.integrity_score >= 50
                      ? "bg-yellow-50 border-yellow-200"
                      : "bg-red-50 border-red-200"
                  }`}>
                    <div
                      className={`text-5xl font-bold mb-2 ${
                        scan.integrity_score >= 70
                          ? "text-green-700"
                          : scan.integrity_score >= 50
                          ? "text-yellow-700"
                          : "text-red-700"
                      }`}
                    >
                      {scan.integrity_score.toFixed(0)}
                    </div>
                    <div className="text-gray-700 text-sm font-medium">
                      {scan.integrity_score >= 70
                        ? "High Integrity"
                        : scan.integrity_score >= 50
                        ? "Medium Integrity"
                        : "Low Integrity"}
                    </div>
                    <div className="text-xs text-gray-600 mt-1">Data Quality Score</div>
                  </div>
                </div>

                {/* Detailed Metrics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">NDVI</div>
                    <div className="text-lg font-semibold text-gray-900">
                      {scan.ndvi.toFixed(3)}
                    </div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">EVI</div>
                    <div className="text-lg font-semibold text-gray-900">
                      {scan.evi.toFixed(3)}
                    </div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">Biomass</div>
                    <div className="text-lg font-semibold text-gray-900">
                      {scan.biomass.toFixed(1)} t/ha
                    </div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600 mb-1">Carbon Density</div>
                    <div className="text-lg font-semibold text-gray-900">
                      {scan.carbon_density.toFixed(2)} tCO2e/ha
                    </div>
                  </div>
                </div>

                {/* Valuation */}
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 mb-6 border border-blue-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm text-gray-600 mb-1">Valuation</div>
                      <div className="text-3xl font-bold text-indigo-700">
                        ${scan.total_value.toFixed(2)}
                      </div>
                      <div className="text-sm text-gray-600 mt-1">
                        ${scan.price_per_tonne.toFixed(2)} per tonne
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-gray-600 mb-1">Permanence Risk</div>
                      <div className="text-2xl font-bold text-gray-900">
                        {scan.risk_score.toFixed(0)}%
                      </div>
                      <div className="mt-2">
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${
                              scan.risk_score < 30
                                ? "bg-green-500"
                                : scan.risk_score < 60
                                ? "bg-yellow-500"
                                : "bg-red-500"
                            }`}
                            style={{ width: `${scan.risk_score}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => handleApprove(scan.credit_id)}
                    disabled={processing}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    ✅ Accept & List on Marketplace
                  </button>
                  <button
                    onClick={() => {
                      setSelectedScan(scan);
                      setShowRejectModal(true);
                    }}
                    disabled={processing}
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    ❌ Reject Listing
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Reject Modal */}
      {showRejectModal && selectedScan && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Reject Listing</h3>
            <p className="text-gray-600 mb-4">
              Please provide a reason for rejecting this listing (optional):
            </p>
            <textarea
              value={rejectionReason}
              onChange={(e) => setRejectionReason(e.target.value)}
              className="w-full border border-gray-300 rounded-lg p-3 mb-4 focus:ring-2 focus:ring-red-500 focus:border-transparent"
              rows={4}
              placeholder="e.g., Valuation too low, needs reassessment..."
            />
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setShowRejectModal(false);
                  setRejectionReason("");
                }}
                className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={handleReject}
                disabled={processing}
                className="flex-1 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg disabled:opacity-50"
              >
                {processing ? "Processing..." : "Confirm Reject"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
