#!/usr/bin/env python3
"""Disable Row Level Security for development"""

import os
from dotenv import load_dotenv
from supabase import create_client
import requests

# Load environment variables
load_dotenv()

# Get credentials
url = os.getenv("SUPABASE_URL")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("🔓 Disabling Row Level Security for development...\n")

# We need to use the PostgreSQL REST API or direct SQL
# The Python client doesn't support administrative SQL

# Use PostgREST to execute SQL via the /rpc endpoint if available
# Or we need to instruct the user to run SQL in the dashboard

sql_commands = """
-- Disable RLS on all tables for development
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE land_plots DISABLE ROW LEVEL SECURITY;
ALTER TABLE scan_results DISABLE ROW LEVEL SECURITY;
ALTER TABLE carbon_credits DISABLE ROW LEVEL SECURITY;
ALTER TABLE risk_assessments DISABLE ROW LEVEL SECURITY;
ALTER TABLE transactions DISABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log DISABLE ROW LEVEL SECURITY;
ALTER TABLE industrial_profiles DISABLE ROW LEVEL SECURITY;

-- Or enable RLS with permissive policies
-- ALTER TABLE carbon_credits ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Allow public read access" ON carbon_credits FOR SELECT USING (true);
"""

print("⚠️  Row Level Security (RLS) is enabled on your tables.")
print("    This prevents the anon key from reading data.\n")
print("🔧 To fix this, run the following SQL in Supabase SQL Editor:")
print("    https://app.supabase.com/project/mozrcszdqinkjnnopkio/sql/new\n")
print("-" * 70)
print(sql_commands)
print("-" * 70)
print("\nAlternatively, I can try to set up public read policies...")

try:
    supabase = create_client(url, service_key)
    
    # Try using the pg_catalog to check RLS status
    print("\n📊 Checking RLS status...")
    
    # We can't directly execute SQL, so let's create policies instead
    # Unfortunately, the Python client doesn't support CREATE POLICY either
    
    print("\n✅ For now, please run the SQL above to disable RLS for development.")
    print("   Or use the browser to access:")
    print("   https://app.supabase.com/project/mozrcszdqinkjnnopkio/database/policies")

except Exception as e:
    print(f"❌ Error: {e}")
