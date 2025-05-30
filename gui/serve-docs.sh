#!/bin/bash

# Script to serve Flutter documentation locally

echo "🌐 Starting local Flutter documentation server..."

# Check if docs exist
if [ ! -d "doc/api" ]; then
    echo "❌ Documentation not found in doc/api/"
    echo "Please run 'dart doc' first to generate the documentation."
    exit 1
fi

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "📡 Starting server at http://localhost:8081"
    echo "Press Ctrl+C to stop the server"
    cd doc/api
    python3 -m http.server 8081
elif command -v python &> /dev/null; then
    echo "📡 Starting server at http://localhost:8081"
    echo "Press Ctrl+C to stop the server"
    cd doc/api
    python -m SimpleHTTPServer 8081
else
    echo "❌ Python not found. Please install Python to serve the documentation."
    echo ""
    echo "Alternatively, you can open doc/api/index.html directly in your browser."
    exit 1
fi