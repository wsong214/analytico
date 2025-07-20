#!/usr/bin/env python3
"""
Example usage of the new data pipeline for velocity cliff analysis.

This script demonstrates how to use the local data pipeline instead of pybaseball
for performing velocity cliff analysis on MLB pitchers.
"""

import sys
sys.path.append("utils")

from DataPipeline import DataPipeline
from VelocityCliffAnalyzer import VelocityCliffAnalyzer

def main():
    """Demonstrate the new data pipeline functionality."""
    print("=" * 60)
    print("VELOCITY CLIFF ANALYSIS - LOCAL DATA PIPELINE")
    print("=" * 60)
    
    # Initialize data pipeline
    print("1. Initializing data pipeline...")
    data_pipeline = DataPipeline()
    
    # Get data info
    data_info = data_pipeline.get_data_info()
    print(f"   ✓ Found {len(data_info['available_years'])} years of data")
    print(f"   ✓ Total players: {data_info['total_players']:,}")
    print(f"   ✓ Total pitches: {data_info['total_pitches']:,}")
    
    # Find a player
    print("\n2. Finding Jack Flaherty...")
    player_id = data_pipeline.find_player_by_name('Jack', 'Flaherty')
    if player_id:
        print(f"   ✓ Found Jack Flaherty (ID: {player_id})")
    else:
        print("   ✗ Could not find Jack Flaherty")
        return
    
    # Get player data
    print("\n3. Retrieving player data...")
    player_data = data_pipeline.get_player_data(player_id, 2024, 2024)
    print(f"   ✓ Retrieved {len(player_data)} pitches")
    
    # Get pitch summary
    print("\n4. Generating pitch summary...")
    summary = data_pipeline.get_pitch_summary(player_data)
    print("   Pitch type summary:")
    for pitch_type in summary.index:
        count = summary.loc[pitch_type, 'release_speed_count']
        avg_velo = summary.loc[pitch_type, 'release_speed_mean']
        avg_woba = summary.loc[pitch_type, 'estimated_woba_using_speedangle_mean']
        print(f"     {pitch_type}: {count} pitches, {avg_velo:.1f} mph, {avg_woba:.3f} wOBA")
    
    # Initialize analyzer
    print("\n5. Initializing velocity cliff analyzer...")
    analyzer = VelocityCliffAnalyzer(data_pipeline)
    
    # Prepare fastball data for analysis
    print("\n6. Preparing fastball data for analysis...")
    fastball_data = data_pipeline.prepare_velocity_analysis_data(player_data, 'FF')
    print(f"   ✓ Prepared {len(fastball_data)} fastball pitches for analysis")
    
    # Perform CUSUM analysis
    print("\n7. Performing CUSUM analysis...")
    cusum_threshold = analyzer.perform_cusum_analysis(fastball_data, "Jack Flaherty")
    print(f"   ✓ CUSUM threshold: {cusum_threshold:.1f} mph")
    
    # Perform Bayesian changepoint analysis
    print("\n8. Performing Bayesian changepoint analysis...")
    bayesian_threshold = analyzer.perform_bayesian_changepoint_analysis(fastball_data, "Jack Flaherty")
    print(f"   ✓ Bayesian threshold: {bayesian_threshold:.1f} mph")
    
    # Summary
    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    print(f"Player: Jack Flaherty")
    print(f"Year: 2024")
    print(f"Total Pitches: {len(player_data)}")
    print(f"Fastball Pitches: {len(fastball_data)}")
    print(f"CUSUM Threshold: {cusum_threshold:.1f} mph")
    print(f"Bayesian Threshold: {bayesian_threshold:.1f} mph")
    print(f"Average Threshold: {(cusum_threshold + bayesian_threshold) / 2:.1f} mph")
    print("=" * 60)
    
    print("\nInterpretation:")
    print(f"When Jack Flaherty's fastball velocity drops below approximately {min(cusum_threshold, bayesian_threshold):.1f} mph,")
    print("his expected wOBA against increases significantly, indicating a performance decline.")
    print("This is his 'velocity cliff' - the point where he starts to struggle.")
    
    print("\n" + "=" * 60)
    print("ADVANTAGES OF LOCAL DATA PIPELINE")
    print("=" * 60)
    print("✓ No API dependencies or rate limits")
    print("✓ Faster execution (no network calls)")
    print("✓ Consistent data structure")
    print("✓ Reproducible results")
    print("✓ Works offline")
    print("✓ No pybaseball required")
    print("=" * 60)

if __name__ == "__main__":
    main() 