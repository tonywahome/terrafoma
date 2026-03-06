#!/usr/bin/env python3
"""Create a default demo user for the application"""

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

print(f"👤 Creating default demo user...\n")

# Create admin client
supabase = create_client(url, service_key)

# Fixed UUID for demo user
DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"

try:
    # Check if demo user already exists
    existing = supabase.table("users").select("*").eq("id", DEMO_USER_ID).execute()
    
    if existing.data:
        print(f"✅ Demo user already exists!")
        print(f"   ID: {DEMO_USER_ID}")
        print(f"   Email: {existing.data[0]['email']}")
        print(f"   Name: {existing.data[0]['full_name']}")
    else:
        # Create demo user
        user_data = {
            "id": DEMO_USER_ID,
            "email": "demo@terrafoma.com",
            "full_name": "Demo User",
            "role": "landowner",
            "company_name": "TerraFoma Demo"
        }
        
        result = supabase.table("users").insert(user_data).execute()
        print(f"✅ Demo user created successfully!")
        print(f"   ID: {DEMO_USER_ID}")
        print(f"   Email: demo@terrafoma.com")
        print(f"   Name: Demo User")
    
    print(f"\n💡 Use this UUID in your frontend: {DEMO_USER_ID}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
