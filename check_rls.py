#!/usr/bin/env python3
"""Check RLS status and provide fix instructions"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
anon_key = os.getenv("SUPABASE_ANON_KEY")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("🔒 Checking Row Level Security (RLS) status...\n")

# Test with anon key (what the frontend uses)
print("1️⃣  Testing with anon key (frontend access)...")
try:
    anon_client = create_client(url, anon_key)
    result = anon_client.table("carbon_credits").select("*").execute()
    print(f"   ✅ Anon key can read {len(result.data)} credits")
    anon_works = True
except Exception as e:
    print(f"   ❌ Anon key BLOCKED: {str(e)[:100]}")
    anon_works = False

# Test with service role key (admin access)
print("\n2️⃣  Testing with service role key (admin access)...")
try:
    admin_client = create_client(url, service_key)
    result = admin_client.table("carbon_credits").select("*").execute()
    print(f"   ✅ Service key can read {len(result.data)} credits")
    admin_works = True
except Exception as e:
    print(f"   ❌ Service key BLOCKED: {str(e)[:100]}")
    admin_works = False

print("\n" + "="*70)

if not anon_works and admin_works:
    print("⚠️  ROW LEVEL SECURITY IS BLOCKING YOUR FRONTEND!")
    print("="*70)
    print("\n🔧 TO FIX:")
    print("   1. Open: https://app.supabase.com/project/mozrcszdqinkjnnopkio/sql/new")
    print("   2. Paste this SQL:")
    print("\n" + "-"*70)
    print("ALTER TABLE users DISABLE ROW LEVEL SECURITY;")
    print("ALTER TABLE land_plots DISABLE ROW LEVEL SECURITY;")
    print("ALTER TABLE scan_results DISABLE ROW LEVEL SECURITY;")
    print("ALTER TABLE carbon_credits DISABLE ROW LEVEL SECURITY;")
    print("ALTER TABLE risk_assessments DISABLE ROW LEVEL SECURITY;")
    print("ALTER TABLE transactions DISABLE ROW LEVEL SECURITY;")
    print("ALTER TABLE audit_log DISABLE ROW LEVEL SECURITY;")
    print("ALTER TABLE industrial_profiles DISABLE ROW LEVEL SECURITY;")
    print("-"*70)
    print("\n   3. Click 'Run'")
    print("\n   4. Try scanning again!")
    print("\n💾 SQL also saved in: disable_rls.sql\n")
elif anon_works:
    print("✅ RLS IS DISABLED - YOUR APP SHOULD WORK!")
    print("="*70)
    print("\n🎯 Ready to test:")
    print("   1. Go to: http://localhost:3001/dashboard")
    print("   2. Draw a plot and click 'Analyze'")
    print("   3. Check: http://localhost:3001/marketplace")
    print("   4. Your credit should appear!\n")
else:
    print("❌ SOMETHING IS WRONG - CONTACT SUPPORT")
    print("="*70)
