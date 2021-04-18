def test_function():
    print("Test function executed.")


def print_user_playlists(sp, user_uri):
    """Prints out user playlist

    Args:
        sp (Object): Spotipy object that can be used to make API calls
        user_uri (string): A spotify user's URI
    """
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

    for artist_uri in artist_uri_list:
        # Get artist name and albums
        artist_name = sp.artist(artist_uri)["name"]
        albums = get_albums_from_artists([artist_uri])

        # Get tracks from artist albums
        tracks_artist_df = get_tracks_from_albums(albums["album_uri"].to_list())
        tracks_artist_df["artist_name"] = artist_name

        # Append new songs to dataframe
        track_df = track_df.append(tracks_artist_df)
    
    return track_df