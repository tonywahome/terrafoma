export interface LandPlot {
  id: string;
  owner_id: string;
  name: string;
  geometry: GeoJSON.Polygon;
  area_hectares: number;
  region: string | null;
  land_use: "forest" | "grassland" | "cropland" | "wetland" | "agroforestry";
}

export interface ScanResult {
  scan_id: string;
  plot_id: string | null;
  mean_ndvi: number;
  mean_evi: number;
  estimated_biomass: number;
  estimated_tco2e: number;
  carbon_density: number;
  integrity_score: number;
  buy_price_per_tonne: number;
  risk_adjustment: number;
  raw_bands?: Record<string, number>;
}

export interface CarbonCredit {
  id: string;
  scan_id?: string;
  plot_id: string;
  owner_id: string;
  vintage_year: number;
  quantity_tco2e: number;
  price_per_tonne: number;
  status: "pending" | "verified" | "listed" | "sold" | "retired";
  integrity_score: number;
  risk_score: number;
  permanence_discount: number;
  listed_at?: string;
  sold_at?: string;
  retired_at?: string;
  created_at?: string;
  region?: string;
  plot_name?: string;
}

export interface Transaction {
  id: string;
  credit_id: string;
  buyer_id: string;
  seller_id?: string;
  quantity_tco2e: number;
  total_price: number;
  currency: string;
  certificate_url?: string;
  status: string;
  created_at?: string;
}

export interface FootprintResult {
  annual_tco2e: number;
  electricity_tco2e: number;
  fuel_tco2e: number;
  monthly_tco2e: number;
}

export interface CreditStats {
  total_credits: number;
  total_verified: number;
  total_listed: number;
  total_sold: number;
  total_retired: number;
  total_tco2e: number;
  avg_price: number;
  avg_integrity: number;
}
