# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json



class ActionMovieSearch(Action):
    def name(self) -> Text:
        return "action_serach_movie" #action name

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        header = tracker.get_slot() # get all the slot values for the api filters
        # make the api call
        # format the result
        # return the information
        return []
