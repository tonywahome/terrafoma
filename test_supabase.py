#!/usr/bin/env python3
"""Test Supabase connection directly"""

import os
import sys
sys.path.insert(0, '/Users/cococe/Desktop/terrafoma/backend')

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/Users/cococe/Desktop/terrafoma/.env')

from supabase import create_client

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')

print(f"URL: {url}")
print(f"Key: {key[:50]}..." if key else "Key: None")
print()

try:
    client = create_client(url, key)
    print("✅ Supabase client created successfully!")
    
    # Try to query carbon_credits table
    result = client.table('carbon_credits').select('*').limit(5).execute()
    print(f"✅ Query successful! Found {len(result.data)} credits")
    
    if result.data:
        print("\nSample credit:")
        credit = result.data[0]
        print(f"  - ID: {credit.get('id')}")
        print(f"  - tCO2e: {credit.get('quantity_tco2e')}")
        print(f"  - Price: ${credit.get('price_per_tonne')}")
    else:
        print("\n⚠️  No credits found in database. Run sample_data.sql first!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"\nError type: {type(e).__name__}")
    
    # Additional debugging
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
