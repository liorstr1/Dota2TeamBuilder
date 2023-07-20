import requests
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta
from update_db import TalkToDb

load_dotenv()


class OpenDotaAPI:
    def __init__(self):
        self.open_dota_api_key = os.getenv('OPENDOTA_API_KEY')
        self.last_public_match = -1
        self.talk_to_db = TalkToDb(True)

    def get_next_matches(self, num_of_matches_to_add):
        twenty_four_hours_ago = datetime.now() - timedelta(days=1)
        timestamp = int(time.mktime(twenty_four_hours_ago.timetuple()))
        matches = []

        while len(matches) < num_of_matches_to_add:
            if self.last_public_match == -1:
                response = requests.get(f"https://api.opendota.com/api/proMatches?date={timestamp}")
            else:
                response = requests.get(
                    f"https://api.opendota.com/api/proMatches?date={timestamp}&less_than_match_id={self.last_public_match}")

            new_matches = response.json()
            if not new_matches:
                break
            matches.extend(new_matches)
            self.last_public_match = new_matches[-1]['match_id']
        return matches[:num_of_matches_to_add]

    def fill_heroes_id(self):
        response = requests.get(f"https://api.opendota.com/api/heroes")
        all_heroes = response.json()
        for one_hero in all_heroes:
            self.talk_to_db.update_one_hero_data(one_hero)


def get_all_matches_using_ids(matches):
    formatted_matches = []
    for match in matches:
        # Make a request to the OpenDota API
        response = requests.get(f"https://api.opendota.com/api/matches/{match['match_id']}")

        # Parse the response
        match_details = response.json()

        # Initialize lists to store the heroes played by each team
        radiant_team = []
        dire_team = []

        # Loop through each player in the match
        for player in match_details['players']:
            # If the player was on the radiant team, add their hero to the radiant team list
            if player['isRadiant']:
                radiant_team.append(player['hero_id'])
            # Otherwise, add their hero to the dire team list
            else:
                dire_team.append(player['hero_name'])

        # Determine the winner of the match
        winner = 'radiant' if match['radiant_win'] else 'dire'

        # Add the formatted match to the list of formatted matches
        formatted_matches.append({
            'match_id': match['match_id'],
            'radiant_team': radiant_team,
            'dire_team': dire_team,
            'winner': winner
        })


if __name__ == "__main__":
    op = OpenDotaAPI()
    op.fill_heroes_id()
    # all_matches_to_add = op.get_next_matches(3)
    # get_all_matches_using_ids(all_matches_to_add)

