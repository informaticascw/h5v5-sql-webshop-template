#!/bin/bash

#
# Stop API if running
#

echo "🔁 Stopping old server..."

# Stop old server if it is running
pkill -f "python app/main.py" 2>/dev/null

# Wait until the process has stopped
while pgrep -f "python app/main.py" > /dev/null; do
    echo "⏳ Waiting for old server to stop..."
    sleep 1
done

echo "✅ Old server stopped"

#
# Rebuild database
#

echo "📦 Initializing database..."

# Remove the old database file if it exists
rm -f data/products.db

# (Re)create database from init.sql
if ! sqlite3 data/products.db < data/init.sql; then
    echo "❌ Error creating database, check init.sql"
    exit 1
else
    echo "✅ Database ready"
fi

#
# Check if FastAPI is installed
#

# 🧪 Check if FastAPI is installed 
echo "🔍 Checking for FastAPI..."
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "❌ FastAPI is not installed. Please install it with: pip install fastapi"
    exit 1
else
    echo "✅ FastAPI is installed."
fi

#
# Start API
#

echo "🚀 Starting FastAPI backend (using python)..."

# Start FastAPI server using python, requires uvicorn.run() in main.py
python app/main.py
