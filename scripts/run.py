from api_connection import *
from functions import *
from data_import import *

import numpy as np 
import pandas as pd

import json



def main():

    # Establish connection to Spotify API through Spotipy
    sp = connect_to_api()

    # Read artists CSV
    artists = read_artists_csv()

    # Get all tracks from artists in CSV file
    tracklist = get_all_tracks_from_artists(sp, artists["artist_uri"])

    print(tracklist)
    


if __name__ == '__main__':
    main()
    