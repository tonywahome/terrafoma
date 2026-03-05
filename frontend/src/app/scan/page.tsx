"use client";

import { useState, useEffect } from "react";
import MapView from "@/components/MapView";
import IntegrityBadge from "@/components/IntegrityBadge";
import RiskGauge from "@/components/RiskGauge";
import { api } from "@/lib/api";
import type { ScanResult } from "@/lib/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ScanPage() {
  const [selectedPlot, setSelectedPlot] = useState<any>(null);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [contracted, setContracted] = useState(false);

  const handlePlotClick = (feature: GeoJSON.Feature) => {
    setSelectedPlot(feature.properties);
    setScanResult(null);
    setContracted(false);
  };

  const handleScan = async () => {
    if (!selectedPlot) return;
    setLoading(true);
    try {
      const result = (await api.runScan({
        plot_id: selectedPlot.id,
        owner_id: selectedPlot.owner_id || "demo-user",
      })) as ScanResult;
      setScanResult(result);
    } catch (err) {
      console.error("Scan failed:", err);
    }
    setLoading(false);
  };

  const handleAcceptContract = async () => {
    if (!scanResult || !selectedPlot) return;
    try {
      await api.createCredit({
        scan_id: scanResult.scan_id,
        plot_id: selectedPlot.id,
        owner_id: selectedPlot.owner_id || "demo-user",
        vintage_year: new Date().getFullYear(),
        quantity_tco2e: scanResult.estimated_tco2e,
        price_per_tonne: scanResult.buy_price_per_tonne,
        integrity_score: scanResult.integrity_score,
        risk_score: scanResult.risk_adjustment,
      });
      setContracted(true);
    } catch (err) {
      console.error("Contract failed:", err);
    }
  };

  return (
    <div className="flex h-[calc(100vh-64px)]">
      {/* Map */}
      <div className="flex-1">
        <MapView
          geojsonUrl={`${API_URL}/api/plots/geojson`}
          onPlotClick={handlePlotClick}
        />
      </div>

      {/* Sidebar */}
      <div className="w-96 bg-white border-l overflow-y-auto">
        <div className="p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-900">Land Scanner</h2>
          <p className="text-sm text-gray-500 mb-6">
            Click on a plot to select it, then run an AI scan to estimate its
            carbon value.
          </p>

          {selectedPlot ? (
            <div className="space-y-4">
              {/* Plot info */}
              <div className="bg-terra-50 rounded-lg p-4">
                <h3 className="font-semibold text-terra-800">
                  {selectedPlot.name}
                </h3>
                <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="text-gray-500">Area:</span>{" "}
                    <span className="font-medium">
                      {selectedPlot.area_hectares} ha
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500">Land use:</span>{" "}
                    <span className="font-medium capitalize">
                      {selectedPlot.land_use}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500">Region:</span>{" "}
                    <span className="font-medium">{selectedPlot.region}</span>
                  </div>
                </div>
              </div>

              {/* Scan button */}
              {!scanResult && (
                <button
                  onClick={handleScan}
                  disabled={loading}
                  className="w-full bg-terra-600 text-white py-3 rounded-lg font-semibold hover:bg-terra-700 disabled:opacity-50 transition"
                >
                  {loading ? "Scanning..." : "Run AI Scan"}
                </button>
              )}

              {/* Scan results */}
              {scanResult && (
                <div className="space-y-4">
                  <div className="bg-white border rounded-lg p-4">
                    <h4 className="font-semibold mb-3">Scan Results</h4>
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <div className="text-3xl font-bold text-terra-600">
                          {scanResult.estimated_tco2e.toFixed(1)}
                        </div>
                        <div className="text-sm text-gray-500">tCO2e</div>
                      </div>
                      <IntegrityBadge score={scanResult.integrity_score} />
                    </div>

                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div className="bg-gray-50 rounded p-2">
                        <div className="text-gray-500">NDVI</div>
                        <div className="font-semibold">
                          {scanResult.mean_ndvi.toFixed(3)}
                        </div>
                      </div>
                      <div className="bg-gray-50 rounded p-2">
                        <div className="text-gray-500">EVI</div>
                        <div className="font-semibold">
                          {scanResult.mean_evi.toFixed(3)}
                        </div>
                      </div>
                      <div className="bg-gray-50 rounded p-2">
                        <div className="text-gray-500">Biomass</div>
                        <div className="font-semibold">
                          {scanResult.estimated_biomass.toFixed(1)} t/ha
                        </div>
                      </div>
                      <div className="bg-gray-50 rounded p-2">
                        <div className="text-gray-500">Carbon Density</div>
                        <div className="font-semibold">
                          {scanResult.carbon_density.toFixed(2)} tCO2e/ha
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white border rounded-lg p-4">
                    <h4 className="font-semibold mb-3">Valuation</h4>
                    <div className="text-center mb-3">
                      <div className="text-2xl font-bold text-terra-600">
                        ${scanResult.buy_price_per_tonne.toFixed(2)}
                      </div>
                      <div className="text-sm text-gray-500">per tonne</div>
                    </div>
                    <div className="text-center text-lg font-semibold text-gray-800 mb-2">
                      Total Value: $
                      {(
                        scanResult.buy_price_per_tonne *
                        scanResult.estimated_tco2e
                      ).toFixed(2)}
                    </div>
                    <RiskGauge
                      score={scanResult.risk_adjustment}
                      label="Permanence Risk"
                    />
                  </div>

                  {/* Accept contract */}
                  {!contracted ? (
                    <button
                      onClick={handleAcceptContract}
                      className="w-full bg-terra-600 text-white py-3 rounded-lg font-semibold hover:bg-terra-700 transition"
                    >
                      Accept Conservation Contract
                    </button>
                  ) : (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                      <div className="text-green-700 font-semibold">
                        Contract Accepted!
                      </div>
                      <div className="text-sm text-green-600 mt-1">
                        Credit issued and added to the registry.
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-400">
              <div className="text-4xl mb-2">🗺️</div>
              <p>Select a plot on the map to begin</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
