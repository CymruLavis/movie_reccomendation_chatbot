# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json



class ActionMovieSearch(Action):
    def name(self) -> Text:
        return "action_serach_movie" #action name

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # api_key = "bd19a230d2f58acc317c86f89d8c7b23"
        api_access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZDE5YTIzMGQyZjU4YWNjMzE3Yzg2Zjg5ZDhjN2IyMyIsInN1YiI6IjY1YzIzMWQ5MDkyOWY2MDE2MWU0YTc0OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-TUBWSOE5-yUi8I8P1t5NrnHXN9BcZy3RATvNY5G2QQ"
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
        headers = {
            "accept": "application/json",
            "Authorization": api_access_token
        }
        slots = self.get_slots(tracker) #get slot values for api filters
        
        url_with_filters = self.build_url(url, slots)
        
        # make the api call
        response = requests.get(url_with_filters, headers=headers)
        
        SlotSet("title", slots["title"])

        # format the result
        # return the information


        return ["title", "rating"]
    
    def build_url(url, arguments):
        filters = {} #slot names mapped to filter names

        # loop through dict or list of all the slots that have been filled by the user
        # if the slot has data then add the argument to the url
        # return new url
        return url
    
    def get_slots(tracker): 
        return {"starring": tracker.get_slot('starring'),
                 "director": tracker.get_slot('director'),
                 "genre": tracker.get_slot('genre'),
                 "title": tracker.get_slot('title'),
                 "rating": tracker.get_slot('aggregate_score')}
    
    def format_resonse(response):
        # will take response.Requests() object
        # parse to json or dictionary
        # organize results into dictionary of:
        # result = [
        #     {
        #         "title": "name",
        #         "rating": "num",
        #         "starring": "person",
        #         "director": "person",
        #         "genre": "genre"

        #     },
        #      {
        #         "title": "name",
        #         "rating": "num",
        #         "starring": "person",
        #         "director": "person",
        #         "genre": "genre"

        #     },
        # ]

        # return result
        pass

    def set_slots():
        # sets the first value of results back to slots
        pass