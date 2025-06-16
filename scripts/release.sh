#!/bin/bash

# Data Contracts Studio Release Script
# Usage: ./scripts/release.sh [version]
# Example: ./scripts/release.sh 0.0.2

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Get the new version
NEW_VERSION=$1

if [ -z "$NEW_VERSION" ]; then
    CURRENT_VERSION=$(cat VERSION)
    print_warning "No version specified. Current version is: $CURRENT_VERSION"
    echo "Usage: $0 <new-version>"
    echo "Example: $0 0.0.2"
    exit 1
fi

# Validate version format (basic semver check)
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    print_error "Invalid version format. Please use semantic versioning (e.g., 0.0.2)"
    exit 1
fi

CURRENT_VERSION=$(cat VERSION)
print_info "Preparing release from $CURRENT_VERSION to $NEW_VERSION"

# Check if git is clean
if ! git diff-index --quiet HEAD --; then
    print_error "Git working directory is not clean. Please commit or stash your changes."
    exit 1
fi

# Check if we're on main/master branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" ]]; then
    print_warning "You are not on main/master branch. Current branch: $CURRENT_BRANCH"
    read -p "Do you want to continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

print_info "Running tests..."
# Run tests
if command -v make &>/dev/null; then
    make test || {
        print_error "Tests failed. Please fix them before releasing."
        exit 1
    }
else
    print_warning "Make not found. Skipping tests."
fi

print_info "Running linting..."
# Run linting (non-blocking - show warnings only)
if command -v make &>/dev/null; then
    make lint
    print_success "Linting completed (warnings are non-blocking)"
else
    print_warning "Make not found. Skipping linting."
fi

print_info "Updating version files..."

# Update VERSION file
echo "$NEW_VERSION" >VERSION

# Update package.json
if command -v node &>/dev/null && command -v npm &>/dev/null; then
    npm version $NEW_VERSION --no-git-tag-version
    print_success "Updated root package.json"

    # Update frontend package.json
    cd frontend
    npm version $NEW_VERSION --no-git-tag-version
    cd ..
    print_success "Updated frontend package.json"
else
    print_warning "Node.js/npm not found. Skipping package.json updates."
fi

# Update backend version
sed -i '' "s/app_version: str = \".*\"/app_version: str = \"$NEW_VERSION\"/" backend/app/core/config.py
sed -i '' "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" backend/app/__version__.py
print_success "Updated backend version files"

# Update frontend version.ts
sed -i '' "s/export const VERSION = '.*';/export const VERSION = '$NEW_VERSION';/" frontend/src/version.ts
print_success "Updated frontend version.ts"

print_info "Creating git commit and tag..."

# Add changes to git
git add VERSION package.json frontend/package.json backend/app/core/config.py backend/app/__version__.py frontend/src/version.ts

# Create commit
git commit -m "chore: bump version to $NEW_VERSION"

# Create tag
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"

print_success "Created git commit and tag v$NEW_VERSION"

print_info "Release $NEW_VERSION is ready!"
echo
echo "Next steps:"
echo "1. Review the changes: git show v$NEW_VERSION"
echo "2. Push to remote: git push && git push --tags"
echo "3. Create a GitHub release from the tag"
echo "4. Update CHANGELOG.md with release notes"
echo "5. Deploy to production if ready"

print_success "Release script completed successfully!"
