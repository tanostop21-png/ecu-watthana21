#!/usr/bin/env python
"""
Desktop application launcher
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from desktop.app import main

if __name__ == '__main__':
    main()
