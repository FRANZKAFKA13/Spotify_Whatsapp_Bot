import pandas as pd
import numpy as np
import datetime
import pprint

def search_artist_by_name(sp, artist_name_input):
    """Get artist name and URI from artist name input
    Args:
        sp (Object): Spotipy object that can be used to make API calls
        artist_name_input (string): A name from an artist
    Returns:
        search_result_artist_name: The top search result artist name for the given name
        search_result_artist_uri: The top search result artist URI for the given name
    """

    results = sp.search(q=artist_name_input, type='artist', limit=20, offset=0, market="DE")

    try:
        result_artist_name = results["artists"]["items"][0]["name"]
        result_artist_uri = results["artists"]["items"][0]["uri"]
    except Exception as e:
        print("Log: No results were found.")
        return "", ""

    return result_artist_name, result_artist_uri


def print_user_playlists(sp, user_uri):
    """Prints out user playlist
    Args:
        sp (Object): Spotipy object that can be used to make API calls
        user_uri (string): A spotify user's URI
    """

    print("Log: Pulling data from Spotify. This can take a while...")
    
    playlists = sp.user_playlists(user_uri) 

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None



def get_albums_from_artists(sp, artist_uri_list):
    """A function returning albums from a list of artist URIs as pandas DataFrame.

    Args:
        sp (Object): Spotipy object that can be used to make API calls
        artist_uri_list (list): A list containing artist URIs.

    Returns:
        DataFrame: A pandas DataFrame containing artist names, URIs, and release date.
    """

    # Create header for output df
    albums_list = [["name", "album_uri", "album_release_date", "artist_uri"]]

    print("Log: Pulling data from Spotify. This can take a while...")

    # Loop through list of artist uris
    for artist_uri in artist_uri_list:
        # Get album from artist
        albums = sp.artist_albums(artist_uri)
        
        # Append each album to list
        for album in albums["items"]:
            album_name = album["name"]
            album_uri = album["uri"]
            album_release_date = album["release_date"]
            albums_list.append([album_name, album_uri, album_release_date, artist_uri])

    # Create df from list of albums for all artist
    albums_df = pd.DataFrame(data=albums_list[1:], columns=albums_list[0])

    print("Log: Finished pulling all albums from artist.")
    return albums_df



def get_tracks_from_albums(sp, album_uri_list):
    """A function returning tracks from a list of album URIs as pandas DataFrame.

    Args:
        sp (Object): Spotipy object that can be used to make API calls
        album_uri_list (list): A list containing album URIs.

    Returns:
        DataFrame: A pandas DataFrame containing track names, URIs and release dates.
    """

    #album_uri_list = albums_df["album_uri"].to_list()

    #track_list = [["track_uri", "track_name", "track_release_date", "artist_uri", "artist_name", "album_uri", "album_name", "album_release_date"]]

    track_list = [["track_name", "track_uri", "track_release_date"]]

    print("Log: Pulling data from Spotify. This can take a while...")

    for album_uri in album_uri_list:
        album_tracks = sp.album_tracks(album_uri, limit=50, offset=0)["items"]
        count_tracks_in_album = len(album_tracks)
        album_release_date = sp.album(album_uri)["release_date"]
        print(sp.album(album_uri)["artists"][0]["name"])

        # This part is probably very slow and should be improved by accessing the API less often
        for track_number in range(count_tracks_in_album):
            track_name = album_tracks[track_number]["name"]
            track_uri = album_tracks[track_number]["uri"]
            track_list.append([track_uri, track_name, album_release_date, ])

    # Create df from list of tracks for all albums
    track_df = pd.DataFrame(data=track_list[1:], columns=track_list[0])
    
    print("Log: Finished pulling all tracks from albums.")
    return track_df


def get_new_tracks_from_artists(sp, artist_uri_list, days=7):
    """A function returning newly released tracks from a list of artist URIs as pandas DataFrame.

    Args:
        sp (Object): Spotipy object that can be used to make API calls
        artist_uri_list (list): A list containing artist URIs.
        days (int): The number of days to look back for new releases

    Returns:
        DataFrame: A pandas DataFrame containing track names, URIs, release dates and artist names.
    """

    # Run function to get all songs
    track_df = get_all_tracks_from_artists(sp, artist_uri_list)

    # Only consider songs that have been released in the last days
    track_df["days_since_release"] = track_df["track_release_date"].apply(str_to_date).apply(datediff_today)
    track_df = track_df[track_df["days_since_release"] <= days]

    print("Log: Finished pulling new tracks from artist.")

    return track_df


def str_to_date(date_as_str):
    """Transforms string with the format "YYYY-MM-DD" into a datetime object.

    Args:
        date_as_str (string): The string containing the date information.

    Returns:
        date_time_obj [datetime]: The given date as datetime object.
    """
    date_time_obj = datetime.datetime.strptime(date_as_str, '%Y-%m-%d').date()
    return date_time_obj


def datediff_today(date):
    """Calculate difference between a datetime date and the current date.

    Args:
        date (datetime): A date which should be used for calculation.

    Returns:
        datediff: The difference between the given date and today in days.
    """
    today = datetime.date.today()
    datediff = (today - date).days
    return datediff


def get_all_tracks_from_artists(sp, artist_uri_list):
    """A function returning tracks from a list of artist URIs as pandas DataFrame.

    Args:
        sp (Object): Spotipy object that can be used to make API calls
        artist_uri_list (list): A list containing artist URIs.

    Returns:
        DataFrame: A pandas DataFrame containing track names, URIs, release dates and artist names.
    """

    track_list = [["track_uri", "track_name", "track_release_date", "artist_uri", "artist_name", "album_uri", "album_name", "album_release_date"]]

    for artist in artist_uri_list:

        albums = sp.artist_albums(artist)

        for album in albums["items"]:
            album_uri = album["uri"]
            album_name = album["name"]
            album_release_date = album["release_date"]
            artist_uri = album["artists"][0]["uri"]
            artist_name = album["artists"][0]["name"]
            #other_artist_uris = []
            #other_artist_names = []

            #for artist in album["artists"][1:]:
            #    other_artist_uris.append(artist["uri"])
            #    other_artist_names.append(artist["name"])

            tracks = sp.album_tracks(album["uri"], limit=50, offset=0)["items"]

            for track in tracks:
                track_name = track["name"]
                track_uri = track["uri"]
                track_release_date = album["release_date"]
                track_list.append([track_uri, track_name, track_release_date, artist_uri, artist_name, album_uri, album_name, album_release_date])

    # Create df from list of tracks
    tracks_df = pd.DataFrame(data=track_list[1:], columns=track_list[0])    
    print(tracks_df)
    return tracks_df
        
