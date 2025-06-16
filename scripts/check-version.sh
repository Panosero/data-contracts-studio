#!/bin/bash

# Pre-commit hook to validate version consistency
# This script checks that all version files are in sync

echo "🔍 Checking version consistency..."

# Get versions from different files
VERSION_FILE=$(cat VERSION 2>/dev/null || echo "missing")
PACKAGE_JSON=$(grep '"version"' package.json | head -1 | cut -d'"' -f4 2>/dev/null || echo "missing")
FRONTEND_PACKAGE=$(grep '"version"' frontend/package.json | head -1 | cut -d'"' -f4 2>/dev/null || echo "missing")
BACKEND_CONFIG=$(grep 'app_version:' backend/app/core/config.py | cut -d'"' -f2 2>/dev/null || echo "missing")
BACKEND_VERSION=$(grep '__version__' backend/app/__version__.py | cut -d'"' -f2 2>/dev/null || echo "missing")

# Check if all versions match
VERSIONS=("$VERSION_FILE" "$PACKAGE_JSON" "$FRONTEND_PACKAGE" "$BACKEND_CONFIG" "$BACKEND_VERSION")
FIRST_VERSION=${VERSIONS[0]}

echo "Version check results:"
echo "- VERSION file:           $VERSION_FILE"
echo "- Root package.json:      $PACKAGE_JSON"
echo "- Frontend package.json:  $FRONTEND_PACKAGE"
echo "- Backend config:         $BACKEND_CONFIG"
echo "- Backend __version__.py: $BACKEND_VERSION"

# Check for inconsistencies
INCONSISTENT=false
for version in "${VERSIONS[@]}"; do
    if [ "$version" != "$FIRST_VERSION" ]; then
        INCONSISTENT=true
        break
    fi
done

if [ "$INCONSISTENT" = true ]; then
    echo "❌ Version inconsistency detected!"
    echo "All version files should have the same version: $FIRST_VERSION"
    echo "Please run: make release VERSION=<correct-version>"
    exit 1
fi

echo "✅ All versions are consistent: $FIRST_VERSION"
exit 0
