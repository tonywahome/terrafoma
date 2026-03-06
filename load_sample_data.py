#!/usr/bin/env python3
"""Load sample data into Supabase database"""

import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Get Supabase credentials
url = os.getenv("SUPABASE_URL")
service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not service_role_key:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
    exit(1)

print(f"🔗 Connecting to Supabase: {url}\n")

# Create admin client
supabase = create_client(url, service_role_key)

try:
    # 1. Create sample user
    print("👤 Step 1: Creating sample user...")
    user_data = {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "kfs@conservation.ke",
        "full_name": "Kenya Forest Service",
        "role": "landowner",
        "company_name": "Kenya Forest Service"
    }
    
    # Check if user exists
    existing_user = supabase.table("users").select("*").eq("id", user_data["id"]).execute()
    if existing_user.data:
        print("   ✓ User already exists")
    else:
        supabase.table("users").insert(user_data).execute()
        print("   ✅ User created")
    
    # 2. Create land plots
    print("\n🌲 Step 2: Creating land plots...")
    plots = [
        {
            "id": "660e8400-e29b-41d4-a716-446655440001",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Aberdare Forest Conservation",
            "geometry": {"type": "Polygon", "coordinates": [[[36.70, -0.50], [36.75, -0.50], [36.75, -0.55], [36.70, -0.55], [36.70, -0.50]]]},
            "area_hectares": 45.3,
            "region": "Nyeri County",
            "land_use": "forest"
        },
        {
            "id": "660e8400-e29b-41d4-a716-446655440002",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Mount Kenya Woodland",
            "geometry": {"type": "Polygon", "coordinates": [[[37.30, -0.10], [37.35, -0.10], [37.35, -0.15], [37.30, -0.15], [37.30, -0.10]]]},
            "area_hectares": 28.7,
            "region": "Meru County",
            "land_use": "forest"
        },
        {
            "id": "660e8400-e29b-41d4-a716-446655440003",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Kakamega Rainforest Conservation",
            "geometry": {"type": "Polygon", "coordinates": [[[34.85, 0.25], [34.92, 0.25], [34.92, 0.18], [34.85, 0.18], [34.85, 0.25]]]},
            "area_hectares": 67.2,
            "region": "Kakamega County",
            "land_use": "forest"
        },
        {
            "id": "660e8400-e29b-41d4-a716-446655440004",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Mau Forest Complex",
            "geometry": {"type": "Polygon", "coordinates": [[[35.80, -0.45], [35.88, -0.45], [35.88, -0.52], [35.80, -0.52], [35.80, -0.45]]]},
            "area_hectares": 52.1,
            "region": "Nakuru County",
            "land_use": "forest"
        },
        {
            "id": "660e8400-e29b-41d4-a716-446655440005",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Loita Forest Conservation",
            "geometry": {"type": "Polygon", "coordinates": [[[35.65, -1.35], [35.72, -1.35], [35.72, -1.42], [35.65, -1.42], [35.65, -1.35]]]},
            "area_hectares": 38.9,
            "region": "Narok County",
            "land_use": "forest"
        }
    ]
    
    for plot in plots:
        existing_plot = supabase.table("land_plots").select("*").eq("id", plot["id"]).execute()
        if existing_plot.data:
            print(f"   ✓ {plot['name']} already exists")
        else:
            supabase.table("land_plots").insert(plot).execute()
            print(f"   ✅ Created {plot['name']}")
    
    # 3. Create scan results
    print("\n📊 Step 3: Creating scan results...")
    scans = [
        {
            "id": "770e8400-e29b-41d4-a716-446655440001",
            "plot_id": "660e8400-e29b-41d4-a716-446655440001",
            "estimated_biomass": 180.5,
            "estimated_tco2e": 12101.2,
            "carbon_density": 267.1,
            "integrity_score": 92.4,
            "model_version": "rf_v1"
        },
        {
            "id": "770e8400-e29b-41d4-a716-446655440002",
            "plot_id": "660e8400-e29b-41d4-a716-446655440002",
            "estimated_biomass": 125.3,
            "estimated_tco2e": 6198.1,
            "carbon_density": 215.9,
            "integrity_score": 88.1,
            "model_version": "rf_v1"
        },
        {
            "id": "770e8400-e29b-41d4-a716-446655440003",
            "plot_id": "660e8400-e29b-41d4-a716-446655440003",
            "estimated_biomass": 210.8,
            "estimated_tco2e": 24415.3,
            "carbon_density": 363.3,
            "integrity_score": 94.7,
            "model_version": "rf_v1"
        },
        {
            "id": "770e8400-e29b-41d4-a716-446655440004",
            "plot_id": "660e8400-e29b-41d4-a716-446655440004",
            "estimated_biomass": 95.4,
            "estimated_tco2e": 8566.2,
            "carbon_density": 164.4,
            "integrity_score": 76.3,
            "model_version": "rf_v1"
        },
        {
            "id": "770e8400-e29b-41d4-a716-446655440005",
            "plot_id": "660e8400-e29b-41d4-a716-446655440005",
            "estimated_biomass": 142.7,
            "estimated_tco2e": 9567.8,
            "carbon_density": 245.9,
            "integrity_score": 85.2,
            "model_version": "rf_v1"
        }
    ]
    
    for scan in scans:
        existing_scan = supabase.table("scan_results").select("*").eq("id", scan["id"]).execute()
        if existing_scan.data:
            print(f"   ✓ Scan for plot {scan['plot_id'][-4:]} already exists")
        else:
            supabase.table("scan_results").insert(scan).execute()
            print(f"   ✅ Created scan for plot {scan['plot_id'][-4:]}")
    
    # 4. Create carbon credits
    print("\n💰 Step 4: Creating carbon credits...")
    credits = [
        {
            "id": "880e8400-e29b-41d4-a716-446655440001",
            "scan_id": "770e8400-e29b-41d4-a716-446655440001",
            "plot_id": "660e8400-e29b-41d4-a716-446655440001",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "vintage_year": 2024,
            "quantity_tco2e": 12101.2,
            "price_per_tonne": 29.30,
            "status": "listed",
            "integrity_score": 92.4,
            "risk_score": 0.12
        },
        {
            "id": "880e8400-e29b-41d4-a716-446655440002",
            "scan_id": "770e8400-e29b-41d4-a716-446655440002",
            "plot_id": "660e8400-e29b-41d4-a716-446655440002",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "vintage_year": 2024,
            "quantity_tco2e": 6198.1,
            "price_per_tonne": 23.25,
            "status": "listed",
            "integrity_score": 88.1,
            "risk_score": 0.18
        },
        {
            "id": "880e8400-e29b-41d4-a716-446655440003",
            "scan_id": "770e8400-e29b-41d4-a716-446655440003",
            "plot_id": "660e8400-e29b-41d4-a716-446655440003",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "vintage_year": 2024,
            "quantity_tco2e": 24415.3,
            "price_per_tonne": 37.78,
            "status": "listed",
            "integrity_score": 94.7,
            "risk_score": 0.08
        },
        {
            "id": "880e8400-e29b-41d4-a716-446655440004",
            "scan_id": "770e8400-e29b-41d4-a716-446655440004",
            "plot_id": "660e8400-e29b-41d4-a716-446655440004",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "vintage_year": 2024,
            "quantity_tco2e": 8566.2,
            "price_per_tonne": 21.30,
            "status": "listed",
            "integrity_score": 76.3,
            "risk_score": 0.28
        },
        {
            "id": "880e8400-e29b-41d4-a716-446655440005",
            "scan_id": "770e8400-e29b-41d4-a716-446655440005",
            "plot_id": "660e8400-e29b-41d4-a716-446655440005",
            "owner_id": "550e8400-e29b-41d4-a716-446655440000",
            "vintage_year": 2024,
            "quantity_tco2e": 9567.8,
            "price_per_tonne": 22.62,
            "status": "listed",
            "integrity_score": 85.2,
            "risk_score": 0.22
        }
    ]
    
    for credit in credits:
        existing_credit = supabase.table("carbon_credits").select("*").eq("id", credit["id"]).execute()
        if existing_credit.data:
            print(f"   ✓ Credit {credit['id'][-4:]} already exists")
        else:
            supabase.table("carbon_credits").insert(credit).execute()
            print(f"   ✅ Created credit {credit['id'][-4:]}")
    
    # 5. Verify the data
    print("\n📈 Step 5: Verifying data...")
    result = supabase.table("carbon_credits").select("*").eq("status", "listed").execute()
    
    if result.data:
        total_credits = len(result.data)
        total_tco2e = sum(c["quantity_tco2e"] for c in result.data)
        total_value = sum(c["quantity_tco2e"] * c["price_per_tonne"] for c in result.data)
        
        print(f"\n{'='*60}")
        print(f"✅ SUCCESS! Database populated with sample data")
        print(f"{'='*60}")
        print(f"   📊 Credits loaded: {total_credits}")
        print(f"   🌍 Total carbon: {total_tco2e:,.1f} tCO₂e")
        print(f"   💵 Total value: ${total_value:,.2f}")
        print(f"{'='*60}\n")
        
        print("🎉 You can now access the marketplace at: http://localhost:3001/marketplace")
        print("📋 API endpoint: http://localhost:8002/api/credits?status=listed")
    else:
        print("⚠️  No credits found. Something went wrong.")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
