#!/usr/bin/env python3
"""
Launcher script for the Velocity Cliff Analysis Streamlit app.
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app."""
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Set environment variables for better performance
    os.environ["STREAMLIT_SERVER_PORT"] = "8501"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "localhost"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    print("🚀 Starting Velocity Cliff Analysis Streamlit App...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("-" * 50)
    
    # Run the streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    main() 