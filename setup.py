#!/usr/bin/env python3
"""
Setup script for Analytico - Baseball Analytics Platform

This script helps new users set up the project environment and get started quickly.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Main setup function."""
    
    print("⚾ Analytico - Baseball Analytics Platform Setup")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {python_version.major}.{python_version.minor}")
        return
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return
    
    # Check if data files exist
    data_dir = Path("data")
    if data_dir.exists() and any((data_dir / "savant" / "season_data").glob("*.feather")):
        print("\n✅ Data files found - Full functionality available!")
        print("\n🚀 Quick Start:")
        print("   1. Run the web app: streamlit run streamlit_app.py")
        print("   2. Or use CLI: python velocliff/velo_cliff_local.py --player 'Jack Flaherty'")
    else:
        print("\n📊 No data files found - Demo mode available!")
        print("\n🎮 Demo Mode:")
        print("   1. Run: streamlit run streamlit_app.py")
        print("   2. Click 'Launch Demo Mode' when prompted")
        print("   3. Try analyzing sample pitchers")
        
        print("\n📥 To get full functionality:")
        print("   1. Run: python download_data.py")
        print("   2. Follow the instructions to download data files")
    
    print("\n📚 Documentation:")
    print("   - README.md: Complete project documentation")
    print("   - example_usage.py: Usage examples")
    print("   - velocliff/velo_cliff_local.py: Command-line interface")
    
    print("\n🎉 Setup complete! Enjoy analyzing baseball data!")

if __name__ == "__main__":
    main() 