from api_connection import *
from functions import *
from data_import import *

import numpy as np 
import pandas as pd

import json



def main():

    print("Log: Started main function.")

    # Establish connection to Spotify API through Spotipy
    sp = connect_to_api()

    # Read artists CSV
    artists = read_artists_csv()

    # Get all new tracks from artists in CSV file
    days = 30
    tracklist = get_new_tracks_from_artists(sp, artists["artist_uri"], days=days)
    print("Log: Tracks from selected artists in the last " + str(days) + " days:")
    print(tracklist)
    


if __name__ == '__main__':
    main()
    