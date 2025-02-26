import os
import requests
from dotenv import load_dotenv
from game.genre_mapping import GENRE_MAPPING

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'project', '.env')
load_dotenv(dotenv_path=dotenv_path)

CLIENT_ID = os.getenv('IGDB_CLIENT_ID')
CLIENT_SECRET = os.getenv('IGDB_CLIENT_SECRET')

IGDB_API_URL = 'https://api.igdb.com/v4/games'
ACCESS_TOKEN_URL = 'https://id.twitch.tv/oauth2/token'


class IGDBAPI:
    def __init__(self):
        self.access_token = None
        self.get_access_token()

    def get_access_token(self):
        """
        Get or refresh the access token.
        """
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }

        response = requests.post(ACCESS_TOKEN_URL, data=payload)
        response_data = response.json()

        if response.status_code == 200:
            self.access_token = response_data['access_token']
        else:
            raise Exception(f"Error fetching access token: {response_data.get('message', 'Unknown error')}")

    def make_request(self, endpoint, data):
        """
        Generic method to make a request to the IGDB API, with automatic token refresh.
        """
        headers = {
            'Client-ID': CLIENT_ID,
            'Authorization': f'Bearer {self.access_token}'
        }

        response = requests.post(endpoint, headers=headers, data=data)

        if response.status_code == 401: 
            self.get_access_token()
            headers['Authorization'] = f'Bearer {self.access_token}'
            response = requests.post(endpoint, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error in IGDB API request: {response.text}")

    def search_games(self, search_term, fields='id,name,cover.url,first_release_date,total_rating,genres,storyline', limit=10):
        """
        Search games in IGDB API and map genres.
        """
        query = f"fields {fields}; search \"{search_term}\"; limit {limit};"
        games = self.make_request(IGDB_API_URL, query)

        for game in games:
            game['mapped_genres'] = [GENRE_MAPPING.get(genre, f"ID:{genre}") for genre in game.get('genres', [])]
        
        return games
