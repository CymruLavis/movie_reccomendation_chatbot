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
        api_key = "bd19a230d2f58acc317c86f89d8c7b23"
        api_access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZDE5YTIzMGQyZjU4YWNjMzE3Yzg2Zjg5ZDhjN2IyMyIsInN1YiI6IjY1YzIzMWQ5MDkyOWY2MDE2MWU0YTc0OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-TUBWSOE5-yUi8I8P1t5NrnHXN9BcZy3RATvNY5G2QQ"
        url = "https://api.themoviedb.org/3/discover/movie?"
        "include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
        headers = {
            "accept": "application/json",
            "Authorization": api_access_token
        }
        slots = {"starring": "this guy",
                 "director": "that guy",
                 "genre": "comedy"}
        url_with_filters = self.build_url(url, )

        # make the api call
        # format the result
        # return the information
        return ["title", "rating"]
    
    def build_url(url, arguments):
        # loop through dict or list of all the slots that have been filled by the user
        # if the slot has data then add the argument to the url
        # return new url
        return url