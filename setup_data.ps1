#!/usr/bin/env pwsh

Write-Host "Setting up MoMA dataset..." -ForegroundColor Green

# Create data directory if it doesn't exist
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}

# Add MoMA collection as submodule
if (-not (Test-Path "data/moma-collection/.git")) {
    git submodule add https://github.com/MuseumofModernArt/collection data/moma-collection
    Write-Host "[OK] Submodule added" -ForegroundColor Green
} else {
    Write-Host "[OK] Submodule already exists" -ForegroundColor Yellow
}

# Initialize and update submodule
git submodule update --init --recursive

Write-Host "[OK] Setup complete! You can now run the notebooks." -ForegroundColor Green
