#!/bin/bash
# TerraFoma Project Cleanup Script
# Removes unnecessary files and organizes the project for submission

echo "🧹 Cleaning TerraFoma project for hackathon submission..."
echo ""

# Navigate to project root
cd "$(dirname "$0")"

# 1. Remove Python cache files
echo "📦 Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# 2. Remove log files
echo "📝 Removing log files..."
find . -type f -name "*.log" -delete 2>/dev/null
find backend/ml -name "*.pid" -delete 2>/dev/null

# 3. Remove OS-specific files
echo "🖥️  Removing OS-specific files..."
find . -name ".DS_Store" -delete 2>/dev/null
find . -name "Thumbs.db" -delete 2>/dev/null

# 4. Clean Jupyter notebook checkpoints
echo "📓 Removing Jupyter checkpoints..."
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null

# 5. Remove temporary files
echo "🗑️  Removing temporary files..."
find . -type f -name "*.tmp" -delete 2>/dev/null
find . -type f -name "*.bak" -delete 2>/dev/null
find . -type f -name "*~" -delete 2>/dev/null

# 6. Remove duplicate model (keep only v1)
echo "🤖 Organizing ML models..."
if [ -f "backend/ml/biomass_model_v2_improved.pkl" ]; then
    echo "   Removing duplicate model (keeping biomass_model_v1.pkl)"
    rm -f backend/ml/biomass_model_v2_improved.pkl
fi

# 7. Remove empty directories
echo "📁 Removing empty directories..."
find . -type d -empty -delete 2>/dev/null

# 8. Clean frontend build artifacts (but keep node_modules if installed)
echo "⚛️  Cleaning frontend build artifacts..."
rm -rf frontend/.next 2>/dev/null
rm -rf frontend/out 2>/dev/null

# 9. Clean backend artifacts
echo "🐍 Cleaning backend artifacts..."
rm -rf backend/dist 2>/dev/null
rm -rf backend/build 2>/dev/null
rm -rf backend/*.egg-info 2>/dev/null

# 10. Create necessary directories if they don't exist
echo "📂 Ensuring directory structure..."
mkdir -p backend/ml/models
mkdir -p backend/ml/data
mkdir -p docs

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Project size:"
du -sh . 2>/dev/null
echo ""
echo "📁 Main directories:"
ls -lh | grep "^d" | awk '{print "   " $9}'
echo ""
echo "✨ Project is ready for submission!"
