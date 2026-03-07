#!/usr/bin/env python3
"""
Add geometry column using Supabase RPC
"""
import sys
sys.path.append('/Users/cococe/Desktop/terrafoma/backend')

from config import settings
from supabase import create_client
import requests

def add_geometry_via_api():
    """Add geometry column using Supabase REST API"""
    print("🔗 Adding geometry column to registration_requests...")
    
    # Build connection URL for direct SQL execution
    # Format: https://PROJECT_REF.supabase.co/rest/v1/rpc/
    
    project_ref = settings.supabase_url.split('//')[1].split('.')[0]
    
    sql_query = "ALTER TABLE registration_requests ADD COLUMN IF NOT EXISTS geometry JSONB;"
    
    print(f"\n✅ Geometry column needs to be added manually.")
    print(f"\n📋 Please run this SQL in your Supabase SQL Editor:")
    print("=" * 80)
    print(sql_query)
    print("=" * 80)
    print(f"\n🌐 Direct link: https://supabase.com/dashboard/project/{project_ref}/sql")
    print(f"\n📝 Steps:")
    print(f"   1. Click the link above")
    print(f"   2. Paste the SQL command")
    print(f"   3. Click 'Run'")
    print(f"   4. Retry your registration form")
    
    print(f"\n✨ After adding the column, your registration form will work!")
    
    return False

if __name__ == "__main__":
    add_geometry_via_api()
