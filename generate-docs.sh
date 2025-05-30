#!/bin/bash

# Generate documentation for the latency-recorder project

set -e

echo "🚀 Starting documentation generation..."

# Create output directories
mkdir -p docs/public/docs-api/firmware
mkdir -p docs/public/docs-api/gui

# Generate Rust documentation
echo "📦 Generating Rust documentation..."
cd firmware

# Build docs for all packages in the workspace
echo "  Building docs for all firmware packages..."

# Try to build for each package, handling AVR target issues
for package in */Cargo.toml; do
    dir=$(dirname "$package")
    if [ -d "$dir" ]; then
        echo "  Building docs for $dir..."
        cd "$dir"
        
        # Try to build docs, but continue if it fails (e.g., AVR target issues)
        if cargo doc --no-deps --target-dir ../target 2>/dev/null; then
            echo "    ✓ Successfully built docs for $dir"
        else
            echo "    ⚠️  Failed to build docs for $dir (likely AVR target required)"
            # Try building with --all-features flag which might help
            cargo doc --no-deps --all-features --target-dir ../target 2>/dev/null || true
        fi
        
        cd ..
    fi
done

# Copy generated docs to public directory
echo "  Copying Rust docs..."
cp -r target/doc/* ../docs/public/docs-api/firmware/

cd ..

# Generate Flutter documentation
echo "🎯 Generating Flutter documentation..."
cd gui

# Check if docs already exist locally
if [ -d "doc/api" ]; then
    echo "  Found existing Flutter docs in gui/doc/api"
    echo "  Copying to public directory..."
    cp -r doc/api/* ../docs/public/docs-api/gui/
    echo "  ✓ Flutter docs copied successfully"
elif command -v dart &> /dev/null; then
    echo "  Running dart doc..."
    dart doc --output ../docs/public/docs-api/gui
else
    echo "  ⚠️  Dart not found and no local docs found. Skipping Flutter documentation."
fi

cd ..

# Create index pages for API documentation
echo "📝 Creating API index pages..."

# Create firmware API index
cat > docs/content/developers-hardware-api.md << 'EOF'
+++
Title = "Hardware API Reference"
Description = "Auto-generated API documentation for the firmware components"
SequenceNumber = 3
+++

# Hardware API Reference

This section contains auto-generated API documentation for the firmware components.

## Components

### latreclib
Core library providing helper functions and abstractions for the latency recorder.

[View Documentation →](/api/firmware/latreclib/index.html)

### recorder
Main firmware application that runs on the Arduino hardware.

[View Documentation →](/api/firmware/recorder/index.html)

### simulator
Hardware simulator for testing without physical Arduino.

[View Documentation →](/api/firmware/simulator/index.html)

## Building Documentation Locally

To regenerate the documentation:

```bash
cd firmware/latreclib
cargo doc --no-deps --open
```

EOF

# Create GUI API index
cat > docs/content/developers-firmware-api.md << 'EOF'
+++
Title = "GUI API Reference"
Description = "Auto-generated API documentation for the Flutter GUI"
SequenceNumber = 3
+++

# GUI API Reference

This section contains auto-generated API documentation for the Flutter GUI application.

[View Full Documentation →](/api/gui/index.html)

## Key Components

- **Device Management**: Classes for detecting and communicating with the hardware
- **Recording Interface**: UI components for starting/stopping recordings
- **Data Analysis**: Tools for analyzing recorded latency data
- **Port Management**: Serial port detection and configuration

## Building Documentation Locally

To regenerate the documentation:

```bash
cd gui
dart doc
```

EOF

echo "✅ Documentation generation complete!"
echo ""
echo "📂 Generated files:"
echo "  - Firmware docs: docs/public/docs-api/firmware/"
echo "  - GUI docs: docs/public/docs-api/gui/"
echo "  - Index pages created in docs/content/"
echo ""
echo "🌐 To view the docs in the website:"
echo "  cd docs && npm run dev"
echo ""
echo "📖 To view Flutter docs locally (without the website):"
echo "  cd gui && ./serve-docs.sh"
echo ""
echo "⚠️  Note: AVR packages (recorder, simulator) may require special setup."
echo "  To build AVR docs, run: cd firmware && ./build-avr-docs.sh"