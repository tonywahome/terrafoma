EMISSION_FACTORS = {
    "electricity_kwh": 0.000527,  # tCO2e per kWh (Kenya grid average)
    "diesel_litre": 0.002676,
    "petrol_litre": 0.002315,
    "natural_gas_m3": 0.002020,
    "lpg_kg": 0.002983,
    # Transportation
    "flight_km_short": 0.000255,  # tCO2e per km (flights < 1500 km)
    "flight_km_long": 0.000195,  # tCO2e per km (flights > 1500 km)
    # Waste
    "waste_landfill_kg": 0.000465,  # tCO2e per kg to landfill
    "waste_recycled_kg": 0.000021,  # tCO2e per kg recycled
    # Water
    "water_m3": 0.000344,  # tCO2e per m³ (treatment + supply)
    # Shipping/Freight
    "freight_truck_tonne_km": 0.000062,  # tCO2e per tonne-km
    "freight_ship_tonne_km": 0.000011,  # tCO2e per tonne-km
}

# Carbon Credit Pricing (USD per tonne CO2e)
# Based on 2024-2026 voluntary carbon market rates for nature-based solutions in East Africa
BASE_PRICE_PER_TONNE = 5.00  # USD - Market average for forestry/conservation credits
PREMIUM_PRICE = 8.00  # High-integrity, verified conservation projects
STANDARD_PRICE = 4.00  # Standard conservation credits
MINIMUM_PRICE = 2.00  # Entry-level credits

# Community benefit allocation (% of credit sale going to local communities)
COMMUNITY_BENEFIT_PERCENTAGE = 0.60  # 60% goes directly to communities


def calculate_footprint(
    energy_kwh_monthly: float = 0,
    fuel_litres_monthly: float = 0,
    fuel_type: str = "diesel",
    flights_short_km_annual: float = 0,
    flights_long_km_annual: float = 0,
    waste_landfill_kg_monthly: float = 0,
    waste_recycled_kg_monthly: float = 0,
    water_m3_monthly: float = 0,
    freight_tonne_km_monthly: float = 0,
) -> dict:
    """Calculate carbon footprint from multiple sources."""
    # Energy
    electricity_emissions = energy_kwh_monthly * 12 * EMISSION_FACTORS["electricity_kwh"]
    
    # Fuel
    fuel_key = f"{fuel_type}_litre"
    fuel_factor = EMISSION_FACTORS.get(fuel_key, EMISSION_FACTORS["diesel_litre"])
    fuel_emissions = fuel_litres_monthly * 12 * fuel_factor
    
    # Flights (annual input)
    flight_short_emissions = flights_short_km_annual * EMISSION_FACTORS["flight_km_short"]
    flight_long_emissions = flights_long_km_annual * EMISSION_FACTORS["flight_km_long"]
    flights_emissions = flight_short_emissions + flight_long_emissions
    
    # Waste (monthly)
    waste_landfill_emissions = waste_landfill_kg_monthly * 12 * EMISSION_FACTORS["waste_landfill_kg"]
    waste_recycled_emissions = waste_recycled_kg_monthly * 12 * EMISSION_FACTORS["waste_recycled_kg"]
    waste_emissions = waste_landfill_emissions + waste_recycled_emissions
    
    # Water (monthly)
    water_emissions = water_m3_monthly * 12 * EMISSION_FACTORS["water_m3"]
    
    # Freight (monthly)
    freight_emissions = freight_tonne_km_monthly * 12 * EMISSION_FACTORS["freight_truck_tonne_km"]
    
    # Total
    total = (
        electricity_emissions + 
        fuel_emissions + 
        flights_emissions + 
        waste_emissions + 
        water_emissions + 
        freight_emissions
    )
    
    return {
        "annual_tco2e": round(total, 2),
        "electricity_tco2e": round(electricity_emissions, 2),
        "fuel_tco2e": round(fuel_emissions, 2),
        "flights_tco2e": round(flights_emissions, 2),
        "waste_tco2e": round(waste_emissions, 2),
        "water_tco2e": round(water_emissions, 2),
        "freight_tco2e": round(freight_emissions, 2),
        "monthly_tco2e": round(total / 12, 2),
        "breakdown": {
            "electricity": round(electricity_emissions, 2),
            "fuel": round(fuel_emissions, 2),
            "flights": round(flights_emissions, 2),
            "waste": round(waste_emissions, 2),
            "water": round(water_emissions, 2),
            "freight": round(freight_emissions, 2),
        }
    }


def calculate_credit_price(integrity_score: float, risk_score: float) -> float:
    """
    Calculate carbon credit price based on quality metrics.
    
    Pricing tiers:
    - Premium (90-100 integrity, <0.15 risk): $30-40/tonne
    - High Quality (75-89 integrity, 0.15-0.30 risk): $22-30/tonne  
    - Standard (60-74 integrity, 0.30-0.45 risk): $15-22/tonne
    - Basic (<60 integrity, >0.45 risk): $10-15/tonne
    
    Args:
        integrity_score: 0-100 score (higher = better monitoring/verification)
        risk_score: 0-1 score (higher = more risk)
    
    Returns:
        Price per tonne in USD
    """
    # Determine base price tier
    if integrity_score >= 90 and risk_score < 0.15:
        base = PREMIUM_PRICE
    elif integrity_score >= 75 and risk_score < 0.30:
        base = BASE_PRICE_PER_TONNE
    elif integrity_score >= 60 and risk_score < 0.45:
        base = STANDARD_PRICE
    else:
        base = MINIMUM_PRICE
    
    # Fine-tune within tier
    integrity_bonus = (integrity_score - 50) / 100 * 8  # +/- $4 based on integrity
    risk_penalty = risk_score * 10  # Up to -$10 for high risk
    
    adjusted_price = base + integrity_bonus - risk_penalty
    
    # Enforce minimum viable price for communities
    adjusted_price = max(adjusted_price, MINIMUM_PRICE)
    
    return round(adjusted_price, 2)


def calculate_community_benefit(credit_value: float) -> dict:
    """
    Calculate how much goes to local communities.
    
    Args:
        credit_value: Total value of carbon credit in USD
        
    Returns:
        Dict with community benefit breakdown
    """
    community_share = credit_value * COMMUNITY_BENEFIT_PERCENTAGE
    platform_fee = credit_value * 0.15  # 15% platform/verification costs
    conservation_fund = credit_value * 0.25  # 25% to ongoing conservation activities
    
    return {
        "community_direct": round(community_share, 2),
        "conservation_fund": round(conservation_fund, 2),
        "platform_fee": round(platform_fee, 2),
        "community_percentage": COMMUNITY_BENEFIT_PERCENTAGE * 100,
    }
