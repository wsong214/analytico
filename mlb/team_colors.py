# MLB HEX color codes (only primary colors are used)
team_colors = {
    "ATL": "#CE1141",
    "BAL": "#DF4601",
    "BOS": "#BD3039",
    "CHC": "#0E3386",
    "CHW": "#27251F",
    "CIN": "#C6011F",
    "CLE": "#00385D",
    "COL": "#333366",
    "DET": "#0C2340",
    "HOU": "#002D62",
    "KCR": "#004687",
    "LAA": "#BA0021",
    "LAD": "#005A9C",
    "MIA": "#00A3E0",
    "MIL": "#12284B",
    "MIN": "#002B5C",
    "NYM": "#002D72",
    "NYY": "#003087",
    "OAK": "#003831",
    "PHI": "#E81828",
    "PIT": "#FDB827",
    "SDP": "#2F241D",
    "SFG": "#FD5A1E",
    "SEA": "#0C2C56",
    "STL" "#C41E3A",
    "TBR": "#092C5C",
    "TEX": "#003278",
    "TOR": "#134A8E",
    "WSN": "#AB0003"
}

# Teams that became current franchises with their current names
relocated_teams = {
    "BSN": "ATL",
    "St. Louis Browns": "BAL",
    "Philadelphia Athletics": "Oakland Athletics",
    "New York Giants": "SFG",
    "Brooklyn Dodgers": "Los Angeles Dodgers",
    "Washington Senators": "Minnesota Twins",
    "Milwaukee Braves": "ATL",
    "Kansas City Athletics": "Oakland Athletics",
    "Seattle Pilots": "Milwaukee Brewers",
    "Washington Senators (1961)": "Texas Rangers",
    "Montreal Expos": "Washington Nationals"
}

# Any defunct teams will be colored grey
defunct_color = "#808080"

# Dictionary to hold defunct teams
defunct_teams = [
    "Louisville Colonels", "BAL (NL)", "Cleveland Spiders", 
    "Washington Senators (NL)", "Indianapolis Hoosiers", "Kansas City Packers", 
    "Chicago Whales", "Baltimore Terrapins", "St. Louis Terriers", 
    "Brooklyn Tip-Tops", "Pittsburgh Rebels", "Buffalo Blues", "Newark Peppers"
]

# Data of teams for the plot
teams = [
    "Boston Braves", "St. Louis Browns", "Philadelphia Athletics", 
    "New York Giants", "Brooklyn Dodgers", "Washington Senators", 
    "Milwaukee Braves", "Kansas City Athletics", "Seattle Pilots", 
    "Montreal Expos", "Louisville Colonels", "Cleveland Spiders"
] + defunct_teams

# Generate a color for each team based on their current status
team_color_map = {}

for team in teams:
    if team in defunct_teams:
        team_color_map[team] = defunct_color
    elif team in relocated_teams:
        current_team = relocated_teams[team]
        team_color_map[team] = team_colors[current_team]
    else:
        team_color_map[team] = team_colors.get(team, defunct_color)
