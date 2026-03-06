"use client";

import { useState, useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import IntegrityBadge from "@/components/IntegrityBadge";
import RiskGauge from "@/components/RiskGauge";
import { api } from "@/lib/api";
import type { ScanResult } from "@/lib/types";

export default function ScanPage() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const draw = useRef<MapboxDraw | null>(null);

  const [drawnGeometry, setDrawnGeometry] = useState<any>(null);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [area, setArea] = useState<number>(0);
  const [contracted, setContracted] = useState(false);

  useEffect(() => {
    console.log(
      "useEffect running, mapContainer:",
      mapContainer.current ? "exists" : "null",
      "map:",
      map.current ? "exists" : "null",
    );

    if (map.current) {
      console.log("Map already initialized, skipping");
      return;
    }

    if (!mapContainer.current) {
      console.log("Map container not ready yet");
      return;
    }

    const mapboxToken = process.env.NEXT_PUBLIC_MAPBOX_TOKEN || "";
    console.log("Mapbox token loaded:", mapboxToken ? "YES" : "NO");
    if (mapboxToken) {
      console.log("Token starts with:", mapboxToken.substring(0, 20) + "...");
    }

    if (!mapboxToken) {
      console.error("Mapbox token not found in environment");
      return;
    }

    console.log("Initializing Mapbox map...");
    mapboxgl.accessToken = mapboxToken;

    try {
      const mapInstance = new mapboxgl.Map({
        container: mapContainer.current,
        style: "mapbox://styles/mapbox/satellite-streets-v12",
        center: [36.8, -0.4],
        zoom: 12,
      });

      map.current = mapInstance;
      console.log("Mapbox map instance created successfully");

      const drawInstance = new MapboxDraw({
        displayControlsDefault: false,
        controls: {
          polygon: true,
          trash: true,
        },
        defaultMode: "draw_polygon",
      });

      draw.current = drawInstance;

      mapInstance.addControl(drawInstance);
      mapInstance.addControl(new mapboxgl.NavigationControl(), "top-right");

      mapInstance.on("draw.create", updateArea);
      mapInstance.on("draw.delete", updateArea);
      mapInstance.on("draw.update", updateArea);

      mapInstance.on("load", () => {
        console.log("Mapbox map loaded and tiles rendered successfully!");
      });

      mapInstance.on("error", (e) => {
        console.error("Mapbox error:", e);
      });
    } catch (error) {
      console.error("Failed to initialize Mapbox:", error);
    }

    return () => {
      if (map.current) {
        console.log("Cleaning up map");
        map.current.remove();
        map.current = null;
      }
    };
  }, []);

  function updateArea() {
    const data = draw.current?.getAll();
    if (data && data.features.length > 0) {
      const feature = data.features[0];
      setDrawnGeometry(feature.geometry);

      // Type guard to ensure it's a Polygon geometry
      if (feature.geometry.type === "Polygon") {
        const coords = (feature.geometry as any).coordinates[0];
        const areaKm2 = calculatePolygonArea(coords);
        setArea(areaKm2 * 100);
      }
    } else {
      setDrawnGeometry(null);
      setArea(0);
      setScanResult(null);
    }
  }

  function calculatePolygonArea(coords: number[][]): number {
    let area = 0;
    for (let i = 0; i < coords.length - 1; i++) {
      const [x1, y1] = coords[i];
      const [x2, y2] = coords[i + 1];
      area += x1 * y2 - x2 * y1;
    }
    area = Math.abs(area / 2);
    return area * 111 * 111;
  }

  const handleScan = async () => {
    if (!drawnGeometry) return;
    setLoading(true);
    setScanResult(null);

    try {
      const result = (await api.runScan({
        geometry: drawnGeometry,
        owner_id: "demo-user",
      })) as ScanResult;
      setScanResult(result);
    } catch (err) {
      console.error("Scan failed:", err);
      alert("Scan failed. Make sure the backend is running on port 8002.");
    }
    setLoading(false);
  };

  const handleAcceptContract = async () => {
    if (!scanResult) return;
    try {
      await api.createCredit({
        scan_id: scanResult.scan_id,
        plot_id: null,
        owner_id: "demo-user",
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
      <div className="flex-1 relative">
        <div ref={mapContainer} className="absolute inset-0 w-full h-full" />
      </div>

      <div className="w-96 bg-white border-l overflow-y-auto">
        <div className="p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-900">Land Scanner</h2>
          <p className="text-sm text-gray-500 mb-6">
            Draw a polygon on the map to select your plot, then run an AI scan
            to estimate its carbon value using real satellite imagery.
          </p>

          {drawnGeometry ? (
            <div className="space-y-4">
              <div className="bg-terra-50 rounded-lg p-4">
                <h3 className="font-semibold text-terra-800">Selected Plot</h3>
                <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <span className="text-gray-500">Area:</span>{" "}
                    <span className="font-medium">{area.toFixed(2)} ha</span>
                  </div>
                  <div>
                    <span className="text-gray-500">Status:</span>{" "}
                    <span className="font-medium text-green-600">
                      Ready to scan
                    </span>
                  </div>
                </div>
              </div>

              {!scanResult && (
                <button
                  onClick={handleScan}
                  disabled={loading}
                  className="w-full bg-terra-600 text-white py-3 rounded-lg font-semibold hover:bg-terra-700 disabled:opacity-50 transition"
                >
                  {loading ? "Scanning with AI Model..." : "🛰️ Run AI Scan"}
                </button>
              )}

              {loading && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                    <span className="font-semibold text-blue-900">
                      Processing...
                    </span>
                  </div>
                  <ul className="space-y-1 text-blue-700 ml-6">
                    <li>• Extracting Sentinel-2 imagery</li>
                    <li>• Calculating vegetation indices (NDVI, EVI, SAVI)</li>
                    <li>• Running Random Forest model</li>
                    <li>• Estimating carbon stock</li>
                  </ul>
                </div>
              )}

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
            <div className="text-center py-12">
              <div className="text-4xl mb-3">✏️</div>
              <p className="text-gray-500 mb-4">
                Draw a polygon on the map to begin
              </p>
              <div className="text-xs text-gray-400 space-y-1">
                <p>1. Click on the map to start drawing</p>
                <p>2. Click to place points around your plot</p>
                <p>3. Double-click to complete the polygon</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
