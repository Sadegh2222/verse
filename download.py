import os
from spotdl import Spotdl
from dotenv import load_dotenv

load_dotenv()

def download_song(song_name):
    # Initialize SpotDL and download the song
    sp = Spotdl()
    song = sp.search(song_name)

    if not song:
        return None

    song_path = sp.download(song)
    return song_path
