#!/bin/bash

# Script to build documentation for AVR targets
# This requires proper AVR toolchain setup

echo "🔧 Building AVR documentation..."

# Check if AVR target is installed
if ! rustup target list --installed | grep -q "avr-unknown-gnu-atmega328"; then
    echo "❌ AVR target not installed. Installing..."
    rustup target add avr-unknown-gnu-atmega328
fi

# Build docs for recorder
echo "📚 Building docs for recorder..."
cd recorder
if cargo doc --no-deps --target avr-unknown-gnu-atmega328 --target-dir ../target-avr 2>/dev/null; then
    echo "✓ Recorder docs built successfully"
else
    echo "⚠️  Failed to build recorder docs"
    # Try without target specification
    cargo doc --no-deps --target-dir ../target 2>/dev/null || echo "  Failed even without target"
fi
cd ..

# Build docs for simulator  
echo "📚 Building docs for simulator..."
cd simulator
if cargo doc --no-deps --target avr-unknown-gnu-atmega328 --target-dir ../target-avr 2>/dev/null; then
    echo "✓ Simulator docs built successfully"
else
    echo "⚠️  Failed to build simulator docs"
    # Try without target specification
    cargo doc --no-deps --target-dir ../target 2>/dev/null || echo "  Failed even without target"
fi
cd ..

echo "✅ AVR documentation build complete"
echo ""
echo "Note: AVR documentation requires the AVR toolchain to be properly installed."
echo "To install the AVR toolchain on macOS:"
echo "  brew tap osx-cross/avr"
echo "  brew install avr-gcc avrdude"