#!/bin/bash

echo "Setting up MoMA dataset..."

# Create data directory if it doesn't exist
mkdir -p data

# Add MoMA collection as submodule
if [ ! -d "data/moma-collection/.git" ]; then
    git submodule add https://github.com/MuseumofModernArt/collection data/moma-collection
    echo "✓ Submodule added"
else
    echo "✓ Submodule already exists"
fi

# Initialize and update submodule
git submodule update --init --recursive

echo "✓ Setup complete! You can now run the notebooks."
