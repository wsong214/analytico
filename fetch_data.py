#!/usr/bin/env python3
"""
Practical Data Download Script

This script downloads the required data files for the Velocity Cliff Analysis app
using pybaseball. It creates the proper directory structure and downloads
both player metadata and season data.
"""

import pandas as pd
import os
import sys
from pathlib import Path
import time

def main():
    """Download data files using pybaseball."""
    
    print("⚾ Velocity Cliff Analysis - Data Download")
    print("=" * 50)
    
    # Check if pybaseball is installed
    try:
        from pybaseball import statcast, playerid_lookup
        print("✅ pybaseball is installed")
    except ImportError:
        print("❌ pybaseball not found. Installing...")
        os.system("pip install pybaseball")
        try:
            from pybaseball import statcast, playerid_lookup
            print("✅ pybaseball installed successfully")
        except ImportError:
            print("❌ Failed to install pybaseball")
            return
    
    # Create directories
    print("\n📁 Creating directory structure...")
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    season_dir = data_dir / "savant" / "season_data"
    season_dir.mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")
    
    # Download player metadata
    print("\n👥 Downloading player metadata...")
    try:
        # Get all players from recent years to build metadata
        all_players = []
        for year in [2024, 2023, 2022]:
            print(f"  Fetching {year} player data...")
            try:
                players = playerid_lookup('', '')  # Get all players
                if not players.empty:
                    players['year'] = year
                    all_players.append(players)
                time.sleep(1)  # Rate limiting
            except Exception as e:
                print(f"  Warning: Could not fetch {year} players: {e}")
        
        if all_players:
            player_meta = pd.concat(all_players, ignore_index=True)
            player_meta = player_meta.drop_duplicates(subset=['key_mlbam']).reset_index(drop=True)
            
            # Save player metadata
            player_meta.to_feather(data_dir / "player_meta.feather")
            print(f"✅ Player metadata saved ({len(player_meta)} players)")
        else:
            print("❌ Could not download player metadata")
            return
            
    except Exception as e:
        print(f"❌ Error downloading player metadata: {e}")
        return
    
    # Download season data
    print("\n📊 Downloading season data...")
    years = [2024, 2023, 2022]  # Start with recent years
    
    for year in years:
        print(f"\n📅 Downloading {year} data...")
        try:
            # Download full season data
            data = statcast(f'{year}-01-01', f'{year}-12-31')
            
            if not data.empty:
                # Save to feather format
                output_file = season_dir / f"{year}.feather"
                data.to_feather(output_file)
                
                size_mb = output_file.stat().st_size / (1024 * 1024)
                print(f"✅ {year} data saved ({len(data):,} pitches, {size_mb:.1f}MB)")
            else:
                print(f"⚠️  No data found for {year}")
                
        except Exception as e:
            print(f"❌ Error downloading {year}: {e}")
        
        # Rate limiting
        if year != years[-1]:  # Don't sleep after last year
            print("  Waiting 5 seconds for rate limiting...")
            time.sleep(5)
    
    print("\n🎉 Download complete!")
    print("\n📋 Summary:")
    
    # Check what was downloaded
    check_downloaded_files()
    
    print("\n🚀 You can now run the Streamlit app:")
    print("   streamlit run streamlit_app.py")

def check_downloaded_files():
    """Check what files were successfully downloaded."""
    
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
            print(f"✅ Season data: {len(feather_files)} files")
            total_size = sum(f.stat().st_size for f in feather_files) / (1024 * 1024)
            print(f"   Total size: {total_size:.1f}MB")
            for file in sorted(feather_files):
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"   - {file.name} ({size_mb:.1f}MB)")
        else:
            print("❌ No season data files found")

if __name__ == "__main__":
    main() 