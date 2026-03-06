#!/usr/bin/env python3
"""Setup Supabase database by running schema.sql and sample_data.sql"""

import os
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

print(f"🔗 Connecting to Supabase: {url}")

# Create admin client with service role key (has permission to create tables)
supabase = create_client(url, service_role_key)

print("\n📋 Step 1: Creating database schema...")
print("-" * 60)

# Read and execute schema.sql
try:
    with open("backend/data/schema.sql", "r") as f:
        schema_sql = f.read()
    
    # Execute using the REST API's RPC function
    # Note: Supabase Python client doesn't directly support raw SQL execution
    # We need to use the PostgREST API or run via SQL Editor
    print("⚠️  Note: The Supabase Python client doesn't support direct SQL execution.")
    print("   You need to run the SQL scripts through the Supabase SQL Editor.")
    print()
    print("   📍 Go to: https://app.supabase.com/project/mozrcszdqinkjnnopkio/sql/new")
    print()
    print("   1️⃣  Copy the contents of: backend/data/schema.sql")
    print("   2️⃣  Paste into the SQL Editor")
    print("   3️⃣  Click 'Run'")
    print()
    print("   Expected result: 'Success. No rows returned' (creates 8 tables)")
    print()
    
    # Check if tables exist by trying to query one
    try:
        result = supabase.table("users").select("count", count="exact").limit(0).execute()
        print("✅ Tables already exist! Checking for data...")
        
        # Check if data exists
        credits = supabase.table("carbon_credits").select("*").execute()
        if credits.data:
            print(f"✅ Found {len(credits.data)} carbon credits in database")
            print("\n🎉 Database is already set up and populated!")
        else:
            print("\n📋 Step 2: Loading sample data...")
            print("-" * 60)
            print("   📍 Go to: https://app.supabase.com/project/mozrcszdqinkjnnopkio/sql/new")
            print()
            print("   1️⃣  Click 'New query'")
            print("   2️⃣  Copy the contents of: backend/data/sample_data.sql")
            print("   3️⃣  Paste into the SQL Editor")
            print("   4️⃣  Click 'Run'")
            print()
            print("   Expected result: 'Credits loaded: 5, Total: 62,847 tCO₂e, $1,819,900'")
    except Exception as e:
        if "relation" in str(e).lower() or "does not exist" in str(e).lower():
            print(f"⚠️  Tables don't exist yet. Please run schema.sql first.")
        else:
            print(f"⚠️  Could not check tables: {e}")

except FileNotFoundError as e:
    print(f"❌ Error: Could not find SQL file: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("📚 Documentation:")
print("   Full guide: docs/SUPABASE_SETUP.md")
print("   Quick start: docs/SUPABASE_QUICK_START.md")
print("=" * 60)
