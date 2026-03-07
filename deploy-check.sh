#!/bin/bash
# Quick deployment verification script
# Run this before deploying to catch common issues

set -e

echo "🔍 TerraFoma Pre-Deployment Checklist"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

echo ""
echo "📦 Checking Frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠️  Installing frontend dependencies..."
    npm install
fi

# Try to build
echo "🔨 Building frontend..."
if npm run build; then
    echo "✅ Frontend build successful"
else
    echo "❌ Frontend build failed - fix errors before deploying"
    exit 1
fi

cd ..

echo ""
echo "⚙️  Checking Backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "⚠️  Virtual environment not found"
    echo "   Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

# Check for critical files
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found"
    exit 1
fi

if [ ! -f "Procfile" ]; then
    echo "❌ Procfile not found - needed for Railway/Render"
    exit 1
fi

echo "✅ Backend files verified"

cd ..

echo ""
echo "🔐 Checking Environment Variables..."

# Check frontend env
if [ ! -f "frontend/.env.local" ] && [ ! -f "frontend/.env.production" ]; then
    echo "⚠️  No frontend environment file found"
    echo "   Create frontend/.env.production with:"
    echo "   - NEXT_PUBLIC_API_URL"
    echo "   - NEXT_PUBLIC_MAPBOX_TOKEN"
fi

# Check backend env
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No backend environment file found"
    echo "   Create backend/.env with:"
    echo "   - SUPABASE_URL"
    echo "   - SUPABASE_ANON_KEY"
    echo "   - SUPABASE_SERVICE_ROLE_KEY"
    echo "   - GEE_SERVICE_ACCOUNT_EMAIL"
fi

echo ""
echo "📊 Checking Git Status..."

# Check if git repo
if [ -d ".git" ]; then
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo "⚠️  You have uncommitted changes"
        echo "   Commit your changes before deploying"
        git status --short
    else
        echo "✅ Git repository clean"
    fi
    
    # Check current branch
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    echo "📍 Current branch: $BRANCH"
    
    # Check if pushed to remote
    if git rev-parse --abbrev-ref --symbolic-full-name @{u} > /dev/null 2>&1; then
        LOCAL=$(git rev-parse @)
        REMOTE=$(git rev-parse @{u})
        
        if [ "$LOCAL" = "$REMOTE" ]; then
            echo "✅ Local branch is up to date with remote"
        else
            echo "⚠️  Local branch differs from remote - push your changes"
        fi
    else
        echo "⚠️  No upstream branch set"
    fi
else
    echo "⚠️  Not a git repository - initialize git for easier deployment"
fi

echo ""
echo "🗄️  Checking Database..."
echo "   ℹ️  Verify Supabase manually:"
echo "   - Tables created (carbon_credits, land_plots, notifications, etc.)"
echo "   - RLS policies enabled"
echo "   - Service role key available"

echo ""
echo "🤖 Checking ML Model..."
if [ -f "backend/ml/models/biomass_model_v1.pkl" ]; then
    MODEL_SIZE=$(du -h "backend/ml/models/biomass_model_v1.pkl" | cut -f1)
    echo "✅ ML model found (Size: $MODEL_SIZE)"
    
    if [ "${MODEL_SIZE%M*}" -gt 100 ]; then
        echo "⚠️  Model is large (>100MB) - consider using Git LFS or cloud storage"
    fi
else
    echo "❌ ML model not found at backend/ml/models/biomass_model_v1.pkl"
    echo "   Model is required for predictions to work"
fi

echo ""
echo "======================================"
echo "📋 Deployment Checklist Summary:"
echo ""
echo "Frontend:"
echo "  ✅ Build successful"
echo "  ☐ Environment variables configured in Vercel"
echo "  ☐ Deployed to Vercel"
echo ""
echo "Backend:"
echo "  ✅ Files verified"
echo "  ☐ Environment variables configured in Railway/Render"
echo "  ☐ ML model accessible"
echo "  ☐ Deployed to Railway/Render"
echo ""
echo "Database:"
echo "  ☐ Supabase project configured"
echo "  ☐ Tables and RLS policies verified"
echo ""
echo "Post-Deployment:"
echo "  ☐ Update CORS origins in backend"
echo "  ☐ Test API endpoints"
echo "  ☐ Test frontend functionality"
echo "  ☐ Set up monitoring"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
echo "======================================"
