import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def connect_to_api():
    """Returns access point to Spotify

    Returns:
        sp (object): Spotipy object that can be used to make API calls
    """

    # Credentials are specified as environment variables in the "activate" script from the venv and can be obtained in the Spotify Developer Platform
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    spotipy.Spotify()

    print("Log: Connection to Spotify API established.")

    return sp


