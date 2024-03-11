# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import json
page_num = 1
api_access_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZDE5YTIzMGQyZjU4YWNjMzE3Yzg2Zjg5ZDhjN2IyMyIsInN1YiI6IjY1YzIzMWQ5MDkyOWY2MDE2MWU0YTc0OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-TUBWSOE5-yUi8I8P1t5NrnHXN9BcZy3RATvNY5G2QQ"
url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page_num}&sort_by=popularity.desc"
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

       









def send_message( suggestion, dispatcher, new_slots):
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



def fill_id_slots( slots):
    for key in slots.keys():
        if slots[key] is not None:
            if key == "starring" or key == "director":
                id_key = key+"_id"
                slots[id_key] = get_person_id(slots[key])
            elif key == "genre":
                    # print(key)
                    # print(slots[key])
                    # slots[key] = slots[key]
                    try:
                        id_key = key+"_id"
                        slots[id_key] = genres[slots[key].upper()]
                    except KeyError:
                        print(f"I couldn't find a movie with type {slots[key]}")
    return slots

def get_suggestions( slots):
    response = requests.get(build_url(slots), headers=headers)
    data = response.json()['results']
    if data:
        results = []
        iterations = min(10, len(data))
        for i in range(iterations):
            movie_id = data[i]['id']
            people = get_movie_credits(movie_id)
            # print(people)
            if slots['director']:
                if people[1].lower() != slots['director'].lower():
                    pass
                else:
                    useful_data = {
                        "title": data[i]['title'],
                        "aggregate_rating": data[i]['vote_average'],
                        "genre": data[i]['genre_ids'],
                        "starring": people[0],
                        "director": people[1],
                    }
                    results.append(useful_data)
            else:
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


def build_url( slots):
    base_url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    if slots['starring_id'] is not None:
        base_url = base_url + "&with_cast="+str(slots['starring_id'])
    if slots['director_id'] is not None:
        base_url = base_url + "&with_crew="+str(slots['director_id'])
    if slots['genre_id'] is not None:
        base_url = base_url + "&with_genres="+str(slots['genre_id'])
    
    return base_url

def get_movie_credits( movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"
    response = requests.get(url, headers=headers)
    starring = response.json()['cast'][0]['name']
    crew = response.json()['crew']
    director = ''
    for member in crew:
        if member['job'].lower() == 'director':
            # print(member['name'])
            # print(member['job'])
            director = member['name']

    return starring, director


def get_person_id( person_name):
    person_name_no_spaces = person_name.replace(" ", "%20")
    url = f"https://api.themoviedb.org/3/search/person?query={person_name_no_spaces}&include_adult=false&language=en-US&page=1"
    response = requests.get(url, headers=headers)

    return response.json()['results'][0]['id']


def choose_suggestion( results):
    max_score = 0
    max_ind=0
    for i in range(len(results)):
        if results[i]['aggregate_rating'] > max_score:
            max_score = results[i]['aggregate_rating']
            max_ind = i
    suggestion =  {
        'title': results[max_ind]['title'],
        'aggregate_rating': results[max_ind]['aggregate_rating'],
        'genre':choose_genre(genre_id_to_str(results[max_ind]['genre'])),
        'starring': results[max_ind]['starring'],
        'director': results[max_ind]['director']
    }
    if suggestion["title"] == slots['title']:
        del results[max_ind]
        return choose_suggestion(results)
    else:
        return suggestion

def choose_genre( genres):
    slot_string = ""
    slot = slots['genre']
    if genres is not None:
        for genre in genres:
            slot_string += f"{genre.capitalize()}, "
        return slot_string
    else:
        return None


def genre_id_to_str( genre_list):
    for i in range(len(genre_list)):
        for key, val in genres.items():
            if val == genre_list[i]:
                genre_list[i] = key
    return genre_list

slots = {"starring":None,
                "starring_id":None,
                 "director": None,
                 "director_id": None,
                 "genre": 'comic',
                 "genre_id": None,
                 "title": None,
                 "rating": None}   

slots_with_ids = fill_id_slots(slots=slots) #fill slot values with ids
results = get_suggestions(slots_with_ids)
if results == "Empty":
    msg = "I couldn't find anything that matched your criteria. Please try for something else"
    print(msg)
else:
    suggestion = choose_suggestion(results)
    print(f"{suggestion['title']} is a {suggestion['genre']} directed by {suggestion['director']}. It is starring {suggestion['starring']} and has a rating of {suggestion['aggregate_rating']}")
