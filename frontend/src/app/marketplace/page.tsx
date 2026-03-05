"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import type { CarbonCredit } from "@/lib/types";
import IntegrityBadge from "@/components/IntegrityBadge";
import RiskGauge from "@/components/RiskGauge";

export default function MarketplacePage() {
  const [credits, setCredits] = useState<CarbonCredit[]>([]);
  const [loading, setLoading] = useState(true);
  const [purchasing, setPurchasing] = useState<string | null>(null);
  const [purchased, setPurchased] = useState<string[]>([]);

  useEffect(() => {
    api
      .getCredits({ status: "listed" })
      .then((data) => {
        let items = data as CarbonCredit[];
        // Also show verified credits if no listed ones
        if (items.length === 0) {
          api.getCredits({ status: "verified" }).then((d) => {
            setCredits(d as CarbonCredit[]);
            setLoading(false);
          });
        } else {
          setCredits(items);
          setLoading(false);
        }
      })
      .catch(() => setLoading(false));
  }, []);

  const handlePurchase = async (credit: CarbonCredit) => {
    setPurchasing(credit.id);
    try {
      const tx = (await api.createTransaction({
        credit_id: credit.id,
        buyer_id: "demo-buyer",
        quantity_tco2e: credit.quantity_tco2e,
        total_price: credit.price_per_tonne * credit.quantity_tco2e,
      })) as any;
      setPurchased([...purchased, credit.id]);
    } catch (err) {
      console.error("Purchase failed:", err);
    }
    setPurchasing(null);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Credit Marketplace</h1>
        <p className="text-gray-500 mt-1">
          Browse and purchase verified carbon credits from local conservation
          projects
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-400">Loading credits...</div>
      ) : credits.length === 0 ? (
        <div className="text-center py-12 text-gray-400">
          No credits available. Run a scan first to generate credits.
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {credits.map((credit) => (
            <div
              key={credit.id}
              className="bg-white rounded-xl border shadow-sm overflow-hidden hover:shadow-md transition"
            >
              <div className="bg-terra-50 p-4 border-b">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {credit.plot_name || `Credit ${credit.id.slice(0, 8)}`}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {credit.region || "Kenya"} &middot; {credit.vintage_year}
                    </p>
                  </div>
                  <IntegrityBadge score={credit.integrity_score} size="sm" />
                </div>
              </div>
              <div className="p-4 space-y-3">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="text-2xl font-bold text-terra-600">
                      {credit.quantity_tco2e.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-500">tCO2e</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold text-gray-800">
                      ${credit.price_per_tonne.toFixed(2)}
                    </div>
                    <div className="text-sm text-gray-500">per tonne</div>
                  </div>
                </div>

                <div className="text-sm font-medium text-gray-600">
                  Total: $
                  {(credit.price_per_tonne * credit.quantity_tco2e).toFixed(2)}
                </div>

                <RiskGauge score={credit.risk_score} label="Risk Score" />

                {purchased.includes(credit.id) ? (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-center">
                    <span className="text-green-700 font-semibold">
                      Purchased!
                    </span>
                  </div>
                ) : (
                  <button
                    onClick={() => handlePurchase(credit)}
                    disabled={purchasing === credit.id}
                    className="w-full bg-terra-600 text-white py-2.5 rounded-lg font-semibold hover:bg-terra-700 disabled:opacity-50 transition"
                  >
                    {purchasing === credit.id ? "Processing..." : "Purchase"}
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
