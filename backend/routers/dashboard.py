from fastapi import APIRouter
from models.risk import FootprintRequest, FootprintResponse
from services.carbon_calculator import calculate_footprint

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.post("/footprint", response_model=FootprintResponse)
async def calculate_carbon_footprint(request: FootprintRequest):
    result = calculate_footprint(
        energy_kwh_monthly=request.energy_kwh_monthly,
        fuel_litres_monthly=request.fuel_litres_monthly,
        fuel_type=request.fuel_type,
    )
    return FootprintResponse(**result)
