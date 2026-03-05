"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { CreditStats } from "@/lib/types";

export default function StatsBar() {
  const [stats, setStats] = useState<CreditStats | null>(null);

  useEffect(() => {
    api
      .getCreditStats()
      .then((data) => setStats(data as CreditStats))
      .catch(() => {});
  }, []);

  const items = stats
    ? [
        { label: "Credits Verified", value: stats.total_credits },
        { label: "tCO2e Offset", value: stats.total_tco2e.toFixed(0) },
        { label: "Avg Integrity", value: `${stats.avg_integrity.toFixed(0)}/100` },
        { label: "Avg Price", value: `$${stats.avg_price.toFixed(2)}/t` },
      ]
    : [
        { label: "Credits Verified", value: "--" },
        { label: "tCO2e Offset", value: "--" },
        { label: "Avg Integrity", value: "--" },
        { label: "Avg Price", value: "--" },
      ];

  return (
    <div className="bg-terra-800 text-white py-4">
      <div className="max-w-7xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
        {items.map((item) => (
          <div key={item.label}>
            <div className="text-2xl font-bold">{item.value}</div>
            <div className="text-terra-200 text-sm">{item.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
