#!/bin/bash

# Test script to verify version endpoints are working
# Run this after starting the backend server

echo "🧪 Testing Data Contracts Studio Version Endpoints"
echo "================================================"

API_URL="http://localhost:8000"

echo "1. Testing main version endpoint..."
echo "GET $API_URL/version"
curl -s "$API_URL/version" | python3 -m json.tool || echo "❌ Version endpoint failed"

echo -e "\n2. Testing API v1 version endpoint..."
echo "GET $API_URL/api/v1/version"
curl -s "$API_URL/api/v1/version" | python3 -m json.tool || echo "❌ API version endpoint failed"

echo -e "\n3. Testing health endpoint..."
echo "GET $API_URL/health"
curl -s "$API_URL/health" | python3 -m json.tool || echo "❌ Health endpoint failed"

echo -e "\n✅ Version endpoint testing completed!"
echo -e "\nNote: Make sure the backend server is running with 'make backend-dev' or 'make dev'"
