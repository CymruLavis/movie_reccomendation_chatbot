import requests
import json

def make_discover_cast_and_crew_url(movie_id):
    return f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"

def build_discover_movie_url(slots):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres={slots['genre_id']}&with_cast={slots['starring_id']}&with_crew={slots['director_id']}"
    print(url)
    return url
    
def call_default():
        default_movie_url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

        pass
def build_url(slots):
        base_url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
        if slots['starring_id'] is not None:
            base_url = base_url + "&with_cast="+str(slots['starring_id'])
        if slots['director_id'] is not None:
            base_url = base_url + "&with_crew="+str(slots['director_id'])
        if slots['genre_id'] is not None:
            base_url = base_url + "&with_genres="+str(slots['genre_id'])
        
        return base_url
api_access_token = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZDE5YTIzMGQyZjU4YWNjMzE3Yzg2Zjg5ZDhjN2IyMyIsInN1YiI6IjY1YzIzMWQ5MDkyOWY2MDE2MWU0YTc0OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-TUBWSOE5-yUi8I8P1t5NrnHXN9BcZy3RATvNY5G2QQ"

headers = {
    "accept": "application/json",
    "Authorization": api_access_token
}
slots = {"starring": None,
             'starring_id': None,
                 "director": None,
                 "director_id": None,
                 "genre": None,
                 "genre_id": None,
                 "title": None,
                 "rating": None}
url = build_url(slots)
print(url)
response = requests.get(url, headers=headers)
data = response.json()['results']
print(type(data))
# response = requests.get(url, headers=headers)
# data = response.json()['results']

# print(data)