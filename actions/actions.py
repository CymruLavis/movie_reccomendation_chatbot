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

api_access_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZDE5YTIzMGQyZjU4YWNjMzE3Yzg2Zjg5ZDhjN2IyMyIsInN1YiI6IjY1YzIzMWQ5MDkyOWY2MDE2MWU0YTc0OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-TUBWSOE5-yUi8I8P1t5NrnHXN9BcZy3RATvNY5G2QQ"
url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
headers = {
    "accept": "application/json",
    "Authorization": api_access_token
}
genres = {
    "ACTION": 28,
    "ADVENTURE": 12,
    "ANIMATION": 16,
    "COMEDY": 35,
    "CRIME": 80,
    "DOCUMENTARY": 99,
    "DRAMA": 18,
    "FAMILY": 10751,
    "FANTASY": 14,
    "HISTORY": 36,
    "HORROR": 27,
    "MUSIC": 10402,
    "MYSTERY": 9648,
    "ROMANCE": 10749,
    "SCIENCE FICTION": 878,
    "TV MOVIE" : 10770,
    "THRILLER": 53,
    "WAR": 10752,
    "WESTERN": 37
}
filters = ['with_cast', 'with_crew', 'with_genres']

class ActionMovieSearch(Action):
    def name(self) -> Text:
        return "action_search_movie" #action name

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # old_slots = self.get_old_slots(tracker)
        new_slots = self.get_new_slots(tracker) #get slot values for api filters
        # self.set_old_slots(tracker)
        slots_with_ids = self.fill_id_slots(slots=new_slots) #fill slot values with ids
        results = self.get_suggestions(slots_with_ids, tracker)
        if results == "Empty":
            msg = "I couldn't find anything that matched your criteria. Please try for something else"
            dispatcher.utter_message(text=msg)
            return []
        else:
            suggestion = self.choose_suggestion(results, tracker)
            self.send_message(suggestion, dispatcher, new_slots)

        return [SlotSet("title", suggestion["title"]), 
                SlotSet("aggregate_rating", suggestion["aggregate_rating"]), 
                SlotSet("starring", suggestion["starring"]),
                SlotSet("director", suggestion["director"]),
                SlotSet("genre", suggestion["genre"])]  # may need to utilize dispatcher for returning values









    def send_message(self, suggestion, dispatcher, new_slots):
        if new_slots['starring'] is None and new_slots['director'] is  None and new_slots['genre'] is  None:
            message = f"How about {suggestion['title']}? It has a rating of {suggestion['aggregate_rating']}"
            dispatcher.utter_message(text=message)
        elif new_slots['starring'] is None and new_slots['director'] is not None and new_slots['genre'] is None:
            message = f"{suggestion['title']} is directed by {suggestion['director']} and has a rating of {suggestion['aggregate_rating']}"
            dispatcher.utter_message(text=message)
        elif new_slots['starring'] is not None and new_slots['director'] is None and new_slots['genre'] is None:
            message = f"{suggestion['title']}, is starring {suggestion['starring']} and has a rating of {suggestion['aggregate_rating']}"
            dispatcher.utter_message(text=message)
        elif new_slots['starring'] is not None and new_slots['director'] is not None and new_slots['genre'] is None:
            message = f"{suggestion['title']} is starring {suggestion['starring']} and directed by {suggestion['director']}. It has a rating of {suggestion['aggregate_rating']}"
            dispatcher.utter_message(text=message)
        elif new_slots['starring'] is None and new_slots['director'] is None and new_slots['genre'] is not None:
            message = f"{suggestion['title']} is a {suggestion['genre']} and has a rating of {suggestion['aggregate_rating']}"
            dispatcher.utter_message(text=message)
        elif new_slots['starring'] is not None and new_slots['director'] is None and new_slots['genre'] is not None:
            message = f"{suggestion['title']} is a {suggestion['genre']} with {suggestion['starring']} and has a rating of {suggestion['aggregate_rating']}"
            dispatcher.utter_message(text=message)
        elif new_slots['starring'] is None and new_slots['director'] is not None and new_slots['genre'] is not None:
            message = f"{suggestion['title']} is a {suggestion['genre']} directed by {suggestion['director']} and has a rating of {suggestion['aggregate_rating']}"
            dispatcher.utter_message(text=message)
        elif new_slots['starring'] is not None and new_slots['director'] is not None and new_slots['genre'] is not None:
            message = f"{suggestion['title']} is a {suggestion['genre']} directed by {suggestion['director']}. It is starring {suggestion['starring']} and has a rating of {suggestion['aggregate_rating']}"
            dispatcher.utter_message(text=message)
    # def get_old_slots(self, tracker):
    #     slots = {"starring": tracker.get_slot("clarified_starring"),
    #              "director": tracker.get_slot("clarified_director"),
    #              "genre": tracker.get_slot("clarified_genre")
    #             }
    #     return slots
    

    # def set_old_slots(self, tracker):
    #     if next(tracker.get_latest_entity_values("starring"), None) is not None:
    #         tracker._set_slot('clarified_starring', next(tracker.get_latest_entity_values("starring")))
    #     if next(tracker.get_latest_entity_values("director"), None) is not None:
    #         tracker._set_slot('clarified_director', next(tracker.get_latest_entity_values("director")))
    #     if next(tracker.get_latest_entity_values("genre"), None) is not None:
    #         tracker._set_slot('clarified_genre', next(tracker.get_latest_entity_values("genre")))

    def get_new_slots(self, tracker): 
        slots = {"starring": self.get_entity(tracker=tracker, entity_name='starring'),
                "starring_id":None,
                 "director":self.get_entity(tracker=tracker, entity_name='director'),
                 "director_id": None,
                 "genre": self.get_entity(tracker=tracker, entity_name='genre'),
                 "genre_id": None,
                 "title": None,
                 "rating": None}     
        # slots = {"starring": next(tracker.get_latest_entity_values("starring"), None),
        #         "starring_id":None,
        #          "director": next(tracker.get_latest_entity_values("director"), None),
        #          "director_id": None,
        #          "genre": next(tracker.get_latest_entity_values("genre"), None),
        #          "genre_id": None,
        #          "title": None,
        #          "rating": None}        
        return slots
    def get_entity(self, tracker, entity_name):
        entity_values = []

        # Iterate over the events in the tracker to extract entity values
        for event in tracker.events:
            if 'parse_data' in event:
                for entity in event['parse_data']['entities']:
                    if entity['entity'] == entity_name and entity['value'] is not None:
                        entity_values.append(entity['value'])
        if entity_values:
            return entity_values[-1]
        else:
            return None


    def fill_id_slots(self, slots):
        for key in slots.keys():
            if slots[key] is not None:
                if key == "starring" or key == "director":
                    id_key = key+"_id"
                    slots[id_key] = self.get_person_id(slots[key])
                elif key == "genre":
                        slots[key] = slots[key]
                        id_key = key+"_id"
                        slots[id_key] = genres[slots[key].upper()]
        return slots
    
    def get_suggestions(self, slots, tracker):
        response = requests.get(self.build_url(slots), headers=headers)
        data = response.json()['results']
        if data:
            results = []
            iterations = min(10, len(data))
            for i in range(iterations):
                movie_id = data[i]['id']
                people = self.get_movie_credits(movie_id, tracker)
                useful_data = {
                    "title": data[i]['title'],
                    "aggregate_rating": data[i]['vote_average'],
                    "genre": data[i]['genre_ids'],
                    "starring": people[0],
                    "director": people[1],
                }
                results.append(useful_data)
            return results
        else:
            return "Empty"

    
    def build_url(self, slots):
        base_url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
        if slots['starring_id'] is not None:
            base_url = base_url + "&with_cast="+str(slots['starring_id'])
        if slots['director_id'] is not None:
            base_url = base_url + "&with_crew="+str(slots['director_id'])
        if slots['genre_id'] is not None:
            base_url = base_url + "&with_genres="+str(slots['genre_id'])
        
        return base_url
    
    def get_movie_credits(self, movie_id, tracker):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"
        response = requests.get(url, headers=headers)
        starring = response.json()['cast'][0]['name']
        crew = response.json()['crew']
        director = ''
        for member in crew:
            if member['job'].lower() == 'director':
                director = member['name']
        return starring, director
    
    
    def get_person_id(self, person_name):
        person_name_no_spaces = person_name.replace(" ", "%20")
        url = f"https://api.themoviedb.org/3/search/person?query={person_name_no_spaces}&include_adult=false&language=en-US&page=1"
        response = requests.get(url, headers=headers)

        return response.json()['results'][0]['id']
    

    def choose_suggestion(self, results, tracker):
        max_score = 0
        max_ind=0
        for i in range(len(results)):
            if results[i]['aggregate_rating'] > max_score:
                max_score = results[i]['aggregate_rating']
                max_ind = i
        suggestion =  {
            'title': results[max_ind]['title'],
            'aggregate_rating': results[max_ind]['aggregate_rating'],
            'genre':self.choose_genre(self.genre_id_to_str(results[max_ind]['genre']), tracker),
            'starring': results[max_ind]['starring'],
            'director': results[max_ind]['director']
        }
        if suggestion["title"] == tracker.get_slot('title'):
            del results[max_ind]
            return self.choose_suggestion(results, tracker)
        else:
            return suggestion

    def choose_genre(self, genres, tracker):
        slot_string = ""
        slot = tracker.get_slot('genre')
        if genres is not None:
            for genre in genres:
                slot_string += f"{genre.capitalize()}, "
            return slot_string
        else:
            return None


    def genre_id_to_str(self, genre_list):
        for i in range(len(genre_list)):
            for key, val in genres.items():
                if val == genre_list[i]:
                    genre_list[i] = key
        return genre_list
    
class Reset(Action):
    def name(self) -> Text:
        return "reset_slots" #action name

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # intent_name = tracker.latest_message['intent'].get('name')
        # if intent_name == "reset":
        return [SlotSet("title", None), 
            SlotSet("aggregate_rating", None), 
            SlotSet("starring", None),
            SlotSet("director", None),
            SlotSet("genre", None)]
