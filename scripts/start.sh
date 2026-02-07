#!/bin/bash

echo "🎓 Starting ClassAI..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if dependencies are installed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "⚠️  Dependencies not installed. Installing..."
    pip3 install -r requirements.txt
fi

echo "✓ Dependencies installed"
echo ""

# Start backend server in background
echo "🚀 Starting backend server on port 8001..."
python3 main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend server
echo "🌐 Starting frontend server on port 3001..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ ClassAI is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Open your browser and go to:"
echo "   http://localhost:3001"
echo ""
echo "📚 API Documentation:"
echo "   http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start frontend server (this will block)
python3 -m http.server 3001

# Cleanup on exit
kill $BACKEND_PID 2>/dev/null
