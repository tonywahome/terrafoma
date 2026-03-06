"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import type { FootprintResult } from "@/lib/types";

export default function DashboardPage() {
  const [energyKwh, setEnergyKwh] = useState(5000);
  const [fuelLitres, setFuelLitres] = useState(500);
  const [fuelType, setFuelType] = useState("diesel");
  const [result, setResult] = useState<FootprintResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [calcError, setCalcError] = useState<string | null>(null);

  const handleCalculate = async () => {
    setLoading(true);
    setCalcError(null);
    try {
      const data = (await api.calculateFootprint({
        energy_kwh_monthly: energyKwh,
        fuel_litres_monthly: fuelLitres,
        fuel_type: fuelType,
      })) as FootprintResult;
      setResult(data);
    } catch (err: any) {
      setCalcError(
        err?.message ||
          "Calculation failed. Is the backend running on port 8002?",
      );
    }
    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Industrial Dashboard
        </h1>
        <p className="text-gray-500 mt-1">
          Calculate your carbon footprint and find offset opportunities
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Calculator */}
        <div className="bg-white rounded-xl border shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">
            Carbon Footprint Calculator
          </h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Monthly Electricity (kWh)
              </label>
              <input
                type="number"
                value={energyKwh}
                onChange={(e) => setEnergyKwh(Number(e.target.value))}
                className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-terra-500 focus:border-terra-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Monthly Fuel (litres)
              </label>
              <input
                type="number"
                value={fuelLitres}
                onChange={(e) => setFuelLitres(Number(e.target.value))}
                className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-terra-500 focus:border-terra-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Fuel Type
              </label>
              <select
                value={fuelType}
                onChange={(e) => setFuelType(e.target.value)}
                className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-terra-500 focus:border-terra-500"
              >
                <option value="diesel">Diesel</option>
                <option value="petrol">Petrol</option>
                <option value="natural_gas">Natural Gas</option>
                <option value="lpg">LPG</option>
              </select>
            </div>
            <button
              onClick={handleCalculate}
              disabled={loading}
              className="w-full bg-terra-600 text-white py-3 rounded-lg font-semibold hover:bg-terra-700 disabled:opacity-50 transition"
            >
              {loading ? "Calculating..." : "Calculate Footprint"}
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="bg-white rounded-xl border shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Your Footprint</h2>
          {result ? (
            <div className="space-y-6">
              <div className="text-center">
                <div className="text-5xl font-bold text-terra-600">
                  {result.annual_tco2e.toFixed(1)}
                </div>
                <div className="text-gray-500 mt-1">tCO2e per year</div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-gray-800">
                    {result.electricity_tco2e.toFixed(1)}
                  </div>
                  <div className="text-sm text-gray-500">
                    Electricity (tCO2e)
                  </div>
                </div>
                <div className="bg-gray-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-gray-800">
                    {result.fuel_tco2e.toFixed(1)}
                  </div>
                  <div className="text-sm text-gray-500">Fuel (tCO2e)</div>
                </div>
              </div>

              <div className="bg-terra-50 rounded-lg p-4 text-center">
                <div className="text-lg font-semibold text-terra-700">
                  Monthly: {result.monthly_tco2e.toFixed(2)} tCO2e
                </div>
              </div>

              <a
                href="/marketplace"
                className="block w-full bg-gray-800 text-white py-3 rounded-lg font-semibold text-center hover:bg-gray-900 transition"
              >
                Offset Now →
              </a>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-400">
              <div className="text-4xl mb-2">📊</div>
              <p>Enter your consumption data and click calculate</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
