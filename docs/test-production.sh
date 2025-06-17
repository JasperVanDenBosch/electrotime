#!/bin/bash

# Script to test the production build locally with the correct base path

echo "🔨 Building the production site..."
npm run build

echo ""
echo "🚀 Starting local server..."
echo "Note: The site will be served at http://localhost:8080/latency-recorder/"
echo ""

# Use npx serve with the correct base path
npx serve out -p 8080 --no-port-switching &
SERVER_PID=$!

# Wait for server to start
sleep 2

echo "✨ Server started!"
echo ""
echo "📍 Visit: http://localhost:8080/latency-recorder/"
echo ""
echo "Press Ctrl+C to stop the server"

# Wait for user to stop
wait $SERVER_PID