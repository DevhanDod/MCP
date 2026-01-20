#!/bin/bash

echo "========================================"
echo "MCP - Menstrual Cycle Prediction"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Virtual environment found. Skipping installation..."
    source venv/bin/activate
fi

echo ""
echo "========================================"
echo "Starting Flask application..."
echo "========================================"
echo ""
echo "Open your browser and navigate to:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python app.py
