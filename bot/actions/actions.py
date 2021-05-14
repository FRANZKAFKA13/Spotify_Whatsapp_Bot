# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# Add subfolder folder to sys.path
# import os, sys, inspect
# cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"functions")))
# if cmd_subfolder not in sys.path:
#     sys.path.insert(0, 'cmd_subfolder')

# Import rasa funcations
from typing import Text, Dict, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

# Import custom functions
from actions.functions.api_connection import *
from actions.functions.data_import import *
from actions.functions.database_access import *
from actions.functions.api_connection import *
from actions.functions.api_functions import *


# Import useful libraries
import numpy as np 
import pandas as pd
import sqlalchemy
import json

# Define custom action classes
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


class AddNewUser(Action):

    def name(self) -> Text:
        return "custom_action_add_new_user"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get user name
        user_name = ""
        
        # Add new user to db
        db_path = "data/test.db"
        user_uri = tracker.get_slot("user_uri")
        user_name = tracker.get_slot("user_name")

        try:
            add_user(db_path, user_uri, user_name)
            dispatcher.utter_message(text="Registered new user: " + str(user_name) + ".")
        except Exception as e:
            print(e)

        
        

        return []