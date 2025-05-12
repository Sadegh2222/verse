import requests

GENIUS_API_TOKEN = "توکن Genius شما"

def get_lyrics(song_title):
    base_url = "https://api.genius.com"
    search_url = base_url + "/search"
    params = {'q': song_title}
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}

    response = requests.get(search_url, params=params, headers=headers)
    json = response.json()
    
    song_path = json['response']['hits'][0]['result']['path']
    song_url = base_url + song_path

    lyrics_response = requests.get(song_url)
    lyrics = lyrics_response.text  # متن آهنگ

    return lyrics
