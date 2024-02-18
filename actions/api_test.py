
def make_discover_cast_and_crew_url(movie_id):
    return f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"

def build_discover_movie_url(slots):
    slots = {"starring": "Ma Dong-seok",
                 "director": "Heo Myeong-haeng",
                 "genre": "Action",
                 "title": "",
                 "rating": ""}
    
def call_default():
        default_movie_url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

        pass
