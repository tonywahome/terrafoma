from fastapi import APIRouter, HTTPException
from models.land_plot import LandPlotCreate, LandPlotResponse
from database import get_supabase_client
import uuid

router = APIRouter(prefix="/api/plots", tags=["plots"])


@router.get("")
async def list_plots():
    db = get_supabase_client()
    result = db.table("land_plots").select("*").execute()
    return result.data


@router.get("/geojson")
async def get_plots_geojson():
    db = get_supabase_client()
    result = db.table("land_plots").select("*").execute()
    features = []
    for plot in result.data:
        feature = {
            "type": "Feature",
            "properties": {
                "id": plot["id"],
                "name": plot["name"],
                "area_hectares": plot["area_hectares"],
                "region": plot.get("region"),
                "land_use": plot.get("land_use"),
                "owner_id": plot.get("owner_id"),
            },
            "geometry": plot.get("geometry", {}),
        }
        features.append(feature)

    return {"type": "FeatureCollection", "features": features}


@router.get("/{plot_id}")
async def get_plot(plot_id: str):
    db = get_supabase_client()
    result = db.table("land_plots").select("*").eq("id", plot_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Plot not found")

    plot = result.data[0]

    # Get latest scan
    scan_result = (
        db.table("scan_results")
        .select("*")
        .eq("plot_id", plot_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    plot["latest_scan"] = scan_result.data[0] if scan_result.data else None
    return plot


@router.post("", response_model=LandPlotResponse)
async def create_plot(plot: LandPlotCreate):
    db = get_supabase_client()
    plot_data = {
        "id": str(uuid.uuid4()),
        **plot.model_dump(),
    }
    result = db.table("land_plots").insert(plot_data).execute()
    return result.data[0]
