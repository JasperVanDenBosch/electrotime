#!/bin/bash

# Script to copy README.md to docs/content/repo/index.md with front matter

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define source and destination paths
SOURCE_FILE="$SCRIPT_DIR/../README.md"
DEST_FILE="$SCRIPT_DIR/content/repo/index.md"

# Front matter to prepend
FRONT_MATTER='+++
title = "Repo"
description = "Main repository documentation and quick start guide"
SequenceNumber = 1
+++

'

# Check if source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: README.md not found at $SOURCE_FILE"
    exit 1
fi

# Create destination directory if it doesn't exist
mkdir -p "$(dirname "$DEST_FILE")"

# Copy README.md with front matter
echo "$FRONT_MATTER" > "$DEST_FILE"
cat "$SOURCE_FILE" >> "$DEST_FILE"

echo "Successfully copied README.md to $DEST_FILE"