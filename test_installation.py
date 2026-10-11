#!/usr/bin/env python
"""
Quick test script to verify installation
"""
import sys
import requests
from pathlib import Path

print("="*50)
print("ECU-Watthana21 Installation Test")
print("="*50)
print()

# Test 1: Check dependencies
print("Test 1: Checking dependencies...")
try:
    import flask
    import flask_sqlalchemy
    import flask_jwt_extended
    import flask_bcrypt
    print("✓ Flask dependencies installed")
except ImportError as e:
    print(f"✗ Missing Flask dependency: {e}")
    sys.exit(1)

try:
    from PyQt6.QtWidgets import QApplication
    print("✓ PyQt6 installed")
except ImportError:
    print("⚠ PyQt6 not installed (optional for desktop app)")

print()

# Test 2: Check database
print("Test 2: Checking database...")
db_file = Path("ecu_watthana.db")
if db_file.exists():
    print(f"✓ Database file exists: {db_file}")
else:
    print("⚠ Database file not found. Run: python init_db.py")

print()

# Test 3: Check .env file
print("Test 3: Checking configuration...")
if Path(".env").exists():
    print("✓ .env file exists")
else:
    print("⚠ .env file not found. Run: cp .env.example .env")

print()
print("="*50)
print("Installation check complete!")
print("="*50)
print()
print("To start the application:")
print()
print("1. Start API server:")
print("   python run_server.py")
print()
print("2. In another terminal, start desktop app:")
print("   python run_desktop.py")
print()
print("Test login credentials:")
print("  Username: demo")
print("  Password: demo123456")
print()
