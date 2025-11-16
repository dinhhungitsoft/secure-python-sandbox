#!/bin/bash

# Quick Test Runner Script
# Usage: ./quick_test.sh

echo "=========================================="
echo "Python Code Sandbox - Quick Test Runner"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install dependencies if needed
if ! python -c "import pytest" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo ""
echo "🧪 Running Unit Tests..."
echo "=========================================="
echo ""

# Run tests
python tests/run_tests.py

echo ""
echo "=========================================="
echo "✅ Testing complete!"
echo ""
echo "To run with pytest and coverage:"
echo "  pytest --cov=src --cov-report=html"
echo ""
echo "To view coverage report:"
echo "  open htmlcov/index.html"
echo "=========================================="
