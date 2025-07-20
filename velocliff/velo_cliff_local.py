#!/usr/bin/env python3
"""
VeloCliff Analysis - Local Data Pipeline Version

This script performs velocity cliff analysis using local feather data files
instead of relying on pybaseball API calls. It analyzes MLB pitcher performance
thresholds, focusing on metrics like xwOBA to pinpoint when pitchers start to
struggle as their velocity decreases.

Usage:
    python velo_cliff_local.py --player "Jack Flaherty" --year 2024
    python velo_cliff_local.py --player "Jacob deGrom" --start-year 2022 --end-year 2024
"""

import sys
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Optional, Tuple

# Add utils to path - handle both running from root and from velocliff directory
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(script_dir) == 'velocliff':
    # Script is in velocliff directory, add utils from parent
    sys.path.append(os.path.join(script_dir, "..", "utils"))
else:
    # Script is in root directory, add utils directly
    sys.path.append("utils")

from DataPipeline import DataPipeline
from VelocityCliffAnalyzer import VelocityCliffAnalyzer

def main():
    """Main function to run velocity cliff analysis."""
    parser = argparse.ArgumentParser(description='Velocity Cliff Analysis')
    parser.add_argument('--player', required=True, help='Player name (e.g., "Jack Flaherty")')
    parser.add_argument('--start-year', type=int, default=2024, help='Starting year (default: 2024)')
    parser.add_argument('--end-year', type=int, default=2024, help='Ending year (default: 2024)')
    parser.add_argument('--pitch-type', default='FF', help='Pitch type to analyze (default: FF)')
    parser.add_argument('--plots', action='store_true', help='Generate and display plots (default: False)')
    
    args = parser.parse_args()
    
    try:
        # Initialize data pipeline
        data_pipeline = DataPipeline()
        
        # Initialize analyzer
        analyzer = VelocityCliffAnalyzer(data_pipeline)
        
        # Run analysis
        results = analyzer.run_full_analysis(
            args.player, args.start_year, args.end_year, args.pitch_type, generate_plots=args.plots
        )
        
        # Print results
        if 'error' not in results:
            print("\n" + "="*50)
            print("VELOCITY CLIFF ANALYSIS RESULTS")
            print("="*50)
            print(f"Player: {results['player_name']}")
            print(f"Years: {results['years']}")
            print(f"Total Pitches: {results['total_pitches']}")
            print(f"Fastball Pitches: {results['fastball_pitches']}")
            print(f"CUSUM Threshold: {results['cusum_threshold']:.1f} mph")
            print(f"Bayesian Threshold: {results['bayesian_threshold']:.1f} mph")
            print(f"Average Threshold: {results['average_threshold']:.1f} mph")
            print("="*50)
        else:
            print(f"Error: {results['error']}")
            
    except Exception as e:
        print(f"Error running analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 