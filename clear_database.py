#!/usr/bin/env python3
"""Clear all sample data from Supabase database"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Get Supabase credentials
url = os.getenv("SUPABASE_URL")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not url or not service_key:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
    exit(1)

print(f"🗑️  Clearing all data from Supabase database...\n")

# Create admin client
supabase = create_client(url, service_key)

try:
    # Delete in reverse order of dependencies
    print("1️⃣  Deleting carbon credits...")
    result = supabase.table("carbon_credits").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print(f"   ✅ Deleted carbon credits")
    
    print("\n2️⃣  Deleting scan results...")
    result = supabase.table("scan_results").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print(f"   ✅ Deleted scan results")
    
    print("\n3️⃣  Deleting land plots...")
    result = supabase.table("land_plots").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print(f"   ✅ Deleted land plots")
    
    print("\n4️⃣  Deleting users...")
    result = supabase.table("users").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print(f"   ✅ Deleted users")
    
    print("\n5️⃣  Deleting transactions...")
    result = supabase.table("transactions").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print(f"   ✅ Deleted transactions")
    
    print("\n6️⃣  Deleting risk assessments...")
    result = supabase.table("risk_assessments").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    print(f"   ✅ Deleted risk assessments")
    
    # Verify all tables are empty
    print("\n📊 Verifying database is empty...")
    credits = supabase.table("carbon_credits").select("*").execute()
    scans = supabase.table("scan_results").select("*").execute()
    plots = supabase.table("land_plots").select("*").execute()
    users = supabase.table("users").select("*").execute()
    
    print(f"\n{'='*60}")
    print(f"✅ Database cleared successfully!")
    print(f"{'='*60}")
    print(f"   Carbon credits: {len(credits.data)}")
    print(f"   Scan results:   {len(scans.data)}")
    print(f"   Land plots:     {len(plots.data)}")
    print(f"   Users:          {len(users.data)}")
    print(f"{'='*60}\n")
    
    print("🎯 Your database is now empty and ready for new scans!")
    print("   Go to: http://localhost:3001/dashboard")
    print("   Draw a plot on the map and click 'Analyze Plot'")
    print("   New credits will appear in: http://localhost:3001/marketplace\n")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
