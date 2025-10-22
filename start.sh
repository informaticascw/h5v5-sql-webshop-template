#!/bin/bash


echo "🔁 Stopping old server..."

# Stop old server if it is running
pkill -f "python app/main.py" 2>/dev/null

# Wait until the process has stopped
while pgrep -f "python app/main.py" > /dev/null; do
    echo "⏳ Waiting for old server to stop..."
    sleep 1
done

echo "✅ Old server stopped"

echo "📦 Initializing database..."

# Remove the old database file if it exists
rm -f data/products.db

# (Re)create database from init.sql
sqlite3 data/products.db < data/init.sql

echo "✅ Database ready"

# 🧪 Check if FastAPI is installed
echo "🔍 Checking for FastAPI..."
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "⚠️ FastAPI is not installed. Please install it with: pip install fastapi"
    exit 1
else
    echo "✅ FastAPI is installed."
fi

echo "🚀 Starting FastAPI backend (using python)..."

# Start FastAPI server using python, requires uvicorn.run() in main.py
python app/main.py
