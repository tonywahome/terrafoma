#!/usr/bin/env python3
"""Disable Row Level Security on all tables for development"""]

# project

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

url = os.getenv("SUPABASE_URL")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("🔓 Disabling Row Level Security...\n")

# Use Supabase Management API to execute SQL
# The endpoint format is: https://[project-ref].supabase.co/rest/v1/rpc/[function-name]

headers = {
    "apikey": service_key,
    "Authorization": f"Bearer {service_key}",
    "Content-Type": "application/json"
}

# List of SQL statements to disable RLS
sql_statements = [
    "ALTER TABLE users DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE land_plots DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE scan_results DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE carbon_credits DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE risk_assessments DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE transactions DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE audit_log DISABLE ROW LEVEL SECURITY;",
    "ALTER TABLE industrial_profiles DISABLE ROW LEVEL SECURITY;"
]

print("⚠️  The Supabase Python client doesn't support ALTER TABLE commands.")
print("    You need to disable RLS through the SQL Editor.\n")
print("📍 Go to: https://app.supabase.com/project/mozrcszdqinkjnnopkio/sql/new\n")
print("Copy and paste this SQL:\n")
print("-" * 70)
for stmt in sql_statements:
    print(stmt)
print("-" * 70)
print("\nThen click 'Run'\n")
print("✅ This will allow the anon key to read data from all tables.")
print("   (For production, you'll want to set up proper RLS policies instead)\n")

# Save SQL to a file for convenience
with open("disable_rls.sql", "w") as f:
    for stmt in sql_statements:
        f.write(stmt + "\n")

print("💾 SQL saved to: disable_rls.sql")
print("   You can copy from this file and paste into Supabase SQL Editor.\n")
