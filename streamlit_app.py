#!/usr/bin/env python3
"""
Velocity Cliff Analysis - Streamlit App

A web interface for analyzing MLB pitcher velocity cliffs using local Statcast data.
"""

import streamlit as st
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Add utils to path
script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(script_dir) == 'velocliff':
    sys.path.append(os.path.join(script_dir, "..", "utils"))
else:
    sys.path.append("utils")

from DataPipeline import DataPipeline
from VelocityCliffAnalyzer import VelocityCliffAnalyzer

# Page configuration
st.set_page_config(
    page_title="Velocity Cliff Analysis",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .results-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit app function."""
    
    # Header
    st.markdown('<h1 class="main-header">⚾ Velocity Cliff Analysis</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.1rem; color: #666;'>
            Analyze MLB pitcher performance thresholds using Statcast data to identify when pitchers 
            start to struggle as their velocity decreases.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize data pipeline
    @st.cache_resource
    def load_data_pipeline():
        """Load and cache the data pipeline."""
        try:
            pipeline = DataPipeline()
            return pipeline, None
        except Exception as e:
            return None, str(e)
    
    data_pipeline, error = load_data_pipeline()
    
    # Handle missing data files
    if data_pipeline is None:
        show_missing_data_help(error)
        return
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎯 Analysis Parameters")
        
        # Player search
        st.subheader("Player Selection")
        player_name = st.text_input(
            "Enter Player Name",
            placeholder="e.g., Jack Flaherty, Gerrit Cole",
            help="Enter the full name of the pitcher you want to analyze"
        )
        
        # Year selection
        st.subheader("Year Range")
        available_years = data_pipeline.get_available_years()
        if available_years:
            start_year = st.selectbox(
                "Start Year",
                options=available_years,
                index=len(available_years) - 1  # Default to most recent year
            )
            
            end_year = st.selectbox(
                "End Year", 
                options=available_years,
                index=len(available_years) - 1  # Default to most recent year
            )
        else:
            st.error("No data years available")
            return
        
        # Pitch type selection
        st.subheader("Pitch Type")
        pitch_type = st.selectbox(
            "Select Pitch Type",
            options=['FF', 'SI', 'FC', 'SL', 'CT', 'CB', 'CH', 'KC', 'EP'],
            index=0,
            help="FF=Four-Seam Fastball, SI=Sinker, FC=Cutter, SL=Slider, CT=Cutter, CB=Curveball, CH=Changeup, KC=Knuckle Curve, EP=Eephus"
        )
        
        # Analysis options
        st.subheader("Analysis Options")
        generate_plots = st.checkbox(
            "Generate Visualizations",
            value=False,
            help="Enable to show velocity vs performance plots"
        )
        
        # Run analysis button
        st.markdown("---")
        run_analysis = st.button(
            "🚀 Run Analysis",
            type="primary",
            use_container_width=True
        )
    
    # Main content area
    if run_analysis and player_name:
        with st.spinner("Running velocity cliff analysis..."):
            try:
                # Initialize analyzer
                analyzer = VelocityCliffAnalyzer(data_pipeline)
                
                # Run analysis
                results = analyzer.run_full_analysis(
                    player_name, start_year, end_year, pitch_type, generate_plots
                )
                
                if 'error' in results:
                    st.error(f"Analysis failed: {results['error']}")
                    return
                
                # Display results
                display_results(results, player_name, pitch_type, generate_plots)
                
            except Exception as e:
                st.error(f"Error during analysis: {e}")
                st.exception(e)
    
    elif not player_name and run_analysis:
        st.warning("Please enter a player name to run the analysis.")
    
    # Show example usage
    else:
        show_example_usage(data_pipeline)

def display_results(results, player_name, pitch_type, generate_plots):
    """Display analysis results in a formatted way."""
    
    st.markdown('<div class="results-section">', unsafe_allow_html=True)
    st.header(f"📊 Analysis Results: {player_name}")
    
    # Create three columns for key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Velocity Threshold</h3>
            <h2 style="color: #1f77b4; margin: 0;">{results['average_threshold']:.1f} mph</h2>
            <p style="margin: 0; font-size: 0.9rem; color: #666;">
                Average of CUSUM and Bayesian methods
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 CUSUM Method</h3>
            <h2 style="color: #ff7f0e; margin: 0;">{results['cusum_threshold']:.1f} mph</h2>
            <p style="margin: 0; font-size: 0.9rem; color: #666;">
                Cumulative sum analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔬 Bayesian Method</h3>
            <h2 style="color: #2ca02c; margin: 0;">{results['bayesian_threshold']:.1f} mph</h2>
            <p style="margin: 0; font-size: 0.9rem; color: #666;">
                Change point detection
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed results table
    st.subheader("📋 Analysis Details")
    
    details_data = {
        "Metric": [
            "Player Name",
            "Analysis Period", 
            "Total Pitches Analyzed",
            f"{pitch_type} Pitches",
            "CUSUM Threshold",
            "Bayesian Threshold",
            "Average Threshold"
        ],
        "Value": [
            results['player_name'],
            results['years'],
            f"{results['total_pitches']:,}",
            f"{results['fastball_pitches']:,}",
            f"{results['cusum_threshold']:.1f} mph",
            f"{results['bayesian_threshold']:.1f} mph", 
            f"{results['average_threshold']:.1f} mph"
        ]
    }
    
    details_df = pd.DataFrame(details_data)
    st.dataframe(details_df, use_container_width=True, hide_index=True)
    
    # Interpretation section
    st.subheader("💡 Interpretation")
    
    threshold = results['average_threshold']
    
    if threshold >= 96:
        performance_level = "Excellent"
        color = "green"
        interpretation = f"{player_name} maintains strong performance down to {threshold:.1f} mph, indicating excellent velocity retention and effectiveness."
    elif threshold >= 94:
        performance_level = "Good"
        color = "blue"
        interpretation = f"{player_name} shows good performance until {threshold:.1f} mph, with moderate velocity sensitivity."
    elif threshold >= 92:
        performance_level = "Average"
        color = "orange"
        interpretation = f"{player_name} begins to struggle around {threshold:.1f} mph, showing typical velocity sensitivity."
    else:
        performance_level = "Below Average"
        color = "red"
        interpretation = f"{player_name} shows performance decline at {threshold:.1f} mph, indicating high velocity sensitivity."
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid {color};">
        <h4 style="margin: 0 0 0.5rem 0; color: {color};">Performance Level: {performance_level}</h4>
        <p style="margin: 0; line-height: 1.5;">{interpretation}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Method comparison
    st.subheader("🔍 Method Comparison")
    
    method_diff = abs(results['cusum_threshold'] - results['bayesian_threshold'])
    
    if method_diff <= 1.0:
        agreement = "Strong"
        agreement_color = "green"
        agreement_text = "Both methods agree closely, indicating high confidence in the result."
    elif method_diff <= 2.0:
        agreement = "Moderate"
        agreement_color = "orange"
        agreement_text = "Methods show moderate agreement, suggesting reasonable confidence."
    else:
        agreement = "Weak"
        agreement_color = "red"
        agreement_text = "Methods show significant disagreement, suggesting lower confidence in the result."
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid {agreement_color};">
        <h4 style="margin: 0 0 0.5rem 0; color: {agreement_color};">Method Agreement: {agreement}</h4>
        <p style="margin: 0; line-height: 1.5;">{agreement_text}</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #666;">
            Difference between methods: {method_diff:.1f} mph
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_example_usage(data_pipeline):
    """Show example usage and available data information."""
    
    st.header("🎯 How to Use")
    
    st.markdown("""
    ### Getting Started
    1. **Enter a player name** in the sidebar (e.g., "Jack Flaherty", "Gerrit Cole")
    2. **Select the year range** you want to analyze
    3. **Choose a pitch type** (default is FF for Four-Seam Fastball)
    4. **Optionally enable visualizations** for detailed plots
    5. **Click "Run Analysis"** to get your results
    
    ### What the Analysis Shows
    - **Velocity Threshold**: The speed at which a pitcher's performance starts to decline
    - **CUSUM Method**: Uses cumulative sum analysis to detect performance changes
    - **Bayesian Method**: Uses change point detection for statistical analysis
    - **Performance Level**: Interpretation of the results (Excellent/Good/Average/Below Average)
    """)
    
    # Show available data info
    st.header("📊 Available Data")
    
    available_years = data_pipeline.get_available_years()
    if available_years:
        st.success(f"✅ Data available for years: {', '.join(map(str, available_years))}")
        
        # Show sample players
        st.subheader("Sample Players to Try")
        sample_players = [
            "Jack Flaherty",
            "Gerrit Cole", 
            "Max Fried",
            "Zack Wheeler",
            "Jacob deGrom"
        ]
        
        cols = st.columns(len(sample_players))
        for i, player in enumerate(sample_players):
            with cols[i]:
                st.button(f"Try {player}", key=f"sample_{i}", on_click=lambda p=player: st.session_state.update({"player_name": p}))
    
    else:
        st.error("❌ No data available. Please check your data files.")

def show_missing_data_help(error_message):
    """Show helpful information when data files are missing."""
    
    st.markdown('<h1 class="main-header">⚾ Velocity Cliff Analysis</h1>', unsafe_allow_html=True)
    
    st.error("❌ **Data Files Not Found**")
    
    st.markdown("""
    ### 🔧 Setup Required
    
    This app requires local Statcast data files to run. Here are your options:
    """)
    
    # Option 1: Download data
    with st.expander("📥 **Option 1: Download Data Files**", expanded=True):
        st.markdown("""
        #### Download the required data files:
        
        1. **Create the data directory structure:**
        ```bash
        mkdir -p data/savant/season_data
        ```
        
        2. **Download player metadata (9.7MB):**
        ```bash
        # You'll need to obtain the player_meta.feather file
        # This contains player IDs and names
        ```
        
        3. **Download season data files (~160MB each):**
        ```bash
        # You'll need to obtain the year-specific .feather files
        # For example: 2024.feather, 2023.feather, etc.
        ```
        
        4. **Place files in the correct structure:**
        ```
        data/
        ├── player_meta.feather
        └── savant/season_data/
            ├── 2024.feather
            ├── 2023.feather
            └── ... (other years)
        ```
        """)
    
    # Option 2: Demo mode
    with st.expander("🎮 **Option 2: Demo Mode**", expanded=True):
        st.markdown("""
        #### Try the app with sample data:
        
        The app can run in demo mode with pre-generated sample results for popular pitchers.
        """)
        
        if st.button("🚀 Launch Demo Mode", type="primary"):
            st.session_state.demo_mode = True
            st.rerun()
    
    # Option 3: Use CLI version
    with st.expander("💻 **Option 3: Use Command Line Version**", expanded=True):
        st.markdown("""
        #### If you have the data files, use the CLI version:
        
        ```bash
        # Install dependencies
        pip install -r requirements.txt
        
        # Run analysis
        python velocliff/velo_cliff_local.py --player "Jack Flaherty" --start-year 2024 --end-year 2024
        ```
        """)
    
    # Error details
    with st.expander("🔍 **Technical Details**"):
        st.code(f"Error: {error_message}")
        st.markdown("""
        **Expected data structure:**
        - `data/player_meta.feather` - Player metadata
        - `data/savant/season_data/YYYY.feather` - Year-specific Statcast data
        
        **Data sources:**
        - Statcast data from MLB (2015-2024)
        - Player metadata from MLB player database
        """)

def run_demo_mode():
    """Run the app in demo mode with sample data."""
    
    st.markdown('<h1 class="main-header">⚾ Velocity Cliff Analysis (Demo Mode)</h1>', unsafe_allow_html=True)
    
    st.info("🎮 **Demo Mode**: This is a demonstration with sample data. Install data files for full functionality.")
    
    # Sidebar for demo controls
    with st.sidebar:
        st.header("🎯 Demo Parameters")
        
        # Player selection (demo data)
        demo_players = [
            "Jack Flaherty",
            "Gerrit Cole", 
            "Max Fried",
            "Zack Wheeler",
            "Jacob deGrom",
            "Corbin Burnes"
        ]
        
        player_name = st.selectbox(
            "Select Player",
            options=demo_players,
            index=0
        )
        
        # Year selection
        start_year = st.selectbox("Start Year", [2024, 2023, 2022], index=0)
        end_year = st.selectbox("End Year", [2024, 2023, 2022], index=0)
        
        # Pitch type
        pitch_type = st.selectbox(
            "Pitch Type",
            options=['FF', 'SI', 'FC', 'SL'],
            index=0
        )
        
        # Run demo analysis
        run_demo = st.button("🚀 Run Demo Analysis", type="primary")
    
    # Demo results
    if run_demo:
        display_demo_results(player_name, start_year, end_year, pitch_type)
    else:
        show_demo_info()

def display_demo_results(player_name, start_year, end_year, pitch_type):
    """Display demo results with sample data."""
    
    # Sample demo data
    demo_results = {
        "Jack Flaherty": {"cusum": 93.4, "bayesian": 93.3, "total": 329, "ff": 329},
        "Gerrit Cole": {"cusum": 96.4, "bayesian": 93.9, "total": 243, "ff": 243},
        "Max Fried": {"cusum": 94.2, "bayesian": 95.6, "total": 258, "ff": 258},
        "Zack Wheeler": {"cusum": 94.8, "bayesian": 94.8, "total": 299, "ff": 299},
        "Jacob deGrom": {"cusum": 97.3, "bayesian": 97.3, "total": 19, "ff": 19},
        "Corbin Burnes": {"cusum": 94.7, "bayesian": 97.0, "total": 59, "ff": 59}
    }
    
    if player_name not in demo_results:
        st.error("Demo data not available for this player")
        return
    
    data = demo_results[player_name]
    average_threshold = (data["cusum"] + data["bayesian"]) / 2
    
    results = {
        'player_name': player_name,
        'years': f"{start_year}-{end_year}",
        'total_pitches': data["total"],
        'fastball_pitches': data["ff"],
        'cusum_threshold': data["cusum"],
        'bayesian_threshold': data["bayesian"],
        'average_threshold': average_threshold
    }
    
    # Display results (same as real results)
    display_results(results, player_name, pitch_type, False)
    
    # Demo notice
    st.warning("""
    ⚠️ **Demo Mode Notice**: 
    These are sample results for demonstration purposes. 
    Install the actual data files to analyze real Statcast data.
    """)

def show_demo_info():
    """Show demo mode information."""
    
    st.header("🎮 Demo Mode Features")
    
    st.markdown("""
    ### What You Can Do in Demo Mode:
    
    - **Select from popular pitchers**: Jack Flaherty, Gerrit Cole, Max Fried, etc.
    - **Choose different years**: 2022-2024
    - **Try different pitch types**: FF, SI, FC, SL
    - **See the full interface**: All features work with sample data
    - **Understand the analysis**: See how velocity cliff analysis works
    
    ### Sample Results Include:
    - Velocity thresholds for each pitcher
    - CUSUM and Bayesian analysis results
    - Performance level interpretations
    - Method agreement assessments
    """)
    
    st.header("📊 Sample Analysis")
    
    # Show sample results table
    sample_data = {
        "Player": ["Jack Flaherty", "Gerrit Cole", "Max Fried", "Zack Wheeler"],
        "CUSUM Threshold": ["93.4 mph", "96.4 mph", "94.2 mph", "94.8 mph"],
        "Bayesian Threshold": ["93.3 mph", "93.9 mph", "95.6 mph", "94.8 mph"],
        "Average": ["93.4 mph", "95.2 mph", "94.9 mph", "94.8 mph"],
        "Performance": ["Average", "Good", "Good", "Good"]
    }
    
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    # Check if demo mode is enabled
    if hasattr(st.session_state, 'demo_mode') and st.session_state.demo_mode:
        run_demo_mode()
    else:
        main() 