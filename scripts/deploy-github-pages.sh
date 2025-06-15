#!/bin/bash

# GitHub Pages Deployment Script
# This script prepares the frontend for GitHub Pages deployment

set -e

echo "📦 Preparing frontend for GitHub Pages deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Configuration
FRONTEND_DIR="frontend"
BUILD_DIR="$FRONTEND_DIR/build"
GITHUB_PAGES_DIR="docs"

# Check if we're in the right directory
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "Error: Frontend directory not found. Run this script from the project root."
    exit 1
fi

cd $FRONTEND_DIR

# Install dependencies
print_status "Installing dependencies..."
npm ci

# Create production environment for GitHub Pages
print_status "Creating GitHub Pages environment..."
cat >.env.production <<EOF
# GitHub Pages Configuration
REACT_APP_API_URL=https://your-backend-api.herokuapp.com/api/v1
REACT_APP_APP_NAME=Data Contracts Studio
REACT_APP_VERSION=1.0.0
PUBLIC_URL=/data-contracts-studio
EOF

# Build for production
print_status "Building for production..."
npm run build

# Create GitHub Pages directory
cd ..
rm -rf $GITHUB_PAGES_DIR
mkdir -p $GITHUB_PAGES_DIR

# Copy build files to docs directory (GitHub Pages source)
cp -r $BUILD_DIR/* $GITHUB_PAGES_DIR/

# Create CNAME file if deploying to custom domain
# echo "your-custom-domain.com" > $GITHUB_PAGES_DIR/CNAME

# Create .nojekyll file to prevent Jekyll processing
touch $GITHUB_PAGES_DIR/.nojekyll

# Create 404.html for client-side routing
cp $GITHUB_PAGES_DIR/index.html $GITHUB_PAGES_DIR/404.html

print_status "GitHub Pages deployment prepared ✓"
echo ""
echo "Next steps:"
echo "1. Commit and push the changes"
echo "2. Go to your GitHub repository settings"
echo "3. Enable GitHub Pages with source: 'Deploy from a branch'"
echo "4. Select branch: main, folder: /docs"
echo "5. Your site will be available at: https://username.github.io/repository-name"
