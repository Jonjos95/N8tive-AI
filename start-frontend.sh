#!/bin/bash

# Start Frontend Server
echo "Starting N8tive AI Frontend..."
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
fi

# Start dev server
echo "Starting frontend server on http://localhost:5173"
npm run dev







