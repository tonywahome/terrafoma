EMISSION_FACTORS = {
    "electricity_kwh": 0.000527,  # tCO2e per kWh (Kenya grid average)
    "diesel_litre": 0.002676,
    "petrol_litre": 0.002315,
    "natural_gas_m3": 0.002020,
    "lpg_kg": 0.002983,
}

BASE_PRICE_PER_TONNE = 15.00  # USD


def calculate_footprint(
    energy_kwh_monthly: float,
    fuel_litres_monthly: float,
    fuel_type: str = "diesel",
) -> dict:
    electricity_emissions = energy_kwh_monthly * 12 * EMISSION_FACTORS["electricity_kwh"]
    fuel_key = f"{fuel_type}_litre"
    fuel_factor = EMISSION_FACTORS.get(fuel_key, EMISSION_FACTORS["diesel_litre"])
    fuel_emissions = fuel_litres_monthly * 12 * fuel_factor
    total = electricity_emissions + fuel_emissions
    return {
        "annual_tco2e": round(total, 2),
        "electricity_tco2e": round(electricity_emissions, 2),
        "fuel_tco2e": round(fuel_emissions, 2),
        "monthly_tco2e": round(total / 12, 2),
    }


def calculate_credit_price(integrity_score: float, risk_score: float) -> float:
    integrity_multiplier = 0.7 + (integrity_score / 100) * 0.6  # 0.7 to 1.3
    risk_discount = risk_score * 0.3  # up to 30% discount
    adjusted_price = BASE_PRICE_PER_TONNE * integrity_multiplier * (1 - risk_discount)
    return round(adjusted_price, 2)
