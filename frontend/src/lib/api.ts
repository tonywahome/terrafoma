const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${API_URL}${endpoint}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "API request failed");
  }

  return res.json();
}

export const api = {
  // Scan
  runScan: (data: { plot_id?: string; geometry?: object; owner_id: string }) =>
    fetchAPI("/api/scan", { method: "POST", body: JSON.stringify(data) }),

  getScan: (scanId: string) => fetchAPI(`/api/scan/${scanId}`),

  // Plots
  getPlots: () => fetchAPI("/api/plots"),
  getPlotsGeoJSON: () => fetchAPI("/api/plots/geojson"),
  getPlot: (plotId: string) => fetchAPI(`/api/plots/${plotId}`),

  // Credits
  getCredits: (params?: { status?: string; min_integrity?: number }) => {
    const query = new URLSearchParams();
    if (params?.status) query.set("status", params.status);
    if (params?.min_integrity)
      query.set("min_integrity", String(params.min_integrity));
    return fetchAPI(`/api/credits?${query}`);
  },
  getCredit: (creditId: string) => fetchAPI(`/api/credits/${creditId}`),
  getCreditStats: () => fetchAPI("/api/credits/stats"),
  createCredit: (data: object) =>
    fetchAPI("/api/credits", { method: "POST", body: JSON.stringify(data) }),
  updateCreditStatus: (creditId: string, status: string) =>
    fetchAPI(`/api/credits/${creditId}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    }),

  // Transactions
  createTransaction: (data: object) =>
    fetchAPI("/api/transactions", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  getTransaction: (txId: string) => fetchAPI(`/api/transactions/${txId}`),

  // Certificates
  getCertificateURL: (txId: string) =>
    `${API_URL}/api/certificates/${txId}`,

  // Dashboard
  calculateFootprint: (data: {
    energy_kwh_monthly: number;
    fuel_litres_monthly: number;
    fuel_type: string;
  }) =>
    fetchAPI("/api/dashboard/footprint", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};
