#!/bin/bash
# Railway Backend Deployment Check
# Run this before deploying to Railway

echo "🚂 Railway Backend Deployment Checklist"
echo "========================================"
echo ""

cd "$(dirname "$0")/backend"

# Check critical files
echo "📁 Checking required files..."

files_ok=true

if [ -f "Procfile" ]; then
    echo "✓ Procfile exists"
    echo "  Content: $(cat Procfile)"
else
    echo "✗ Procfile missing"
    files_ok=false
fi

if [ -f "requirements.txt" ]; then
    echo "✓ requirements.txt exists"
    lines=$(wc -l < requirements.txt)
    echo "  Contains $lines packages"
else
    echo "✗ requirements.txt missing"
    files_ok=false
fi

if [ -f "main.py" ]; then
    echo "✓ main.py exists"
else
    echo "✗ main.py missing"
    files_ok=false
fi

if [ -f "railway.json" ]; then
    echo "✓ railway.json exists (optional)"
else
    echo "ℹ railway.json not found (optional)"
fi

echo ""
echo "🔐 Checking environment variables..."
echo ""
echo "Required environment variables to set in Railway:"
echo "  1. SUPABASE_URL"
echo "  2. SUPABASE_ANON_KEY"
echo "  3. SUPABASE_SERVICE_ROLE_KEY"
echo "  4. GEE_SERVICE_ACCOUNT_EMAIL"
echo "  5. PYTHONUNBUFFERED=1"
echo ""

echo "📦 Checking Python dependencies..."
if [ -f "requirements.txt" ]; then
    echo "Key packages:"
    grep -E "fastapi|uvicorn|supabase|scikit-learn" requirements.txt | head -5
fi

echo ""
echo "🤖 Checking ML model..."
if [ -f "ml/models/biomass_model_v1.pkl" ]; then
    model_size=$(du -h "ml/models/biomass_model_v1.pkl" | cut -f1)
    echo "✓ ML model found (Size: $model_size)"
    
    # Check size in MB
    size_mb=$(du -m "ml/models/biomass_model_v1.pkl" | cut -f1)
    if [ "$size_mb" -gt 100 ]; then
        echo "⚠️  Warning: Model is large (${size_mb}MB)"
        echo "   Consider using Git LFS or cloud storage"
        echo ""
        echo "   Quick fix for Railway:"
        echo "   1. Upload model to Supabase Storage"
        echo "   2. Download in app startup code"
    fi
else
    echo "⚠️  ML model not found at ml/models/biomass_model_v1.pkl"
    echo "   App will fail when trying to make predictions"
fi

echo ""
echo "========================================"
if [ "$files_ok" = true ]; then
    echo "✅ Backend is ready for Railway deployment!"
    echo ""
    echo "Next steps:"
    echo "1. Push code to GitHub: git push origin main"
    echo "2. Go to railway.app"
    echo "3. New Project → Deploy from GitHub"
    echo "4. Select repository"
    echo "5. Set Root Directory to: backend"
    echo "6. Add environment variables"
    echo "7. Deploy!"
else
    echo "❌ Some required files are missing"
    echo "   Fix the issues above before deploying"
fi
echo "========================================"
