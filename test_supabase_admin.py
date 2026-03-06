#!/usr/bin/env python3
"""Test Supabase connection with service role key"""

import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Get credentials
url = os.getenv("SUPABASE_URL")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print(f"URL: {url}")
print(f"Service Key: {service_key[:50]}...\n")

# Create client with service role key
supabase = create_client(url, service_key)

print("✅ Supabase admin client created!")

# Query carbon credits
try:
    result = supabase.table("carbon_credits").select("*").execute()
    print(f"✅ Query successful! Found {len(result.data)} credits\n")
    
    if result.data:
        print("Credits:")
        for credit in result.data:
            print(f"  - {credit.get('id')}: {credit.get('quantity_tco2e')} tCO₂e @ ${credit.get('price_per_tonne')}/t")
    else:
        print("⚠️  No credits found!")
        
        # Check users table
        users_result = supabase.table("users").select("*").execute()
        print(f"\nUsers: {len(users_result.data)}")
        
        # Check land_plots table
        plots_result = supabase.table("land_plots").select("*").execute()
        print(f"Land plots: {len(plots_result.data)}")
        
        # Check scan_results table
        scans_result = supabase.table("scan_results").select("*").execute()
        print(f"Scan results: {len(scans_result.data)}")
        
except Exception as e:
    print(f"❌ Error querying database: {e}")
