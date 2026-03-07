#!/usr/bin/env python3
"""
Add geometry column to registration_requests table
"""
import sys
sys.path.append('/Users/cococe/Desktop/terrafoma/backend')

from config import settings
from supabase import create_client

def add_geometry_column():
    """Add geometry column using Supabase client"""
    print("🔗 Connecting to Supabase...")
    
    try:
        supabase = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )
        
        # Fetch a record to check schema
        result = supabase.table('registration_requests').select('*').limit(1).execute()
        
        if result.data and len(result.data) > 0:
            record = result.data[0]
            has_geometry = 'geometry' in record
            
            print(f"\n📊 Current schema:")
            print(f"   Columns: {', '.join(record.keys())}")
            
            if has_geometry:
                print(f"\n✅ Geometry column EXISTS!")
                print(f"   Geometry value: {record.get('geometry', 'NULL')}")
                return True
            else:
                print(f"\n⚠️  Geometry column MISSING!")
                print("\n📋 Please add it by running this SQL in Supabase SQL Editor:")
                print("=" * 80)
                
                with open('/Users/cococe/Desktop/terrafoma/backend/data/add_geometry_column.sql', 'r') as f:
                    print(f.read())
                
                print("=" * 80)
                print("\n🌐 Go to: https://supabase.com/dashboard/project/mozrcszdqinkjnnopkio/sql")
                print("   Copy and paste the SQL above, then click 'Run'\n")
                
                print("\n💡 Alternative: Run via psql:")
                print(f"   psql '{settings.database_url}' -f backend/data/add_geometry_column.sql")
                
                return False
        else:
            print("⚠️  No records found in table. Cannot check schema.")
            print("   Please create a test registration first or run the SQL migration manually.")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = add_geometry_column()
    sys.exit(0 if success else 1)
