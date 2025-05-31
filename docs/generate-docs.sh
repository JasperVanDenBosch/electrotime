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

FIRMWARE_DIR="$PROJECT_ROOT/firmware"

# Clean existing firmware docs
echo "  - Cleaning existing firmware documentation..."
rm -rf "$DOCS_DIR/firmware"
mkdir -p "$DOCS_DIR/firmware"

# Temporarily rename .cargo/config.toml to avoid AVR target issues
if [ -f "$FIRMWARE_DIR/.cargo/config.toml" ]; then
    echo "  - Temporarily disabling AVR configuration..."
    mv "$FIRMWARE_DIR/.cargo/config.toml" "$FIRMWARE_DIR/.cargo/config.toml.bak"
fi

# Build documentation for each crate individually
for crate in latreclib recorder simulator; do
    if [ -d "$FIRMWARE_DIR/$crate" ]; then
        echo ""
        echo "  📚 Building docs for $crate..."
        cd "$FIRMWARE_DIR/$crate"
        
        # Create a temp directory for this crate
        TEMP_DIR="$DOCS_DIR/firmware/temp_$crate"
        
        if [ "$crate" = "latreclib" ]; then
            # latreclib should build normally
            if cargo doc --no-deps --target-dir "$TEMP_DIR" 2>/dev/null; then
                echo "  ✅ $crate docs generated successfully"
                # Move the docs to the main firmware directory
                if [ -d "$TEMP_DIR/doc/$crate" ]; then
                    cp -r "$TEMP_DIR/doc/$crate" "$DOCS_DIR/firmware/"
                fi
                # Copy any additional dependencies that were documented
                if [ -d "$TEMP_DIR/doc" ]; then
                    cp -r "$TEMP_DIR/doc/"* "$DOCS_DIR/firmware/" 2>/dev/null || true
                fi
            else
                echo "  ❌ Failed to build $crate docs"
            fi
        else
            # For recorder and simulator, try the special AVR docs script if it exists
            if [ -f "$FIRMWARE_DIR/build-avr-docs.sh" ]; then
                echo "  - Using build-avr-docs.sh for $crate..."
                cd "$FIRMWARE_DIR"
                ./build-avr-docs.sh "$crate" "$TEMP_DIR" 2>/dev/null || {
                    echo "  ⚠️  AVR docs build failed, trying standard cargo doc..."
                    cd "$FIRMWARE_DIR/$crate"
                    cargo doc --no-deps --target-dir "$TEMP_DIR" 2>/dev/null || echo "  ⚠️  $crate docs failed (AVR target issue)"
                }
            else
                # Try standard cargo doc
                cargo doc --no-deps --target-dir "$TEMP_DIR" 2>/dev/null || echo "  ⚠️  $crate docs failed (likely AVR target issue)"
            fi
            
            # Copy generated docs if they exist
            if [ -d "$TEMP_DIR/doc/$crate" ]; then
                echo "  - Copying $crate documentation..."
                cp -r "$TEMP_DIR/doc/$crate" "$DOCS_DIR/firmware/"
            fi
        fi
        
        # Clean up temp directory
        rm -rf "$TEMP_DIR"
    fi
done

# Restore .cargo/config.toml if it was renamed
if [ -f "$FIRMWARE_DIR/.cargo/config.toml.bak" ]; then
    echo "  - Restoring AVR configuration..."
    mv "$FIRMWARE_DIR/.cargo/config.toml.bak" "$FIRMWARE_DIR/.cargo/config.toml"
fi

# Create an index page for firmware docs
echo ""
echo "  - Creating firmware documentation index..."
cat > "$DOCS_DIR/firmware/index.html" << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Rust Firmware Documentation</title>
    <meta charset="utf-8">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            max-width: 900px; 
            margin: 0 auto; 
            padding: 40px 20px;
            background-color: #f5f5f5;
        }
        h1 { 
            color: #333; 
            border-bottom: 2px solid #ddd;
            padding-bottom: 10px;
        }
        .crate { 
            margin: 20px 0; 
            padding: 25px; 
            background: white;
            border: 1px solid #ddd; 
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: box-shadow 0.3s ease;
        }
        .crate:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .crate h2 { 
            margin-top: 0;
            color: #2c3e50;
        }
        .crate p {
            color: #555;
            line-height: 1.6;
        }
        a { 
            color: #0066cc; 
            text-decoration: none;
            font-weight: 500;
        }
        a:hover { 
            text-decoration: underline; 
        }
        .status {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }
        .status.available {
            background-color: #d4edda;
            color: #155724;
        }
        .status.unavailable {
            background-color: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <h1>🦀 Latency Recorder Firmware Documentation</h1>
    
    <div class="crate">
        <h2>📚 latreclib
EOF

# Check if latreclib docs exist
if [ -d "$DOCS_DIR/firmware/latreclib" ]; then
    echo '            <span class="status available">Available</span>' >> "$DOCS_DIR/firmware/index.html"
else
    echo '            <span class="status unavailable">Not Available</span>' >> "$DOCS_DIR/firmware/index.html"
fi

cat >> "$DOCS_DIR/firmware/index.html" << 'EOF'
        </h2>
        <p>Core library providing helper functions and abstractions for the latency recorder hardware. This includes timing utilities, ADC handling, and serial communication abstractions.</p>
EOF

if [ -d "$DOCS_DIR/firmware/latreclib" ]; then
    echo '        <p><a href="./latreclib/index.html">View Documentation →</a></p>' >> "$DOCS_DIR/firmware/index.html"
else
    echo '        <p><em>Documentation not available - run cargo doc in the latreclib directory</em></p>' >> "$DOCS_DIR/firmware/index.html"
fi

cat >> "$DOCS_DIR/firmware/index.html" << 'EOF'
    </div>
    
    <div class="crate">
        <h2>🎯 recorder
EOF

# Check if recorder docs exist
if [ -d "$DOCS_DIR/firmware/recorder" ]; then
    echo '            <span class="status available">Available</span>' >> "$DOCS_DIR/firmware/index.html"
else
    echo '            <span class="status unavailable">Not Available</span>' >> "$DOCS_DIR/firmware/index.html"
fi

cat >> "$DOCS_DIR/firmware/index.html" << 'EOF'
        </h2>
        <p>Main firmware application that runs on the Arduino hardware. This is the embedded application that handles real-time latency measurements and communicates with the GUI.</p>
EOF

if [ -d "$DOCS_DIR/firmware/recorder" ]; then
    echo '        <p><a href="./recorder/index.html">View Documentation →</a></p>' >> "$DOCS_DIR/firmware/index.html"
else
    echo '        <p><em>Documentation not available - AVR target required for building</em></p>' >> "$DOCS_DIR/firmware/index.html"
fi

cat >> "$DOCS_DIR/firmware/index.html" << 'EOF'
    </div>
    
    <div class="crate">
        <h2>🔧 simulator
EOF

# Check if simulator docs exist
if [ -d "$DOCS_DIR/firmware/simulator" ]; then
    echo '            <span class="status available">Available</span>' >> "$DOCS_DIR/firmware/index.html"
else
    echo '            <span class="status unavailable">Not Available</span>' >> "$DOCS_DIR/firmware/index.html"
fi

cat >> "$DOCS_DIR/firmware/index.html" << 'EOF'
        </h2>
        <p>Hardware simulator for testing firmware logic without physical Arduino. Useful for development and testing of timing algorithms.</p>
EOF

if [ -d "$DOCS_DIR/firmware/simulator" ]; then
    echo '        <p><a href="./simulator/index.html">View Documentation →</a></p>' >> "$DOCS_DIR/firmware/index.html"
else
    echo '        <p><em>Documentation not available - AVR target required for building</em></p>' >> "$DOCS_DIR/firmware/index.html"
fi

cat >> "$DOCS_DIR/firmware/index.html" << 'EOF'
    </div>
</body>
</html>
EOF

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

# Fix Flutter/Dart documentation base paths and internal links
echo ""
echo "🔧 Fixing Flutter/Dart documentation base paths and internal links..."
if [ -d "$DOCS_DIR/gui" ]; then
    # Update base-href in all HTML files to use relative paths
    find "$DOCS_DIR/gui" -name "*.html" -type f -exec sed -i '' 's|data-base-href=""|data-base-href="."|g' {} \; 2>/dev/null || true
    find "$DOCS_DIR/gui" -name "*.html" -type f -exec sed -i '' 's|<base href="/">|<base href=".">|g' {} \; 2>/dev/null || true
    
    # Fix internal library links to use absolute paths from the docs-api root
    echo "  - Fixing internal library links..."
    
    # Process all HTML files to fix relative links
    find "$DOCS_DIR/gui" -name "*.html" -type f | while read -r file; do
        # Get the depth of the current file relative to gui directory
        depth=$(echo "$file" | sed "s|$DOCS_DIR/gui/||" | tr -cd '/' | wc -c)
        
        # Fix library links based on the file location
        if [ "$depth" -eq 0 ]; then
            # Root level files (like index.html)
            sed -i '' 's|href="about/"|href="/docs-api/gui/about/"|g' "$file"
            sed -i '' 's|href="device/"|href="/docs-api/gui/device/"|g' "$file"
            sed -i '' 's|href="home/"|href="/docs-api/gui/home/"|g' "$file"
            sed -i '' 's|href="main/"|href="/docs-api/gui/main/"|g' "$file"
            sed -i '' 's|href="ports/"|href="/docs-api/gui/ports/"|g' "$file"
            sed -i '' 's|href="recordbutton/"|href="/docs-api/gui/recordbutton/"|g' "$file"
        elif [ "$depth" -eq 1 ]; then
            # One level deep (library directories)
            sed -i '' 's|href="../about/"|href="/docs-api/gui/about/"|g' "$file"
            sed -i '' 's|href="../device/"|href="/docs-api/gui/device/"|g' "$file"
            sed -i '' 's|href="../home/"|href="/docs-api/gui/home/"|g' "$file"
            sed -i '' 's|href="../main/"|href="/docs-api/gui/main/"|g' "$file"
            sed -i '' 's|href="../ports/"|href="/docs-api/gui/ports/"|g' "$file"
            sed -i '' 's|href="../recordbutton/"|href="/docs-api/gui/recordbutton/"|g' "$file"
            sed -i '' 's|href="../index.html"|href="/docs-api/gui/index.html"|g' "$file"
        elif [ "$depth" -eq 2 ]; then
            # Two levels deep
            sed -i '' 's|href="../../about/"|href="/docs-api/gui/about/"|g' "$file"
            sed -i '' 's|href="../../device/"|href="/docs-api/gui/device/"|g' "$file"
            sed -i '' 's|href="../../home/"|href="/docs-api/gui/home/"|g' "$file"
            sed -i '' 's|href="../../main/"|href="/docs-api/gui/main/"|g' "$file"
            sed -i '' 's|href="../../ports/"|href="/docs-api/gui/ports/"|g' "$file"
            sed -i '' 's|href="../../recordbutton/"|href="/docs-api/gui/recordbutton/"|g' "$file"
            sed -i '' 's|href="../../index.html"|href="/docs-api/gui/index.html"|g' "$file"
        fi
        
        # Fix search.html links
        sed -i '' 's|href="search.html"|href="/docs-api/gui/search.html"|g' "$file"
        sed -i '' 's|href="../search.html"|href="/docs-api/gui/search.html"|g' "$file"
        sed -i '' 's|href="../../search.html"|href="/docs-api/gui/search.html"|g' "$file"
    done
    
    echo "  ✅ Flutter docs base paths and internal links updated"
fi

# Summary
echo ""
echo "✨ Documentation generation complete!"
echo ""
echo "Generated documentation locations:"
if [ -f "$DOCS_DIR/firmware/index.html" ]; then
    echo "  - Rust firmware index: $DOCS_DIR/firmware/index.html"
    [ -d "$DOCS_DIR/firmware/latreclib" ] && echo "    - latreclib: $DOCS_DIR/firmware/latreclib/index.html"
    [ -d "$DOCS_DIR/firmware/recorder" ] && echo "    - recorder: $DOCS_DIR/firmware/recorder/index.html"
    [ -d "$DOCS_DIR/firmware/simulator" ] && echo "    - simulator: $DOCS_DIR/firmware/simulator/index.html"
fi
[ -d "$DOCS_DIR/gui" ] && echo "  - Flutter/Dart: $DOCS_DIR/gui/index.html"
echo ""
echo "To serve the documentation locally, run:"
echo "  cd $SCRIPT_DIR && npm run dev"