#!/bin/bash

# Script to generate API documentation for the Latency Recorder project
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCS_DIR="$SCRIPT_DIR/public/docs-api"

echo "🚀 Starting documentation generation..."
echo "Project root: $PROJECT_ROOT"
echo "Docs output: $DOCS_DIR"

# Create docs directory if it doesn't exist
mkdir -p "$DOCS_DIR"

# Generate Rust documentation
echo ""
echo "📦 Generating Rust documentation..."

# Generate docs for latreclib
if [ -d "$PROJECT_ROOT/firmware/latreclib" ]; then
    echo "  - Building docs for latreclib..."
    cd "$PROJECT_ROOT/firmware/latreclib"
    cargo doc --no-deps --target-dir "$DOCS_DIR/firmware"
    echo "  ✅ latreclib docs generated"
else
    echo "  ⚠️  latreclib directory not found"
fi

# Generate docs for recorder (if AVR toolchain is available)
if [ -d "$PROJECT_ROOT/firmware/recorder" ]; then
    echo "  - Checking for AVR toolchain..."
    if command -v avr-gcc &> /dev/null; then
        echo "  - Building docs for recorder..."
        cd "$PROJECT_ROOT/firmware/recorder"
        cargo doc --no-deps --target-dir "$DOCS_DIR/firmware" 2>/dev/null || echo "  ⚠️  Recorder docs failed (AVR toolchain required)"
    else
        echo "  ⚠️  AVR toolchain not found, skipping recorder docs"
    fi
fi

# Generate docs for simulator
if [ -d "$PROJECT_ROOT/firmware/simulator" ]; then
    echo "  - Building docs for simulator..."
    cd "$PROJECT_ROOT/firmware/simulator"
    cargo doc --no-deps --target-dir "$DOCS_DIR/firmware" 2>/dev/null || echo "  ⚠️  Simulator docs failed"
fi

# Generate Flutter/Dart documentation
echo ""
echo "🎯 Generating Flutter/Dart documentation..."

if [ -d "$PROJECT_ROOT/gui" ]; then
    cd "$PROJECT_ROOT/gui"
    
    # Check if dart is available
    if command -v dart &> /dev/null; then
        echo "  - Running dart doc..."
        dart doc --output "$DOCS_DIR/gui" || echo "  ⚠️  Dart doc failed"
        echo "  ✅ Flutter/Dart docs generated"
    else
        echo "  ⚠️  Dart not found in PATH"
        
        # Try to find existing Flutter docs
        if [ -d "$PROJECT_ROOT/gui/doc/api" ]; then
            echo "  - Found existing Flutter docs, copying..."
            cp -r "$PROJECT_ROOT/gui/doc/api/"* "$DOCS_DIR/gui/"
            echo "  ✅ Existing Flutter docs copied"
        else
            echo "  ⚠️  No existing Flutter docs found"
        fi
    fi
else
    echo "  ⚠️  GUI directory not found"
fi

# Fix permissions
echo ""
echo "🔧 Setting permissions..."
chmod -R 755 "$DOCS_DIR"

# Create index files if missing
echo ""
echo "📝 Creating index files..."

# Create a simple index for firmware docs if it doesn't exist
if [ -d "$DOCS_DIR/firmware" ] && [ ! -f "$DOCS_DIR/firmware/index.html" ]; then
    cat > "$DOCS_DIR/firmware/index.html" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Rust Firmware Documentation</title>
    <meta http-equiv="refresh" content="0; url=./doc/latreclib/index.html">
</head>
<body>
    <p>Redirecting to <a href="./doc/latreclib/index.html">latreclib documentation</a>...</p>
</body>
</html>
EOF
fi

# Summary
echo ""
echo "✨ Documentation generation complete!"
echo ""
echo "Generated documentation locations:"
[ -d "$DOCS_DIR/firmware/doc/latreclib" ] && echo "  - Rust firmware: $DOCS_DIR/firmware/doc/latreclib/index.html"
[ -d "$DOCS_DIR/gui" ] && echo "  - Flutter/Dart: $DOCS_DIR/gui/index.html"
echo ""
echo "To serve the documentation locally, run:"
echo "  cd $SCRIPT_DIR && npm run dev"