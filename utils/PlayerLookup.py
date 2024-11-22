import os
import pandas as pd

def player_lookup(player_id, start_year, end_year, data_dir='../data/savant/season_data/'):
    """
    Retrieve data for a specific player from the feather database within a specified year range.

    Args:
        player_id (int): MLBAM ID of the player.
        start_year (int): Starting year of the range.
        end_year (int): Ending year of the range.
        data_dir (str): Path to the directory containing season data feather files.

    Returns:
        pd.DataFrame: DataFrame containing the filtered data for the player.
    """
    # Initialize an empty list to store data
    data_frames = []

    # Loop through the years in the range
    for year in range(start_year, end_year + 1):
        file_path = os.path.join(data_dir, f'{year}.feather')

        # Check if the feather file exists for the year
        if os.path.exists(file_path):
            try:
                # Read the feather file
                data = pd.read_feather(file_path)
                # Filter data for the given player_id
                player_data = data[data['pitcher'] == player_id]
                data_frames.append(player_data)
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        else:
            print(f"File not found for year {year}: {file_path}")

    # Concatenate all filtered data
    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        # Return an empty DataFrame if no data was found
        return pd.DataFrame()

if __name__ == "__main__":
    # Example usage
    example_player_id = 656427
    example_start_year = 2024
    example_end_year = 2024

    player_data = player_lookup(example_player_id, example_start_year, example_end_year)
    print(player_data.head())
