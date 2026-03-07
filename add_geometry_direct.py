#!/usr/bin/env python3
"""
Add geometry column using psycopg2
"""
import sys
sys.path.append('/Users/cococe/Desktop/terrafoma/backend')

from config import settings

def add_geometry_column_psql():
    """Add geometry column using psycopg2"""
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        if not settings.database_url:
            print("❌ DATABASE_URL not configured")
            print(f"   Supabase URL configured: {settings.supabase_url}")
            return False
        
        print(f"🔗 Connecting to database...")
        
        conn = psycopg2.connect(settings.database_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'registration_requests' 
            AND column_name = 'geometry'
        """)
        
        exists = cur.fetchone()
        
        if exists:
            print("✅ Geometry column already exists!")
            cur.close()
            conn.close()
            return True
        
        # Add the column
        print("➕ Adding geometry column...")
        cur.execute("ALTER TABLE registration_requests ADD COLUMN geometry JSONB")
        
        print("✅ Successfully added geometry column!")
        
        cur.close()
        conn.close()
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed. Install with: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📋 Please run this SQL in Supabase SQL Editor instead:")
        print("   ALTER TABLE registration_requests ADD COLUMN geometry JSONB;")
        print(f"\n🌐 https://supabase.com/dashboard/project/mozrcszdqinkjnnopkio/sql")
        return False

if __name__ == "__main__":
    success = add_geometry_column_psql()
    sys.exit(0 if success else 1)
