"use client";

import { useState, useEffect, useRef } from "react";
import mapboxgl from "mapbox-gl";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import "mapbox-gl/dist/mapbox-gl.css";
import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
import IntegrityBadge from "@/components/IntegrityBadge";
import RiskGauge from "@/components/RiskGauge";
import ProtectedRoute from "@/components/ProtectedRoute";
import { api } from "@/lib/api";
import type { ScanResult } from "@/lib/types";

function ScanPageContent() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const draw = useRef<MapboxDraw | null>(null);

  const [drawnGeometry, setDrawnGeometry] = useState<any>(null);
  const [scanResult, setScanResult] = useState<ScanResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [area, setArea] = useState<number>(0);
  const [contracted, setContracted] = useState(false);
  const [ownerInfo, setOwnerInfo] = useState<any>(null);

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
    // Point to the worker file served from /public (required for Next.js standalone mode)
    // @ts-ignore
    mapboxgl.workerUrl = '/mapbox-gl-csp-worker.js';
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
        
        // Check if there's a geometry from registration request
        const storedGeometry = localStorage.getItem("scanGeometry");
        const storedOwnerInfo = localStorage.getItem("scanOwnerInfo");
        
        if (storedGeometry && drawInstance) {
          try {
            const geometry = JSON.parse(storedGeometry);
            const feature = {
              type: "Feature" as const,
              geometry: geometry,
              properties: {}
            };
            
            // Add the geometry to the map
            drawInstance.add(feature as any);
            setDrawnGeometry(geometry);
            
            // Calculate area
            if (geometry.type === "Polygon") {
              const coords = geometry.coordinates[0];
              const areaKm2 = calculatePolygonArea(coords);
              setArea(areaKm2 * 100);
            }
            
            // Set owner info if available
            if (storedOwnerInfo) {
              setOwnerInfo(JSON.parse(storedOwnerInfo));
            }
            
            // Fit map to the geometry bounds
            const coordinates = geometry.coordinates[0];
            const bounds = coordinates.reduce((bounds: any, coord: any) => {
              return bounds.extend(coord);
            }, new mapboxgl.LngLatBounds(coordinates[0], coordinates[0]));
            
            mapInstance.fitBounds(bounds, { padding: 50 });
            
            // Clear localStorage after loading
            localStorage.removeItem("scanGeometry");
            localStorage.removeItem("scanOwnerInfo");
            localStorage.removeItem("scanRequestId");
          } catch (error) {
            console.error("Failed to load stored geometry:", error);
          }
        }
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
      // Get owner_id from stored request info or use demo user
      const requestId = localStorage.getItem("scanRequestId");
      const storedOwnerInfoStr = localStorage.getItem("scanOwnerInfo");
      let ownerId = "demo-user";
      
      // If we have owner info, try to find the user by email
      if (storedOwnerInfoStr) {
        const storedOwnerInfo = JSON.parse(storedOwnerInfoStr);
        // Look up user by email to get their user_id
        try {
          const userResponse = await fetch(
            `/api/auth/user-by-email?email=${encodeURIComponent(storedOwnerInfo.email)}`
          );
          if (userResponse.ok) {
            const userData = await userResponse.json();
            ownerId = userData.id;
          }
        } catch (err) {
          console.warn("Could not fetch user by email:", err);
        }
      }
      
      const result = (await api.runScan({
        geometry: drawnGeometry,
        owner_id: ownerId,
      })) as ScanResult;
      setScanResult(result);
      
      // Alert admin that notification was sent to landowner
      if (ownerInfo) {
        alert(`✅ Scan complete! A notification has been sent to ${ownerInfo.name} (${ownerInfo.email}) to review and approve the results.`);
      }
    } catch (err) {
      console.error("Scan failed:", err);
      alert("Scan failed. Make sure the backend is running on port 8002.");
    }
    setLoading(false);
  };

  const handleAcceptContract = async () => {
    alert("This button is for the admin view. Landowners approve via their dashboard under 'Pending Scans'.");
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

          {ownerInfo && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
              <h3 className="font-semibold text-blue-900 mb-2">Registration Request</h3>
              <div className="text-sm text-blue-800 space-y-1">
                <p><strong>Owner:</strong> {ownerInfo.name}</p>
                <p><strong>Email:</strong> {ownerInfo.email}</p>
                <p><strong>Location:</strong> {ownerInfo.location}</p>
                <p><strong>Type:</strong> {ownerInfo.type}</p>
              </div>
            </div>
          )}

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

                  {/* Admin Info - No contract acceptance here */}
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="font-semibold text-blue-900 mb-2">Next Steps</h4>
                    <div className="text-sm text-blue-800 space-y-2">
                      <p>✅ Scan complete and saved</p>
                      <p>📧 Notification sent to landowner</p>
                      <p>⏳ Awaiting landowner approval</p>
                      {ownerInfo && (
                        <p className="mt-3 pt-3 border-t border-blue-300">
                          <strong>Landowner:</strong> {ownerInfo.name}<br/>
                          They will review via their dashboard.
                        </p>
                      )}
                    </div>
                  </div>
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

export default function ScanPage() {
  return (
    <ProtectedRoute allowedRoles={["admin"]}>
      <ScanPageContent />
    </ProtectedRoute>
  );
}
