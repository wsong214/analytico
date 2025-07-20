# Analytico - Baseball Analytics Platform

A comprehensive baseball analytics platform focused on MLB pitcher performance analysis, specifically the "velocity cliff" phenomenon. This project analyzes when pitchers start to struggle as their velocity decreases using advanced statistical methods.

## 🚀 New: Local Data Pipeline

**The data pipeline has been completely refactored to work with local feather files instead of pybaseball API calls!**

### Key Improvements:
- ✅ **No API dependencies** - All data stored locally
- ✅ **Faster execution** - No network calls required  
- ✅ **Consistent data** - Same structure across all analyses
- ✅ **Reproducible results** - No API rate limits or data changes
- ✅ **Offline capability** - Works without internet connection
- ✅ **Better error handling** - Robust data validation and logging

## 📊 What This Project Does

### Core Functionality:
1. **Data Collection & Management** (`utils/`):
   - **DataPipeline**: Comprehensive data handler for local feather files
   - **StatcastDataHandler**: Fetches and manages MLB Statcast data (2015-2024)
   - **PlayerLookup**: Retrieves individual player data from local database

2. **Velocity Cliff Analysis** (`velocliff/`):
   - Analyzes when pitchers start to struggle as their velocity decreases
   - Uses advanced statistical methods:
     - **CUSUM (Cumulative Sum) Analysis**: Detects performance decline thresholds
     - **Bayesian Changepoint Detection**: Identifies critical velocity points
     - **LOWESS Smoothing**: Smooths data for trend analysis
     - **Survival Analysis**: Kaplan-Meier curves and Cox proportional hazards

3. **Career Analysis** (`mlb/`):
   - **bWAR Graphing**: Creates career WAR (Wins Above Replacement) visualizations
   - **Team Color Mapping**: Maps historical team colors for visual consistency

## 🛠️ Quick Start

### 1. Web Interface (Recommended)
Launch the interactive Streamlit app for the best user experience:

```bash
# Option 1: Use the launcher script
python run_streamlit.py

# Option 2: Run directly with streamlit
streamlit run streamlit_app.py
```

The web app will open at `http://localhost:8501` and provides:
- Interactive player selection
- Year range selection  
- Pitch type selection
- Optional visualizations
- Detailed results with interpretation
- Performance level assessment

**🎮 Demo Mode**: If you don't have the data files, the app will automatically offer a demo mode with sample results for popular pitchers!

### 2. Test the Data Pipeline
```bash
python test_data_pipeline.py
```

### 3. Run Velocity Cliff Analysis (CLI)
```bash
# Command line interface
python velocliff/velo_cliff_local.py --player "Jack Flaherty" --start-year 2024 --end-year 2024

# Or use the example script
python example_usage.py
```

### 3. Use in Your Own Code
```python
import sys
sys.path.append("utils")

from DataPipeline import DataPipeline
from VelocityCliffAnalyzer import VelocityCliffAnalyzer

# Initialize data pipeline
data_pipeline = DataPipeline()

# Find a player
player_id = data_pipeline.find_player_by_name('Jack', 'Flaherty')

# Get player data
player_data = data_pipeline.get_player_data(player_id, 2024, 2024)

# Initialize analyzer
analyzer = VelocityCliffAnalyzer(data_pipeline)

# Run full analysis
results = analyzer.run_full_analysis("Jack Flaherty", 2024, 2024)
```

## 📁 Project Structure

```
analytico/
├── data/                          # Local data storage
│   ├── player_meta.feather        # Player metadata (9.7MB)
│   └── savant/season_data/        # Statcast data by year (~160MB each)
│       ├── 2015.feather
│       ├── 2016.feather
│       └── ... (2015-2024)
├── utils/                         # Core utilities
│   ├── DataPipeline.py           # NEW: Main data pipeline
│   ├── VelocityCliffAnalyzer.py  # NEW: Analysis engine
│   ├── StatcastDataHandler.py    # Data fetching (legacy)
│   └── PlayerLookup.py           # Player lookup utilities
├── velocliff/                     # Velocity cliff analysis
│   ├── velo_cliff_local.py       # NEW: CLI interface
│   └── velo_cliff.ipynb          # Original notebook (legacy)
├── mlb/                          # Career analysis tools
│   ├── career_bWAR_graph.ipynb   # WAR visualization
│   └── team_colors.py            # Team color mapping
├── streamlit_app.py              # NEW: Web interface
├── run_streamlit.py              # NEW: App launcher
├── download_data.py              # NEW: Data download helper
├── requirements.txt              # NEW: Dependencies
├── example_usage.py              # NEW: Usage examples
├── test_data_pipeline.py         # NEW: Pipeline testing
└── README.md                     # This file
```

## 🔧 Data Pipeline Features

### DataPipeline Class
- **Auto-detection**: Automatically finds data directory
- **Player lookup**: Find players by name or ID
- **Data filtering**: Filter by year, pitch type, etc.
- **Summary statistics**: Generate pitch type summaries
- **Data validation**: Robust error handling and logging

### VelocityCliffAnalyzer Class
- **CUSUM Analysis**: Detect performance decline thresholds
- **Bayesian Changepoint**: Alternative statistical method
- **Visualization**: Comprehensive plotting capabilities
- **Full analysis**: Complete end-to-end analysis pipeline

## 📈 Example Results

For Jack Flaherty (2024):
- **Total Pitches**: 3,190
- **Fastball Pitches**: 329 (analyzed)
- **CUSUM Threshold**: 93.4 mph
- **Bayesian Threshold**: 93.3 mph
- **Average Threshold**: 93.3 mph

**Interpretation**: When Jack Flaherty's fastball velocity drops below approximately 93.3 mph, his expected wOBA against increases significantly, indicating a performance decline.

## 🎯 Use Cases

1. **Player Development**: Identify when pitchers need velocity training
2. **Injury Prevention**: Detect early signs of fatigue
3. **Game Strategy**: Know when to pull pitchers
4. **Scouting**: Evaluate pitcher effectiveness at different velocities
5. **Research**: Academic analysis of pitching mechanics

## 🔄 Migration from pybaseball

### Old Way (pybaseball):
```python
from pybaseball import statcast, playerid_lookup

# API calls (slow, rate-limited)
pitcher_lookup = playerid_lookup('flaherty', 'jack')
pitcher_data = statcast(start_dt='2024-02-15', end_dt='2024-11-15')
```

### New Way (Local Pipeline):
```python
from DataPipeline import DataPipeline

# Local data (fast, reliable)
data_pipeline = DataPipeline()
player_id = data_pipeline.find_player_by_name('Jack', 'Flaherty')
pitcher_data = data_pipeline.get_player_data(player_id, 2024, 2024)
```

## 📊 Data Requirements

### Full Dataset (Recommended)
- **Player Metadata**: 9.7MB feather file
- **Season Data**: ~160MB per year (2015-2024)
- **Total Storage**: ~1.6GB for complete dataset
- **Format**: Feather files for fast I/O

### Demo Mode (No Data Required)
- **Sample Results**: Pre-generated data for popular pitchers
- **Full Interface**: All features work with demo data
- **Perfect For**: Testing, demonstrations, learning the tool

### Getting Data Files
```bash
# Check what data you have
python download_data.py

# The script will guide you through:
# 1. Manual download instructions
# 2. Pybaseball API download
# 3. Demo mode information
```

## 🚀 Future Enhancements

- [ ] Web dashboard interface
- [ ] Machine learning models for predictive analytics
- [ ] Real-time data updates
- [ ] Multi-player comparison tools
- [ ] Advanced visualization options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please respect MLB's data usage policies.

---

**Note**: This project uses local Statcast data files. Ensure you have the proper data files in the `data/` directory before running analyses.