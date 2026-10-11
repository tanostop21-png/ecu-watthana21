#!/bin/bash
# Install script for ECU-Watthana21

echo "================================"
echo "ECU-Watthana21 Installation"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python --version || { echo "Python not found. Please install Python 3.8+"; exit 1; }

echo ""
echo "Creating virtual environment..."
python -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Copying environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file (edit if needed)"
fi

echo ""
echo "Initializing database..."
python init_db.py

echo ""
echo "================================"
echo "Installation Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start API server:"
echo "   python run_server.py"
echo ""
echo "3. In another terminal, start desktop app:"
echo "   python run_desktop.py"
echo ""
echo "Demo Credentials:"
echo "  Username: demo"
echo "  Password: demo123456"
echo ""
