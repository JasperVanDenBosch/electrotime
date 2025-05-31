#!/bin/bash

# Test script to verify all documentation routes work correctly
set -e

echo "🧪 Testing documentation routes..."

# Start the server
echo "Starting server..."
npx serve out -p 3001 --no-port-switching &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to test a route
test_route() {
    local route=$1
    local description=$2
    
    if curl -f -s -o /dev/null "http://localhost:3001${route}"; then
        echo -e "${GREEN}✅ ${description}${NC} - ${route}"
    else
        echo -e "${RED}❌ ${description}${NC} - ${route}"
        FAILED=true
    fi
}

# Function to test iframe content
test_iframe() {
    local route=$1
    local description=$2
    
    # Test if the page loads and contains iframe
    if curl -s "http://localhost:3001${route}" | grep -q "iframe"; then
        echo -e "${GREEN}✅ ${description}${NC} - ${route} (iframe present)"
    else
        echo -e "${RED}❌ ${description}${NC} - ${route} (iframe missing)"
        FAILED=true
    fi
}

FAILED=false

echo ""
echo "📄 Testing main pages..."
test_route "/" "Homepage"
test_route "/developers" "Developers Overview"
test_route "/hackathon" "Hackathon Overview"
test_route "/api-docs" "API Documentation Hub"

echo ""
echo "👨‍💻 Testing developer pages..."
test_route "/developers/hardware" "Hardware Development"
test_route "/developers/firmware" "GUI Development"
test_route "/developers/data-analytics" "Data Analytics"

echo ""
echo "🎯 Testing hackathon pages..."
test_route "/hackathon/hardware" "Hackathon Hardware"
test_route "/hackathon/firmware" "Hackathon Firmware"
test_route "/hackathon/user-interface" "User Interface"
test_route "/hackathon/data-analysis" "Data Analysis"
test_route "/hackathon/website-documentation" "Website Documentation"
test_route "/hackathon/misc" "Miscellaneous"
test_route "/hackathon/syrinx" "Syrinx"

echo ""
echo "📚 Testing API documentation routes..."
test_route "/docs-api/firmware/latreclib/index.html" "Rust API Docs"
test_route "/docs-api/gui/index.html" "Flutter API Docs"

echo ""
echo "🖼️ Testing API documentation viewers..."
test_iframe "/developers/hardware-api" "Hardware API Viewer"
test_iframe "/developers/gui-api" "GUI API Viewer"

echo ""
echo "🔍 Testing specific API endpoints..."
test_route "/docs-api/firmware/latreclib/fn.bools2num.html" "Rust function docs"
test_route "/docs-api/gui/main/main.html" "Flutter main docs"

# Kill the server
kill $SERVER_PID 2>/dev/null || true

echo ""
if [ "$FAILED" = true ]; then
    echo -e "${RED}❌ Some routes failed!${NC}"
    exit 1
else
    echo -e "${GREEN}✅ All routes tested successfully!${NC}"
fi