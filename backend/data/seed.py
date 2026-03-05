"""Seed Supabase with real Auth users + profile data for TerraFoma demo."""

import json
import uuid
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import get_admin_client

# ---------------------------------------------------------------------------
# Demo users – Auth credentials + profile info
# ---------------------------------------------------------------------------
USERS = [
    # Landowners
    {
        "email": "grace.wanjiku@terrafoma.demo",
        "password": "TerraDemo2024!",
        "full_name": "Grace Wanjiku",
        "role": "landowner",
        "company_name": None,
    },
    {
        "email": "james.omondi@terrafoma.demo",
        "password": "TerraDemo2024!",
        "full_name": "James Omondi",
        "role": "landowner",
        "company_name": None,
    },
    {
        "email": "faith.njeri@terrafoma.demo",
        "password": "TerraDemo2024!",
        "full_name": "Faith Njeri",
        "role": "landowner",
        "company_name": None,
    },
    {
        "email": "peter.kamau@terrafoma.demo",
        "password": "TerraDemo2024!",
        "full_name": "Peter Kamau",
        "role": "landowner",
        "company_name": None,
    },
    # Buyers (industrial SMEs)
    {
        "email": "manager@nairobi-textiles.demo",
        "password": "TerraDemo2024!",
        "full_name": "David Mwangi",
        "role": "buyer",
        "company_name": "Nairobi Textiles Ltd",
        "industry_sector": "Textiles",
        "annual_emissions_tco2": 3200.0,
        "energy_kwh_monthly": 45000.0,
        "fuel_litres_monthly": 2500.0,
        "employees": 320,
        "offset_target_pct": 30.0,
    },
    {
        "email": "ops@thika-foods.demo",
        "password": "TerraDemo2024!",
        "full_name": "Sarah Akinyi",
        "role": "buyer",
        "company_name": "Thika Food Processors",
        "industry_sector": "Food & Beverage",
        "annual_emissions_tco2": 1850.0,
        "energy_kwh_monthly": 28000.0,
        "fuel_litres_monthly": 1200.0,
        "employees": 140,
        "offset_target_pct": 50.0,
    },
    {
        "email": "ceo@mombasa-cement.demo",
        "password": "TerraDemo2024!",
        "full_name": "Hassan Ali",
        "role": "buyer",
        "company_name": "Mombasa Cement Works",
        "industry_sector": "Construction Materials",
        "annual_emissions_tco2": 12400.0,
        "energy_kwh_monthly": 180000.0,
        "fuel_litres_monthly": 9500.0,
        "employees": 780,
        "offset_target_pct": 20.0,
    },
    # Admin
    {
        "email": "admin@terrafoma.demo",
        "password": "TerraAdmin2024!",
        "full_name": "TerraFoma Admin",
        "role": "admin",
        "company_name": None,
    },
]


def create_or_get_auth_user(admin, user: dict) -> str:
    """Create a Supabase Auth user and return their UUID.
    If the user already exists, retrieve their existing UUID."""
    try:
        response = admin.auth.admin.create_user(
            {
                "email": user["email"],
                "password": user["password"],
                "email_confirm": True,
                "user_metadata": {
                    "full_name": user["full_name"],
                    "role": user["role"],
                },
            }
        )
        return response.user.id
    except Exception as e:
        err = str(e).lower()
        if "already been registered" in err or "already exists" in err or "duplicate" in err:
            # User exists – look them up by iterating the admin user list
            page = admin.auth.admin.list_users()
            for u in page:
                if hasattr(u, "email") and u.email == user["email"]:
                    return u.id
            raise RuntimeError(
                f"User {user['email']} exists but could not be retrieved: {e}"
            )
        raise


def seed():
    admin = get_admin_client()
    db = admin  # service role key bypasses RLS on table writes

    print("=" * 60)
    print("TerraFoma – Supabase Seeder")
    print("=" * 60)

    # -----------------------------------------------------------------------
    # 1. Auth users + users table
    # -----------------------------------------------------------------------
    print("\n[1/3] Creating Auth users and profiles...")
    seeded_users = []

    for user in USERS:
        try:
            auth_id = create_or_get_auth_user(admin, user)
            profile = {
                "id": auth_id,
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
                "company_name": user.get("company_name"),
            }
            db.table("users").upsert(profile).execute()
            seeded_users.append({**user, "id": auth_id})
            print(f"  + {user['role']:10s}  {user['full_name']:20s}  {user['email']}")
        except Exception as e:
            print(f"  ! Failed for {user['email']}: {e}")

    # -----------------------------------------------------------------------
    # 2. Industrial profiles for buyers
    # -----------------------------------------------------------------------
    print("\n[2/3] Creating industrial profiles for buyers...")
    for user in seeded_users:
        if user["role"] != "buyer":
            continue
        try:
            profile = {
                "id": str(uuid.uuid4()),
                "user_id": user["id"],
                "company_name": user["company_name"],
                "industry_sector": user.get("industry_sector"),
                "annual_emissions_tco2": user.get("annual_emissions_tco2"),
                "energy_kwh_monthly": user.get("energy_kwh_monthly"),
                "fuel_litres_monthly": user.get("fuel_litres_monthly"),
                "employees": user.get("employees"),
                "offset_target_pct": user.get("offset_target_pct", 0),
            }
            db.table("industrial_profiles").upsert(profile, on_conflict="user_id").execute()
            print(f"  + {user['company_name']}")
        except Exception as e:
            print(f"  ! {user.get('company_name', user['email'])}: {e}")

    # -----------------------------------------------------------------------
    # 3. Land plots from GeoJSON
    # -----------------------------------------------------------------------
    print("\n[3/3] Seeding land plots...")
    geojson_path = os.path.join(os.path.dirname(__file__), "sample_plots.geojson")
    with open(geojson_path) as f:
        geojson = json.load(f)

    landowner_ids = [u["id"] for u in seeded_users if u["role"] == "landowner"]
    if not landowner_ids:
        print("  ! No landowners created – skipping plots.")
        return

    plots_inserted = 0
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
        try:
            db.table("land_plots").insert(plot).execute()
            plots_inserted += 1
            print(
                f"  + {props['name']:35s}  "
                f"{props['area_hectares']:5.1f} ha  "
                f"{props.get('land_use', '')}"
            )
        except Exception as e:
            print(f"  ! {props['name']}: {e}")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"Done.  {len(seeded_users)} users   {plots_inserted} land plots")
    print("\nDemo login credentials:")
    print("  Landowners / buyers password : TerraDemo2024!")
    print("  Admin password               : TerraAdmin2024!")
    print()
    print(f"  {'Role':<12} {'Email'}")
    print("  " + "-" * 52)
    for u in seeded_users:
        print(f"  {u['role']:<12} {u['email']}")


if __name__ == "__main__":
    seed()
