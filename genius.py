import requests
from dotenv import load_dotenv

load_dotenv()

GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")

def get_lyrics(song_name):
    search_url = f"https://api.genius.com/search?q={song_name}"
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
    response = requests.get(search_url, headers=headers).json()

    if response['response']['hits']:
        song_url = response['response']['hits'][0]['result']['url']
        song_page = requests.get(song_url)
        # Parse the lyrics from the page using BeautifulSoup or regex
        lyrics = "Lyrics not found"
        return lyrics
    else:
        return "No lyrics found"
