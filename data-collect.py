import json
from lib.CaptureWinnings import CaptureWinnings
from lib.StatusExtractor import StatusExtractor

capture_winnings = CaptureWinnings()
status_extractor = StatusExtractor()


def data_collector(new_data):
    # Read the existing JSON data from 'data-collect.json'
    try:
        with open('data-collect.json', 'r') as f:
            previous_data = json.load(f)
            # Ensure previous_data is a list
            if not isinstance(previous_data, list):
                previous_data = []
    except FileNotFoundError:
        previous_data = []

    # Combine the new data with the existing data
    previous_data.append(new_data)

    # Write the combined data back to 'data-collect.json'
    with open('data-collect.json', 'w') as f:
        json.dump(previous_data, f, indent=4)

while True:
    winning_number = capture_winnings.run()
    status = status_extractor.run()

    new_data = {
        "winning_number": winning_number,
        "total_players": status['players'],
        "total_coins": status['bets'],
        "total_winned_coins": status['winnings']
    }

    data_collector(new_data)
