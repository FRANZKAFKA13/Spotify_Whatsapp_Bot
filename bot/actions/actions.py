# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


from scripts.api_connection import *
from scripts.data_import import *
from scripts.api_connection import *

import numpy as np 
import pandas as pd
import sqlalchemy

import json

class GetNewTracks(Action):

    def name(self) -> Text:
        return "custom_action_get_new_tracks"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Establish connection to Spotify API through Spotipy
        sp = connect_to_api()

        # Read artists CSV
        artists = read_artists_csv()

        # # Get all new tracks from artists in CSV file
        days = 10
        tracklist = get_new_tracks_from_artists(sp, artists["artist_uri"], days=days)
        dispatcher.utter_message(text="Tracks from selected artists in the last " + str(days) + " days:")

        for track_name in tracklist['track_name']:
            dispatcher.utter_message(text=track_name)

        return []

