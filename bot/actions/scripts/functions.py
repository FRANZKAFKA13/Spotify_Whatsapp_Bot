import pandas as pd
import numpy as np
import datetime

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

    track_list = [["track_name", "track_uri", "track_release_date"]]

    print("Log: Pulling data from Spotify. This can take a while...")

    for album_uri in album_uri_list:
        album_tracks = sp.album_tracks(album_uri, limit=50, offset=0)["items"]
        count_tracks_in_album = len(album_tracks)
        album_release_date = sp.album(album_uri)["release_date"]

        # This part is probably very slow and should be improved by accessing the API less often
        for track_number in range(count_tracks_in_album):
            track_name = album_tracks[track_number]["name"]
            track_uri = album_tracks[track_number]["uri"]
             
            track_list.append([track_name, track_uri, album_release_date])

    # Create df from list of tracks for all albums
    track_df = pd.DataFrame(data=track_list[1:], columns=track_list[0])
    
    print("Log: Finished pulling all tracks from albums.")
    return track_df


def get_all_tracks_from_artists(sp, artist_uri_list):
    """A function returning tracks from a list of artist URIs as pandas DataFrame.

    Args:
        sp (Object): Spotipy object that can be used to make API calls
        artist_uri_list (list): A list containing artist URIs.

    Returns:
        DataFrame: A pandas DataFrame containing track names, URIs, release dates and artist names.
    """

    track_list = [["track_name", "track_uri", "track_release_date", "artist_name"]]
    track_df = pd.DataFrame(columns=track_list[0])

    print("Log: Pulling data from Spotify. This can take a while...")

    for artist_uri in artist_uri_list:
        # Get artist name and albums
        artist_name = sp.artist(artist_uri)["name"]
        albums = get_albums_from_artists(sp, [artist_uri])

        # Get tracks from artist albums
        tracks_artist_df = get_tracks_from_albums(sp, albums["album_uri"].to_list())
        tracks_artist_df["artist_name"] = artist_name

        # Append new songs to dataframe
        track_df = track_df.append(tracks_artist_df)
    
    print("Log: Finished pulling all tracks from artist.")
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


