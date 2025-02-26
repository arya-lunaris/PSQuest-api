import os
import requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'project', '.env')
load_dotenv(dotenv_path=dotenv_path)

CLIENT_ID = os.getenv('IGDB_CLIENT_ID')
CLIENT_SECRET = os.getenv('IGDB_CLIENT_SECRET')

IGDB_API_URL = 'https://api.igdb.com/v4/games'
ACCESS_TOKEN_URL = 'https://id.twitch.tv/oauth2/token'

class IGDBAPI:
    def __init__(self):
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """
        Get the access token from Twitch OAuth2 API
        """
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }

        response = requests.post(ACCESS_TOKEN_URL, data=payload)
        response_data = response.json()

        if response.status_code == 200:
            return response_data['access_token']
        else:
            raise Exception(f"Error fetching access token: {response_data.get('message', 'Unknown error')}")

    def fetch_games(self, fields='*', limit=10):
        """
        Fetch games from IGDB API.
        
        :param fields: The fields to fetch from the database.
        :param limit: The number of games to retrieve.
        :return: The response from the IGDB API containing the game data.
        """
        headers = {
            'Client-ID': CLIENT_ID,
            'Authorization': f'Bearer {self.access_token}'
        }

        data = f"fields {fields}; limit {limit};"

        response = requests.post(IGDB_API_URL, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching games: {response.text}")


if __name__ == "__main__":
    igdb_api = IGDBAPI()
    try:
        games = igdb_api.fetch_games(fields="name,cover.url", limit=5)
        print(games)  
    except Exception as e:
        print(f"An error occurred: {e}")
