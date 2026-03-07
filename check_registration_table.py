#!/usr/bin/env python3
"""
Create registration_requests table directly using Supabase client
"""
import sys
sys.path.append('/Users/cococe/Desktop/terrafoma/backend')

from config import settings
from supabase import create_client

def create_table():
    """Create the registration_requests table"""
    if not settings.supabase_url or not settings.supabase_service_role_key:
        print("❌ Error: Supabase credentials not configured")
        return False
    
    print(f"🔗 Connecting to Supabase: {settings.supabase_url}")
    
    try:
        # Use service role key for admin operations
        supabase = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )
        
        # Test if table exists by querying it
        try:
            result = supabase.table('registration_requests').select('id').limit(1).execute()
            print("✅ Table 'registration_requests' already exists!")
            print(f"   Found {len(result.data)} records")
            
            # Check if geometry column exists
            if result.data and len(result.data) > 0:
                first_record = result.data[0]
                if 'geometry' in first_record:
                    print("✅ Geometry column exists")
                else:
                    print("⚠️  Geometry column might not exist in all records")
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            if 'does not exist' in error_msg.lower() or 'relation' in error_msg.lower():
                print("⚠️  Table doesn't exist. Creating via SQL query...")
                print("\n📋 Please run this SQL in your Supabase SQL Editor:")
                print("=" * 80)
                
                with open('/Users/cococe/Desktop/terrafoma/backend/data/migration_add_registration_requests.sql', 'r') as f:
                    print(f.read())
                
                print("=" * 80)
                print("\n🌐 Go to: https://supabase.com/dashboard/project/_/sql")
                print("   Copy and paste the SQL above, then click 'Run'\n")
                return False
            else:
                print(f"❌ Error querying table: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = create_table()
    sys.exit(0 if success else 1)
