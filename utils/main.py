import os
import sys
import logging
from StatcastDataHandler import StatcastDataHandler

def ensure_data_directory(directory='../data'):
    """Ensure the data directory exists and create any missing subdirectories."""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")
        except Exception as e:
            logging.error(f"Failed to create directory {directory}: {e}")
            sys.exit(1)
    
    # Ensure subdirectories under 'savant/season_data' also exist
    savant_dir = os.path.join(directory, 'savant', 'season_data')
    if not os.path.exists(savant_dir):
        try:
            os.makedirs(savant_dir)
            logging.info(f"Created subdirectory: {savant_dir}")
        except Exception as e:
            logging.error(f"Failed to create subdirectory {savant_dir}: {e}")
            sys.exit(1)

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Ensure the data directory exists
    ensure_data_directory()

    # Create an instance of the StatcastDataHandler class
    data_handler = StatcastDataHandler()

    # Fetch player meta data (path and update can be parameterized)
    player_meta_path = '../data/player_meta.feather'
    logging.info("Fetching player meta data...")
    try:
        player_meta = data_handler.get_player_meta(path=player_meta_path, update=False)
        logging.info(f"Fetched player meta data with {player_meta.shape[0]} rows.")
    except Exception as e:
        logging.error(f"Error fetching player meta data: {e}")
        sys.exit(1)

    # Update local Statcast data for the current year
    logging.info("Updating local Statcast data for the current year...")
    try:
        data_handler.update_local_sc(just_current=True)
        logging.info("Local Statcast data updated.")
    except Exception as e:
        logging.error(f"Error updating Statcast data: {e}")
        sys.exit(1)

    # Fetch Statcast data for a specific range of years (e.g., 2015-2024)
    start_year = 2015
    end_year = 2024
    logging.info(f"Fetching Statcast data for {start_year} to {end_year}...")
    try:
        statcast_data = data_handler.fetch_statcast(start_year=start_year, end_year=end_year)
        logging.info(f"Fetched {statcast_data.shape[0]} rows of Statcast data.")
    except Exception as e:
        logging.error(f"Error fetching Statcast data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
