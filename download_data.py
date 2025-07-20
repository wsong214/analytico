#!/usr/bin/env python3
"""
Data Download Helper Script

This script helps users download the required data files for the Velocity Cliff Analysis app.
"""

import os
import sys
import requests
import zipfile
from pathlib import Path

def main():
    """Main function to guide users through data download."""
    
    print("⚾ Velocity Cliff Analysis - Data Download Helper")
    print("=" * 50)
    
    # Check if data directory exists
    data_dir = Path("data")
    if not data_dir.exists():
        print("📁 Creating data directory structure...")
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "savant" / "season_data").mkdir(parents=True, exist_ok=True)
        print("✅ Data directory created")
    
    print("\n📋 Required Data Files:")
    print("1. player_meta.feather (9.7MB) - Player metadata")
    print("2. YYYY.feather files (~160MB each) - Statcast data by year")
    print("   - 2024.feather")
    print("   - 2023.feather")
    print("   - 2022.feather")
    print("   - etc. (2015-2024)")
    
    print("\n🔍 Current Status:")
    check_data_files()
    
    print("\n📥 Download Options:")
    print("1. Manual download (recommended for large files)")
    print("2. Use pybaseball to fetch data (requires internet)")
    print("3. Demo mode (no download required)")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        manual_download_guide()
    elif choice == "2":
        pybaseball_download()
    elif choice == "3":
        demo_mode_info()
    else:
        print("❌ Invalid choice")

def check_data_files():
    """Check which data files are present."""
    
    data_dir = Path("data")
    
    # Check player metadata
    player_meta = data_dir / "player_meta.feather"
    if player_meta.exists():
        size_mb = player_meta.stat().st_size / (1024 * 1024)
        print(f"✅ player_meta.feather ({size_mb:.1f}MB)")
    else:
        print("❌ player_meta.feather (missing)")
    
    # Check season data
    season_dir = data_dir / "savant" / "season_data"
    if season_dir.exists():
        feather_files = list(season_dir.glob("*.feather"))
        if feather_files:
            print(f"✅ Season data: {len(feather_files)} files found")
            for file in sorted(feather_files):
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"   - {file.name} ({size_mb:.1f}MB)")
        else:
            print("❌ No season data files found")
    else:
        print("❌ Season data directory missing")

def manual_download_guide():
    """Provide manual download instructions."""
    
    print("\n📥 Manual Download Instructions:")
    print("=" * 40)
    
    print("\n1. **Player Metadata** (player_meta.feather):")
    print("   - Source: MLB player database")
    print("   - Size: ~9.7MB")
    print("   - Place in: data/player_meta.feather")
    
    print("\n2. **Season Data Files** (YYYY.feather):")
    print("   - Source: MLB Statcast data")
    print("   - Size: ~160MB per year")
    print("   - Place in: data/savant/season_data/")
    print("   - Files needed: 2015.feather through 2024.feather")
    
    print("\n3. **Data Sources:**")
    print("   - MLB Statcast: https://baseballsavant.mlb.com/")
    print("   - Baseball Reference: https://www.baseball-reference.com/")
    print("   - Fangraphs: https://www.fangraphs.com/")
    
    print("\n4. **Alternative: Use pybaseball**")
    print("   - Install: pip install pybaseball")
    print("   - Run: python -c \"from pybaseball import statcast; statcast('2024-01-01', '2024-12-31')\"")
    
    print("\n5. **Verify Installation:**")
    print("   - Run: python test_data_pipeline.py")
    print("   - Or: python velocliff/velo_cliff_local.py --player 'Jack Flaherty'")

def pybaseball_download():
    """Guide users through pybaseball download."""
    
    print("\n🐍 Pybaseball Download Guide:")
    print("=" * 35)
    
    print("\n1. **Install pybaseball:**")
    print("   pip install pybaseball")
    
    print("\n2. **Create download script:**")
    print("   Create a file called 'fetch_data.py' with:")
    
    script_content = '''
import pandas as pd
from pybaseball import statcast, playerid_lookup
import os

# Create directories
os.makedirs("data/savant/season_data", exist_ok=True)

# Download player metadata (example)
print("Downloading player metadata...")
# Note: You'll need to create this from playerid_lookup data
# This is a simplified example

# Download season data
years = [2024, 2023, 2022, 2021, 2020]
for year in years:
    print(f"Downloading {year} data...")
    try:
        data = statcast(f'{year}-01-01', f'{year}-12-31')
        data.to_feather(f'data/savant/season_data/{year}.feather')
        print(f"✅ {year} data saved")
    except Exception as e:
        print(f"❌ Error downloading {year}: {e}")

print("Download complete!")
'''
    
    print(script_content)
    
    print("\n3. **Run the script:**")
    print("   python fetch_data.py")
    
    print("\n⚠️  **Note:** This may take a while and requires internet connection.")
    print("   The pybaseball API has rate limits, so be patient.")

def demo_mode_info():
    """Provide information about demo mode."""
    
    print("\n🎮 Demo Mode Information:")
    print("=" * 30)
    
    print("\n✅ **Demo Mode Available:**")
    print("   - No data files required")
    print("   - Sample results for popular pitchers")
    print("   - Full interface functionality")
    print("   - Perfect for testing and demonstration")
    
    print("\n🚀 **To run demo mode:**")
    print("   streamlit run streamlit_app.py")
    print("   Then click 'Launch Demo Mode' when prompted")
    
    print("\n📊 **Demo includes:**")
    print("   - Jack Flaherty, Gerrit Cole, Max Fried")
    print("   - Zack Wheeler, Jacob deGrom, Corbin Burnes")
    print("   - Sample velocity thresholds and analysis")
    
    print("\n💡 **Demo limitations:**")
    print("   - Pre-generated sample data only")
    print("   - Cannot analyze custom players")
    print("   - Limited to specific years and pitch types")

if __name__ == "__main__":
    main() 