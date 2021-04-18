from api_connection import *
from functions import *

import numpy as np 
import pandas as pd

import json



def main():

    # Establish connection to Spotify API through Spotipy
    sp = connect_to_api()

    
    print_user_playlists(sp, "arthevard")


if __name__ == '__main__':
    main()
    