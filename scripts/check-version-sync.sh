#!/bin/bash

# Data Contracts Studio Version Sync Checker
# This script ensures all version files are in sync

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

print_info "Checking version consistency across all components..."

# Get versions from different sources
VERSION_FILE=$(cat VERSION)
ROOT_PACKAGE_JSON=$(grep '"version":' package.json | sed 's/.*"version": *"\([^"]*\)".*/\1/')
FRONTEND_PACKAGE_JSON=$(grep '"version":' frontend/package.json | sed 's/.*"version": *"\([^"]*\)".*/\1/')
BACKEND_VERSION=$(grep '__version__:' backend/app/__version__.py | sed 's/.*"\([^"]*\)".*/\1/')
FRONTEND_VERSION_TS=$(grep "export const VERSION" frontend/src/version.ts | sed "s/.*'\([^']*\)'.*/\1/")

echo
print_info "Found versions:"
echo "  VERSION file:           $VERSION_FILE"
echo "  Root package.json:      $ROOT_PACKAGE_JSON"
echo "  Frontend package.json:  $FRONTEND_PACKAGE_JSON"
echo "  Backend __version__.py: $BACKEND_VERSION"
echo "  Frontend version.ts:    $FRONTEND_VERSION_TS"
echo

# Check if all versions match
VERSIONS_MATCH=true

if [[ "$VERSION_FILE" != "$ROOT_PACKAGE_JSON" ]]; then
    print_error "VERSION file ($VERSION_FILE) does not match root package.json ($ROOT_PACKAGE_JSON)"
    VERSIONS_MATCH=false
fi

if [[ "$VERSION_FILE" != "$FRONTEND_PACKAGE_JSON" ]]; then
    print_error "VERSION file ($VERSION_FILE) does not match frontend package.json ($FRONTEND_PACKAGE_JSON)"
    VERSIONS_MATCH=false
fi

if [[ "$VERSION_FILE" != "$BACKEND_VERSION" ]]; then
    print_error "VERSION file ($VERSION_FILE) does not match backend __version__.py ($BACKEND_VERSION)"
    VERSIONS_MATCH=false
fi

if [[ "$VERSION_FILE" != "$FRONTEND_VERSION_TS" ]]; then
    print_error "VERSION file ($VERSION_FILE) does not match frontend version.ts ($FRONTEND_VERSION_TS)"
    VERSIONS_MATCH=false
fi

if $VERSIONS_MATCH; then
    print_success "All versions are in sync! Current version: $VERSION_FILE"
    exit 0
else
    print_error "Version mismatch detected!"
    echo
    print_info "To fix this, run: ./scripts/release.sh $VERSION_FILE"
    echo "This will sync all version files to match the VERSION file."
    exit 1
fi
