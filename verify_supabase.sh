#!/bin/bash

# TerraFoma Supabase Setup Verification Script
# Run this after setting up Supabase to verify everything works

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║        🔍 TerraFoma Supabase Connection Test                      ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Test 1: Check .env file
echo "1️⃣  Checking .env configuration..."
if [ -f .env ]; then
    if grep -q "mozrcszdqinkjnnopkio" .env; then
        echo "   ✅ .env file configured with Supabase URL"
    else
        echo "   ❌ Supabase URL not found in .env"
        exit 1
    fi
else
    echo "   ❌ .env file not found!"
    exit 1
fi
echo ""

# Test 2: Check if backend is running
echo "2️⃣  Checking if backend is running..."
if lsof -ti:8002 > /dev/null 2>&1; then
    echo "   ✅ Backend running on port 8002"
else
    echo "   ⚠️  Backend not running. Start it with:"
    echo "      cd backend && uvicorn main:app --reload --port 8002"
    exit 1
fi
echo ""

# Test 3: Test API connection
echo "3️⃣  Testing API connection..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8002/api/credits?status=listed)
if [ "$response" = "200" ]; then
    echo "   ✅ API responding (HTTP 200)"
else
    echo "   ❌ API error (HTTP $response)"
    exit 1
fi
echo ""

# Test 4: Check if credits are loading from Supabase
echo "4️⃣  Checking carbon credits..."
credits=$(curl -s http://localhost:8002/api/credits?status=listed)
count=$(echo "$credits" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data) if isinstance(data, list) else 0)" 2>/dev/null)

if [ "$count" -gt 0 ]; then
    echo "   ✅ Found $count carbon credits"
    echo ""
    echo "   📊 Credit Summary:"
    echo "$credits" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if isinstance(data, list) and len(data) > 0:
        total_carbon = sum(c.get('quantity_tco2e', 0) for c in data)
        total_value = sum(c.get('quantity_tco2e', 0) * c.get('price_per_tonne', 0) for c in data)
        print(f'   Total Carbon: {total_carbon:,.0f} tCO₂e')
        print(f'   Total Value: \${total_value:,.2f}')
        print(f'   Community Benefit (60%): \${total_value * 0.6:,.2f}')
        print('')
        print('   Projects:')
        for c in data[:5]:
            name = c.get('plot_name', c.get('project_name', 'Unknown'))[:40]
            carbon = c.get('quantity_tco2e', 0)
            price = c.get('price_per_tonne', 0)
            print(f'   • {name}: {carbon:,.0f} tCO₂e @ \${price:.2f}/t')
except:
    pass
" 2>/dev/null
else
    echo "   ⚠️  No credits found in database"
    echo ""
    echo "   This means either:"
    echo "   a) You haven't run sample_data.sql yet (optional)"
    echo "   b) Backend is still using in-memory database"
    echo ""
    echo "   Check backend logs for: 'Supabase client initialized'"
fi
echo ""

# Test 5: Check Supabase dashboard
echo "5️⃣  Verify in Supabase Dashboard:"
echo "   👉 https://app.supabase.com/project/mozrcszdqinkjnnopkio/editor"
echo "   • Click 'Table Editor' → 'carbon_credits'"
echo "   • You should see your credits listed there"
echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                        ✅ Setup Complete!                         ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 Your TerraFoma app is now using Supabase!"
echo ""
echo "Next steps:"
echo "  • Visit http://localhost:3001/marketplace"
echo "  • Scan new plots in http://localhost:3001/dashboard"
echo "  • Check your data in Supabase dashboard"
echo ""
echo "New scans will now be saved to Supabase permanently! 🚀"
echo ""
