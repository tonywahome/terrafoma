"""Seed Supabase database with demo data."""

import json
import uuid
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_supabase_client


def seed():
    db = get_supabase_client()

    # --- Users ---
    users = [
        {"id": str(uuid.uuid4()), "email": "wanjiku@land.co.ke", "full_name": "Grace Wanjiku", "role": "landowner"},
        {"id": str(uuid.uuid4()), "email": "omondi@farm.co.ke", "full_name": "James Omondi", "role": "landowner"},
        {"id": str(uuid.uuid4()), "email": "njeri@conserve.org", "full_name": "Faith Njeri", "role": "landowner"},
        {"id": str(uuid.uuid4()), "email": "kamau@trees.co.ke", "full_name": "Peter Kamau", "role": "landowner"},
        {"id": str(uuid.uuid4()), "email": "manager@nairobi-textiles.co.ke", "full_name": "David Mwangi", "role": "buyer", "company_name": "Nairobi Textiles Ltd"},
        {"id": str(uuid.uuid4()), "email": "ops@thika-foods.co.ke", "full_name": "Sarah Akinyi", "role": "buyer", "company_name": "Thika Food Processors"},
        {"id": str(uuid.uuid4()), "email": "ceo@mombasa-cement.co.ke", "full_name": "Hassan Ali", "role": "buyer", "company_name": "Mombasa Cement Works"},
        {"id": str(uuid.uuid4()), "email": "admin@terrafoma.io", "full_name": "TerraFoma Admin", "role": "admin"},
    ]
    print("Seeding users...")
    for user in users:
        try:
            db.table("users").upsert(user).execute()
        except Exception as e:
            print(f"  Warning: {e}")

    # --- Land Plots ---
    with open(os.path.join(os.path.dirname(__file__), "sample_plots.geojson")) as f:
        geojson = json.load(f)

    landowner_ids = [u["id"] for u in users if u["role"] == "landowner"]
    plots = []
    print("Seeding land plots...")
    for i, feature in enumerate(geojson["features"]):
        props = feature["properties"]
        plot = {
            "id": str(uuid.uuid4()),
            "owner_id": landowner_ids[i % len(landowner_ids)],
            "name": props["name"],
            "geometry": feature["geometry"],
            "area_hectares": props["area_hectares"],
            "region": props.get("region", "Nyeri"),
            "land_use": props.get("land_use", "forest"),
        }
        plots.append(plot)
        try:
            db.table("land_plots").upsert(plot).execute()
        except Exception as e:
            print(f"  Warning: {e}")

    print(f"Seeded {len(users)} users and {len(plots)} land plots.")
    print("Done! User IDs for reference:")
    for u in users:
        print(f"  {u['role']:12s} {u['full_name']:20s} {u['id']}")


if __name__ == "__main__":
    seed()
