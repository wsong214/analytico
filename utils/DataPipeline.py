import os
import pandas as pd
import numpy as np
from typing import Optional, List, Dict, Tuple
import logging

class DataPipeline:
    """
    A comprehensive data pipeline for baseball analytics that works with local feather files.
    Replaces the need for pybaseball calls in analysis notebooks.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the data pipeline.
        
        Args:
            data_dir (str): Path to the data directory (if None, will auto-detect)
        """
        if data_dir is None:
            # Auto-detect the data directory based on current working directory
            current_dir = os.getcwd()
            if os.path.basename(current_dir) == 'analytico':
                self.data_dir = 'data'
            else:
                self.data_dir = '../data'
        else:
            self.data_dir = data_dir
            
        self.savant_dir = os.path.join(self.data_dir, 'savant', 'season_data')
        self.player_meta_path = os.path.join(self.data_dir, 'player_meta.feather')
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate data directory structure
        self._validate_data_structure()
    
    def _validate_data_structure(self):
        """Validate that the required data files exist."""
        if not os.path.exists(self.savant_dir):
            raise FileNotFoundError(f"Savant data directory not found: {self.savant_dir}")
        
        if not os.path.exists(self.player_meta_path):
            raise FileNotFoundError(f"Player metadata file not found: {self.player_meta_path}")
        
        # Check for available years
        available_years = self.get_available_years()
        if not available_years:
            raise FileNotFoundError("No season data files found")
        
        self.logger.info(f"Data pipeline initialized with {len(available_years)} years of data")
    
    def get_available_years(self) -> List[int]:
        """Get list of available years in the data."""
        years = []
        for file in os.listdir(self.savant_dir):
            if file.endswith('.feather'):
                try:
                    year = int(file.replace('.feather', ''))
                    years.append(year)
                except ValueError:
                    continue
        return sorted(years)
    
    def get_player_metadata(self) -> pd.DataFrame:
        """Load player metadata."""
        return pd.read_feather(self.player_meta_path)
    
    def find_player_by_name(self, first_name: str, last_name: str) -> Optional[int]:
        """
        Find player MLBAM ID by name.
        
        Args:
            first_name (str): Player's first name
            last_name (str): Player's last name
            
        Returns:
            Optional[int]: MLBAM ID if found, None otherwise
        """
        player_meta = self.get_player_metadata()
        
        # Create full name for matching
        full_name = f"{first_name} {last_name}".lower()
        
        # Try exact match first
        match = player_meta[
            player_meta['name_full'].str.lower() == full_name
        ]
        
        if len(match) > 0:
            return match.iloc[0]['key_mlbam']
        
        # Try partial matches
        match = player_meta[
            (player_meta['name_first'].str.lower().str.contains(first_name.lower())) &
            (player_meta['name_last'].str.lower().str.contains(last_name.lower()))
        ]
        
        if len(match) > 0:
            self.logger.info(f"Found {len(match)} potential matches for {first_name} {last_name}")
            return match.iloc[0]['key_mlbam']
        
        return None
    
    def get_player_data(self, player_id: int, start_year: int, end_year: int) -> pd.DataFrame:
        """
        Get player data for specified years.
        
        Args:
            player_id (int): MLBAM ID of the player
            start_year (int): Starting year
            end_year (int): Ending year
            
        Returns:
            pd.DataFrame: Player data for the specified years
        """
        data_frames = []
        
        for year in range(start_year, end_year + 1):
            file_path = os.path.join(self.savant_dir, f'{year}.feather')
            
            if os.path.exists(file_path):
                try:
                    data = pd.read_feather(file_path)
                    # Filter for pitcher data
                    player_data = data[data['pitcher'] == player_id]
                    if len(player_data) > 0:
                        data_frames.append(player_data)
                        self.logger.info(f"Found {len(player_data)} pitches for {player_id} in {year}")
                except Exception as e:
                    self.logger.error(f"Error reading {file_path}: {e}")
            else:
                self.logger.warning(f"No data file for year {year}")
        
        if data_frames:
            combined_data = pd.concat(data_frames, ignore_index=True)
            self.logger.info(f"Total pitches found: {len(combined_data)}")
            return combined_data
        else:
            self.logger.warning(f"No data found for player {player_id}")
            return pd.DataFrame()
    
    def get_pitcher_data_by_name(self, first_name: str, last_name: str, 
                                start_year: int, end_year: int) -> pd.DataFrame:
        """
        Get pitcher data by name.
        
        Args:
            first_name (str): Player's first name
            last_name (str): Player's last name
            start_year (int): Starting year
            end_year (int): Ending year
            
        Returns:
            pd.DataFrame: Pitcher data
        """
        player_id = self.find_player_by_name(first_name, last_name)
        
        if player_id is None:
            self.logger.error(f"Player not found: {first_name} {last_name}")
            return pd.DataFrame()
        
        self.logger.info(f"Found player {first_name} {last_name} with ID: {player_id}")
        return self.get_player_data(player_id, start_year, end_year)
    
    def get_pitch_type_data(self, player_data: pd.DataFrame, pitch_type: str) -> pd.DataFrame:
        """
        Filter player data for specific pitch type.
        
        Args:
            player_data (pd.DataFrame): Full player data
            pitch_type (str): Pitch type to filter for (e.g., 'FF' for fastball)
            
        Returns:
            pd.DataFrame: Filtered data for the specified pitch type
        """
        filtered_data = player_data[player_data['pitch_type'] == pitch_type].copy()
        self.logger.info(f"Found {len(filtered_data)} {pitch_type} pitches")
        return filtered_data
    
    def get_pitch_summary(self, player_data: pd.DataFrame) -> pd.DataFrame:
        """
        Get summary statistics by pitch type.
        
        Args:
            player_data (pd.DataFrame): Player data
            
        Returns:
            pd.DataFrame: Summary statistics by pitch type
        """
        summary = player_data.groupby('pitch_type').agg({
            'release_speed': ['count', 'mean', 'std', 'min', 'max'],
            'estimated_woba_using_speedangle': ['mean', 'std'],
            'delta_run_exp': ['mean', 'std']
        }).round(3)
        
        # Flatten column names
        summary.columns = ['_'.join(col).strip() for col in summary.columns]
        return summary
    
    def prepare_velocity_analysis_data(self, player_data: pd.DataFrame, 
                                     pitch_type: str = 'FF') -> pd.DataFrame:
        """
        Prepare data specifically for velocity cliff analysis.
        
        Args:
            player_data (pd.DataFrame): Player data
            pitch_type (str): Pitch type to analyze (default: 'FF' for fastball)
            
        Returns:
            pd.DataFrame: Prepared data for velocity analysis
        """
        # Filter for specific pitch type
        pitch_data = self.get_pitch_type_data(player_data, pitch_type)
        
        if len(pitch_data) == 0:
            self.logger.warning(f"No {pitch_type} data found")
            return pd.DataFrame()
        
        # Remove rows with missing velocity or wOBA data
        clean_data = pitch_data.dropna(subset=['release_speed', 'estimated_woba_using_speedangle'])
        
        # Sort by velocity for analysis
        clean_data = clean_data.sort_values('release_speed').reset_index(drop=True)
        
        self.logger.info(f"Prepared {len(clean_data)} {pitch_type} pitches for velocity analysis")
        return clean_data
    
    def get_team_colors(self) -> Dict[str, str]:
        """Get team color mapping."""
        # Import team colors from the existing module
        try:
            from mlb.team_colors import team_colors
            return team_colors
        except ImportError:
            self.logger.warning("Team colors module not found, using default colors")
            return {}
    
    def get_data_info(self) -> Dict:
        """Get information about available data."""
        years = self.get_available_years()
        player_meta = self.get_player_metadata()
        
        # Get total pitches across all years
        total_pitches = 0
        for year in years:
            try:
                file_path = os.path.join(self.savant_dir, f'{year}.feather')
                data = pd.read_feather(file_path)
                total_pitches += len(data)
            except Exception as e:
                self.logger.error(f"Error reading {year} data: {e}")
        
        return {
            'available_years': years,
            'total_players': len(player_meta),
            'total_pitches': total_pitches,
            'data_directory': self.savant_dir
        } 